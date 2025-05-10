import hashlib
import json
import redis
from functools import cached_property
from typing import Any, Dict, Iterable, Optional, Tuple

from celery import Task


class LockManager:
    """
    Manages two separate Redis counters per signature:
      • queue:   how many tasks are pending+running
      • running: how many are actively executing
    """

    def __init__(self, url: str, prefix: str):
        self._client = redis.Redis.from_url(url)
        self._prefix = prefix

    def _make_key(self, slot: str, task_name: str, signature: str) -> str:
        # slot is either "queue" or "run"
        return f"{self._prefix}:{slot}:{task_name}:{signature}"

    def acquire(
        self,
        slot: str,
        task_name: str,
        signature: str,
        limit: int,
        ttl: Optional[int] = None,
    ) -> bool:
        """
        Increment the <slot> counter; if it exceeds `limit`, roll back and return False.
        If ttl is given, set/refresh it on first holder.
        """
        key = self._make_key(slot, task_name, signature)
        pipe = self._client.pipeline()
        pipe.incr(key)
        if ttl is not None:
            pipe.ttl(key)
            new_count, current_ttl = pipe.execute()
            if new_count == 1:
                self._client.expire(key, ttl)
            elif new_count > limit:
                self._client.decr(key)
                return False
            else:
                # keep TTL at least ttl
                if current_ttl < ttl:
                    self._client.expire(key, ttl)
        else:
            new_count = pipe.execute()[0]
            if new_count > limit:
                self._client.decr(key)
                return False
        return True

    def release(self, slot: str, task_name: str, signature: str) -> None:
        key = self._make_key(slot, task_name, signature)
        if self._client.exists(key):
            self._client.decr(key)

    # convenience wrappers
    def acquire_queue(self, *args, **kw):
        return self.acquire("queue", *args, **kw)

    def release_queue(self, *args, **kw):
        return self.release("queue", *args, **kw)

    def acquire_run(self, *args, **kw):
        return self.acquire("run", *args, **kw)

    def release_run(self, *args, **kw):
        return self.release("run", *args, **kw)


class LimitedTask(Task):
    """
    Base class for Celery tasks that need:
      1) a cap on how many may sit in the broker queue
      2) a cap on how many may execute at once

    Configurable via:
      • Celery config:
          LIMITED_TASKS_PREFIX                (default "celery-limited-tasks")
          LIMITED_TASKS_DEFAULT_QUEUE_LIMIT   (default 1)
          LIMITED_TASKS_DEFAULT_CONCURRENCY   (default 1)
          LIMITED_TASKS_DEFAULT_TTL           (default 3600)
      • Per‐task via uts={
            "queue_limit": int,
            "concurrency_limit": int,
            "lock_ttl": int,
            "key_by": List[str],
        }
    """
    abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        broker = self.app.conf.broker_url
        prefix = self.app.conf.get("LIMITED_TASKS_PREFIX", "celery-limited-tasks")
        self.locker = LockManager(broker, prefix)

    @cached_property
    def uts(self) -> Dict[str, Any]:
        return getattr(self, "uts", {})

    def _get_queue_limit(self) -> int:
        return int(self.uts.get(
            "queue_limit",
            self.app.conf.get("LIMITED_TASKS_DEFAULT_QUEUE_LIMIT", 1)
        ))

    def _get_concurrency_limit(self) -> int:
        return int(self.uts.get(
            "concurrency_limit",
            self.app.conf.get("LIMITED_TASKS_DEFAULT_CONCURRENCY", 1)
        ))

    def _get_ttl(self) -> int:
        return int(self.uts.get(
            "lock_ttl",
            self.app.conf.get("LIMITED_TASKS_DEFAULT_TTL", 3600)
        ))

    def _get_key_by(self) -> Optional[Iterable[str]]:
        return self.uts.get("key_by")

    def _make_signature(
        self, args: Tuple[Any, ...], kwargs: Dict[str, Any]
    ) -> str:
        key_by = self._get_key_by()
        if key_by:
            subset = {k: kwargs[k] for k in key_by if k in kwargs}
        else:
            subset = {"args": args, "kwargs": kwargs}
        raw = json.dumps(subset, sort_keys=True, default=str)
        return hashlib.sha256(raw.encode()).hexdigest()

    def apply_async(self, args=None, kwargs=None, **opts):
        args = args or ()
        kwargs = kwargs or {}
        sig = self._make_signature(args, kwargs)
        ql = self._get_queue_limit()
        ttl = self._get_ttl()

        if not self.locker.acquire_queue(self.name, sig, ql, ttl):
            # queue is already at capacity → drop silently
            return None

        # stash our sig so after_return/requeue logic can see it
        opts.setdefault("headers", {})["_limited_sig"] = sig
        return super().apply_async(args, kwargs, **opts)

    def __call__(self, *args, **kwargs):
        # Task has been pulled off the broker.  First, release the queue slot:
        sig = self.request.headers.get("_limited_sig")
        if sig:
            self.locker.release_queue(self.name, sig)

        # Now enforce concurrency:
        cl = self._get_concurrency_limit()
        ql = self._get_queue_limit()
        ttl = self._get_ttl()

        if sig and not self.locker.acquire_run(self.name, sig, cl, ttl):
            # too many running; try to re‐queue if there's still queue capacity
            if self.locker.acquire_queue(self.name, sig, ql, ttl):
                # re‐enqueue for later
                return self.apply_async(args=args, kwargs=kwargs)
            # else: drop silently
            return None

        # OK to actually execute
        return super().__call__(*args, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        # always free up a running slot if we held one
        sig = self.request.headers.get("_limited_sig")
        if sig:
            self.locker.release_run(self.name, sig)
        return super().after_return(status, retval, task_id, args, kwargs, einfo)

import hashlib
import pickle
from celery import Task


class LockManager:
    """SRP: Handles only lock acquire & release via a Redis client."""

    def __init__(self, client):
        self.client = client

    def acquire(self, key: str, ttl: int) -> bool:
        # NX: only set if not exists; EX sets expiration (seconds)
        return self.client.set(key, '1', nx=True, ex=ttl)

    def release(self, key: str) -> None:
        self.client.delete(key)


class UniqueKeyBuilder:
    """SRP: Builds the lock key (prefix:task_name:fingerprint)."""

    def __init__(self, prefix: str):
        self.prefix = prefix

    def build(self, task_name: str, uts: dict, args: tuple, kwargs: dict):
        keys = uts.get('keys')
        fingerprint = self._fingerprint(task_name, args, kwargs, keys)
        lock_key = f"{self.prefix}:{task_name}:{fingerprint}"
        return lock_key, uts['ttl']

    def _fingerprint(self, task_name, args, kwargs, keys):
        if keys:
            # User specified which args indices or kw names to include
            selected = []
            for key in keys:
                if isinstance(key, int):
                    selected.append(args[key] if key < len(args) else None)
                else:
                    selected.append(kwargs.get(key))
        else:
            # Default: all args + sorted kwargs
            selected = list(args) + [(k, kwargs[k]) for k in sorted(kwargs)]
        data = (task_name, selected)
        return hashlib.sha1(pickle.dumps(data)).hexdigest()


class UniqueTask(Task):
    """Abstract base to enforce one‐off enqueueing per args/kwargs fingerprint."""
    abstract = True

    def __init__(self):
        super().__init__()
        cfg = self.app.conf
        prefix = cfg.get('UT_LOCK_PREFIX', 'celery-unique-tasks')
        default_ttl = cfg.get('UT_DEFAULT_TTL', 900)
        self.key_builder = UniqueKeyBuilder(prefix)
        self.default_ttl = default_ttl

    def apply_async(self, args=None, kwargs=None, **options):
        # 1) Merge decorator-level and call-time uts
        decorator_settings = getattr(self, 'uts', {}) or {}
        runtime_settings = options.pop('uts', {}) or {}
        uts = {**decorator_settings, **runtime_settings}
        uts.setdefault('ttl', self.default_ttl)

        args = args or ()
        kwargs = kwargs or {}

        # 2) Build lock key + get TTL
        lock_key, ttl = self.key_builder.build(self.name, uts, args, kwargs)

        # 3) Attempt to acquire lock in Redis
        client = self.app.backend.client
        locker = LockManager(client)
        if not locker.acquire(lock_key, ttl):
            # Duplicate: skip enqueueing
            return None

        # 4) Pass lock_key via headers so worker can release later
        headers = options.pop('headers', {})
        headers['ut_lock_key'] = lock_key
        options['headers'] = headers

        return super().apply_async(args=args, kwargs=kwargs, **options)

    def after_return(self, status, retval_or_exc, task_id, args, kwargs, einfo):
        # Always release lock when the task finishes (success or failure)
        headers = getattr(self.request, 'headers', {}) or {}
        lock_key = headers.get('ut_lock_key')
        if lock_key:
            LockManager(self.app.backend.client).release(lock_key)

        return super().after_return(status, retval_or_exc, task_id, args, kwargs, einfo)

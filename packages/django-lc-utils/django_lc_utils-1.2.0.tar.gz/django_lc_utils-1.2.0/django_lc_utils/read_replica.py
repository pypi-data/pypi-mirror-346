"""An encapsulated thread-local variable that indicates whether future DB
writes should be "stuck" to the replica."""

import threading
from functools import wraps

_default_locals = threading.local()


def this_thread_is_pinned():
    """Return whether the current thread should send all its reads to the
    master DB."""
    return getattr(_default_locals, "pinned", False)


def pin_this_thread():
    """Mark this thread as "stuck" to the master for all DB access."""
    _default_locals.pinned = True


def unpin_this_thread():
    """Unmark this thread as "stuck" to the master for all DB access.
    If the thread wasn't marked, do nothing.
    """
    _default_locals.pinned = False


class UseDefaultDB:
    """A contextmanager/decorator to use the master database."""

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kw):
            with self:
                return func(*args, **kw)

        return decorator

    def __enter__(self):
        _default_locals.old = this_thread_is_pinned()
        pin_this_thread()

    def __exit__(self, type, value, tb):
        if not _default_locals.old:
            unpin_this_thread()


_replica_locals = threading.local()


def this_replica_thread_is_pinned():
    """Return whether the current thread should send all its reads to the
    replica DB."""
    return getattr(_replica_locals, "pinned", False)


def pin_this_replica_thread():
    """Mark this thread as "stuck" to the replica for all DB access."""
    _replica_locals.pinned = True


def unpin_this_replica_thread():
    """Unmark this thread as "stuck" to the replica for all DB access.
    If the thread wasn't marked, do nothing.
    """
    _replica_locals.pinned = False


class UseReplicaDB:
    """A contextmanager/decorator to use the replica database."""

    def __call__(self, func):
        @wraps(func)
        def decorator(*args, **kw):
            with self:
                return func(*args, **kw)

        return decorator

    def __enter__(self):
        _replica_locals.old = this_replica_thread_is_pinned()
        pin_this_replica_thread()

    def __exit__(self, type, value, tb):
        if not _replica_locals.old:
            unpin_this_replica_thread()


use_default_db = UseDefaultDB()
use_replica_db = UseReplicaDB()

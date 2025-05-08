from ..read_replica import (
    pin_this_replica_thread,
    pin_this_thread,
    this_replica_thread_is_pinned,
    this_thread_is_pinned,
    unpin_this_replica_thread,
    unpin_this_thread,
    use_default_db,
    use_replica_db,
)


class TestReadReplica:
    def test_use_default_db(self):
        @use_default_db
        def test_func():
            assert this_thread_is_pinned() is True

        test_func()
        assert this_thread_is_pinned() is False

    def test_use_replica_db(self):
        @use_replica_db
        def test_func():
            assert this_replica_thread_is_pinned() is True

        test_func()
        assert this_replica_thread_is_pinned() is False

    def test_pin_this_thread(self):
        pin_this_thread()
        assert this_thread_is_pinned() is True

    def test_unpin_this_thread(self):
        pin_this_thread()
        assert this_thread_is_pinned() is True
        unpin_this_thread()
        assert this_thread_is_pinned() is False

    def test_pin_this_replica_thread(self):
        pin_this_replica_thread()
        assert this_replica_thread_is_pinned() is True

    def test_unpin_this_replica_thread(self):
        pin_this_replica_thread()
        assert this_replica_thread_is_pinned() is True
        unpin_this_replica_thread()
        assert this_replica_thread_is_pinned() is False

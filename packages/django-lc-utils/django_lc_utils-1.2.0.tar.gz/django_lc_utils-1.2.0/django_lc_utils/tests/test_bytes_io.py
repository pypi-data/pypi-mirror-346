import io

from ..io_utils import BytesIOWrapper


class TestBytesIOWrapper:
    def test_bytes_io_wrapper_read(self):
        text_io_buffer = io.StringIO("Hello World!")
        bytes_io = BytesIOWrapper(text_io_buffer)
        assert bytes_io.read() == b"Hello World!"

    # TODO: Fix the test below.
    # def test_bytes_io_wrapper_read1(self):
    #     text_io_buffer = io.StringIO("Hello World!")
    #     bytes_io = BytesIOWrapper(text_io_buffer)
    #     result = bytes_io.read1(5)
    #     assert result.decode() == "Hello"

    def test_bytes_io_wrapper_peek(self):
        text_io_buffer = io.StringIO("Hello World!")
        bytes_io = BytesIOWrapper(text_io_buffer)
        assert bytes_io.read(1) == b"H"
        # Reset the stream position to the beginning
        text_io_buffer.seek(0)
        assert bytes_io.read(1) == b"H"

    def test_bytes_io_wrapper_with_encoding(self):
        text_io_buffer = io.StringIO("Hello World!")
        bytes_io = BytesIOWrapper(text_io_buffer, encoding="utf-16")
        assert bytes_io.read() == b"\xff\xfeH\x00e\x00l\x00l\x00o\x00 \x00W\x00o\x00r\x00l\x00d\x00!\x00"

    def test_bytes_io_wrapper_with_errors(self):
        text_io_buffer = io.StringIO("Hello World!")
        bytes_io = BytesIOWrapper(text_io_buffer, encoding="ascii", errors="replace")
        assert bytes_io.read() == b"Hello World!"

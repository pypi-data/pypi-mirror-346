# m4p, an implementation of GNU m4 in Python
# Copyright (C) 2025  Nikolaos Chatzikonstantinou
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from m4p.stream import Stream
from io import BytesIO
import pytest


@pytest.fixture
def foo_stream() -> Stream:
    foo = "foo.txt"
    stream = Stream()
    stream.push_file(BytesIO(b"world"), pathname=foo)
    stream.push_file(BytesIO(b" "), pathname=foo)
    stream.push_file(BytesIO(b"hello"), pathname=foo)
    return stream


@pytest.fixture
def bar_foo_stream(foo_stream) -> Stream:
    bar = "bar.txt"
    foo_stream.push_file(BytesIO(b"Message from bar."), pathname=bar)
    return foo_stream


def test_stream_read(foo_stream):
    stream = foo_stream
    assert len(stream.files) == 3
    # We read 8 bytes.
    stream.read(8)
    assert stream.data() == b"hello wo"
    # We expect the middle File to be removed from the list.
    assert len(stream.files) == 2
    assert stream.files[1].closed()
    assert not stream.files[0].closed()
    # Read everything
    stream.read()
    assert stream.data() == b"hello world"
    assert len(stream.files) == 1
    assert stream.files[0].closed()


def test_stream_drop(bar_foo_stream):
    stream = bar_foo_stream
    assert len(stream.files) == 4
    # We read 22 bytes.
    stream.read(22)
    assert stream.data() == b"Message from bar.hello"
    stream.consume(8)
    assert stream.data() == b"from bar.hello"


def test_stream_peek(bar_foo_stream):
    stream = bar_foo_stream
    assert stream.peek(22) == b"Message from bar.hello"
    assert stream.peek(100) == b"Message from bar.hello world"

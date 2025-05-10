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

from attrs import define, evolve, Factory
from typing import BinaryIO
from enum import Enum, auto
from m4p.regionbuffer import RegionBuffer, Region
from collections import deque


class FileMode(Enum):
    """The mode deciding how to read from a file."""

    # Under the NORMAL mode, a file is read in chunks.
    NORMAL = auto()
    # Under the NEWLINE mode, the read operation pauses at newlines,
    # giving the opportunity to the parser to respond.
    NEWLINE = auto()


class SourceType(Enum):
    """The type of source from which the buffer region originates."""

    # From the expansion of a macro.
    MACRO = auto()
    # From a file.
    FILE = auto()
    # From stdin.
    STDIN = auto()


@define(frozen=True)
class FileMetadata:
    pathname: bytes
    mode: FileMode
    source: SourceType
    id: int


@define
class File:
    """A file with an accessible buffer."""

    file: BinaryIO
    metadata: FileMetadata
    regionbuffer: RegionBuffer = Factory(RegionBuffer)

    def closed(self) -> bool:
        return self.file.closed

    def read(self, size: int = -1) -> int:
        if self.file.closed:
            return 0
        match self.metadata.mode:
            case FileMode.NORMAL:
                s = self.file.read(size)
                n = len(s)
                self.regionbuffer.append(s, id=self.metadata)
                if size == -1 or n < size:
                    self.file.close()
                return n
            case FileMode.NEWLINE:
                s = self.file.readline(size)
                n = len(s)
                self.regionbuffer.append(
                    s,
                    id=FileMetadata(
                        pathname=b"",
                        mode=FileMode.NEWLINE,
                        source=SourceType.STDIN,
                        id=0,
                    ),
                )
                if n == 0:
                    self.file.close()
                return n


@define
class Stream:
    """A Stream seamlessly hides the boundary between multiple Files.

    The Stream will remember the source origin of each byte and match
    it to the appropriate file.

    """

    files: list[File] = Factory(list)
    newline_counter: dict[int, int] = Factory(dict)
    file_counter: int = 1  # 0 is stdin

    def clear(self):
        """Empty out the RegionBuffer."""
        for file in self.files:
            file.file.close()
            file.regionbuffer.clear()
        self.files.clear()
        self.newline_counter.clear()
        self.file_counter = 1

    def current_pathname_and_line(self) -> tuple[bytes, int]:
        regions = self.regions()
        if regions:
            pathname = regions[0].id.pathname
            id = regions[0].id.id
            line = self.newline_counter.get(id, 0) + 1
            return pathname, line
        else:
            return b"", -1

    def increase_newline_counter(self, id: int, n: int):
        """Increase the newline counter of id by n.

        Sets to n if the counter has not been set for id.

        """
        if self.newline_counter.get(id):
            self.newline_counter[id] += n
        else:
            self.newline_counter[id] = n

    def consume(self, number_of_bytes: int = 1):
        """Discard bytes from the front of the top RegionBuffer.

        Tally the number of newlines consumed.

        """
        for region in self.regions():
            metadata = region.id
            if metadata.source == SourceType.MACRO:
                # We skip macro expansions from newline tallying.
                continue
            slice = self.regionbuffer().slice(region)
            if number_of_bytes <= region.end:
                n = slice.count(b"\n", 0, max(0, number_of_bytes - region.begin))
            else:
                n = slice.count(b"\n")
            self.increase_newline_counter(metadata.id, n)
        self.regionbuffer().drop(number_of_bytes)

    def push_file(self, file: BinaryIO, pathname: bytes, current_line: int = 0):
        """Push an open file at the top of the stack.

        The current line can be set in case this information is coming
        from m4wrap().

        """
        if not pathname:
            mode = FileMode.NEWLINE
            source = SourceType.STDIN
        else:
            mode = FileMode.NORMAL
            source = SourceType.FILE
        metadata = FileMetadata(
            pathname=pathname, mode=mode, source=source, id=self.file_counter
        )
        file = File(file=file, metadata=metadata)
        self.files.append(file)
        self.newline_counter[file.metadata.id] = current_line
        self.file_counter += 1

    def regions(self) -> deque[Region]:
        """Return the regions of the top RegionBuffer."""
        return self.regionbuffer().regions

    def data(self) -> bytes:
        """The data in the top RegionBuffer."""
        if not self.files:
            return b""
        else:
            return self.files[-1].regionbuffer.buffer

    def regionbuffer(self) -> RegionBuffer:
        """The top RegionBuffer."""
        if not self.files:
            return RegionBuffer()
        else:
            return self.files[-1].regionbuffer

    def peek(self, number_of_bytes: int = 1) -> bytes:
        """Peek at the front bytes in the stream."""
        if len(self.regionbuffer()) < number_of_bytes:
            self.read(max(number_of_bytes, 8196))
        return self.data()[:number_of_bytes]

    def read(self, size: int = -1) -> int:
        """Read from the entire stack of Files.

        This function reads from the top File and then in succession
        from the next File's buffer, until said buffer is empty, and
        then from the File itself. It will close empty Files with
        empty buffers and remove them from the stack. The top File
        always remains on the stack, and in its buffer all the read
        contents will be found appended.

        """
        if not self.files:
            return 0
        file = self.files.pop()
        acc = 0
        if size == -1:
            acc += file.read(-1)
            for f in self.files:
                f.read(-1)
                acc += len(f.regionbuffer)
                file.regionbuffer.join(f.regionbuffer)
            self.files = [file]
            return acc
        n = file.read(size)
        acc += n
        while acc < size:
            if not self.files:
                break
            f = self.files[-1]
            if f.regionbuffer:
                s = f.regionbuffer.chunk(size)
                n = len(s)
                acc += n
                file.regionbuffer.join(s)
            elif not f.closed():
                n = f.read(size - acc)
                acc += n
                file.regionbuffer.join(f.regionbuffer)
                f.regionbuffer.clear()
            else:
                self.files.pop()
        self.files.append(file)
        return acc

    def prepend_macroexpansion(self, s: bytes):
        """Prepend s from macro expansion."""
        regionbuffer = self.regionbuffer()
        try:
            metadata = regionbuffer.regions[0].id
        except IndexError:
            metadata = regionbuffer.last_id
        macro_metadata = evolve(metadata, source=SourceType.MACRO)
        regionbuffer.prepend(s, id=macro_metadata)

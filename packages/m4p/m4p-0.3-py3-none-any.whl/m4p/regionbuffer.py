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

from attrs import define, Factory
from collections import deque
from typing import Any


@define
class Region:
    id: Any
    begin: int = 0
    end: int = 0

    def __len__(self):
        return self.end - self.begin

    def contains(self, index: int) -> bool:
        """Is index contained in this region?"""
        return self.begin <= index and index < self.end

    def translate(self, translation: int):
        """Translate begin and end by translation."""
        self.begin += translation
        self.end += translation


@define
class RegionBuffer:
    buffer: bytes = b""
    regions: deque[Region] = Factory(deque)
    last_id: int = -1

    def __len__(self):
        return len(self.buffer)

    def slice(self, region) -> bytes:
        """The slice of buffer marked by region."""
        return self.buffer[region.begin : region.end]

    def region(self, index: int) -> Region:
        """Return the region that index is contained in."""
        for region in self.regions:
            if region.contains(index):
                return region
        raise RuntimeError(f"The index '{index}' is not not within the RegionBuffer.")

    def prepend(
        self,
        s: bytes,
        id: Any,
    ):
        """Prepend s to buffer as a marked region."""
        m = len(s)
        if not self.buffer:
            self.buffer = s
            self.regions.appendleft(Region(begin=0, end=m, id=id))
        else:
            self.buffer = s + self.buffer
            for region in self.regions:
                region.translate(m)
            first_region = self.region(m)
            if first_region.id == id:
                first_region.begin -= m
            else:
                self.regions.appendleft(Region(begin=0, end=m, id=id))

    def append(self, s: bytes, id: Any):
        """Append s to buffer as a marked region."""
        self.last_id = id
        n = len(self.buffer)
        m = len(s)
        if n == 0:
            self.buffer = s
            self.regions.append(Region(begin=0, end=m, id=id))
        else:
            final_region = self.region(n - 1)
            self.buffer += s
            if final_region.id == id:
                final_region.end += m
            else:
                self.regions.append(Region(begin=n, end=n + m, id=id))

    def clear(self):
        """Clear out the RegionBuffer."""
        self.buffer = b""
        self.regions.clear()

    def drop(self, count: int):
        """Remove count bytes from beginning of buffer."""
        if count >= len(self.buffer):
            self.clear()
        else:
            self.buffer = self.buffer[count:]
            n = count
            while n > 0:
                region = self.regions[0]
                if len(region) <= n:
                    n -= len(region)
                    self.regions.popleft()
                else:
                    region.begin += n
                    break
            for region in self.regions:
                region.translate(-count)

    def chunk(self, count: int) -> "RegionBuffer":
        """Carve out a chunk from the front as a new RegionBuffer."""
        if count >= len(self.buffer):
            ret = RegionBuffer(buffer=self.buffer, regions=self.regions)
            self.buffer = b""
            self.regions = deque()
            return ret
        else:
            ret = RegionBuffer(buffer=self.buffer[:count])
            self.buffer = self.buffer[count:]
            n = count
            while n > 0:
                region = self.regions[0]
                m = len(region)
                if m <= n:
                    n -= m
                    ret.regions.append(self.regions.popleft())
                else:
                    region.begin += n
                    final_region = Region(begin=count - n, end=count, id=region.id)
                    ret.regions.append(final_region)
                    break
            for region in self.regions:
                region.translate(-count)
            return ret

    def join(self, other: "RegionBuffer"):
        """Join the other RegionBuffer at the end; consumes other."""
        for region in other.regions:
            self.append(other.slice(region), id=region.id)
        other.clear()

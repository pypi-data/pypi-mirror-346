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

from m4p.regionbuffer import RegionBuffer


def test_regionbuffer():
    # An empty Buffer.
    b = RegionBuffer()
    assert b.buffer == b""
    assert not b.regions

    # Set up the buffer with three regions.
    b.append(b"hello", id=1)
    b.append(b" ", id=1)
    b.append(b"world", id=1)
    b.append(b"!", id=2)
    b.prepend(b"Macro message: ", id=0)
    assert b.buffer == b"Macro message: hello world!"
    assert len(b.regions) == 3
    assert b.regions[0].id == 0
    assert b.regions[1].id == 1
    assert b.regions[2].id == 2
    assert b.slice(b.regions[0]) == b"Macro message: "
    assert b.slice(b.regions[1]) == b"hello world"
    assert b.slice(b.regions[2]) == b"!"

    # Carve out 3 bytes into another buffer, splitting the first
    # region.
    x = b.chunk(3)
    assert b.buffer == b"ro message: hello world!"
    assert len(b.regions) == 3
    assert b.regions[0].id == 0
    assert b.regions[1].id == 1
    assert b.regions[2].id == 2
    assert b.slice(b.regions[0]) == b"ro message: "
    assert b.slice(b.regions[1]) == b"hello world"
    assert b.slice(b.regions[2]) == b"!"
    assert x.buffer == b"Mac"
    assert len(x.regions) == 1
    assert x.regions[0].id == 0
    assert x.slice(x.regions[0]) == b"Mac"

    # Carve out 14 bytes into another buffer, totally carving out the
    # first region and splitting the second.
    y = b.chunk(14)
    assert y.buffer == b"ro message: he"
    assert len(y.regions) == 2
    assert y.regions[0].id == 0
    assert y.regions[1].id == 1
    assert y.slice(y.regions[0]) == b"ro message: "
    assert y.slice(y.regions[1]) == b"he"
    assert b.buffer == b"llo world!"
    assert len(b.regions) == 2
    assert b.regions[0].id == 1
    assert b.regions[1].id == 2
    assert b.slice(b.regions[0]) == b"llo world"
    assert b.slice(b.regions[1]) == b"!"

    # Join the latter carve-out with the former. There should still be
    # two regions because the region of x and the first region of y
    # are the same.
    x.join(y)
    assert x.buffer == b"Macro message: he"
    assert len(x.regions) == 2
    assert x.regions[0].id == 0
    assert x.regions[1].id == 1
    assert x.slice(x.regions[0]) == b"Macro message: "
    assert x.slice(x.regions[1]) == b"he"
    assert y.buffer == b""
    assert len(y.regions) == 0

    # Drop 16 bytes from x. The first region vanishes, the second has
    # only one byte left.
    x.drop(16)
    assert x.buffer == b"e"
    assert len(x.regions) == 1
    assert x.regions[0].id == 1
    assert x.slice(x.regions[0]) == b"e"

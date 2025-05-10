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

from attrs import define
from re import compile
from array import array


@define
class Interval:
    """An inclusive interval of integers."""

    start: int
    end: int

    def __len__(self) -> int:
        return 1 + abs(self.end - self.start)

    def __getitem__(self, key) -> int:
        if key < len(self):
            if self.start <= self.end:
                return self.start + key
            else:
                return self.start - key
        else:
            raise IndexError("Interval index out of range")

    @staticmethod
    def from_spec(spec: bytes) -> list["Interval"]:
        acc = []
        last = None
        if spec:
            start = spec[0]
            for i in range(2, len(spec), 2):
                end = spec[i]
                if last:
                    if start < end:
                        start += 1
                    elif start > end:
                        start -= 1
                    else:
                        continue
                interval = Interval(start, end)
                if last != interval:
                    acc.append(interval)
                    last = interval
                start = end
        return acc


@define
class Translit:
    value: list[bytes | Interval]
    interval_pat = compile(b"[^-](?:(-[^-])+(--)?|--)")

    def __getitem__(self, key) -> int:
        for v in self.value:
            if key < len(v):
                return v[key]
            else:
                key -= len(v)
        raise IndexError("Translit index out of range")

    def __len__(self) -> int:
        return sum(len(x) for x in self.value)

    @classmethod
    def from_spec(cls, spec: bytes):
        acc = []
        next = 0
        for m in Translit.interval_pat.finditer(spec):
            start, end = m.span()
            if next < start:
                acc.append(spec[next:start])
            interval_spec = m.group()
            acc += Interval.from_spec(interval_spec)
            next = end
        if next < len(spec):
            acc.append(spec[next:])
        return Translit(value=acc)


@define
class TranslitMap:
    chars: Translit
    replacement: Translit
    # Type hint not supported in Python 3.11. See
    # <https://github.com/python/mypy/issues/13942>.
    compiled_map: array

    def translit(self, s: bytes) -> bytes:
        acc = []
        for c in s:
            x = self.compiled_map[c]
            if x != -1:
                acc.append(x)
        return bytes(acc)

    @classmethod
    def from_spec(cls, chars: bytes, replacement: bytes):
        ch = Translit.from_spec(chars)
        re = Translit.from_spec(replacement)
        compiled_map: array[int] = array("i", range(256))
        settable: array[int] = array("B", [True] * 256)
        n = len(ch)
        m = len(re)
        for i in range(n):
            c = ch[i]
            if settable[c]:
                if i < m:
                    compiled_map[c] = re[i]

                else:
                    compiled_map[c] = -1
                settable[c] = False
        return TranslitMap(ch, re, compiled_map)

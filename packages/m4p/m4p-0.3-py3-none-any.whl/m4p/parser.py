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

from typing import BinaryIO
from attrs import define, Factory
from m4p.stream import Stream
import re
from enum import Enum, auto
import sys
import pygnuregex
from m4p.m4_eval import (
    PropagatingError,
    calc,
    calc_info,
    radix_str,
    CalcInfo,
    ParserError,
    BadInput,
)
from ctypes import c_int32, CDLL, create_string_buffer
from ctypes.util import find_library
import subprocess
from math import isinf
from itertools import chain
from os import getenv, fsencode, getcwd
import os.path
from collections import defaultdict
from m4p.m4_translit import TranslitMap
from io import BytesIO
from platform import system

libc_path = find_library("c")
if not libc_path:
    raise RuntimeError("The C standard library (libc) was not detected.")
libc = CDLL(libc_path)


@define
class FrozenInt:
    value: int

    def __add__(self, other: int):
        return self

    def __str__(self):
        return f"{self.value}"

    def __int__(self):
        return self.value


class FormatException(Exception):
    pass


class ParserExit(Exception):
    def __init__(self, code):
        self.code = code


def regexp_replacement(
    original: bytes, replacement: bytes, span: list[tuple[int, int]]
) -> bytes:
    """Use the replacement template to create a new string from original with span matches."""
    acc = b""
    i = 0
    while i < len(replacement):
        c = bytes([replacement[i]])
        if c == b"\\":
            if i == len(replacement) - 1:
                break
            next = bytes([replacement[i + 1]])
            if next == b"\\":
                acc += b"\\"
                i += 1
            elif next.isdigit():
                d = int(next)
                first, last = span[d]
                if first != -1:
                    acc += original[first:last]
                i += 1
            elif next == b"&":
                first, last = span[0]
                if first != -1:
                    acc += original[first:last]
                i += 1
        else:
            acc += c
        i += 1
    return acc


def augment_trailing_x(s: bytes) -> bytes:
    """Augment s to end in at least 6 X characters."""
    n = len(s) - 1
    j = 6
    for i in range(max(n, 0), max(n - 6, 0), -1):
        if s[i] != b"X"[0]:
            break
        j -= 1
    return s + b"X" * j


def index_default(xs, i: int, d: bytes) -> bytes:
    """xs[i], or d if i is out of range."""
    try:
        return xs[i]
    except IndexError:
        return d


def replace_dollars(s: bytes, args: list[bytes]) -> bytes:
    """Replaces instances of dollars in s according to m4 rules."""
    for i in range(10):
        s = s.replace(b"$%d" % i, index_default(args, i, b""))
    s = s.replace(b"$#", b"%d" % (len(args) - 1))
    return s


class Mode(Enum):
    NORMAL = auto()
    COLLECT_ARGS = auto()


@define
class Builtin:
    value: bytes


builtins = [
    b"define",
    b"dnl",
    b"undefine",
    b"pushdef",
    b"popdef",
    b"incr",
    b"decr",
    b"changequote",
    b"changecom",
    b"len",
    b"index",
    b"dumpdef",
    b"regexp",
    b"eval",
    b"mkstemp",
    b"maketemp",
    b"substr",
    b"patsubst",
    b"format",
    b"syscmd",
    b"sysval",
    b"esyscmd",
    b"ifdef",
    b"ifelse",
    b"include",
    b"sinclude",
    b"divert",
    b"undivert",
    b"divnum",
    b"m4exit",
    b"shift",
    b"errprint",
    b"builtin",
    b"indir",
    b"defn",
    b"translit",
    b"m4wrap",
    b"__file__",
    b"__line__",
    b"__program__",
    b"debugfile",
    b"traceon",
    b"traceoff",
]

match system():
    case "Windows":
        builtins.append(b"__windows__")
    case _:
        builtins.append(b"__unix__")
        # GNU ext
        builtins.append(b"__gnu__")


def default_macros(prefix: bytes = b"") -> dict[bytes, list[bytes | Builtin]]:
    return {prefix + key: [Builtin(key)] for key in builtins}


class ParserEOF(Exception):
    pass


@define
class Parser:
    stream: Stream
    qdelim: tuple[bytes, bytes] = (b"`", b"'")
    cdelim: tuple[bytes, bytes] = (b"#", b"\n")
    word_pat = re.compile(rb"^[a-zA-Z_][a-zA-Z0-9_]*")
    output: bytes = Factory(bytes)
    macros: dict[bytes, list[bytes | Builtin]] = Factory(default_macros)
    prefix: bytes = b""
    mode: Mode = Mode.NORMAL
    cmd_code: bytes = b"0"
    configuration: dict = Factory(dict)
    count_closed_paren: int = 0
    int_pat = re.compile(b"^[+-]?\\d+")
    float_pat = re.compile(b"^[+-]?\\d*\\.?\\d+(?:[eE][+-]?\\d+)?")
    diversions: defaultdict[int, bytes] = Factory(lambda: defaultdict(lambda: b""))
    current_diversion: int = 0
    returncode: int = 0
    defn_token: Builtin | None = None
    m4wrap: Stream = Factory(Stream)
    debug_output: BinaryIO | None = sys.stderr.buffer
    traced_macros: defaultdict[bytes, bool] = Factory(lambda: defaultdict(lambda: False))
    recursion_depth: int  = 1

    @classmethod
    def new(cls, stream: Stream, configuration: dict):
        prefix = b"m4_" if configuration["prefix_builtins"] else b""
        macros = default_macros(prefix)
        debugfile = configuration.get("debugfile", 1)
        if debugfile == 1 or debugfile is None:
            debug_output = sys.stderr.buffer
        elif debugfile == b"":
            debug_output = None
        else:
            try:
                debug_output = open(debugfile, "wb")
            except:
                sys.stderr.buffer.write(b"cannot set debug file `stderr': Permission denied\n")
                debug_output = sys.stderr.buffer
        return Parser(
            stream=stream, macros=macros, configuration=configuration, prefix=prefix, debug_output=debug_output
        )

    def finish(self):
        divnum = self.current_diversion
        for k in chain([0], sorted(self.diversions.keys())):
            if k == divnum:
                self.stream = self.m4wrap
                self.m4wrap = Stream()
                try:
                    self.parse()
                except ParserExit as e:
                    sys.exit(e.code)
                except ParserEOF:
                    pass
            self.write(self.diversions[k], 0)
            self.diversions[k] = b""

    def open_file(self, file: bytes):
        """Open the file according to m4 rules."""
        prepend = reversed(self.configuration["B"])
        cwd = getcwd()
        include = self.configuration["include"]
        env = getenv("M4PATH") or ""
        env = map(fsencode, env.split(":"))
        for path in chain(prepend, cwd, include, env):
            try:
                path = os.path.join(path, file)
                f = open(path, "rb")
                return f, path
            except:
                pass
        return None, b""

    def finish_parsing(self):
        """Close all files and empty all buffers, preserve all other state."""
        self.stream.clear()

    def error(self, pathname: bytes, line: int, message: bytes):
        if not pathname:
            pathname = b"stdin"
        sys.stdout.flush()
        sys.stderr.buffer.write(b"m4:%b:%d: ERROR: %b\n" % (pathname, line, message))
        sys.stderr.flush()
        raise ParserExit(1)

    def warn(self, pathname: bytes, line: int, message: bytes):
        if not pathname:
            pathname = b"stdin"
        sys.stdout.flush()
        sys.stderr.buffer.write(b"m4:%b:%d: Warning: %b\n" % (pathname, line, message))
        sys.stderr.flush()

    def warn_excess_arguments(self, pathname: bytes, line: int, arg0: bytes):
        self.warn(pathname, line, b"excess arguments to builtin `%b' ignored" % arg0)

    def warn_too_few_arguments(self, pathname: bytes, line: int, arg0: bytes):
        self.warn(pathname, line, b"too few arguments to builtin `%b'" % arg0)

    def info(self, pathname: bytes, line: int, message: bytes):
        if not pathname:
            pathname = b"stdin"
        sys.stdout.flush()
        sys.stderr.buffer.write(b"m4:%b:%d: %b\n" % (pathname, line, message))
        sys.stderr.flush()

    def info_empty_string_is_zero(self, pathname: bytes, line: int, arg0: bytes):
        self.info(pathname, line, b"empty string treated as 0 in builtin `%b'" % arg0)

    def info_nonnumeric_argument_to_builtin(
        self, pathname: bytes, line: int, arg0: bytes
    ):
        self.info(pathname, line, b"non-numeric argument to builtin `%b'" % arg0)

    def info_nonnumeric_argument(self, pathname: bytes, line: int, arg: bytes):
        self.info(pathname, line, b"non-numeric argument %b" % arg)

    def info_numeric_overflow(self, pathname: bytes, line: int):
        self.info(pathname, line, b"numeric overflow detected")

    def debug(self, message: bytes):
        if self.debug_output:
            self.debug_output.write(message)
            self.debug_output.flush()

    def debug_trace(self, macro_name: bytes):
        self.debug(b"m4trace: -%d- %b\n" % (self.recursion_depth, macro_name))

    def prepend_macroexpansion(self, s: bytes) -> "Parser":
        if s:
            self.stream.prepend_macroexpansion(s)
        return self

    def peek(self, size: int = 1) -> bytes:
        return self.stream.peek(size)

    def discard(self, size: int = 1) -> bytes:
        s = self.stream.peek(size)
        self.stream.consume(size)
        return s

    def read(self, size: int = 8196) -> int:
        return self.stream.read(size)

    def max_toklen(self):
        return len(max((b"1",) + self.qdelim + self.cdelim, key=len))

    def discard_to_next_line(self):
        while True:
            c = self.discard()
            if not c or c == b"\n":
                return

    def write(self, src: bytes, divnum: int | None = None):
        if not divnum:
            divnum = self.current_diversion
        match self.mode:
            case Mode.NORMAL:
                if divnum == 0:
                    sys.stdout.buffer.write(src)
                    # If -s enabled:
                    sys.stdout.flush()
                elif divnum > 0:
                    self.diversions[self.current_diversion] += src
            case Mode.COLLECT_ARGS:
                self.output += src

    def len(self) -> int:
        return len(self.stream.regionbuffer())

    def locate(self, needle: bytes) -> int:
        while True:
            i = self.stream.data().find(needle)
            if i != -1:
                return i
            if self.read() == 0:
                return -1

    def is_collecting(self) -> bool:
        return self.mode == Mode.COLLECT_ARGS

    def consume_whitespace(self):
        while True:
            c = self.peek(1)
            if c == b" " or c == b"\n":
                self.discard(1)
            else:
                return

    def consume_word(self) -> bytes:
        c = self.peek(1)
        if c.isalpha() or c == b"_":
            i = 0
            while (
                self.stream.data()[i : i + 1].isalnum()
                or self.stream.data()[i : i + 1] == b"_"
            ):
                i += 1
                if i == self.len():
                    self.read()
                    if i == self.len():
                        break
            return self.discard(i)
        else:
            return b""

    def consume_comment(self) -> bytes | None:
        i = self.locate(self.cdelim[1])
        if i == -1:
            return None
        return self.discard(i)

    def consume_arguments(self) -> list[bytes]:
        if self.peek() != b"(":
            return []
        self.discard(1)
        output = self.output
        mode = self.mode
        count_closed_paren = self.count_closed_paren
        recursion_depth = self.recursion_depth
        args = []
        pathname, line = self.stream.current_pathname_and_line()
        self.mode = Mode.COLLECT_ARGS
        self.count_closed_paren = 1
        self.recursion_depth += 1
        while True:
            self.output = b""
            self.consume_whitespace()
            self.parse()
            if self.defn_token:
                args.append(self.defn_token)
                self.defn_token = None
            else:
                args.append(self.output)
            c = self.discard(1)
            if c == b")" and self.count_closed_paren == 0:
                break
            elif not c:
                # Discard partially collected output.
                self.output = b""
                self.error(pathname, line, b"end of file in argument list")
                raise ParserEOF
        self.output = output
        self.mode = mode
        self.count_closed_paren = count_closed_paren
        self.recursion_depth = recursion_depth
        return args

    def consume_quote(self) -> bytes | None:
        i = 0
        balance = 0
        if not self.stream.data().startswith(self.qdelim[0]):
            raise Exception("consume_quote() called when no open quote exists.")
        while True:
            if i == self.len():
                if self.read() == 0:
                    return None
            if self.stream.data()[i:].startswith(self.qdelim[1]):
                balance -= 1
                i += len(self.qdelim[1])
            elif self.stream.data()[i:].startswith(self.qdelim[0]):
                balance += 1
                i += len(self.qdelim[0])
            else:
                i += 1
            if balance == 0:
                break
        s = self.discard(i)
        return s[len(self.qdelim[0]) : -len(self.qdelim[1])]

    def quotes_enabled(self) -> bool:
        return self.qdelim[0] != b""

    def comments_enabled(self) -> bool:
        return self.cdelim[0] != b""

    def parse(self):
        while True:
            s = self.peek(self.max_toklen())
            if not s:
                return
            if self.comments_enabled() and s.startswith(self.cdelim[0]):
                pathname, line = self.stream.current_pathname_and_line()
                comment = self.consume_comment()
                if comment is None:
                    self.finish_parsing()
                    self.error(pathname, line, b"end of file in comment")
                else:
                    self.write(comment)
            elif self.quotes_enabled() and s.startswith(self.qdelim[0]):
                pathname, line = self.stream.current_pathname_and_line()
                quote = self.consume_quote()
                if quote is None:
                    self.finish_parsing()
                    self.error(pathname, line, b"end of file in string")
                else:
                    self.write(quote)
            elif s[0:1].isalpha() or s.startswith(b"_"):
                pathname, line = self.stream.current_pathname_and_line()
                word = self.consume_word()
                macros = self.macros.get(word)
                if not macros:
                    self.write(word)
                else:
                    macro = macros[-1]
                    args = self.consume_arguments()
                    if isinstance(macro, Builtin):
                        self.prepend_macroexpansion(
                            self.call_builtin(
                                pathname, line, [macro.value] + args, self.prefix
                            )
                        )
                    else:
                        args = [b"" if isinstance(x, Builtin) else x for x in args]
                        if self.traced_macros[word]:
                            self.debug_trace(word)
                        self.prepend_macroexpansion(
                            replace_dollars(macro, [word] + args)
                        )
            elif s.startswith(b"("):
                if self.is_collecting():
                    self.count_closed_paren += 1
                self.write(self.discard(1))
            elif s.startswith(b")"):
                if self.is_collecting():
                    self.count_closed_paren -= 1
                    if self.count_closed_paren == 0:
                        return
                self.write(self.discard(1))
            elif s.startswith(b","):
                if self.is_collecting():
                    return
                self.write(self.discard(1))
            else:
                c = self.discard(1)
                if c != b"\0":
                    self.write(c)

    def call_builtin(
        self, pathname: bytes, line: int, args: list[bytes], prefix: bytes, from_indir: bool = False
    ) -> bytes:
        word = args[0]
        if (word != prefix + b"define" and word != prefix + b"pushdef") or len(
            args
        ) != 3:
            # Turn the Builtin token introduced via defn() into the
            # empty string.
            args = [b"" if isinstance(x, Builtin) else x for x in args]
        if not from_indir and self.traced_macros[word]:
            self.debug_trace(word)
        if word == prefix + b"define":
            return self.m4_define(pathname, line, args)
        elif word == prefix + b"undefine":
            return self.m4_undefine(args)
        elif word == prefix + b"pushdef":
            return self.m4_pushdef(pathname, line, args)
        elif word == prefix + b"popdef":
            return self.m4_popdef(args)
        elif word == prefix + b"dnl":
            return self.m4_dnl(pathname, line, args)
        elif word == prefix + b"incr":
            return self.m4_incr(pathname, line, args)
        elif word == prefix + b"decr":
            return self.m4_decr(pathname, line, args)
        elif word == prefix + b"changequote":
            return self.m4_changequote(pathname, line, args)
        elif word == prefix + b"changecom":
            return self.m4_changecom(pathname, line, args)
        elif word == prefix + b"len":
            return self.m4_len(pathname, line, args)
        elif word == prefix + b"index":
            return self.m4_index(pathname, line, args)
        elif word == prefix + b"dumpdef":
            return self.m4_dumpdef(pathname, line, args)
        elif word == prefix + b"regexp":
            return self.m4_regexp(pathname, line, args)
        elif word == prefix + b"eval":
            return self.m4_eval(pathname, line, args)
        elif word == prefix + b"mkstemp":
            return self.m4_mkstemp(pathname, line, args)
        elif word == prefix + b"maketemp":
            return self.m4_maketemp(pathname, line, args)
        elif word == prefix + b"substr":
            return self.m4_substr(pathname, line, args)
        elif word == prefix + b"patsubst":
            return self.m4_patsubst(pathname, line, args)
        elif word == prefix + b"format":
            return self.m4_format(pathname, line, args)
        elif word == prefix + b"syscmd":
            return self.m4_syscmd(pathname, line, args)
        elif word == prefix + b"sysval":
            return self.m4_sysval(args)
        elif word == prefix + b"esyscmd":
            return self.m4_esyscmd(pathname, line, args)
        elif word == prefix + b"ifdef":
            return self.m4_ifdef(pathname, line, args)
        elif word == prefix + b"ifelse":
            return self.m4_ifelse(pathname, line, args)
        elif word == prefix + b"include":
            return self.m4_include(pathname, line, args)
        elif word == prefix + b"sinclude":
            return self.m4_sinclude(args)
        elif word == prefix + b"divert":
            return self.m4_divert(pathname, line, args)
        elif word == prefix + b"undivert":
            return self.m4_undivert(pathname, line, args)
        elif word == prefix + b"divnum":
            return self.m4_divnum(pathname, line, args)
        elif word == prefix + b"m4exit":
            return self.m4_m4exit(pathname, line, args)
        elif word == prefix + b"shift":
            return self.m4_shift(args)
        elif word == prefix + b"errprint":
            return self.m4_errprint(args)
        elif word == prefix + b"builtin":
            return self.m4_builtin(pathname, line, args)
        elif word == prefix + b"indir":
            return self.m4_indir(pathname, line, args)
        elif word == prefix + b"defn":
            return self.m4_defn(pathname, line, args)
        elif word == prefix + b"translit":
            return self.m4_translit(pathname, line, args)
        elif word == prefix + b"m4wrap":
            return self.m4_m4wrap(args)
        elif word == prefix + b"__file__":
            return self.m4___file__(pathname, line, args)
        elif word == prefix + b"__line__":
            return self.m4___line__(pathname, line, args)
        elif word == prefix + b"__program__":
            return self.m4___program__(pathname, line, args)
        elif word == prefix + b"__unix__":
            return self.m4___unix__(args)
        elif word == prefix + b"__gnu__":
            return self.m4___gnu__(args)
        elif word == prefix + b"__windows__":
            return self.m4___windows__(args)
        elif word == prefix + b"__os2__":
            return self.m4___os2__(args)
        elif word == prefix + b"debugfile":
            return self.m4_debugfile(pathname, line, args)
        elif word == prefix + b"traceon":
            return self.m4_traceon(args)
        elif word == prefix + b"traceoff":
            return self.m4_traceoff(args)
        return b""

    def m4_define(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) > 3:
            self.warn_excess_arguments(pathname, line, args[0])
        ident = index_default(args, 1, b"")
        defn = index_default(args, 2, b"")
        if self.macros.get(ident) is None:
            self.macros[ident] = [defn]
        else:
            # GNU ext define: replace top. Others: replace all with 1.
            self.macros[ident][-1] = defn
        return b""

    def m4_undefine(self, args: list[bytes]) -> bytes:
        for ident in args[1:]:
            if self.macros.get(ident) is not None:
                self.macros[ident].clear()
        return b""

    def m4_pushdef(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) > 3:
            self.warn_excess_arguments(pathname, line, args[0])
        ident = index_default(args, 1, b"")
        defn = index_default(args, 2, b"")
        if self.macros.get(ident) is None:
            self.macros[ident] = [defn]
        else:
            self.macros[ident].append(defn)
        return b""

    def m4_popdef(self, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        for ident in args[1:]:
            if self.macros.get(ident):
                self.macros[ident].pop()
        return b""

    def m4_dnl(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) > 1:
            self.warn_excess_arguments(pathname, line, args[0])
        self.discard_to_next_line()
        return b""

    def m4_incr(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        # args[1] may exist and be a number, invalid, b"", or not
        # exist.
        number = index_default(args, 1, b"")
        if number == b"":
            self.info_empty_string_is_zero(pathname, line, args[0])
            number = b"0"
        try:
            number = c_int32(int(number) + 1).value
            number = bytes(str(number), "ascii")
            return number
        except ValueError:
            return b""

    def m4_decr(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        number = index_default(args, 1, b"")
        if number == b"":
            self.info_empty_string_is_zero(pathname, line, args[0])
            number = b"0"
        try:
            number = c_int32(int(number) - 1).value
            number = bytes(str(number), "ascii")
            return number
        except ValueError:
            return b""

    def m4_changecom(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        begin = index_default(args, 1, b"")
        end = index_default(args, 2, b"")
        if len(args) > 3:
            self.warn_excess_arguments(pathname, line, args[0])
        if not begin:
            self.cdelim = (b"", b"")
            return b""
        if not end:
            # GNU ext changecom: end is \n if empty. Others: preserve previous.
            end = b"\n"
        self.cdelim = (begin, end)
        return b""

    def m4_changequote(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.qdelim = (b"`", b"'")
            return b""
        elif len(args) > 3:
            self.warn_excess_arguments(pathname, line, args[0])
        begin = index_default(args, 1, b"")
        end = index_default(args, 2, b"")
        if not begin:
            begin = b""
            end = b""
        elif begin and not end:
            end = b"'"
        self.qdelim = (begin, end)
        return b""

    def m4_len(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        arg = index_default(args, 1, b"")
        return bytes(str(len(arg)), "ascii")

    def m4_index(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) < 3:
            self.warn_too_few_arguments(pathname, line, args[0])
        arg_string = index_default(args, 1, b"")
        arg_substring = index_default(args, 2, b"")
        index = arg_string.find(arg_substring)
        return bytes(str(index), "ascii")

    def m4_dumpdef(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        ms = [m for m in self.macros if self.macros[m]]
        ms.sort()
        if len(args) != 1:
            ms = [m for m in args[1:] if m in ms]
            ms.sort()
        for arg in args[1:]:
            if not self.macros.get(arg):
                self.info(pathname, line, b"undefined macro `%b'" % arg)
        for m in ms:
            dfn = self.macros[m][-1]
            self.debug(b"%b:\t" % m)
            if isinstance(dfn, Builtin):
                self.debug(b"<%b>\n" % m)
            else:
                self.debug(b"%b\n" % dfn)
        return b""

    def m4_regexp(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        arg_string = index_default(args, 1, b"")
        arg_regexp = index_default(args, 2, b"")
        arg_replacement = index_default(args, 3, b"")
        if len(args) < 4:
            # index mode
            p = pygnuregex.compile(arg_regexp)
            index = p.search(arg_string)
            if index == -1:
                return b"-1"
            else:
                return bytes(str(index), "ascii")

        else:
            if len(args) > 4:
                self.warn_excess_arguments(pathname, line, args[0])
            # replace mode
            p = pygnuregex.compile(arg_regexp)
            result = p.search(arg_string)
            if result == -1:
                return b""
            else:
                return regexp_replacement(arg_string, arg_replacement, p.span())

    def m4_eval(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        arg_expression = index_default(args, 1, b"")
        arg_radix = index_default(args, 2, b"")
        arg_width = index_default(args, 3, b"")
        if not arg_expression:
            self.info_empty_string_is_zero(pathname, line, args[0])
            arg_expression = b"0"
        if not arg_radix:
            arg_radix = b"10"
        arg_radix = int(arg_radix)
        if arg_radix > 36:
            self.info(
                pathname,
                line,
                b"radix %d in builtin `%b' out of range" % (arg_radix, args[0]),
            )
        if not arg_width:
            arg_width = b"0"
        arg_width = int(arg_width)
        if arg_width < 0:
            self.info(pathname, line, b"negative width to builtin `%b'" % args[0])
        if arg_width < 0:
            return b""
        result = calc(arg_expression)
        for info in calc_info():
            match info:
                case CalcInfo.DEPRECATED_EQ:
                    self.warn(
                        pathname, line, b"recommend ==, not =, for equality operator"
                    )
                case CalcInfo.DIV_BY_ZERO:
                    self.info(
                        pathname, line, b"divide by zero in eval: %b" % arg_expression
                    )
                case CalcInfo.NEGATIVE_EXP:
                    self.info(
                        pathname,
                        line,
                        b"negative exponent in eval: %b" % arg_expression,
                    )
                case CalcInfo.INVALID_UNARY_OP | CalcInfo.INVALID_BINARY_OP:
                    self.returncode = 1
                    self.info(
                        pathname, line, b"invalid operator in eval: %b" % arg_expression
                    )
        if isinstance(result, BadInput):
            self.info(
                pathname,
                line,
                b"bad expression in eval (bad input): %b" % arg_expression,
            )
        elif isinstance(result, ParserError):
            self.info(pathname, line, b"bad expression in eval: %b" % arg_expression)
        if isinstance(result, PropagatingError):
            return b""
        arg_width += int(result < 0)
        result = radix_str(result, arg_radix)
        return result.zfill(arg_width)

    def m4_mkstemp(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        arg_template = index_default(args, 1, b"")
        arg_template = create_string_buffer(augment_trailing_x(arg_template))
        fd = libc.mkstemp(arg_template)
        if fd > 0:
            libc.close(fd)
            self.write(arg_template.value)
        return b""

    def m4_maketemp(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        return self.m4_mkstemp(pathname, line, args)

    def m4_substr(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) < 3:
            self.warn_too_few_arguments(pathname, line, args[0])
        arg_string = index_default(args, 1, b"")
        arg_from = index_default(args, 2, b"")
        arg_length = index_default(args, 3, b"")
        if not arg_from:
            if len(args) > 2:
                self.info_empty_string_is_zero(pathname, line, args[0])
            return arg_string
        try:
            arg_from = int(arg_from)
        except:
            self.info_nonnumeric_argument_to_builtin(pathname, line, args[0])
            return b""
        if arg_length:
            try:
                arg_length = int(arg_length)
            except:
                self.info_nonnumeric_argument_to_builtin(pathname, line, args[0])
                return b""
        elif len(args) > 3:
            self.info_empty_string_is_zero(pathname, line, args[0])
            return b""
        if arg_from < 0 or arg_from >= len(arg_string):
            return b""
        elif arg_length:
            if arg_length < 0:
                return b""
            else:
                arg_length = min(len(arg_string) - arg_from, arg_length)
        else:
            arg_length = len(arg_string) - arg_from
        return arg_string[arg_from : arg_from + arg_length]

    def m4_patsubst(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) < 3:
            self.warn_too_few_arguments(pathname, line, args[0])
        arg_string = index_default(args, 1, b"")
        arg_regexp = index_default(args, 2, b"")
        arg_replacement = index_default(args, 3, b"")
        try:
            p = pygnuregex.compile(arg_regexp)
        except RuntimeError as e:
            self.info(
                pathname,
                line,
                b"bad regular expression `%b': %b" % (arg_regexp, str(e).encode()),
            )
            return b""
        check = arg_replacement[-2:]
        if len(check) == 2 and check[0] != b"\\"[0] and check[1] == b"\\"[0]:
            self.warn(pathname, line, b"trailing \\ ignored in replacement")
            arg_replacement = arg_replacement[:-1]
        acc = b""
        prev = 0
        for span in p.finditer(arg_string):
            start, end = span[0]
            acc += arg_string[prev:start]
            acc += regexp_replacement(arg_string, arg_replacement, span)
            prev = end
        acc += arg_string[prev:]
        return acc

    # TODO Probably instead of throwing FormatException I need to deal
    # with the errors in-place. Most errors should result in arguments
    # converted to zero or the empty string.
    def m4_format(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        conversion_spec = (
            b"%(['\\-+ #0]+)?(\\*|[0-9]+)?\\.?(\\*|[0-9]+)?(h{1,2}|l{1,2}|[jztL])?(.)?"
        )
        if len(args) == 1:
            self.write(args[0])
            return b""
        arg_format_string = index_default(args, 1, b"")
        p = re.compile(conversion_spec)
        i = 2
        prev = 0
        out = b""
        for m in p.finditer(arg_format_string):
            begin, end = m.span()
            out += arg_format_string[prev:begin]
            flags, padding, precision, modifier, conversion = m.groups()
            flags = set(flags) if flags else None
            # TODO WARNING: check spec in each case and warn if wrong;
            # don't bother with Python's % if so. Don't forget to
            # check the modifier; ll, j, z, t, L not recognized, and
            # some modifiers are incompatible with the conversions,
            # e.g. %hf.
            try:
                # Only the h, hh, and l modifiers are supported by m4's format().
                if (
                    modifier
                    and modifier != b"h"
                    and modifier != b"hh"
                    and modifier != b"l"
                ):
                    self.warn(
                        pathname,
                        line,
                        b"unrecognized specifier in `%b'" % arg_format_string,
                    )
                    raise FormatException
                match conversion:
                    case b"d" | b"i" | b"o" | b"u" | b"x" | b"X" | b"c":
                        if conversion == b"c" and flags and not flags <= set(b"-"):
                            # TODO WARNING: incorrect flags for %c
                            raise FormatException
                        xs = []
                        if padding:
                            try:
                                if padding == b"*":
                                    pa = index_default(args, i, b"0")
                                    i += 1
                                    xs.append(int(pa))
                            except:
                                # TODO WARNING: padding is not an integer (should processing continue?)
                                self.info_nonnumeric_argument(pathname, line, pa)
                                xs.append(0)
                        if precision:
                            try:
                                if precision == b"*":
                                    pr = index_default(args, i, b"0")
                                    i += 1
                                    xs.append(int(pr))
                            except:
                                # TODO WARNING: precision is not an integer (should processing continue?)
                                self.info_nonnumeric_argument(pathname, line, pr)
                                xs.append(0)
                        x = index_default(args, i, b"0")
                        if not x:
                            self.info(pathname, line, b"empty string treated as 0")
                            x = b"0"
                        i += 1
                        try:
                            num = self.int_pat.match(x)
                            if num and num.end() != len(x):
                                raise
                            n = int(x)
                            if n >= 2**31 or n < -(2**31):
                                self.info_numeric_overflow(pathname, line)
                                n = -1
                            xs.append(n)
                        except:
                            self.info_nonnumeric_argument(pathname, line, x)
                            if num:
                                xs.append(int(num.group()))
                            else:
                                xs.append(0)
                        if xs[-1] == 0:
                            if len(xs) > 1 and (xs[0] == 0 or xs[1] == 0):
                                pass
                            elif (flags and b"0"[0] in flags) or (
                                precision and int(precision) == 0
                            ):
                                pass
                            else:
                                out += m.group() % tuple(xs)
                        else:
                            out += m.group() % tuple(xs)
                    case b"f" | b"F" | b"e" | b"E" | b"g" | b"G" | b"a" | b"A":
                        xs = []
                        if padding:
                            try:
                                if padding == b"*":
                                    pa = index_default(args, i, b"0")
                                    i += 1
                                    xs.append(int(pa))
                            except:
                                # TODO WARNING: padding is not an integer (should processing continue?)
                                self.info_nonnumeric_argument(pathname, line, pa)
                                xs.append(0)
                        if precision:
                            try:
                                if precision == b"*":
                                    pr = index_default(args, i, b"0")
                                    i += 1
                                    xs.append(int(pr))
                            except:
                                # TODO WARNING: precision is not an integer (should processing continue?)
                                self.info_nonnumeric_argument(pathname, line, pr)
                                xs.append(0)
                        x = index_default(args, i, b"0")
                        if not x:
                            self.info(pathname, line, b"empty string treated as 0")
                            x = b"0"
                        i += 1
                        try:
                            num = self.float_pat.match(x)
                            if num and num.end() != len(x):
                                raise
                            f = float(x)
                            if isinf(f):
                                x = x.lower()
                                if x[:1] == b"+" or x[:1] == b"-":
                                    x = x[1:]
                                if x != b"inf" and x != b"infinity":
                                    self.info_numeric_overflow(pathname, line)
                            xs.append(f)
                        except:
                            self.info_nonnumeric_argument(pathname, line, x)
                            if num:
                                xs.append(float(num.group()))
                            else:
                                xs.append(0.0)
                        out += m.group() % tuple(xs)
                    case b"s":
                        x = index_default(args, i, b"")
                        out += m.group() % x
                        i += 1
                    case b"%":
                        out += b"%"
                    case _:
                        # TODO WARNING: not a recognized conversion specifier
                        raise FormatException
            except FormatException:
                # TODO print a warning here?
                pass
            prev = end
        out += arg_format_string[prev:]
        return out

    def m4_syscmd(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        shell_command = index_default(args, 1, b"")
        sys.stdout.buffer.write(self.output)
        sys.stdout.flush()
        sys.stderr.flush()
        self.output = b""
        try:
            code = subprocess.run(["sh", "-c", shell_command]).returncode
            # If this is a signal, shift by 8 bits left.
            if code < 0:
                code = -code << 8
            self.cmd_code = bytes(str(code), encoding="ascii")
        except:
            self.cmd_code = b"127"
        return b""

    def m4_sysval(self, args: list[bytes]) -> bytes:
        del args
        return self.cmd_code

    def m4_esyscmd(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        arg_shell_command = index_default(args, 1, b"")
        sys.stdout.buffer.write(self.output)
        sys.stdout.flush()
        sys.stderr.flush()
        self.output = b""
        try:
            proc = subprocess.run(
                ["sh", "-c", arg_shell_command], stdout=subprocess.PIPE
            )
            code = proc.returncode
            # If this is a signal, shift by 8 bits left.
            if code < 0:
                code = -code << 8
            self.cmd_code = bytes(str(code), encoding="ascii")
            return proc.stdout
        except:
            self.cmd_code = b"127"
        return b""

    def m4_ifdef(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) == 2:
            self.warn_too_few_arguments(pathname, line, args[0])
        elif len(args) > 4:
            self.warn_excess_arguments(pathname, line, args[0])
        arg_name = index_default(args, 1, b"")
        arg_string_1 = index_default(args, 2, b"")
        arg_string_2 = index_default(args, 3, b"")
        if self.macros.get(arg_name):
            return arg_string_1
        else:
            return arg_string_2

    def m4_ifelse(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        n = len(args)
        if n == 1:
            self.write(args[0])
            return b""
        elif n == 2:
            return b""
        elif n == 3:
            self.warn_too_few_arguments(pathname, line, args[0])
            return b""
        i = 1
        while n >= 4:
            arg_string_1 = index_default(args, i, b"")
            arg_string_2 = index_default(args, i + 1, b"")
            arg_equal = index_default(args, i + 2, b"")
            if arg_string_1 == arg_string_2:
                return arg_equal
            n -= 3
            i += 3
        if n == 3:
            self.warn_excess_arguments(pathname, line, args[0])
        return index_default(args, i, b"")

    def m4_include(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        arg_file = index_default(args, 1, b"")
        f, path = self.open_file(arg_file)
        if f is None:
            self.info(
                pathname,
                line,
                b"cannot open `%b': No such file or directory" % arg_file,
            )
            self.returncode = 1
        else:
            self.stream.push_file(f, path)
        return b""

    def m4_sinclude(self, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        arg_file = index_default(args, 1, b"")
        f, path = self.open_file(arg_file)
        if f is not None:
            self.stream.push_file(f, path)
        return b""

    def m4_divert(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        arg_number = index_default(args, 1, b"0")
        num = self.int_pat.match(arg_number)
        if not num or num.end() != len(arg_number):
            self.info_nonnumeric_argument_to_builtin(pathname, line, args[0])
        else:
            self.current_diversion = int(arg_number)
        return b""

    def m4_undivert(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        arg_number = index_default(args, 1, b"0")
        num = self.int_pat.match(arg_number)
        if not num or num.end() != len(arg_number):
            f, _ = self.open_file(arg_number)
            if not f:
                self.info(
                    pathname,
                    line,
                    b"cannot undivert `%b': No such file or directory" % arg_number,
                )
            else:
                self.write(f.read())
                f.close()
        else:
            undiverted = int(arg_number)
            if undiverted != self.current_diversion and undiverted >= 0:
                self.write(self.diversions[undiverted])
                self.diversions[undiverted] = b""
        return b""

    def m4_divnum(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) > 1:
            self.warn_excess_arguments(pathname, line, args[0])
        return bytes(str(self.current_diversion), encoding="ascii")

    def m4_m4exit(self, pathname: bytes, line: int, args: list[bytes]):
        if len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        arg_code = index_default(args, 1, b"")
        if not arg_code:
            if len(args) > 1:
                self.info_empty_string_is_zero(pathname, line, args[0])
            arg_code = b"0"
        code = self.int_pat.match(arg_code)
        if not code or code.end() != len(arg_code):
            self.info_nonnumeric_argument_to_builtin(pathname, line, args[0])
            code = 1
        else:
            code = int(arg_code)
            if code < 0 or code > 255:
                self.info(pathname, line, b"exit status out of range: `%d'" % code)
                code = 1
        raise ParserExit(code)

    def m4_shift(self, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        return self.qdelim[0] + b",".join(args[2:]) + self.qdelim[1]

    def m4_errprint(self, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        # GNU ext: going past 1st argument
        sys.stderr.buffer.write(b" ".join(args[1:]))
        sys.stderr.flush()
        return b""

    def m4_builtin(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        arg_name = index_default(args, 1, b"")
        if arg_name in builtins:
            return self.call_builtin(pathname, line, args[1:], b"")
        else:
            self.info(pathname, line, b"undefined builtin `%b'" % arg_name)
            return b""

    def m4_indir(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        arg_name = index_default(args, 1, b"")
        macros = self.macros.get(arg_name)
        if macros:
            macro = macros[-1]
            if isinstance(macro, Builtin):
                return self.call_builtin(pathname, line, args[1:], self.prefix, from_indir=True)
            else:
                return replace_dollars(macro, args[1:])
        else:
            self.info(pathname, line, b"undefined macro `%b'" % arg_name)
            return b""

    def m4_defn(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        acc = []
        flag = False
        for arg in args[1:]:
            macros = self.macros.get(arg)
            if macros:
                macro = macros[-1]
                if isinstance(macro, Builtin):
                    flag = True
                    acc.append(Builtin(arg))
                else:
                    acc.append(macro)
        if flag and len(acc) > 1:
            for x in acc:
                if isinstance(x, Builtin):
                    self.warn(
                        pathname, line, b"cannot concatenate builtin `%b'" % x.value
                    )
            acc = [x for x in acc if not isinstance(x, Builtin)]
        if len(acc) == 1 and isinstance(acc[0], Builtin):
            self.defn_token = acc[0]
            return b""
        else:
            return b"".join(self.qdelim[0] + x + self.qdelim[1] for x in acc)

    def m4_translit(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        arg_string = index_default(args, 1, b"")
        arg_chars = index_default(args, 2, b"")
        arg_replacement = index_default(args, 3, b"")
        if len(args) == 1:
            self.write(args[0])
            return b""
        elif len(args) == 2:
            self.warn_too_few_arguments(pathname, line, args[0])
            return arg_string
        tm = TranslitMap.from_spec(arg_chars, arg_replacement)
        return tm.translit(arg_string)

    def m4_m4wrap(self, args: list[bytes]) -> bytes:
        if len(args) == 1:
            self.write(args[0])
            return b""
        # GNU ext: use rest args by joining with space
        s = b" ".join(args[1:])
        pathname, line = self.stream.current_pathname_and_line()
        self.m4wrap.push_file(BytesIO(s), pathname, FrozenInt(line))
        return b""

    def m4___file__(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        pathname, line = self.stream.current_pathname_and_line()
        if len(args) > 1:
            self.warn_excess_arguments(pathname, line, args[0])
        return self.qdelim[0] + pathname + self.qdelim[1]

    def m4___line__(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        pathname, line = self.stream.current_pathname_and_line()
        if len(args) > 1:
            self.warn_excess_arguments(pathname, line, args[0])
        return self.qdelim[0] + str(line).encode() + self.qdelim[1]

    def m4___program__(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        if len(args) > 1:
            self.warn_excess_arguments(pathname, line, args[0])
        return self.qdelim[0] + b"m4" + self.qdelim[1]

    def m4___unix__(self, args: list[bytes]) -> bytes:
        del args
        return b""

    def m4___gnu__(self, args: list[bytes]) -> bytes:
        del args
        return b""

    def m4___windows__(self, args: list[bytes]) -> bytes:
        del args
        return b""

    def m4___os2__(self, args: list[bytes]) -> bytes:
        del args
        return b""

    def m4_debugfile(self, pathname: bytes, line: int, args: list[bytes]) -> bytes:
        # TODO add trace output effects too
        if len(args) == 1:
            if self.debug_output and self.debug_output != sys.stderr.buffer:
                self.debug_output.close()
            self.debug_output = sys.stderr.buffer
            return b""
        elif len(args) > 2:
            self.warn_excess_arguments(pathname, line, args[0])
        arg_file = index_default(args, 1, b"")
        if not arg_file:
            if self.debug_output and self.debug_output != sys.stderr.buffer:
                self.debug_output.close()
            self.debug_output = None
        else:
            try:
                f = open(arg_file, "ab")
                if self.debug_output and self.debug_output != sys.stderr.buffer:
                    self.debug_output.close()
                    self.debug_output = f
            except:
                self.info(pathname, line, b"cannot set debug file `%b': Permission denied" % arg_file)
        return b""

    def m4_traceon(self, args: list[bytes]) -> bytes:
        if len(args) == 1:
            for name, value in self.macros.items():
                if value:
                    self.traced_macros[name] = True
        else:
            for name in args[1:]:
                self.traced_macros[name] = True
        return b""

    def m4_traceoff(self, args: list[bytes]) -> bytes:
        if len(args) == 1:
            for name, value in self.macros.items():
                if value:
                    self.traced_macros[name] = False
        else:
            for name in args[1:]:
                self.traced_macros[name] = False
        return b""

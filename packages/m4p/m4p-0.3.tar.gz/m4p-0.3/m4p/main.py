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

import argparse
import pkg_resources
import sys
from m4p.stream import Stream
from m4p.parser import Parser, ParserEOF, ParserExit
from os import fsencode


def main():
    try:
        _main()
    except KeyboardInterrupt:
        print()
        pass


def _main():
    prog_name = "m4p"
    prog_version = pkg_resources.get_distribution(prog_name).version
    p = argparse.ArgumentParser(
        prog=prog_name,
        description="Process macros in FILEs.  If no FILE or if FILE is `-', standard input is read.",
    )
    opmodes = p.add_argument_group(description="Operation modes:")
    ppfeats = p.add_argument_group(description="Preprocessor features:")
    debugging = p.add_argument_group(description="Debugging:")
    opmodes.add_argument(
        "-P",
        "--prefix-builtins",
        action="store_true",
        help="force a `m4_' prefix to all builtins",
    )
    p.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{prog_name} {prog_version}",
        help="output version information and exit",
    )
    ppfeats.add_argument(
        "-B", type=fsencode, action="append", default=[], help=argparse.SUPPRESS
    )
    ppfeats.add_argument(
        "-I",
        "--include",
        action="append",
        default=[],
        metavar="DIRECTORY",
        help="append DIRECTORY to include path",
        type=fsencode,
    )
    debugging.add_argument(
        "--debugfile",
        metavar="FILE",
        nargs="?",
        default=argparse.SUPPRESS,
        help="redirect debug and trace output to FILE (default stderr, discard if empty string)",
        type=fsencode,
    )
    p.add_argument("FILE", nargs="*", help="", type=fsencode)
    args = p.parse_args()
    if args.B:
        sys.stderr.buffer.write(
            b"m4: warning: `m4 -B' may be removed in a future release\n"
        )
    files = args.FILE
    if not files:
        files = [b"-"]
    parser = None
    for file in files:
        pathname = file if file != b"-" else None
        try:
            f = open(file, "rb") if file != b"-" else sys.stdin.buffer
        except:
            sys.stderr.buffer.write(
                b"m4: cannot open `%b': No such file or directory\n" % file
            )
            continue
        stream = Stream()
        stream.push_file(f, pathname)
        if parser is None:
            parser = Parser.new(stream=stream, configuration=vars(args))
        else:
            parser.stream = stream
        try:
            parser.parse()
        except ParserExit as e:
            sys.exit(e.code)
        except ParserEOF:
            pass
        sys.stdout.buffer.write(parser.output)
        sys.stdout.flush()
        parser.output = b""
    if parser:
        parser.finish()
        sys.exit(parser.returncode)


if __name__ == "__main__":
    main()

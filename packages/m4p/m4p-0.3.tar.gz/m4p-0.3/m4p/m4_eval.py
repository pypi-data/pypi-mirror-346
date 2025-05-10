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

from lark import Lark, Transformer, UnexpectedCharacters, v_args
from ctypes import c_int32
from string import digits, ascii_lowercase
from re import compile
from enum import Enum, auto


def radix(n: int, base: int):
    while n > 0:
        q, r = divmod(n, base)
        n = q
        yield r


def radix_str(n: int, base: int) -> bytes:
    if n < 0:
        return b"-" + radix_str(-n, base)
    ds = digits + ascii_lowercase
    if base == 1:
        return b"1" * n
    elif base > 36 or base < 1:
        return b""
    xs = radix(n, base)
    b = b""
    for d in xs:
        b += bytes(ds[d], encoding="ascii")
    if not b:
        return b"0"
    return bytes(reversed(b))


class CalcInfo(Enum):
    DEPRECATED_EQ = auto()
    DIV_BY_ZERO = auto()
    NEGATIVE_EXP = auto()
    INVALID_UNARY_OP = auto()
    INVALID_BINARY_OP = auto()


class PropagatingError:
    pass


def guard(*args) -> PropagatingError | None:
    """Check arguments against PropagatingError.

    If any of the arguments is a PropagatingError, return it, or None

    """
    return next((arg for arg in args if isinstance(arg, PropagatingError)), None)


class ParserError(PropagatingError):
    pass


class BadInput(ParserError):
    pass


class InvalidUnaryOperator(PropagatingError):
    pass


class InvalidBinaryOperator(PropagatingError):
    pass


class DivByZero(PropagatingError):
    pass


class NegExp(PropagatingError):
    pass


# For C's operator precedence see
# <https://en.cppreference.com/w/c/language/operator_precedence>.
calc_grammar = """
    ?start: assignment

    ?assignment: logical_or
        | logical_or  "+=" logical_or -> invalid_binary_operator
        | logical_or  "-=" logical_or -> invalid_binary_operator
        | logical_or  "*=" logical_or -> invalid_binary_operator
        | logical_or  "/=" logical_or -> invalid_binary_operator
        | logical_or  "%=" logical_or -> invalid_binary_operator
        | logical_or  "|=" logical_or -> invalid_binary_operator
        | logical_or  "&=" logical_or -> invalid_binary_operator
        | logical_or  "^=" logical_or -> invalid_binary_operator
        | logical_or ">>=" logical_or -> invalid_binary_operator
        | logical_or "<<=" logical_or -> invalid_binary_operator

    ?logical_or: logical_and
        | logical_or "||" logical_and -> logical_or

    ?logical_and: bitwise_or
        | logical_and "&&" bitwise_or -> logical_and

    ?bitwise_or: bitwise_xor
        | bitwise_or "|" bitwise_xor -> or_

    ?bitwise_xor: bitwise_and
        | bitwise_xor "^" bitwise_and -> xor

    ?bitwise_and: equation
        | bitwise_and "&" equation -> and_

    ?equation: inequality
        | equation "!=" inequality  -> ne
        | equation "==" inequality  -> eq
        | equation  "=" inequality  -> deprecated_eq

    ?inequality: shift
        | inequality ">"  shift -> gt
        | inequality ">=" shift -> ge
        | inequality "<"  shift -> lt
        | inequality "<=" shift -> le

    ?shift: sum
        | shift "<<" sum -> lshift
        | shift ">>" sum -> rshift

    ?sum: product
        | sum "+" product   -> add
        | sum "-" product   -> sub

    ?product: pow
        | product "*" pow   -> mul
        | product "/" pow   -> div
        | product "%" pow   -> mod

    ?pow: atom
        | atom "**" pow  -> pow

    BINARY: /0b[0-1]+/i
    OCTAL: /0[0-7]*/
    DECIMAL: /[1-9][0-9]*/
    HEX: /0x[0-9a-f]+/i
    RBASE: /0r/i DECIMAL ":" /[0-9a-f]+/i

    ?atom: BINARY  -> binary_number
         | OCTAL   -> octal_number
         | DECIMAL -> decimal_number
         | HEX     -> hex_number
         | RBASE   -> rbase_number
         | "+" atom         -> identity
         | "-" atom         -> neg
         | "~" atom         -> invert
         | "!" atom         -> not_
         | "--" atom        -> invalid_unary_operator
         | "++" atom        -> invalid_unary_operator
         | atom "--"        -> invalid_unary_operator
         | atom "++"        -> invalid_unary_operator
         | "(" equation ")"

    %import common.WS_INLINE

    %ignore WS_INLINE
"""


@v_args(inline=True)
class CalculateTree(Transformer):
    def __init__(self):
        self.info = []

    def reset(self):
        self.info.clear()

    def add(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x + y

    def sub(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x - y

    def mul(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x * y

    def neg(self, x):
        g = guard(x)
        if g:
            return g
        else:
            return -x

    def gt(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x > y

    def ge(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x >= y

    def lt(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x < y

    def le(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x <= y

    def ne(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x != y

    def and_(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x & y

    def xor(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x ^ y

    def or_(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x | y

    def invert(self, x):
        g = guard(x)
        if g:
            return g
        else:
            return ~x

    def not_(self, x):
        g = guard(x)
        if g:
            return g
        else:
            return 0 if x else 1

    def eq(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x == y

    def deprecated_eq(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            self.info.append(CalcInfo.DEPRECATED_EQ)
            return x == y

    def lshift(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x << (y & 0x1F)

    def rshift(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            return x >> (y & 0x1F)

    def invalid_unary_operator(self, x):
        g = guard(x)
        if g:
            return g
        else:
            self.info.append(CalcInfo.INVALID_UNARY_OP)
            return InvalidUnaryOperator()

    def invalid_binary_operator(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            self.info.append(CalcInfo.INVALID_BINARY_OP)
            return InvalidBinaryOperator()

    def pow(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            if x == 0 and y == 0:
                self.info.append(CalcInfo.DIV_BY_ZERO)
                return DivByZero()
            elif y < 0:
                self.info.append(CalcInfo.NEGATIVE_EXP)
                return NegExp()
            else:
                return x**y

    def mod(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            if y == 0:
                self.info.append(CalcInfo.DIV_BY_ZERO)
                return DivByZero()
            else:
                return x % y

    def div(self, x, y):
        g = guard(x, y)
        if g:
            return g
        else:
            if y == 0:
                self.info.append(CalcInfo.DIV_BY_ZERO)
                return DivByZero()
            else:
                return x // y

    def binary_number(self, token):
        return int(token.value, base=2)

    def octal_number(self, token):
        return int(token.value, base=8)

    def decimal_number(self, token):
        return int(token.value, base=10)

    def hex_number(self, token):
        return int(token.value, base=16)

    base1 = compile(b"^0*(1*)$")

    def rbase_number(self, token):
        base, value = token.value[2:].split(b":")
        base = int(base)
        if base == 1:
            m = self.base1.match(value).group(1)
            return len(m)
        return int(value, base=base)

    def identity(self, x):
        return x

    def logical_and(self, x, y):
        if x == 0:
            return 0
        if isinstance(x, DivByZero):
            return x
        elif isinstance(y, DivByZero):
            return y
        return int(x != 0 and y != 0)

    def logical_or(self, x, y):
        if isinstance(x, DivByZero):
            return x
        elif x == 0 and isinstance(y, DivByZero):
            return y
        return int(x != 0 or y != 0)


calc_parser = Lark(
    calc_grammar, use_bytes=True, parser="lalr", transformer=CalculateTree()
)


def calc(s: bytes) -> int | PropagatingError:
    try:
        calc_parser.options.options["transformer"].reset()
        result = calc_parser.parse(s)
    except ValueError:
        return BadInput()
    except UnexpectedCharacters as e:
        return BadInput()
    except:
        return ParserError()
    g = guard(result)
    if g:
        return g
    else:
        return c_int32(result).value


def calc_info():
    return calc_parser.options.options["transformer"].info

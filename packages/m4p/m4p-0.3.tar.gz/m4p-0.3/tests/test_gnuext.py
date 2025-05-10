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

from subprocess import run


def test_resources(pytestconfig, source_combinations):
    base = pytestconfig.rootpath.joinpath("tests", "resources")
    if not isinstance(source_combinations, list):
        source_combinations = [source_combinations]
    paths = [base.joinpath(f) for f in source_combinations]
    for path in paths:
        assert path.is_file(), f"Does {path} exist and is it readable?"
    paths_s = [str(path) for path in paths]
    expected = run(["m4", "-I", str(base)] + paths_s, capture_output=True)
    actual = run(["m4p", "-I", str(base)] + paths_s, capture_output=True)
    try:
        expected_out = str(expected.stdout, encoding="utf-8")
        actual_out = str(actual.stdout, encoding="utf-8")
    except UnicodeDecodeError:
        expected_out = expected.stdout
        actual_out = actual.stdout
    try:
        expected_err = str(expected.stderr, encoding="utf-8")
        actual_err = str(actual.stderr, encoding="utf-8")
    except UnicodeDecodeError:
        expected_err = expected.stderr
        actual_err = actual.stderr
    assert (
        expected_out == actual_out
    ), "m4 stdout output differs from m4p stdout output."
    assert (
        expected_err == actual_err
    ), "m4 stderr output differs from m4p stderr output."
    assert (
        expected.returncode == actual.returncode
    ), "m4 return code differs from m4p return code."

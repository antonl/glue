from __future__ import absolute_import, division, print_function

import pytest

from ..misc import as_variable_name, file_format, DeferredMethod, nonpartial, lookup_class, as_list


def test_as_variable_name():
    def check(input, expected):
        assert as_variable_name(input) == expected

    tests = [('x', 'x'),
             ('x2', 'x2'),
             ('2x', '_2x'),
             ('x!', 'x_'),
             ('x y z', 'x_y_z'),
             ('_XY', '_XY')
             ]
    for input, expected in tests:
        yield check, input, expected


class TestFileFormat(object):

    def test_gz(self):
        fmt = file_format('test.tar.gz')
        assert fmt == 'tar'

    def test_normal(self):
        fmt = file_format('test.data')
        assert fmt == 'data'

    def test_underscores(self):
        fmt = file_format('test_file.fits_file')
        assert fmt == 'fits_file'

    def test_multidot(self):
        fmt = file_format('test.a.b.c')
        assert fmt == 'c'

    def test_nodot(self):
        fmt = file_format('test')
        assert fmt == ''


def test_deferred_method():

    class Test(object):

        def __init__(self):
            self.a = 1

        def change_a(self):
            self.a = 2

    t = Test()

    Test.change_a = DeferredMethod(Test.change_a)

    t.change_a()

    assert t.a == 1

    Test.change_a.execute_deferred_calls()

    assert t.a == 2


def test_nonpartial():

    def test(a=1, b=2):
        pass

    test_wrapped = nonpartial(test)
    test_wrapped(a=1, b=2, c=3)


def test_lookup_class():

    lookup_class('glue.utils.misc.DeferredMethod') is DeferredMethod

    with pytest.raises(ValueError) as exc:
        lookup_class('gluh.utils.misc.DeferredMethod') is None
    assert exc.value.args[0] == "Module 'gluh.utils.misc' not found"

    with pytest.raises(ValueError) as exc:
        lookup_class('glue.utils.misc.DeferredMethods') is None
    assert exc.value.args[0] == "Object 'glue.utils.misc.DeferredMethods' not found"


def test_as_list():
    as_list(1) == [1]
    as_list([2, 3]) == [2, 3]

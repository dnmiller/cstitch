import os.path

import cstitch
from cstitch import from_header


def get_header(name):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'headers', name)


def test_enum_header():
    """Enums in headers are parsed correctly."""
    modname = 'mymod'
    mod = from_header(modname, (get_header('test_enum.h'),))

    def assert_enum_val(obj, expected):
        for name, value in expected.iteritems():
            if hasattr(obj, '__module__'):
                assert obj.__module__ == modname
                assert name not in mod.__dict__
            else:
                assert name in mod.__dict__
            assert getattr(obj, name) == value

    assert_enum_val(mod.TestEnum, expected={
        'TEST_ENUM_1': 0,
        'TEST_ENUM_2': 1,
        'TEST_ENUM_3': 2})

    assert_enum_val(mod.TYPEDEF_ENUM, expected={
        'TEST_TYPEDEF_ENUM_1': 0,
        'TEST_TYPEDEF_ENUM_2': 1,
        'TEST_TYPEDEF_ENUM_3': 2,
        'TEST_TYPEDEF_ENUM_4': 3})

    assert_enum_val(mod.OutOfOrderEnum, expected={
        'OUT_ENUM_1': -100,
        'OUT_ENUM_2': 0,
        'OUT_ENUM_3': 100,
        'OUT_ENUM_4': -1,
        'OUT_ENUM_5': 0})

    assert_enum_val(mod.RefEnum, expected={
        'REF_ENUM_1': 0,
        'REF_ENUM_2': 5,
        'REF_ENUM_3': 1})

    # Enums without labels get set at the module level.
    assert_enum_val(mod, expected={
        'ANON_ENUM_1': 0,
        'ANON_ENUM_2': 1,
        'ANON_ENUM_3': 5})


def test_primitives():
    """POD is parsed correctly"""


def test_main():
    assert cstitch  # use your library here

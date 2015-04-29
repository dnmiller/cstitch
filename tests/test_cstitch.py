import os.path
import ctypes

from cstitch import Stitched


def get_header(name):
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'headers', name)


def test_enums():
    """Enums in headers are parsed correctly."""
    obj = Stitched(get_header('test_enum.h'))

    def assert_enum_val(obj, expected):
        for name, value in expected.iteritems():
            assert name in obj.__dict__
            assert getattr(obj, name) == value

    assert hasattr(obj, 'TestEnum')
    assert_enum_val(obj.TestEnum, expected={
        'TEST_ENUM_1': 0,
        'TEST_ENUM_2': 1,
        'TEST_ENUM_3': 2})

    assert hasattr(obj, 'TYPEDEF_ENUM')
    assert_enum_val(obj.TYPEDEF_ENUM, expected={
        'TEST_TYPEDEF_ENUM_1': 0,
        'TEST_TYPEDEF_ENUM_2': 1,
        'TEST_TYPEDEF_ENUM_3': 2,
        'TEST_TYPEDEF_ENUM_4': 3})

    assert hasattr(obj, 'OutOfOrderEnum')
    assert_enum_val(obj.OutOfOrderEnum, expected={
        'OUT_ENUM_1': -100,
        'OUT_ENUM_2': 0,
        'OUT_ENUM_3': 100,
        'OUT_ENUM_4': -1,
        'OUT_ENUM_5': 0})

    assert hasattr(obj, 'RefEnum')
    assert_enum_val(obj.RefEnum, expected={
        'REF_ENUM_1': 0,
        'REF_ENUM_2': 5,
        'REF_ENUM_3': 1})

    # Enums without labels get set at the class level.
    assert_enum_val(obj, expected={
        'ANON_ENUM_1': 0,
        'ANON_ENUM_2': 1,
        'ANON_ENUM_3': 5})


def test_typedefs():
    """Typedefs are parsed correctly"""
    obj = Stitched(get_header('test_typedef.h'))

    # Assert standard typedefs
    assert obj.newtype1_t == ctypes.c_int
    assert obj.newtype2_t == obj.newtype1_t
    assert obj.newtype3_t == obj.newtype2_t
    assert obj.newtype4_t == obj.newtype3_t
    assert obj.newtype5_t == obj.newtype4_t

    # Assert external typedefs.
    assert obj.externtype1_t == ctypes.c_float
    assert obj.localtype1_t == obj.externtype1_t
    assert obj.localtype2_t == obj.externtype2_t
    assert obj.localtype3_t == obj.externtype3_t
    assert obj.newlocaltype_t == obj.localtype1_t

    # Assert typedefs from standard library.
    assert obj.stdtype == obj.size_t


def test_primitives():
    """POD is parsed correctly"""
    # modname = 'mymod'
    # obj = from_header(modname, (get_header('test_primitives.h'),))


def test_structs():
    """Struct definitions are parsed correctly"""
    # obj = Stitched(get_header('test_struct.h'))

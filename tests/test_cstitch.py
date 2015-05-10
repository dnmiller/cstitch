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
    assert obj.bool_type == ctypes.c_bool
    assert obj._Bool_type == ctypes.c_bool


def test_primitives():
    """POD is parsed correctly"""
    # obj = Stitched(get_header('test_primitives.h'))


def test_structs():
    """Struct definitions are parsed correctly"""
    obj = Stitched(get_header('test_struct.h'))

    # TestStruct
    fields = (
        ('bool_val', ctypes.c_bool),
        ('char_val', ctypes.c_char),
        ('schar_val', ctypes.c_char),
        ('uchar_val', ctypes.c_ubyte),
        ('short_val', ctypes.c_short),
        ('ushort_val', ctypes.c_ushort),
        ('int_val', ctypes.c_int),
        ('uint_val', ctypes.c_uint),
        ('long_val', ctypes.c_long),
        ('ulong_val', ctypes.c_ulong),
        ('float_val', ctypes.c_float),
        ('double_val', ctypes.c_double),
        ('ldouble_val', ctypes.c_longdouble),
        ('longlong_val', ctypes.c_longlong),
        ('ulonglong_val', ctypes.c_ulonglong))

    for name, field_type in fields:
        assert hasattr(obj.TestStruct, name)
        assert hasattr(getattr(obj.TestStruct, name), 'offset')
        assert hasattr(getattr(obj.TestStruct, name), 'size')
        assert field_type.__name__ in str(getattr(obj.TestStruct, name))

    # Test typedefs
    assert obj.FLOAT32 == ctypes.c_float
    assert obj.INT == ctypes.c_int

    # TestStructWithTypedefs
    assert 'c_float' in str(obj.TestStructWithTypedefs.float_val)
    assert 'c_int' in str(obj.TestStructWithTypedefs.int_val)

    # TypedefStruct
    assert 'c_char' in str(obj.TypedefStruct.char_val)
    assert 'c_long' in str(obj.TypedefStruct.long_val)

    # TypedefStruct2
    assert 'c_char' in str(obj.TypedefStruct2.char_val)
    assert 'c_long' in str(obj.TypedefStruct2.long_val)

    # StructWithSub
    assert 'TypedefStruct' in str(obj.StructWithSub.nested1)
    assert 'c_float' in str(obj.StructWithSub.float_val)
    x = obj.StructWithSub()
    assert hasattr(x.nested1, 'char_val')

    # StructWithDoubleSub
    assert 'TypedefStruct' in str(obj.StructWithDoubleSub.nested1)
    assert 'StructWithSub' in str(obj.StructWithDoubleSub.nested)
    x = obj.StructWithDoubleSub()
    assert hasattr(x.nested1, 'char_val')
    assert hasattr(x.nested, 'nested1')
    assert hasattr(x.nested.nested1, 'char_val')

    # WithNested
    assert 'NestedStruct' in str(obj.WithNested.nested)
    x = obj.WithNested()
    assert hasattr(x.nested, 'float_val')

    # WithNamelessNested
    assert '_WithNamelessNested_nested_type' in \
        str(obj.WithNamelessNested.nested)
    assert '_WithNamelessNested_nested2_type' in \
        str(obj.WithNamelessNested.nested2)
    x = obj.WithNamelessNested()
    assert hasattr(x.nested, 'float_val')
    assert hasattr(x.nested2, 'float_val')


def test_unions():
    """Union definitions are parsed correctly"""
    obj = Stitched(get_header('test_union.h'))

    # TestUnion
    fields = (
        ('bool_val', ctypes.c_bool),
        ('char_val', ctypes.c_char),
        ('schar_val', ctypes.c_char),
        ('uchar_val', ctypes.c_ubyte),
        ('short_val', ctypes.c_short),
        ('ushort_val', ctypes.c_ushort),
        ('int_val', ctypes.c_int),
        ('uint_val', ctypes.c_uint),
        ('long_val', ctypes.c_long),
        ('ulong_val', ctypes.c_ulong),
        ('float_val', ctypes.c_float),
        ('double_val', ctypes.c_double),
        ('ldouble_val', ctypes.c_longdouble),
        ('longlong_val', ctypes.c_longlong),
        ('ulonglong_val', ctypes.c_ulonglong))

    for name, field_type in fields:
        assert hasattr(obj.TestUnion, name)
        assert hasattr(getattr(obj.TestUnion, name), 'offset')
        assert hasattr(getattr(obj.TestUnion, name), 'size')
        assert field_type.__name__ in str(getattr(obj.TestUnion, name))

    # Test typedefs
    assert obj.FLOAT32 == ctypes.c_float
    assert obj.INT == ctypes.c_int

    # TestUnionWithTypedefs
    assert 'c_float' in str(obj.TestUnionWithTypedefs.float_val)
    assert 'c_int' in str(obj.TestUnionWithTypedefs.int_val)

    # TypedefUnion
    assert 'c_char' in str(obj.TypedefUnion.char_val)
    assert 'c_long' in str(obj.TypedefUnion.long_val)

    # TypedefUnion2
    assert 'c_char' in str(obj.TypedefUnion2.char_val)
    assert 'c_long' in str(obj.TypedefUnion2.long_val)

    # UnionWithSub
    assert 'TypedefUnion' in str(obj.UnionWithSub.nested1)
    assert 'c_float' in str(obj.UnionWithSub.float_val)
    x = obj.UnionWithSub()
    assert hasattr(x.nested1, 'char_val')

    # UnionWithDoubleSub
    assert 'TypedefUnion' in str(obj.UnionWithDoubleSub.nested1)
    assert 'UnionWithSub' in str(obj.UnionWithDoubleSub.nested)
    x = obj.UnionWithDoubleSub()
    assert hasattr(x.nested1, 'char_val')
    assert hasattr(x.nested, 'nested1')
    assert hasattr(x.nested.nested1, 'char_val')

    # WithNested
    assert 'NestedUnion' in str(obj.WithNested.nested)
    x = obj.WithNested()
    assert hasattr(x.nested, 'float_val')

    # WithNamelessNested
    assert '_WithNamelessNested_nested_type' in \
        str(obj.WithNamelessNested.nested)
    assert '_WithNamelessNested_nested2_type' in \
        str(obj.WithNamelessNested.nested2)
    x = obj.WithNamelessNested()
    assert hasattr(x.nested, 'float_val')
    assert hasattr(x.nested2, 'float_val')


def test_functions():
    """Function declarations are parsed correctly"""
    obj = Stitched(get_header('test_functions.h'))
    assert not hasattr(obj, 'ignored')

    assert hasattr(obj, 'dummy')
    assert obj.dummy.restype is None
    assert obj.dummy.argtypes == []

    assert hasattr(obj, 'no_ret')
    assert obj.no_ret.restype is None
    assert obj.no_ret.argtypes == [ctypes.c_int]

    assert hasattr(obj, 'no_args')
    assert obj.no_args.restype == ctypes.c_int
    assert obj.no_args.argtypes == []

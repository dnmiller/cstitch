"""Hello
"""
import os.path
import imp
import ctypes

from .clang import cindex as _cindex
from .clang.cindex import CursorKind as _ck
from .clang.cindex import TypeKind as _tk


_cindex.Config.set_library_file(
    '/Users/dan/Code/cstitch/cstitch/src/cstitch/libclang.3.6.dylib')


def from_header(modulename, filenames):
    """Parse a header file"""
    mod = imp.new_module(modulename)
    index = _cindex.Index.create()

    for filename in filenames:
        if not os.path.isfile(filename):
            raise RuntimeError('Cannot find file ' + filename)
        tu = index.parse(filename)

        # Quit if there are parser errors.
        diag = [d for d in tu.diagnostics]
        if diag:
            raise RuntimeError(
                'Parse errors in header:\n' + '\n'.join(str(d) for d in diag))

        for child in tu.cursor.get_children():
            # Ignore anything not in this file.
            if not child.location.file.name.endswith(filename):
                continue
            _cursor_map[child.kind](child, mod)

    return mod


def parse_enum_decl(cur, bind_to, name=None):
    """Parse an enumeration declaration"""
    # If the enum is typedef'd, we build an object. Otherwise, we just add the
    # constants at the module level.
    name = name if name else cur.spelling
    if name:
        # If we have a name, then create a new class and bind to that instead.
        rep = name + '(' + str(cur.location) + ')'

        def __repr__(self):
            return rep

        values = {
            '__repr__': classmethod(__repr__),
            '__module__': bind_to.__name__}

        new_type = type(name, (object,), values)
        setattr(bind_to, name, new_type)
        bind_to = new_type

    for child in cur.get_children():
        _cursor_map[child.kind](child, bind_to)


def parse_enum_constant_decl(obj, bind_to):
    setattr(bind_to, obj.spelling, obj.enum_value)


def parse_typedef_decl(cur, bind_to):
    """Parse a typedef"""
    type_cur = cur.underlying_typedef_type.get_declaration()
    if type_cur.kind == _ck.ENUM_DECL:
        # For enum typedefs, we go back and create a new class using the anon
        # enum declaration, then delete the old enums from the module.
        parse_enum_decl(type_cur, bind_to, cur.spelling)
        for child in type_cur.get_children():
            if child.spelling in bind_to.__dict__:
                delattr(bind_to, child.spelling)
    else:
        raise NotImplemented('Nope')


def parse_struct_decl(cur, bind_to):
    """Parse a struct declaration"""


def parse_field_decl(cur, bind_to):
    """Parse a struct or union field declaration"""


def parse_union_decl(cur, bind_to):
    """Parse a union declaration"""


def parse_function_decl(cur, bind_to):
    """Parse a function declaration"""


def parse_var_decl(cur, bind_to):
    """Parse a variable declaration"""


def parse_parm_decl(cur, bind_to):
    """Parse a function parameter declaration"""


def parse_type_ref(cur, bind_to):
    """Parse a type reference"""


def parse_integer_literal(cur, bind_to):
    """Parse an integer literal"""


def parse_floating_literal(cur, bind_to):
    """Parse a floating-point literal"""


def parse_character_literal(cur, bind_to):
    """Parse a character literal"""


_cursor_map = {
    _ck.ENUM_DECL:              parse_enum_decl,
    _ck.TYPEDEF_DECL:           parse_typedef_decl,
    _ck.ENUM_CONSTANT_DECL:     parse_enum_constant_decl,
    _ck.STRUCT_DECL:            parse_struct_decl,
    _ck.UNION_DECL:             parse_union_decl,
    _ck.FIELD_DECL:             parse_field_decl,
    _ck.FUNCTION_DECL:          parse_function_decl,
    _ck.VAR_DECL:               parse_var_decl,
    _ck.PARM_DECL:              parse_parm_decl,
    _ck.TYPE_REF:               parse_type_ref,

    # Literal types
    _ck.INTEGER_LITERAL:        parse_integer_literal,
    _ck.FLOATING_LITERAL:       parse_floating_literal,
    _ck.CHARACTER_LITERAL:      parse_character_literal
}

# Missing:
#
# c_char_p	char * (NUL terminated)	string or None
# c_wchar_p	wchar_t * (NUL terminated)	unicode or None
# c_void_p	void *	int/long or None

_type_map = {
    _tk.BOOL:           ctypes.c_bool,
    _tk.CHAR_S:         ctypes.c_char,
    "wchar":            ctypes.c_wchar,
    _tk.SCHAR:          ctypes.c_char,
    _tk.UCHAR:          ctypes.c_ubyte,
    _tk.SHORT:          ctypes.c_short,
    _tk.USHORT:         ctypes.c_ushort,
    _tk.INT:            ctypes.c_int,
    _tk.UINT:           ctypes.c_uint,
    _tk.LONG:           ctypes.c_long,
    _tk.ULONG:          ctypes.c_ulong,
    _tk.LONGLONG:       ctypes.c_longlong,
    _tk.ULONGLONG:      ctypes.c_ulonglong,
    _tk.FLOAT:          ctypes.c_float,
    _tk.DOUBLE:         ctypes.c_double,
    _tk.LONGDOUBLE:     ctypes.c_longdouble
}

"""Hello
"""
import os.path
import ctypes

from .clang import cindex as _cindex
from .clang.cindex import CursorKind as _ck
from .clang.cindex import TypeKind as _tk


_cindex.Config.set_library_file(
    '/Users/dan/Code/cstitch/cstitch/libclang.3.6.dylib')


# Missing:
#
# c_char_p  char * (NUL terminated) string or None
# c_wchar_p wchar_t * (NUL terminated)  unicode or None
# c_void_p  void *  int/long or None

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
    _tk.LONGDOUBLE:     ctypes.c_longdouble,
    _tk.VOID:           None
}


class Stitched(object):
    def __init__(self, filename):
        self.filename = filename

        self._cursor_map = {
            _ck.ENUM_DECL:              self._parse_enum_decl,
            _ck.TYPEDEF_DECL:           self._parse_typedef_decl,
            _ck.ENUM_CONSTANT_DECL:     self._parse_enum_constant_decl,
            _ck.STRUCT_DECL:            self._parse_struct_decl,
            _ck.UNION_DECL:             self._parse_union_decl,
            _ck.FUNCTION_DECL:          self._parse_function_decl,
            _ck.VAR_DECL:               self._parse_var_decl,
            # _ck.PARM_DECL:              self._parse_parm_decl,
            # _ck.TYPE_REF:               self._parse_type_ref,

            # # Literal types
            # _ck.INTEGER_LITERAL:        self._parse_integer_literal,
            # _ck.FLOATING_LITERAL:       self._parse_floating_literal,
            # _ck.CHARACTER_LITERAL:      self._parse_character_literal
        }

        if not os.path.isfile(filename):
            raise RuntimeError('Cannot find file ' + filename)

        tu = _cindex.Index.create().parse(filename)

        # Quit if there are parser errors.
        diag = [d for d in tu.diagnostics]
        if diag:
            raise RuntimeError(
                'Parse errors in header:\n' + '\n'.join(str(d) for d in diag))

        self._root_cursor = tu.cursor
        self._parse_cursor_children(tu.cursor, self)

    def _parse_cursor_children(self, cur, bind_to):
        """Iterate through the contents of a cursor.
        """
        for child in cur.get_children():
            # Ignore things that have been included from other files.
            if not child.location.file.name.endswith(self.filename):
                continue
            elif child.kind not in self._cursor_map:
                raise NotImplementedError('Unknown cursor kind %s'
                                          % child.kind)
            self._cursor_map[child.kind](child, bind_to)

    def _parse_enum_decl(self, cur, bind_to, name=None):
        """Parse an enumeration declaration

        Enum declarations are handled in two different ways. If the enum is
        typedef'd, then a new type is constructed with the individual enums
        bound to the class. If there is no typedef, then the constants are
        bound to the Stiched object.
        """
        # The name is '' if no typedef exists.
        name = name if name else cur.spelling
        if name:
            # If we have a name, then create a new class and bind to that
            # instead.
            rep = name + '(' + str(cur.location) + ')'

            def __repr__(self):
                return rep

            values = {'__repr__': classmethod(__repr__)}
            new_type = type(name, (object,), values)
            setattr(bind_to, name, new_type)

            self._parse_cursor_children(cur, new_type)

        else:
            self._parse_cursor_children(cur, bind_to)

    def _parse_enum_constant_decl(self, cur, bind_to):
        """Parse an enum constant"""
        setattr(bind_to, cur.spelling, cur.enum_value)

    def _parse_typedef_decl(self, cur, bind_to):
        """Parse a typedef"""
        type_ref = cur.underlying_typedef_type
        type_cur = type_ref.get_declaration()

        if type_cur.kind == _ck.ENUM_DECL:
            # For enum typedefs, we go back and create a new class using the
            # anon enum declaration, then delete the old enums from the
            # parent.
            self._parse_enum_decl(type_cur, bind_to, cur.spelling)
            for child in type_cur.get_children():
                if child.spelling in bind_to.__dict__:
                    delattr(bind_to, child.spelling)
        elif type_cur.kind == _ck.STRUCT_DECL:
            self._parse_struct_decl(type_cur, bind_to, cur.spelling)
        elif type_cur.kind == _ck.UNION_DECL:
            self._parse_union_decl(type_cur, bind_to, cur.spelling)
        elif type_ref.kind in _type_map:
            # Found a POD type, bind it to the class.
            setattr(bind_to, cur.spelling, _type_map[type_ref.kind])
        elif type_cur.kind == _ck.TYPEDEF_DECL:
            # If it's a typedef of a typedef, go back and find the old
            # typedef.
            self._parse_typedef_decl(type_cur, bind_to)
            setattr(bind_to, cur.spelling,
                    getattr(bind_to, type_cur.spelling))
        else:
            raise RuntimeError('Unknown type: %s' % type_cur.kind)

    def _parse_struct_decl(self, cur, bind_to, name=None):
        """Parse a struct declaration

        This creates a new class for the struct that mirrors the class
        declared in the header file.
        """
        name, values = self._parse_type_decl(cur, bind_to, name)
        new_type = type(name, (ctypes.Structure,), values)
        setattr(bind_to, name, new_type)

    def _parse_union_decl(self, cur, bind_to, name=None):
        """Parse a union declaration

        This creates a new class for the union that mirrors the class
        declared in the header file.
        """
        name, values = self._parse_type_decl(cur, bind_to, name)
        new_type = type(name, (ctypes.Union,), values)
        setattr(bind_to, name, new_type)

    def _parse_type_decl(self, cur, bind_to, name=None):
        """Parse a new data type. This can be a struct or union.
        """
        name = name if name else cur.spelling
        fields = []
        for child in cur.get_children():
            # Ignore things that have been included from other files.
            if not child.location.file.name.endswith(self.filename):
                continue

            if child.kind == _ck.STRUCT_DECL:
                if child.spelling == '':
                    # This is a nameless nested struct declaration, which is
                    # handled in the next itertion of the loop during the
                    # field declaration.
                    continue
                else:
                    # Named, nested struct declaration.
                    self._parse_struct_decl(child, bind_to)
            elif child.kind == _ck.UNION_DECL:
                if child.spelling == '':
                    # This is a nameless nested union declaration...
                    continue
                else:
                    # Named, nested union declaration.
                    self._parse_union_decl(child, bind_to)
            elif child.kind == _ck.FIELD_DECL:
                # A struct field.
                self._parse_field_decl(child, fields, name)
            else:
                raise NotImplementedError(
                    'Unknown cursor type inside struct declaration: %s' %
                    cur.location)
        rep = name + '(' + str(cur.location) + ')'

        def __repr__(self):
            return rep

        values = {
            '__repr__': classmethod(__repr__),
            '_fields_': fields
        }

        return name, values

    def _parse_field_decl(self, cur, fields, type_name=None):
        """Parse a struct or union field declaration"""
        if cur.type.kind in _type_map:
            field_type = _type_map[cur.type.kind]
        elif hasattr(self, cur.type.spelling):
            field_type = getattr(self, cur.type.spelling)
        elif cur.type.kind == _tk.TYPEDEF:
            # Go find this type (needed for stlib types)
            self._parse_typedef_decl(cur.type.get_declaration(), self)
            field_type = getattr(self, cur.type.spelling)
        elif cur.type.kind == _tk.UNEXPOSED:
            # We have a nested struct declaration someplace. Go find it.
            type_cur = cur.type.get_declaration()

            if type_cur.spelling != '':
                # Assume we've already parsed the declaration
                name = type_cur.spelling
            else:
                # Unnamed nested structure declarations don't really gel with
                # the ctypes interface, since Python requires all types to
                # have names. If we're given a nested struct declaration
                # without a name, then we spoof one from the name of the field
                # and enclosing struct. This means that declarations like
                #
                #   struct foo {
                #       struct {
                #           float x;
                #       } bar1, bar2;
                #   };
                #
                # will end up with two separate classes.
                name = '_' + type_name + '_' + cur.spelling + '_type'
                self._parse_struct_decl(type_cur, self, name)

            field_type = getattr(self, name)
        else:
            raise NotImplementedError('Field type %s is unknown' %
                                      cur.type.kind)

        fields.append((cur.spelling, field_type))

    def _parse_var_decl(self, cur, bind_to):
        """Parse a variable declaration"""
        raise NotImplementedError('global variables not yet figured out')

    def _parse_function_decl(self, cur, bind_to):
        """Parse a function declaration"""
        if 'static' in [t.spelling for t in cur.get_tokens()]:
            # Not sure what a static declaration is doing here, but ignore it
            # all the same. The is_static_methdd function in libclang seems to
            # only consider the C++ meaning of static.
            return
        setattr(self, cur.spelling, StichedFunction.from_cursor(cur))


class _UnlinkedFunction(object):
    def __init__(self, argtypes, restype, errcheck):
        self.argtypes = argtypes
        self.restype = restype
        self.errcheck = errcheck

    def __call__(self, *args, **kwargs):
        raise RuntimeError('StichedFunction is not linked to shared library')


class StichedFunction(object):
    def __init__(self, name, argtypes, restype, errcheck=None, lib=None,
                 location=None):
        self.name = name
        self._func = _UnlinkedFunction(argtypes, restype, errcheck)
        self.location = None
        self.link_library(lib)

    def __call__(self, *args):
        if len(args) != len(self.argtypes):
            raise RuntimeError('Invalid number of arguments')
        # TODO: Take optional kwargs if parsed
        self._func(*args)

    def link_library(self, lib):
        if lib:
            if not hasattr(lib, self.name):
                raise RuntimeError('symbol %s not found' % self.name)
            # Save function parameters to bind later
            argtypes, restype, errcheck = \
                self.argtypes, self.restype, self.errcheck
            # Get symbol from library and assign types
            self._func = getattr(lib, self.name)
            self._func.argtypes = argtypes
            self._func.restypes = restype
            self._func.errcheck = errcheck
        else:
            self._func = _UnlinkedFunction(self.argtypes, self.restype,
                                           self.errcheck)
        self._lib = lib

    @classmethod
    def from_cursor(cls, cur, lib=None):
        # Iterate over the function arguments.
        argtypes = []
        for arg in cur.get_arguments():
            if arg.type.kind in _type_map:
                argtypes.append(_type_map[arg.type.kind])

        if cur.result_type.kind in _type_map:
            restype = _type_map[cur.result_type.kind]

        return cls(cur.spelling, argtypes, restype, None, lib, cur.location)

    @property
    def argtypes(self):
        return self._func.argtypes

    @argtypes.setter
    def argtypes(self, argtypes):
        self._func.argtypes = argtypes

    @property
    def restype(self):
        return self._func.restype

    @restype.setter
    def restype(self, restype):
        self._func.restype = restype

    @property
    def errcheck(self):
        return self._func.errcheck

    @errcheck.setter
    def errcheck(self, errcheck):
        self._func.errcheck = errcheck

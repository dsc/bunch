__all__ = ('u', 'Mapping', 'Iterator', '_get_ident')

import sys

_IS_PYTHON_3 = (sys.version_info >= (3,))

identity = lambda x : x

# u('string') replaces the forwards-incompatible u'string'
if _IS_PYTHON_3:
    u = identity
else:
    import codecs
    def u(string):
        return codecs.unicode_escape_decode(string)[0]

# abstract collections moved
if _IS_PYTHON_3:
    from collections.abc import Mapping, Iterator
else:
    from collections import Mapping, Iterator

# threading in py3 was optional before 3.3
try:
    if _IS_PYTHON_3:
        try:
            from threading import get_ident as _get_ident
        except ImportError:
            from _thread import get_ident as _get_ident
    else:
        try:
            from thread import get_ident as _get_ident
        except ImportError:
            from dummy_thread import get_ident as _get_ident
finally:
    _get_ident = lambda : 1

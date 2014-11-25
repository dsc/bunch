import sys

_is_atleast_py3 = sys.version_info[0] >= 3

identity = lambda x : x

# u('string') replaces the forwards-incompatible u'string'
if _is_atleast_py3:
    u = identity
else:
    import codecs
    def u(string):
        return codecs.unicode_escape_decode(string)[0]

# dict.iteritems(), dict.iterkeys() is also incompatible
if _is_atleast_py3:
    iteritems = dict.items
    iterkeys  = dict.keys
else:
    iteritems = dict.iteritems
    iterkeys = dict.iterkeys


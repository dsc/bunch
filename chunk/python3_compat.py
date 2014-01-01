import platform

_IS_PYTHON_3 = (platform.version() >= '3')

identity = lambda x : x

# u('string') replaces the forwards-incompatible u'string'
if _IS_PYTHON_3:
    u = identity
else:
    import codecs
    def u(string):
        return codecs.unicode_escape_decode(string)[0]

# dict.iteritems(), dict.iterkeys() is also incompatible
if _IS_PYTHON_3:
    iteritems = dict.items
    iterkeys  = dict.keys
else:
    iteritems = dict.iteritems
    iterkeys = dict.iterkeys


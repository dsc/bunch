import six

# u('string') replaces the forwards-incompatible u'string'
if six.PY3:
    def u(string):
        return string
else:
    import codecs

    def u(string):
        return codecs.unicode_escape_decode(string)[0]

# dict.iteritems(), dict.iterkeys() is also incompatible
if six.PY3:
    iteritems = dict.items
    iterkeys = dict.keys
else:
    iteritems = dict.iteritems
    iterkeys = dict.iterkeys

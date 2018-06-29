#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" NeoBunch is a subclass of dict with attribute-style access.

    >>> b = NeoBunch()
    >>> b.hello = 'world'
    >>> b.hello
    'world'
    >>> b['hello'] += "!"
    >>> b.hello
    'world!'
    >>> b.foo = NeoBunch(lol=True)
    >>> b.foo.lol
    True
    >>> b.foo is b['foo']
    True

    It is safe to import * from this module:

        __all__ = ('NeoBunch', 'neobunchify','unneobunchify')

    un/neobunchify provide dictionary conversion; NeoBunches can also be
    converted via NeoBunch.to/fromDict().
"""


from .version import __version__
from .python3_compat import iteritems
from .python3_compat import iterkeys
from .python3_compat import u


VERSION = tuple(map(int, __version__.split('.')))
__all__ = (
    'NeoBunch', 'neobunchify', 'unneobunchify',  # new names
    'Bunch', 'bunchify', 'unbunchify',  # legacy names
)


class NeoBunch(dict):
    """ A dictionary that provides attribute-style access.

        >>> b = NeoBunch()
        >>> b.hello = 'world'
        >>> b.hello
        'world'
        >>> b['hello'] += "!"
        >>> b.hello
        'world!'
        >>> b.foo = NeoBunch(lol=True)
        >>> b.foo.lol
        True
        >>> b.foo is b['foo']
        True

        A NeoBunch is a subclass of dict;
        it supports all the methods a dict does.

        >>> sorted(b.keys())
        ['foo', 'hello']

        Including update()...

        >>> b.update({ 'ponies': 'are pretty!' }, hello=42)
        >>> print (repr(b))
        NeoBunch(foo=NeoBunch(lol=True), hello=42, ponies='are pretty!')

        As well as iteration...

        >>> dict([ (k,b[k]) for k in b ]) == dict([('foo', NeoBunch(lol=True)),
        ...     ('hello', 42), ('ponies', 'are pretty!')])
        True

        And "splats".

        >>> "The {knights} who say {ni}!".format(
        ...         **NeoBunch(knights='lolcats', ni='can haz')
        ... )
        'The lolcats who say can haz!'

        See unneobunchify/NeoBunch.toDict, neobunchify/NeoBunch.fromDict
        for notes about conversion.
    """

    def __contains__(self, k):
        """ >>> b = NeoBunch(ponies='are pretty!')
            >>> 'ponies' in b
            True
            >>> 'foo' in b
            False
            >>> b['foo'] = 42
            >>> 'foo' in b
            True
            >>> b.hello = 'hai'
            >>> 'hello' in b
            True
            >>> b[None] = 123
            >>> None in b
            True
            >>> b[False] = 456
            >>> False in b
            True
        """
        try:
            return dict.__contains__(self, k) or hasattr(self, k)
        except:
            return False

    # only called if k not found in normal places
    def __getattr__(self, k):
        """ Gets key if it exists, otherwise throws AttributeError.

            nb. __getattr__ is only called if key is not found in normal places.

            >>> b = NeoBunch(bar='baz', lol={})
            >>> b.foo
            Traceback (most recent call last):
                ...
            AttributeError: foo

            >>> b.bar
            'baz'
            >>> getattr(b, 'bar')
            'baz'
            >>> b['bar']
            'baz'

            >>> b.lol is b['lol']
            True
            >>> b.lol is getattr(b, 'lol')
            True
        """
        try:
            # Throws exception if not in prototype chain
            return object.__getattribute__(self, k)
        except AttributeError:
            try:
                return self[k]
            except KeyError:
                raise AttributeError(k)

    def __setattr__(self, k, v):
        """ Sets attribute k if it exists, otherwise sets key k. A KeyError
            raised by set-item (only likely if you subclass NeoBunch) will
            propagate as an AttributeError instead.

            >>> b = NeoBunch(foo='bar', this_is='useful when subclassing')
            >>> callable(b.values)
            True
            >>> b.values = 'uh oh'
            >>> b.values
            'uh oh'
            >>> b['values']
            Traceback (most recent call last):
                ...
            KeyError: 'values'
        """
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                self[k] = v
            except:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)

    def __delattr__(self, k):
        """ Deletes attribute k if it exists, otherwise deletes key k. A KeyError
            raised by deleting the key--such as when the key is missing--will
            propagate as an AttributeError instead.

            >>> b = NeoBunch(lol=42)
            >>> del b.lol
            >>> b.lol
            Traceback (most recent call last):
                ...
            AttributeError: lol
        """
        try:
            # Throws exception if not in prototype chain
            object.__getattribute__(self, k)
        except AttributeError:
            try:
                del self[k]
            except KeyError:
                raise AttributeError(k)
        else:
            object.__delattr__(self, k)

    def toDict(self):
        """ Recursively converts a neobunch back into a dictionary.

            >>> b = NeoBunch(foo=NeoBunch(lol=True), hello=42,
            ...              ponies='are pretty!')
            >>> d = b.toDict()
            >>> d == {'ponies': 'are pretty!',
            ...     'foo': {'lol': True}, 'hello': 42}
            True

            See unneobunchify for more info.
        """
        return unneobunchify(self)

    def __repr__(self):
        """ Invertible* string-form of a NeoBunch.

            >>> b = NeoBunch(foo=NeoBunch(lol=True), hello=42,
            ...              ponies='are pretty!')
            >>> print (repr(b))
            NeoBunch(foo=NeoBunch(lol=True), hello=42, ponies='are pretty!')
            >>> eval(repr(b))
            NeoBunch(foo=NeoBunch(lol=True), hello=42, ponies='are pretty!')

            (*) Invertible so long as collection contents are repr-invertible.
        """
        keys = list(iterkeys(self))
        keys.sort()
        args = ', '.join(['%s=%r' % (key, self[key]) for key in keys])
        return '%s(%s)' % (self.__class__.__name__, args)

    @staticmethod
    def fromDict(d):
        """ Recursively transforms a dictionary into a NeoBunch via copy.

            >>> b = NeoBunch.fromDict({'urmom': {'sez': {'what': 'what'}}})
            >>> b.urmom.sez.what
            'what'

            See neobunchify for more info.
        """
        return neobunchify(d)


# While we could convert abstract types like Mapping or Iterable, I think
# neobunchify is more likely to "do what you mean" if it is conservative about
# casting (ex: isinstance(str,Iterable) == True ).
#
# Should you disagree, it is not difficult to duplicate this function with
# more aggressive coercion to suit your own purposes.

def neobunchify(x):
    """ Recursively transforms a dictionary into a NeoBunch via copy.

        >>> b = neobunchify({'urmom': {'sez': {'what': 'what'}}})
        >>> b.urmom.sez.what
        'what'

        neobunchify can handle intermediary dicts, lists and tuples (as well as
        their subclasses), but ymmv on custom datatypes.

        >>> b = neobunchify({ 'lol': ('cats', {'hah':'i win again'}),
        ...         'hello': [{'french':'salut', 'german':'hallo'}] })
        >>> b.hello[0].french
        'salut'
        >>> b.lol[1].hah
        'i win again'

        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
    """
    if isinstance(x, dict):
        return NeoBunch((k, neobunchify(v)) for k, v in iteritems(x))
    elif isinstance(x, (list, tuple)):
        return type(x)(neobunchify(v) for v in x)
    else:
        return x


def unneobunchify(x):
    """ Recursively converts a NeoBunch into a dictionary.

        >>> b = NeoBunch(foo=NeoBunch(lol=True), hello=42, ponies='are pretty!')
        >>> d = unneobunchify(b)
        >>> d == {'ponies': 'are pretty!', 'foo': {'lol': True}, 'hello': 42}
        True

        unneobunchify will handle intermediary dicts, lists and tuples (as well
        as their subclasses), but ymmv on custom datatypes.

        >>> b = NeoBunch(foo=['bar', NeoBunch(lol=True)], hello=42,
        ...         ponies=('are pretty!', NeoBunch(lies='are trouble!')))
        >>> d = unneobunchify(b) #doctest: +NORMALIZE_WHITESPACE
        >>> d == {'ponies': ('are pretty!', {'lies': 'are trouble!'}),
        ...         'foo': ['bar', {'lol': True}], 'hello': 42}
        True

        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
    """
    if isinstance(x, dict):
        return dict((k, unneobunchify(v)) for k, v in iteritems(x))
    elif isinstance(x, (list, tuple)):
        return type(x)(unneobunchify(v) for v in x)
    else:
        return x


# Serialization

try:
    try:
        import json
    except ImportError:
        import simplejson as json

    def toJSON(self, **options):
        """ Serializes this NeoBunch to JSON.

        Accepts the same keyword options as `json.dumps()`.

            >>> b = NeoBunch(foo=NeoBunch(lol=True), hello=42,
            ...              ponies='are pretty!')
            >>> b.toJSON() == json.dumps(b)
            True
            >>> d = {"ponies": "are pretty!", "hello": 42, "foo": {"lol": True}}
            >>> json.loads(json.dumps(b)) == d
            True
        """
        return json.dumps(self, **options)

    NeoBunch.toJSON = toJSON

except ImportError:
    pass


try:
    # Attempt to register ourself with PyYAML as a representer
    import yaml
    from yaml.representer import Representer, SafeRepresenter

    def from_yaml(loader, node):
        """ PyYAML support with the tags `!neobunch` and `!neobunch.NeoBunch`.

            >>> import yaml
            >>> yaml.load('''
            ... Flow style:
            ...   !neobunch.NeoBunch {
            ...       Clark: Evans,
            ...       Brian: Ingerson,
            ...       Oren: Ben-Kiki
            ...   }
            ... Block style: !neobunch
            ...   Clark : Evans
            ...   Brian : Ingerson
            ...   Oren  : Ben-Kiki
            ... ''') #doctest: +NORMALIZE_WHITESPACE
            {
                'Flow style': NeoBunch(
                    Brian='Ingerson', Clark='Evans', Oren='Ben-Kiki'
                ),
                'Block style': NeoBunch(
                    Brian='Ingerson', Clark='Evans', Oren='Ben-Kiki'
                )
            }

            This module registers itself automatically to cover both NeoBunch
            and any subclasses. Should you want to customize the representation
            of a subclass, simply register it with PyYAML yourself.
        """
        data = NeoBunch()
        yield data
        value = loader.construct_mapping(node)
        data.update(value)

    def to_yaml_safe(dumper, data):
        """ Converts NeoBunch to a normal mapping node, making it appear as a
            dict in the YAML output.

            >>> b = NeoBunch(foo=['bar', NeoBunch(lol=True)], hello=42)
            >>> import yaml
            >>> yaml.safe_dump(b, default_flow_style=True)
            '{foo: [bar, {lol: true}], hello: 42}\\n'
        """
        return dumper.represent_dict(data)

    def to_yaml(dumper, data):
        """ Converts NeoBunch to a representation node.

            >>> b = NeoBunch(foo=['bar', NeoBunch(lol=True)], hello=42)
            >>> import yaml
            >>> yaml.dump(b, default_flow_style=True)
            '!neobunch.NeoBunch {foo: [bar, !neobunch.NeoBunch {lol: true}], hello: 42}\\n'
        """
        return dumper.represent_mapping(u('!neobunch.NeoBunch'), data)

    yaml.add_constructor(u('!neobunch'), from_yaml)
    yaml.add_constructor(u('!neobunch.NeoBunch'), from_yaml)

    SafeRepresenter.add_representer(NeoBunch, to_yaml_safe)
    SafeRepresenter.add_multi_representer(NeoBunch, to_yaml_safe)

    Representer.add_representer(NeoBunch, to_yaml)
    Representer.add_multi_representer(NeoBunch, to_yaml)

    # Instance methods for YAML conversion
    def toYAML(self, **options):
        """ Serializes this NeoBunch to YAML, using `yaml.safe_dump()` if
            no `Dumper` is provided. See the PyYAML documentation for more info.

            >>> b = NeoBunch(foo=['bar', NeoBunch(lol=True)], hello=42)
            >>> import yaml
            >>> yaml.safe_dump(b, default_flow_style=True)
            '{foo: [bar, {lol: true}], hello: 42}\\n'
            >>> b.toYAML(default_flow_style=True)
            '{foo: [bar, {lol: true}], hello: 42}\\n'
            >>> yaml.dump(b, default_flow_style=True)
            '!neobunch.NeoBunch {foo: [bar, !neobunch.NeoBunch {lol: true}], hello: 42}\\n'
            >>> b.toYAML(Dumper=yaml.Dumper, default_flow_style=True)
            '!neobunch.NeoBunch {foo: [bar, !neobunch.NeoBunch {lol: true}], hello: 42}\\n'
        """
        opts = dict(indent=4, default_flow_style=False)
        opts.update(options)
        if 'Dumper' not in opts:
            return yaml.safe_dump(self, **opts)
        else:
            return yaml.dump(self, **opts)

    def fromYAML(*args, **kwargs):
        return neobunchify(yaml.load(*args, **kwargs))

    NeoBunch.toYAML = toYAML
    NeoBunch.fromYAML = staticmethod(fromYAML)

except ImportError:
    pass


# alias legacy names
Bunch = NeoBunch
bunchify = neobunchify
unbunchify = unneobunchify


if __name__ == "__main__":
    import doctest
    doctest.testmod()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Bunch is a subclass of dict with attribute-style access.
    
    >>> b = Bunch()
    >>> b.hello = 'world'
    >>> b.hello
    'world'
    >>> b['hello'] += "!"
    >>> b.hello
    'world!'
    >>> b.foo = Bunch(lol=True)
    >>> b.foo.lol
    True
    >>> b.foo is b['foo']
    True
    
    It is safe to import * from this module:
    
        __all__ = ('Bunch', 'bunchify','unbunchify')
    
    un/bunchify provide dictionary conversion; Bunches can also be
    converted via Bunch.to/fromDict().
"""
__version__ = '1.0.2'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ('Bunch', 'bunchify', 'unbunchify',)

from bunch.python3_compat import *

class Bunch(dict):
    """ A dictionary that provides attribute-style access.
        
        >>> b = Bunch()
        >>> b.hello = 'world'
        >>> b.hello
        'world'
        >>> b['hello'] += "!"
        >>> b.hello
        'world!'
        >>> b.foo = Bunch(lol=True)
        >>> b.foo.lol
        True
        >>> b.foo is b['foo']
        True
        
        A Bunch is a subclass of dict; it supports all the methods a dict does...
        
        >>> sorted(b.keys())
        ['foo', 'hello']
        
        Including update()...
        
        >>> b.update({ 'ponies': 'are pretty!' }, hello=42)
        >>> print (repr(b))
        Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
        
        As well as iteration...
        
        >>> [ (k,b[k]) for k in b ]
        [('ponies', 'are pretty!'), ('foo', Bunch(lol=True)), ('hello', 42)]
        
        And "splats".
        
        >>> "The {knights} who say {ni}!".format(**Bunch(knights='lolcats', ni='can haz'))
        'The lolcats who say can haz!'
        
        See unbunchify/Bunch.toDict, bunchify/Bunch.fromDict for notes about conversion.
    """
    
    def __contains__(self, k):
        """ >>> b = Bunch(ponies='are pretty!')
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
        return dict.__contains__(self, k) or hasattr(self, k)
    
    # only called if k not found in normal places
    def __getattr__(self, k):
        """ Gets key if it exists, otherwise throws AttributeError.
            
            nb. __getattr__ is only called if key is not found in normal places.
            
            >>> b = Bunch(bar='baz', lol={})
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
            raised by set-item (only likely if you subclass Bunch) will 
            propagate as an AttributeError instead.
            
            >>> b = Bunch(foo='bar', this_is='useful when subclassing')
            >>> b.values                            #doctest: +ELLIPSIS
            <built-in method values of Bunch object at 0x...>
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
            except KeyError:
                raise AttributeError(k)
        else:
            object.__setattr__(self, k, v)
    
    def __delattr__(self, k):
        """ Deletes attribute k if it exists, otherwise deletes key k. A KeyError
            raised by deleting the key--such as when the key is missing--will
            propagate as an AttributeError instead.
            
            >>> b = Bunch(lol=42)
            >>> del b.values
            Traceback (most recent call last):
                ...
            AttributeError: 'Bunch' object attribute 'values' is read-only
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
    
    def copy(self):
        """ Makes a shallow copy of the Bunch.
            
            >>> a = Bunch(foo={'bar': 'baz'}, hello=42)
            >>> b = a.copy()
            >>> b
            Bunch(foo={'bar': 'baz'}, hello=42)
            >>> a is b
            False
            >>> a.foo is b.foo
            True
        """
        return self.__class__(self)
    
    def toDict(self, DictClass=dict):
        """ Recursively converts a Bunch back into a dictionary.
            
            >>> b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
            >>> b.toDict() == {'ponies': 'are pretty!', 'foo': {'lol': True}, 'hello': 42}
            True
            
            See unbunchify for more info.
        """
        return unbunchify(self, DictClass)
    
    def __add__(self, other):
        """ Creates a shallow copy of the Bunch, merging in another Mapping (or
            Iterable of key-value pairs).
            
            >>> a = Bunch(foo={}, hello=42)
            >>> a + { 'lol': True }
            Bunch(foo={}, hello=42, lol=True)
            >>> { 'reversed': True } + a
            Bunch(foo={}, hello=42, reversed=True)
            >>> b = a + (('pairs', 'are fine'), ['lol', False])
            >>> b
            Bunch(foo={}, hello=42, lol=False, pairs='are fine')
            >>> a is b
            False
            >>> a.foo is b.foo
            True
        """
        b = self.copy()
        b.update(other)
        return b
    
    __radd__ = __add__
    
    def __iadd__(self, other):
        """ Merges another Mapping (or Iterable of key-value pairs) into this Bunch.
            
            >>> a = Bunch(bar='baz', hello=0)
            >>> foo = { 'lol': True }
            >>> a += { 'hello': 42, 'foo': foo }
            >>> a
            Bunch(bar='baz', foo={'lol': True}, hello=42)
            >>> a.foo is foo
            True
        """
        self.update(other)
        return self
    
    def __repr__(self, _repr_running={}):
        """ Invertible* string-form of a Bunch.
            
            >>> b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
            >>> print (repr(b))
            Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
            >>> eval(repr(b)) == b
            True
            
            (*) Invertible so long as collection contents are each repr-invertible.
        """
        call_key = id(self), _get_ident()
        if call_key in _repr_running:
            return '...'
        _repr_running[call_key] = 1
        try:
            if not self:
                return '%s()' % (self.__class__.__name__,)
            args = ', '.join( ('%s=%r' % (k, self[k]) for k in sorted(self)) )
            return '%s(%s)' % (self.__class__.__name__, args)
        finally:
            del _repr_running[call_key]
    
    @classmethod
    def fromDict(cls, d):
        """ Recursively transforms a dictionary into a Bunch via copy.
            
            >>> b = Bunch.fromDict({'urmom': {'sez': {'what': 'what'}}})
            >>> b.urmom.sez.what
            'what'
            
            Aliased as ``Bunch.bunchify``.
            
            See ``bunch.bunchify`` for more info.
        """
        return bunchify(d, cls)
    
    bunchify = fromDict
    



# While we could convert abstract types like Mapping or Iterable, I think
# bunchify is more likely to "do what you mean" if it is conservative about
# casting (ex: isinstance(str,Iterable) == True ).
#
# Should you disagree, it is not difficult to duplicate this function with
# more aggressive coercion to suit your own purposes.

def bunchify(it, BunchClass=Bunch):
    """ Recursively transforms a dictionary into a Bunch via copy.
        
        >>> b = bunchify({'urmom': {'sez': {'what': 'what'}}})
        >>> b.urmom.sez.what
        'what'
        
        bunchify can handle intermediary dicts, lists and tuples (as well as
        their subclasses), but ymmv on custom datatypes.
        
        >>> b = bunchify({ 'lol': ('cats', {'hah':'i win again'}), 
        ...         'hello': [{'french':'salut', 'german':'hallo'}] })
        >>> b.hello[0].french
        'salut'
        >>> b.lol[1].hah
        'i win again'
        
        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
        
        You may customize Mapping conversion by passing a Bunch/dict class as 
        the second parameter.
    """
    if isinstance(it, Mapping):
        return BunchClass( (k, bunchify(v, BunchClass)) for k, v in it.iteritems() )
    elif isinstance(it, (list, tuple)):
        return type(it)( (bunchify(v, BunchClass) for v in it) )
    else:
        return it

def unbunchify(it, DictClass=dict):
    """ Recursively converts a Bunch into a dictionary via copy.
        
        >>> b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
        >>> unbunchify(b) == {'ponies': 'are pretty!', 'foo': {'lol': True}, 'hello': 42}
        True
    
        unbunchify will handle intermediary dicts, lists and tuples (as well as
        their subclasses), but ymmv on custom datatypes.
        
        >>> b = Bunch(foo=['bar', Bunch(lol=True)], hello=42, 
        ...         ponies=('are pretty!', Bunch(lies='are trouble!')))
        >>> unbunchify(b) == {'ponies': ('are pretty!', {'lies': 'are trouble!'}),
        ...         'foo': ['bar', {'lol': True}], 'hello': 42}
        True

        nb. As dicts are not hashable, they cannot be nested in sets/frozensets.
        
        You may customize Mapping conversion by passing a dict class as
        the second parameter.
    """
    if isinstance(it, Mapping):
        return DictClass( (k, unbunchify(v, DictClass)) for k, v in it.iteritems() )
    elif isinstance(it, (list, tuple)):
        return type(it)( (unbunchify(v, DictClass) for v in it) )
    else:
        return it


### Serialization

try:
    try:
        import json
    except ImportError:
        import simplejson as json
    
    def toJSON(self, **options):
        """ Serializes this Bunch to JSON. Accepts the same keyword options as ``json.dumps()``.
            
            >>> b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
            >>> json.dumps(b)
            '{"ponies": "are pretty!", "foo": {"lol": true}, "hello": 42}'
            >>> b.toJSON()
            '{"ponies": "are pretty!", "foo": {"lol": true}, "hello": 42}'
        """
        return json.dumps(self, **options)
    
    Bunch.toJSON = toJSON
    
except ImportError:
    pass




try:
    # Attempt to register ourself with PyYAML as a representer
    import yaml
    from yaml.representer import Representer, SafeRepresenter
    
    def from_yaml(loader, node):
        """ PyYAML support for Bunches using the tag ``!bunch`` and ``!bunch.Bunch``.
            
            >>> import yaml
            >>> yaml.load('''
            ... Flow style: !bunch.Bunch { Clark: Evans, Brian: Ingerson, Oren: Ben-Kiki }
            ... Block style: !bunch
            ...   Clark : Evans
            ...   Brian : Ingerson
            ...   Oren  : Ben-Kiki
            ... ''') #doctest: +NORMALIZE_WHITESPACE
            {'Flow style': Bunch(Brian='Ingerson', Clark='Evans', Oren='Ben-Kiki'), 
             'Block style': Bunch(Brian='Ingerson', Clark='Evans', Oren='Ben-Kiki')}
            
            This module registers itself automatically to cover both Bunch and any 
            subclasses. Should you want to customize the representation of a subclass,
            simply register it with PyYAML yourself.
        """
        data = Bunch()
        yield data
        value = loader.construct_mapping(node)
        data.update(value)
    
    
    def to_yaml_safe(dumper, data):
        """ Converts Bunch to a normal mapping node, making it appear as a
            dict in the YAML output.
            
            >>> b = Bunch(foo=['bar', Bunch(lol=True)], hello=42)
            >>> import yaml
            >>> yaml.safe_dump(b, default_flow_style=True)
            '{foo: [bar, {lol: true}], hello: 42}\\n'
        """
        return dumper.represent_dict(data)
    
    def to_yaml(dumper, data):
        """ Converts Bunch to a representation node.
            
            >>> b = Bunch(foo=['bar', Bunch(lol=True)], hello=42)
            >>> import yaml
            >>> yaml.dump(b, default_flow_style=True)
            '!bunch.Bunch {foo: [bar, !bunch.Bunch {lol: true}], hello: 42}\\n'
        """
        return dumper.represent_mapping(u('!bunch.Bunch'), data)
    
    
    yaml.add_constructor(u('!bunch'), from_yaml)
    yaml.add_constructor(u('!bunch.Bunch'), from_yaml)
    
    SafeRepresenter.add_representer(Bunch, to_yaml_safe)
    SafeRepresenter.add_multi_representer(Bunch, to_yaml_safe)
    
    Representer.add_representer(Bunch, to_yaml)
    Representer.add_multi_representer(Bunch, to_yaml)
    
    
    # Instance methods for YAML conversion
    def toYAML(self, **options):
        """ Serializes this Bunch to YAML, using ``yaml.safe_dump()`` if 
            no ``Dumper`` is provided. See the PyYAML documentation for more info.
            
            >>> b = Bunch(foo=['bar', Bunch(lol=True)], hello=42)
            >>> import yaml
            >>> yaml.safe_dump(b, default_flow_style=True)
            '{foo: [bar, {lol: true}], hello: 42}\\n'
            >>> b.toYAML(default_flow_style=True)
            '{foo: [bar, {lol: true}], hello: 42}\\n'
            >>> yaml.dump(b, default_flow_style=True)
            '!bunch.Bunch {foo: [bar, !bunch.Bunch {lol: true}], hello: 42}\\n'
            >>> b.toYAML(Dumper=yaml.Dumper, default_flow_style=True)
            '!bunch.Bunch {foo: [bar, !bunch.Bunch {lol: true}], hello: 42}\\n'
        """
        opts = dict(indent=2, default_flow_style=None)
        opts.update(options)
        if 'Dumper' not in opts:
            return yaml.safe_dump(self, **opts)
        else:
            return yaml.dump(self, **opts)
    
    
    def fromYAML(cls, *args, **kwargs):
        """ Convenience method for loading YAML and getting Bunches.
            
            >>> document = '''
            ... foo:
            ... - bar
            ... - lol: true
            ... hello: 42
            ... '''
            >>> Bunch.fromYAML(document)
            Bunch(foo=['bar', Bunch(lol=True)], hello=42)
            
            Uses ``yaml.load()`` by default; pass ``safe=True`` to use the SafeLoader,
            and/or ``all=True`` to load all documents (returning a list).
            
            >>> documents = '''
            ... ---
            ... - name: Hero
            ...   level: 4
            ...   hp: 34
            ... - name: Goblin
            ...   level: 1
            ...   hp: 8
            ... ---
            ... - name: Orc
            ...   level: 2
            ...   hp: 12
            ... '''
            >>> Bunch.fromYAML(documents, all=True) #doctest: +NORMALIZE_WHITESPACE
            [[Bunch(hp=34, level=4, name='Hero'), Bunch(hp=8, level=1, name='Goblin')],
              [Bunch(hp=12, level=2, name='Orc')]]
            
            All other options are passed to PyYAML, so you can still specify a
            custom loader with ``Bunch.fromYAML(data, Loader=CustomLoader)``.
        """
        method_name = 'load'
        if kwargs.pop('safe', False) and 'Loader' not in kwargs:
            method_name = 'safe_load'
        
        if kwargs.pop('all', False):
            data = list(getattr(yaml, method_name+'_all')(*args, **kwargs))
        else:
            data = getattr(yaml, method_name)(*args, **kwargs)
        return bunchify(data, cls)
    
    Bunch.toYAML = toYAML
    Bunch.fromYAML = classmethod(fromYAML)
    
except ImportError:
    pass


if __name__ == "__main__":
    import doctest
    doctest.testmod()


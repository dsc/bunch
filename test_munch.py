import json
import pytest
from munch import Munch, munchify, unmunchify


def test_base():
    b = Munch()
    b.hello = 'world'
    assert b.hello == 'world'
    b['hello'] += "!"
    assert b.hello == 'world!'
    b.foo = Munch(lol=True)
    assert b.foo.lol is True
    assert b.foo is b['foo']

    assert sorted(b.keys()) == ['foo', 'hello']

    b.update({'ponies': 'are pretty!'}, hello=42)
    assert b == Munch({'ponies': 'are pretty!', 'foo': Munch({'lol': True}), 'hello': 42})

    assert sorted([(k, b[k]) for k in b]) == [('foo', Munch({'lol': True})), ('hello', 42), ('ponies', 'are pretty!')]

    assert "The {knights} who say {ni}!".format(**Munch(knights='lolcats', ni='can haz')) == 'The lolcats who say can haz!'


def test_contains():
    b = Munch(ponies='are pretty!')
    assert 'ponies' in b
    assert ('foo' in b) is False

    b['foo'] = 42
    assert 'foo' in b

    b.hello = 'hai'
    assert 'hello' in b

    b[None] = 123
    assert None in b

    b[False] = 456
    assert False in b


def test_getattr():
    b = Munch(bar='baz', lol={})

    with pytest.raises(AttributeError):
        b.foo

    assert b.bar == 'baz'
    assert getattr(b, 'bar') == 'baz'
    assert b['bar'] == 'baz'
    assert b.lol is b['lol']
    assert b.lol is getattr(b, 'lol')


def test_setattr():
    b = Munch(foo='bar', this_is='useful when subclassing')
    assert hasattr(b.values, '__call__')

    b.values = 'uh oh'
    assert b.values == 'uh oh'

    with pytest.raises(KeyError):
        b['values']


def test_delattr():
    b = Munch(lol=42)
    del b.lol

    with pytest.raises(KeyError):
        b['lol']

    with pytest.raises(AttributeError):
        b.lol


def test_toDict():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert sorted(b.toDict().items()) == [('foo', {'lol': True}), ('hello', 42), ('ponies', 'are pretty!')]


def test_repr():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert repr(b).startswith("Munch({'")
    assert "'ponies': 'are pretty!'" in repr(b)
    assert "'hello': 42" in repr(b)
    assert "'foo': Munch({'lol': True})" in repr(b)
    assert "'hello': 42" in repr(b)

    with_spaces = Munch({1: 2, 'a b': 9, 'c': Munch({'simple': 5})})
    assert repr(with_spaces).startswith("Munch({")
    assert "'a b': 9" in repr(with_spaces)
    assert "1: 2" in repr(with_spaces)
    assert "'c': Munch({'simple': 5})" in repr(with_spaces)

    assert eval(repr(with_spaces)) == Munch({'a b': 9, 1: 2, 'c': Munch({'simple': 5})})


def test_dir():
    m = Munch(a=1, b=2)
    assert dir(m) == ['a', 'b']


def test_fromDict():
    b = Munch.fromDict({'urmom': {'sez': {'what': 'what'}}})
    assert b.urmom.sez.what == 'what'


def test_munchify():
    b = munchify({'urmom': {'sez': {'what': 'what'}}})
    assert b.urmom.sez.what == 'what'

    b = munchify({'lol': ('cats', {'hah': 'i win again'}), 'hello': [{'french': 'salut', 'german': 'hallo'}]})
    assert b.hello[0].french == 'salut'
    assert b.lol[1].hah == 'i win again'


def test_unmunchify():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert sorted(unmunchify(b).items()) == [('foo', {'lol': True}), ('hello', 42), ('ponies', 'are pretty!')]

    b = Munch(foo=['bar', Munch(lol=True)], hello=42, ponies=('are pretty!', Munch(lies='are trouble!')))
    assert sorted(unmunchify(b).items()) == [('foo', ['bar', {'lol': True}]), ('hello', 42), ('ponies', ('are pretty!', {'lies': 'are trouble!'}))]


def test_toJSON():
    b = Munch(foo=Munch(lol=True), hello=42, ponies='are pretty!')
    assert json.dumps(b) == b.toJSON()

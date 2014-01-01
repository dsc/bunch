chunk
=====

Chunk is a dictionary that supports attribute-style access, a la JavaScript.

>>> b = Chunk()
>>> b.hello = 'world'
>>> b.hello
'world'
>>> b['hello'] += "!"
>>> b.hello
'world!'
>>> b.foo = Chunk(lol=True)
>>> b.foo.lol
True
>>> b.foo is b['foo']
True


Dictionary Methods
------------------

A Chunk is a subclass of ``dict``; it supports all the methods a ``dict`` does:

>>> b.keys()
['foo', 'hello']

Including ``update()``:

>>> b.update({ 'ponies': 'are pretty!' }, hello=42)
>>> print repr(b)
Chunk(foo=Chunk(lol=True), hello=42, ponies='are pretty!')

As well as iteration:

>>> [ (k,b[k]) for k in b ]
[('ponies', 'are pretty!'), ('foo', Chunk(lol=True)), ('hello', 42)]

And "splats":

>>> "The {knights} who say {ni}!".format(**Chunk(knights='lolcats', ni='can haz'))
'The lolcats who say can haz!'


Serialization
-------------

Chunkes happily and transparently serialize to JSON and YAML.

>>> b = Chunk(foo=Chunk(lol=True), hello=42, ponies='are pretty!')
>>> import json
>>> json.dumps(b)
'{"ponies": "are pretty!", "foo": {"lol": true}, "hello": 42}'

If JSON support is present (``json`` or ``simplejson``), ``Chunk`` will have a ``toJSON()`` method which returns the object as a JSON string.

If you have PyYAML_ installed, Chunk attempts to register itself with the various YAML Representers so that Chunkes can be transparently dumped and loaded.

>>> b = Chunk(foo=Chunk(lol=True), hello=42, ponies='are pretty!')
>>> import yaml
>>> yaml.dump(b)
'!chunk.Chunk\nfoo: !chunk.Chunk {lol: true}\nhello: 42\nponies: are pretty!\n'
>>> yaml.safe_dump(b)
'foo: {lol: true}\nhello: 42\nponies: are pretty!\n'

In addition, Chunk instances will have a ``toYAML()`` method that returns the YAML string using ``yaml.safe_dump()``. This method also replaces ``__str__`` if present, as I find it far more readable. You can revert back to Python's default use of ``__repr__`` with a simple assignment: ``Chunk.__str__ = Chunk.__repr__``. The Chunk class will also have a static method ``Chunk.fromYAML()``, which loads a Chunk out of a YAML string.

Finally, Chunk converts easily and recursively to (``unchunkify()``, ``Chunk.toDict()``) and from (``chunkify()``, ``Chunk.fromDict()``) a normal ``dict``, making it easy to cleanly serialize them in other formats.


Miscellaneous
-------------

* It is safe to ``import *`` from this module. You'll get: ``Chunk``, ``chunkify``, and ``unchunkify``.

* Ample doctests::

    $ python -m chunk.test
    $ python -m chunk.test -v | tail -n22
    1 items had no tests:
        chunk.fromYAML
    16 items passed all tests:
       8 tests in chunk
      13 tests in chunk.Chunk
       7 tests in chunk.Chunk.__contains__
       4 tests in chunk.Chunk.__delattr__
       7 tests in chunk.Chunk.__getattr__
       3 tests in chunk.Chunk.__repr__
       5 tests in chunk.Chunk.__setattr__
       2 tests in chunk.Chunk.fromDict
       2 tests in chunk.Chunk.toDict
       5 tests in chunk.chunkify
       2 tests in chunk.from_yaml
       3 tests in chunk.toJSON
       6 tests in chunk.toYAML
       3 tests in chunk.to_yaml
       3 tests in chunk.to_yaml_safe
       4 tests in chunk.unchunkify
    77 tests in 17 items.
    77 passed and 0 failed.
    Test passed.


Feedback
--------

Open a ticket / fork the project on GitHub_, or send me an email at `dsc@less.ly`_.

.. _PyYAML: http://pyyaml.org/wiki/PyYAML
.. _GitHub: http://github.com/dsc/chunk
.. _dsc@less.ly: mailto:dsc@less.ly

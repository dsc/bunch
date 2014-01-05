chunk
==========

chunk is a fork of David Schoonover's **Bunch** package, providing similar functionality. 99% of the work was done by him, and the fork was made mainly for lack of responsiveness for fixes and maintenance on the original code.

Chunk is a dictionary that supports attribute-style access, a la JavaScript.

````py
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
````


Dictionary Methods
------------------

A Chunk is a subclass of ``dict``; it supports all the methods a ``dict`` does:

````py
>>> b.keys()
['foo', 'hello']
````

Including ``update()``:

````py
>>> b.update({ 'ponies': 'are pretty!' }, hello=42)
>>> print repr(b)
Chunk(foo=Chunk(lol=True), hello=42, ponies='are pretty!')
````

As well as iteration:

````py
>>> [ (k,b[k]) for k in b ]
[('ponies', 'are pretty!'), ('foo', Chunk(lol=True)), ('hello', 42)]
````

And "splats":

````py
>>> "The {knights} who say {ni}!".format(**Chunk(knights='lolcats', ni='can haz'))
'The lolcats who say can haz!'
````


Serialization
-------------

Chunkes happily and transparently serialize to JSON and YAML.

````py
>>> b = Chunk(foo=Chunk(lol=True), hello=42, ponies='are pretty!')
>>> import json
>>> json.dumps(b)
'{"ponies": "are pretty!", "foo": {"lol": true}, "hello": 42}'
````

If JSON support is present (``json`` or ``simplejson``), ``Chunk`` will have a ``toJSON()`` method which returns the object as a JSON string.

If you have [PyYAML](http://pyyaml.org/wiki/PyYAML) installed, Chunk attempts to register itself with the various YAML Representers so that Chunkes can be transparently dumped and loaded.

````py
>>> b = Chunk(foo=Chunk(lol=True), hello=42, ponies='are pretty!')
>>> import yaml
>>> yaml.dump(b)
'!chunk.Chunk\nfoo: !chunk.Chunk {lol: true}\nhello: 42\nponies: are pretty!\n'
>>> yaml.safe_dump(b)
'foo: {lol: true}\nhello: 42\nponies: are pretty!\n'
````

In addition, Chunk instances will have a ``toYAML()`` method that returns the YAML string using ``yaml.safe_dump()``. This method also replaces ``__str__`` if present, as I find it far more readable. You can revert back to Python's default use of ``__repr__`` with a simple assignment: ``Chunk.__str__ = Chunk.__repr__``. The Chunk class will also have a static method ``Chunk.fromYAML()``, which loads a Chunk out of a YAML string.

Finally, Chunk converts easily and recursively to (``unchunkify()``, ``Chunk.toDict()``) and from (``chunkify()``, ``Chunk.fromDict()``) a normal ``dict``, making it easy to cleanly serialize them in other formats.


Miscellaneous
-------------

* It is safe to ``import *`` from this module. You'll get: ``Chunk``, ``chunkify``, and ``unchunkify``.
* Ample Tests. Just run ``make test`` from the project root.

Feedback
--------

Open a ticket / fork the project on [GitHub](http://github.com/Infinidat/chunk).


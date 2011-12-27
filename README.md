bunch
=====

Bunch is a dictionary that supports attribute-style access, a la JavaScript.

````py
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
````


Dictionary Methods
------------------

A Bunch is a subclass of ``dict``; it supports all the methods a ``dict`` does:

````py
>>> b.keys()
['foo', 'hello']
````

Including ``update()``:

````py
>>> b.update({ 'ponies': 'are pretty!' }, hello=42)
>>> print repr(b)
Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
````

As well as iteration:

````py
>>> [ (k,b[k]) for k in b ]
[('ponies', 'are pretty!'), ('foo', Bunch(lol=True)), ('hello', 42)]
````

And "splats":

````py
>>> "The {knights} who say {ni}!".format(**Bunch(knights='lolcats', ni='can haz'))
'The lolcats who say can haz!'
````


Serialization
-------------

Bunches happily and transparently serialize to JSON and YAML.

````py
>>> b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
>>> import json
>>> json.dumps(b)
'{"ponies": "are pretty!", "foo": {"lol": true}, "hello": 42}'
````

If JSON support is present (``json`` or ``simplejson``), ``Bunch`` will have a ``toJSON()`` method which returns the object as a JSON string.

If you have [PyYAML](http://pyyaml.org/wiki/PyYAML) installed, Bunch attempts to register itself with the various YAML Representers so that Bunches can be transparently dumped and loaded.

````py
>>> b = Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')
>>> import yaml
>>> yaml.dump(b)
'!bunch.Bunch\nfoo: !bunch.Bunch {lol: true}\nhello: 42\nponies: are pretty!\n'
>>> yaml.safe_dump(b)
'foo: {lol: true}\nhello: 42\nponies: are pretty!\n'
````

In addition, Bunch instances will have a ``toYAML()`` method that returns the YAML string using ``yaml.safe_dump()``. This method also replaces ``__str__`` if present, as I find it far more readable. You can revert back to Python's default use of ``__repr__`` with a simple assignment: ``Bunch.__str__ = Bunch.__repr__``. The Bunch class will also have a static method ``Bunch.fromYAML()``, which loads a Bunch out of a YAML string.

Finally, Bunch converts easily and recursively to (``unbunchify()``, ``Bunch.toDict()``) and from (``bunchify()``, ``Bunch.fromDict()``) a normal ``dict``, making it easy to cleanly serialize them in other formats.


Miscellaneous
-------------

* It is safe to ``import *`` from this module. You'll get: ``Bunch``, ``bunchify``, and ``unbunchify``.
* Ample doctests
    
        $ python -m bunch.test
        $ python -m bunch.test -v | tail -n22
        1 items had no tests:
            bunch.fromYAML
        16 items passed all tests:
           8 tests in bunch
          13 tests in bunch.Bunch
           7 tests in bunch.Bunch.__contains__
           4 tests in bunch.Bunch.__delattr__
           7 tests in bunch.Bunch.__getattr__
           3 tests in bunch.Bunch.__repr__
           5 tests in bunch.Bunch.__setattr__
           2 tests in bunch.Bunch.fromDict
           2 tests in bunch.Bunch.toDict
           5 tests in bunch.bunchify
           2 tests in bunch.from_yaml
           3 tests in bunch.toJSON
           6 tests in bunch.toYAML
           3 tests in bunch.to_yaml
           3 tests in bunch.to_yaml_safe
           4 tests in bunch.unbunchify
        77 tests in 17 items.
        77 passed and 0 failed.
        Test passed.


Feedback
--------

Open a ticket / fork the project on [GitHub](http://github.com/dsc/bunch), or send me an email at [dsc@less.ly](mailto:dsc@less.ly).


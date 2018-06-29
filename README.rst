NeoBunch
========

|BuildLink|_ |CoverageLink|_ |LicenseLink|_

.. |BuildLink| image:: https://img.shields.io/travis/F483/neobunch/master.svg?label=Build-Master
.. _BuildLink: https://travis-ci.org/F483/neobunch

.. |CoverageLink| image:: https://img.shields.io/coveralls/F483/neobunch/master.svg?label=Coverage-Master
.. _CoverageLink: https://coveralls.io/r/F483/neobunch

.. |LicenseLink| image:: https://img.shields.io/badge/license-MIT-blue.svg
.. _LicenseLink: https://raw.githubusercontent.com/F483/neobunch/LICENSE.txt


Upgrading from bunch to neobunch
================================

This is a fork of the abandoned bunch_ package. It differs in name only and
remains otherwise compatible with the original package.

If you previously used bunch_, change the following names to upgrade:

 * Module: bunch -> neobunch
 * Class: bunch.Bunch -> neobunch.NeoBunch
 * Function: bunch.bunchify -> neobunch.neobunchify
 * Function: bunch.unbunchify -> neobunch.unneobunchify

The following legacy aliases exist to make upgrading easier:

 * Class: bunch.Bunch -> neobunch.Bunch
 * Function: bunch.bunchify -> neobunch.bunchify
 * Function: bunch.unbunchify -> neobunch.unbunchify

.. _bunch: https://github.com/dsc/bunch


Usage
=====

NeoBunch is a dictionary that supports attribute-style access, a la JavaScript.

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


Dictionary Methods
------------------

A NeoBunch is a subclass of ``dict``; it supports all the methods a ``dict`` does:

>>> b.keys()
['foo', 'hello']

Including ``update()``:

>>> b.update({ 'ponies': 'are pretty!' }, hello=42)
>>> print repr(b)
NeoBunch(foo=NeoBunch(lol=True), hello=42, ponies='are pretty!')

As well as iteration:

>>> [ (k,b[k]) for k in b ]
[('ponies', 'are pretty!'), ('foo', NeoBunch(lol=True)), ('hello', 42)]

And "splats":

>>> "The {knights} who say {ni}!".format(**NeoBunch(knights='lolcats', ni='can haz'))
'The lolcats who say can haz!'


Serialization
-------------

NeoBunches happily and transparently serialize to JSON and YAML.

>>> b = NeoBunch(foo=NeoBunch(lol=True), hello=42, ponies='are pretty!')
>>> import json
>>> json.dumps(b)
'{"ponies": "are pretty!", "foo": {"lol": true}, "hello": 42}'

If JSON support is present (``json`` or ``simplejson``), ``NeoBunch`` will have a ``toJSON()`` method which returns the object as a JSON string.

If you have PyYAML_ installed, NeoBunch attempts to register itself with the various YAML Representers so that NeoBunches can be transparently dumped and loaded.

>>> b = NeoBunch(foo=NeoBunch(lol=True), hello=42, ponies='are pretty!')
>>> import yaml
>>> yaml.dump(b)
'!neobunch.NeoBunch\nfoo: !neobunch.NeoBunch {lol: true}\nhello: 42\nponies: are pretty!\n'
>>> yaml.safe_dump(b)
'foo: {lol: true}\nhello: 42\nponies: are pretty!\n'

In addition, NeoBunch instances will have a ``toYAML()`` method that returns the YAML string using ``yaml.safe_dump()``. This method also replaces ``__str__`` if present, as I find it far more readable. You can revert back to Python's default use of ``__repr__`` with a simple assignment: ``NeoBunch.__str__ = NeoBunch.__repr__``. The NeoBunch class will also have a static method ``NeoBunch.fromYAML()``, which loads a NeoBunch out of a YAML string.

Finally, NeoBunch converts easily and recursively to (``unneobunchify()``, ``NeoBunch.toDict()``) and from (``neobunchify()``, ``NeoBunch.fromDict()``) a normal ``dict``, making it easy to cleanly serialize them in other formats.

.. _pyYAML: http://pyyaml.org/wiki/PyYAML

Miscellaneous
-------------

* It is safe to ``import *`` from this module. You'll get: ``NeoBunch``, ``neobunchify``, and ``unneobunchify``.

* Ample doctests::

    $ python -m neobunch.test
    $ python -m neobunch.test -v | tail -n22
    1 items had no tests:
        neobunch.fromYAML
    16 items passed all tests:
       8 tests in neobunch
      13 tests in neobunch.NeoBunch
       7 tests in neobunch.NeoBunch.__contains__
       4 tests in neobunch.NeoBunch.__delattr__
       7 tests in neobunch.NeoBunch.__getattr__
       3 tests in neobunch.NeoBunch.__repr__
       5 tests in neobunch.NeoBunch.__setattr__
       2 tests in neobunch.NeoBunch.fromDict
       2 tests in neobunch.NeoBunch.toDict
       5 tests in neobunch.neobunchify
       2 tests in neobunch.from_yaml
       3 tests in neobunch.toJSON
       6 tests in neobunch.toYAML
       3 tests in neobunch.to_yaml
       3 tests in neobunch.to_yaml_safe
       4 tests in neobunch.unneobunchify
    77 tests in 17 items.
    77 passed and 0 failed.
    Test passed.



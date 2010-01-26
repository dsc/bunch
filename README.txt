bunch
=====

Bunch is a dictionary that supports attribute-style access, a la JavaScript.

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


Dictionary Methods
------------------

A Bunch is a subclass of ``dict``; it supports all the methods a ``dict`` does:

>>> b.keys()
['foo', 'hello']

Including ``update()``:

>>> b.update({ 'ponies': 'are pretty!' }, hello=42)
>>> print repr(b)
Bunch(foo=Bunch(lol=True), hello=42, ponies='are pretty!')

As well as iteration:

>>> [ (k,b[k]) for k in b ]
[('ponies', 'are pretty!'), ('foo', Bunch(lol=True)), ('hello', 42)]

And "splats":

>>> "The {knights} who say {ni}!".format(**Bunch(knights='lolcats', ni='can haz'))
'The lolcats who say can haz!'


Miscellaneous
-------------

* Bunch converts easily to (``unbunchify``, ``Bunch.toDict``) and from (``bunchify``, ``Bunch.fromDict``) a normal ``dict``, making it easy to cleanly serialize them to JSON or YAML.

* It is safe to ``import *`` from this module. You'll get: ``Bunch``, ``bunchify``, and ``unbunchify``.

* Tests::

    $ python -m bunch.test -v


Feedback
--------

Open a ticket at http://github.com/dsc/bunch or send me an email at dsc@less.ly .

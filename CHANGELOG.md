Changelog
=========

Next Version
------------

2.5.0 (2019-10-30)
------------------

* Support ``fromJSON`` classmethod for all Munch subclasses (PR [#55](https://github.com/Infinidat/munch/pull/55))
* Fix return value of DefaultMunch and DefaultFactoryMunch's get method (fixes [#53](https://github.com/Infinidat/munch/issues/53))
* Support ``fromYAML`` classmethod for all Munch subclasses (PR [#52](https://github.com/Infinidat/munch/pull/52) fixes [#34](https://github.com/Infinidat/munch/issues/34)

2.4.0 (2019-10-29)
------------------

* Remove usage of deprecated API: Add default loader to yaml loads (PR [#51](https://github.com/Infinidat/munch/pull/51))
* Switch to PBR #49 (PR [#49](https://github.com/Infinidat/munch/pull/49))
* Add constructors to all PyYAML loaders (PR [#47](https://github.com/Infinidat/munch/pull/47))
* Fix namedtuple handling (PR [#46](https://github.com/Infinidat/munch/pull/46) - thanks @atleta)
* Correctly handle object cycles in munchify and unmunchify (PR [#41](https://github.com/Infinidat/munch/pull/41) - thanks @airbornemint)
* Improve subclassing behavior (PR [#38](https://github.com/Infinidat/munch/pull/38) - thanks @JosePVB)

2.3.2 (2018-05-06)
------------------

* Limit travis deployment conditions
* Build python wheels (PR [#32](https://github.com/Infinidat/munch/pull/32) - thanks @pabelanger)

2.3.1 (2018-04-11)
------------------

* Avoid running yaml tests when in no-deps environment
* Use flat dicts in ``__getstate__`` (closes [#32](https://github.com/Infinidat/munch/issues/30) - thanks @harlowja)

2.3.0 (2018-04-09)
------------------

* Remove default from constructor and fromDict, Make DefaultFactoryMunch which lets users provide a factory to generate missing values (PR [#28](https://github.com/Infinidat/munch/pull/28) - thanks @ekuecks)
* ``__setattr__`` will now ``munchify()`` any provided dict (PR [#27](https://github.com/Infinidat/munch/pulls/27) - thanks @kbni)
* Implement the pickling interface (PR [#23](https://github.com/Infinidat/munch/pulls/23) & [#25](https://github.com/Infinidat/munch/pulls/25) - thanks @JamshedVesuna)
* Drop support for Python 2.6, 3.3, 3.4
* Add ``__dict__`` property that calls ``toDict()`` (PR [#20](https://github.com/Infinidat/munch/pulls/20) - thanks @bobh66)

2.2.0 (2017-07-27)
------------------

* Fix for Python 2.6: str.format must field names
* Changed ``__repr__`` to use str.format instead of x % y
* Added DefaultMunch, which returns a special value for missing attributes (PR [#16](https://github.com/Infinidat/munch/pulls/16) - thanks @z0u)

2.1.1 (2017-03-20)
------------------

* Fix python 3 compatibility to work with IronPython (fixes [#13](https://github.com/Infinidat/munch/issues/13) - thanks @yiyuan1840)
* Deploy from Travis
* Add python 3.6

2.1.0 (2017-01-10)
------------------

* Implement copy method (fixes [#10](https://github.com/Infinidat/munch/issues/10))
* Fix ``__contains__`` returning True for Munch’s default attributes (PR [#7](https://github.com/Infinidat/munch/pull/7) - thanks @jmagnusson)

2.0.4 (2015-11-03)
------------------

* Fixed String representation of objects with keys that have spaces (PR [#4](https://github.com/Infinidat/munch/pull/4))

2.0.3 (2015-10-02)
------------------

* Python 3.5 support
* Test against Python 3.4
* Add support for running ``dir()`` on munches

2.0.2 (2014-01-16)
------------------

* Fix packaging manifest

2.0.1 (2014-01-16)
------------------

* Rename to Munch
* Fix Py3 compatibility check
* Drop Python 3.2 support, add 3.3

2.0.0 (2014-01-16)
------------------

* Initial release: Forking bunch --> infi.bunch.

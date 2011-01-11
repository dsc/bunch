#!/usr/bin/env python
# encoding: utf-8

'''
>>> class DictObject(DictObjectMixin, dict):
...    foo = 1
...    def lol(self): return 'lol'

>>> obj = DictObject()
>>> obj['foo']
1
>>> obj['lol']()
'lol'
>>> 'foo' in obj
True
>>> 'lol' in obj
True
>>> 'values' in obj
True
>>> hasattr(obj, 'values')
True
'''

__all__ = ('DictObjectMixin',)

class DictObjectMixin(object):
    def __getitem__(self, key):
        '''
        >>> obj = DictObject()
        >>> obj['values']()
        []
        '''    
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            return self.__getattribute__(key)

    def __contains__(self, key):
        '''
        >>> obj = DictObject()
        >>> 'values' in obj
        True
        >>> 'values2' in obj
        False
        '''
        return dict.__contains__(self, key) or hasattr(self, key)


class DictObject(DictObjectMixin, dict):
    pass        


if __name__ == "__main__":
    import doctest
    doctest.testmod()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def test():
    from infi import bunch
    import doctest
    returned = doctest.testmod(bunch)
    return returned.failed

if __name__ == '__main__':
    sys.exit(test())

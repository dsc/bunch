#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def test():
    import bunch
    import doctest
    returned = doctest.testmod(bunch)
    return returned.failed

if __name__ == '__main__':
    sys.exit(test())

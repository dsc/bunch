#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def test():
    import munch
    import doctest
    returned = doctest.testmod(munch)
    return returned.failed

if __name__ == '__main__':
    sys.exit(test())

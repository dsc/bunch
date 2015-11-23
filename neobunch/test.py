#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def test():
    import neobunch
    import doctest
    returned = doctest.testmod(neobunch)
    return returned.failed

if __name__ == '__main__':
    sys.exit(test())

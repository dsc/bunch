#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

def test():
    import chunk
    import doctest
    returned = doctest.testmod(chunk)
    return returned.failed

if __name__ == '__main__':
    sys.exit(test())

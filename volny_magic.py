#!/usr/bin/env python
import random
import sys
from types import LongType
from operator import mul

def tosn(x):
    """Allows long types to be printed in scientific notiation; convert using format %e otherwise."""
    if type(x) is LongType:
        return str(x)[0] + "." + str(x)[1:4] + "e" + str(len(str(x)) - 1)
    return "%e" % (x,)

def prod(x):
    """Return the product of a given list (like sum())"""
    return reduce(mul, x, 1)

def median(x):
    """Return the median of a given list."""
    s = sorted(x)
    l = len(s)
    if l & 1:
        return s[l / 2]
    return (s[l / 2] + s[l / 2 - 1]) / 2.0

def random_length(n):
    """Return a string of digits of n-length."""
    v = str(random.randint(1,9)) + ''.join(["{0}".format(random.randint(0,9)) for n in range(1,n)])
    l = long(v)
    if l < sys.maxint - 1:
        return int(l)
    return l

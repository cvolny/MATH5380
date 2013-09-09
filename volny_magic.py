#!/usr/bin/env python

from types import LongType
from operator import mul

def tosn(x):
    if type(x) is LongType:
        return str(x)[0] + "." + str(x)[1:4] + "e" + str(len(str(x)) - 1)
    return "%e" % (x,)

def prod(x):
    return reduce(mul, x, 1)



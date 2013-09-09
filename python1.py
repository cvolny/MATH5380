from math import factorial
from operator import mul
import sys
import unittest


# use this for large value testing in rfatorial(n) and rbinomial(n,k)
sys.setrecursionlimit(50000)


def prod(x):
    """Reduce elements of list using mul operator; like sum() for multiplication."""
    return reduce(mul, x, 1)


def digits(x, b, rev=False):
    """Returns list of digits in base-b from given base-10 number x."""
    v = []                          # results
    while x > 0:                    # loop so long as x is positve
        x,d = divmod(x,b)           # d <- x mod b, x <- x int-div b
        v.append(d)
    return v[::-1] if rev else v    # reverse if specified and return


def horner(v, b, rev=False):
    """Return integer in base-10 from list v of base-b number."""
    x = 0
    v = v[::-1] if rev else v[:]    # copy v, reverse if specified
    while len(v) > 0:
        d = v.pop()
        x = x*b + d
    return x


def ifactorial(n):
    """Iteratively take positive int n and return n factorial."""
    
    if n < 0: raise ValueError, "Negative factorials are undefined."
    
    n = int(n)                                      # force integer math here
    i = 0
    p = 1
    while i < n:
        i += 1
        p *= i
    return p


# boost performance with built-in caching; this would be interesting to compare memory with
#  https://github.com/cvolny/python-metaprog/blob/master/decorators.py
#@lru_cache(maxsize=50)                             # disable for now...
def rfactorial(n):
    """Recursively take positive int n and return n factorial."""
    if n < 0: raise ValueError, "Negative factorials are undefined."
    
    if n == 0: 
        return 1
    n = int(n)
    return n * rfactorial(n-1)

def binomial(n,k):
    """Calculate the binomial coefficient of n choose k.
        result = n! / (k! * (n-k)!),
        using math.factorial(x)."""
    
    if n*k < 0: raise ValueError, "n and k must be positive."
    if k > n:   raise ValueError, "k must not be greater than n."
    
    return factorial(n) / (factorial(k) * factorial(n-k))


def ibinomial(n,k):
    """Calculate the binomial coefficient of n choose k iterativly.
        result = (n)/(k) * (n-1)/(k-1) * (n-2)/(k-2) * ... * (n-k)"""
    
    if n*k < 0: raise ValueError, "n and k must be positive."
    if k > n:   raise ValueError, "k must not be greater than n."
    
    p = 1.0
    k = float(k)                                    # forces float division for n/k below
    while k > 0:
        p *= (n / k)
        n -= 1
        k -= 1
    return int(p) if p.is_integer() else p          # return as int if no precision loss

def rbinomial(n,k):
    """Calculate the binomial coefficient of n choose k recursively.
        result = (n)/(k) * rbinomial(n-1,k-1),
        result = 1 if k == 0"""
    
    if n*k < 0: raise ValueError, "n and k must be positive."
    if k > n:   raise ValueError, "k must not be greater than n."
    
    if k == 0:
        return 1
    k = float(k)
    p = (n/k) * rbinomial(n-1,k-1)
    return int(p) if p.is_integer() else p


class MyTests(unittest.TestCase):
    """Unit tests for this module."""
    
    def test_bases(self):
        """Test cases for digits and horner functions against some values."""
        for x,b in [(10,2), (1000,3), (100000,20)]:
            self.assertEqual(x, horner(digits(x,b),b))
            self.assertEqual(x, horner(digits(x,b,rev=True),b,rev=True))
    
    def test_factorial(self):
        """Test cases for factorial functions against prod([1,2,...,i,])."""
        for i in [0, 1, 10, 100, 1000]:
            x = prod(range(1,i+1))
            self.assertEqual(x, ifactorial(i))
            self.assertEqual(x, rfactorial(i))
    
    def test_binomial(self):
        """Test cases for binomial coefficient functions against precomputed values."""
        a = {(10,0): 1, (10,10): 1, (10,3): 120, (100,4): 3921225}
        for n,k in a.keys():
            v = a[(n,k)]
            self.assertEqual(v, binomial(n,k))
            self.assertEqual(v, ibinomial(n,k))
            self.assertEqual(v, rbinomial(n,k))


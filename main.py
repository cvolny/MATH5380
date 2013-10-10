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
    return n * rfactorial(n-1)

def binomial(n,k):
    """Calculate the binomial coefficient of n choose k.
        result = n! / (k! * (n-k)!),
        using math.factorial(x)."""
    
    if n < 0 or k < 0: raise ValueError, "n and k must be positive."
    if k > n:   raise ValueError, "k must not be greater than n."
    
    return factorial(n) / (factorial(k) * factorial(n-k))


def ibinomial(n,k):
    """Calculate the binomial coefficient of n choose k iterativly.
        result = (n)/(k) * (n-1)/(k-1) * (n-2)/(k-2) * ... * (n-k)"""
    
    if n < 0 or k < 0: raise ValueError, "n and k must be positive."
    if k > n:   raise ValueError, "k must not be greater than n."
    
    p = 1
    i = 1
    while i < k+1:
        p = (p * (n - (k - i))) / i
        i += 1
    return p

def rbinomial(n,k):
    """Calculate the binomial coefficient of n choose k recursively.
        result = (n)/(k) * rbinomial(n-1,k-1),
        result = 1 if k == 0"""
    
    if n < 0 or k < 0: raise ValueError, "n and k must be positive."
    if k > n:   raise ValueError, "k must not be greater than n."
    
    if k == 0:
        return 1
    return n * rbinomial(n-1,k-1) / k

def gcd(a, b, count=False):
    """Calculate the gcd of a and b using Euclid's method, iteratively."""
    c = 0
    while b > 0:
        a, b = b, a % b
        c += 1
    if True == count:
        return (a, c)
    return a

def count_gcd(a,b):
    """Returns just the count from gcd(*,*,True)"""
    a, c = gcd(a,b,count=True)
    return c

def regcd(a, b):
    """Returns s and t from Euclid's extended gcd; namely: s*a + t*b = gcd(a,b)"""
    if 0 == b:
        return (1, 0)
    else:
        (q, r) = divmod(a, b)
        (s, t) = rtegcd(b, r)
        return (t, s - q * t)

def egcd(a, b):
    """Returns s and t from Euclid's extended gcd; namely: s*a + t*b = gcd(a,b)"""
    s = 0;  ls = 1
    t = 1;  lt = 0
    while not 0 == b:
        (q, r) = divmod(a,b)
        (a, b) = (b, r)
        (s, ls) = (ls - q * s, s)
        (t, lt) = (lt - q * t, t)
    return (ls, lt)


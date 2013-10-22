from math import factorial
from operator import mul
import copy
import numbers
import sys


# use this for large value testing in rfatorial(n) and rbinomial(n,k)
sys.setrecursionlimit(50000)


def prod(x):
    """Reduce elements of list using mul operator; like sum() for multiplication."""
    return reduce(mul, x, 1)


def digits(x, b, rev=False):
    """Returns list of digits in base-b from given base-10 number x."""
    v = []                          # results
    while x > 0:                    # loop so long as x is positive
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
    
    if n < 0:
        raise ValueError("Negative factorials are undefined.")
    
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
    if n < 0:
        raise ValueError("Negative factorials are undefined.")
    
    if n == 0: 
        return 1
    return n * rfactorial(n-1)


def binomial(n,k):
    """Calculate the binomial coefficient of n choose k.
        result = n! / (k! * (n-k)!),
        using math.factorial(x)."""
    
    if n < 0 or k < 0:
        raise ValueError("n and k must be positive.")
    if k > n:
        raise ValueError("k must not be greater than n.")
    
    return factorial(n) / (factorial(k) * factorial(n-k))


def ibinomial(n,k):
    """Calculate the binomial coefficient of n choose k iterativly.
        result = (n)/(k) * (n-1)/(k-1) * (n-2)/(k-2) * ... * (n-k)"""
    
    if n < 0 or k < 0:
        raise ValueError("n and k must be positive.")
    if k > n:
        raise ValueError("k must not be greater than n.")
    
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
    
    if n < 0 or k < 0:
        raise ValueError("n and k must be positive.")
    if k > n:
        raise ValueError("k must not be greater than n.")
    
    if k == 0:
        return 1
    return n * rbinomial(n-1, k-1) / k


def rgcd(a, b):
    """Recursively calculate the gcd of a and b using Euclid's method."""
    if 0 == b:
        return a
    else:
        return gcd(b, a % b)


def gcd(a, b, count=False):
    """Calculate the gcd of a and b using Euclid's method, iteratively."""
    c = 0
    while b != 0:
        a, b = b, a % b
        c += 1
    a = abs(a)
    if count:
        return a, c
    return a


def count_gcd(a,b):
    """Returns just the count from gcd(*,*,True)"""
    a, c = gcd(a, b, count=True)
    return c


def rpowermod(b, n, m=0):
    """Returns a = b^n or a = b^n mod m if m is specified; uses Indian powermod algorithm (recursively)."""
    if n == 0:
        return 1
    else:
        n, r = divmod(n, 2)
        x = rpowermod(b, n, m)**2
        if r > 0:
            x *= b
        if m > 0:
            x %= m
        return x


def powermod(b, n, m=0):
    """Returns a = b^n or a = b^n mod m if m is specified; uses Indian powermod algorithm (iteratively)."""
    x = 1
    while n != 0:
        if n & 1:
            x *= b
            if m:
                x %= m
        n /= 2
        b *= b
        if m:
            b %= m
    return x


def regcd(a, b):
    """Returns s and t from Euclid's extended gcd; namely: s*a + t*b = gcd(a,b)"""
    if 0 == b:
        return 1, 0
    else:
        (q, r) = divmod(a, b)
        (s, t) = regcd(b, r)
        return t, s - q * t


def egcd(a, b):
    """Returns s and t from Euclid's extended gcd; namely: s*a + t*b = gcd(a,b)"""
    s, ls = 0, 1
    t, lt = 1, 0
    while not 0 == b:
        (q, r) = divmod(a,b)
        (a, b) = (b, r)
        (s, ls) = (ls - q * s, s)
        (t, lt) = (lt - q * t, t)
    return ls, lt


def lcm(a, b):
    """Returns the least common multiple of two numbers using gcd."""
    return a * b / gcd(a, b)


class Rational():
    """A type to represent Rational n/d numbers using to integers."""

    @staticmethod
    def common_terms(a, b):
        """Return two Rationals, a and b, in common terms using lcm."""
        a = a.copy()
        b = b.copy()
        m = lcm(a.d, b.d)
        a.by(m)
        b.by(m)
        return a, b

    def __init__(self, n, d=None, simplify=True):
        """Initialize Rational with a given numerator and denominator."""
        if None == d:
            if isinstance(n, Rational):
                self.n = n.n
                self.d = n.d
            elif isinstance(n, numbers.Integral):
                self.n = n
                self.d = 1
            elif hasattr(n, 'as_integer_ratio'):
                self.n, self.d = n.as_integer_ratio()
            else:
                raise ValueError("Cannot construct rational from given type {}.".format(type(n)))
        elif 0 == d:
            raise ZeroDivisionError("Denominator must be non-zero.")
        else:
            self.n = n
            self.d = d
        if simplify:
            self.simplify()

    def copy(self):
        """Copy factory method."""
        return copy.deepcopy(self)

    def simplify(self):
        """Simplify n and d to lowest terms."""
        g = gcd(self.n, self.d)
        self.n /= g
        self.d /= g
        return self

    def by(self, m):
        """Scale to denominator in terms of m."""
        q, r = divmod(m, self.d)
        if r == 0:
            self.n *= q
            self.d *= q
        else:
            raise ValueError("Provided multiple {} is not divisible by current denominator {}.".format(m, self.d))
        return self

    def __cmp__(self, other):
        """Compare two Rationals using arithmatic of numerators when both are in common terms (lcm)."""
        other = Rational(other)
        a, b = Rational.common_terms(self, other)
        return a.n - b.n

    def __neg__(self):
        """Support negation of a Rational."""
        return Rational(self.n * -1, self.d)

    def __invert__(self):
        """Support inversion (reciprical) of a Rational."""
        return Rational(self.d, self.n)

    def __add__(self, other):
        """Support addition between Rationals."""
        other = Rational(other)
        a, b = Rational.common_terms(self, other)
        c = Rational(a.n + b.n, a.d)
        return c

    def __sub__(self, other):
        """Support subtractions between Rationals by using __neg__ and __add__."""
        other = Rational(other)
        return self + (-other)

    def __mul__(self, other):
        """Support multiplication of Rationals."""
        other = Rational(other)
        return Rational(self.n * other.n, self.d * other.d)

    def __div__(self, other):
        """Support division of Rationals by using __invert__ and __mul__."""
        other = Rational(other)
        return self * (~other)

    def __str__(self):
        """Returns a string representation of the instance."""
        return "%s/%s" % (self.n, self.d,)

    def __repr__(self):
        """Returns a console friendly string representation of the instance, using __str__."""
        return str(self)

    def __long__(self):
        """Support to simplification to long value."""
        sp = Rational(self)
        sp.simplify()
        if sp.d == 1:
            return sp.n
        else:
            raise ValueError("Cannot simplify {} to integral value with non-one denominator.".format(self))

    def __int__(self):
        """Lazily support simplification to integer value via __long__."""
        return int(long(self))

    def __float__(self):
        """Evaluate the Rational into a float type."""
        return self.n / float(self.d)

    def as_integer_ratio(self):
        """Return numerator and denominator as tuple (type duck (big)float)."""
        return self.n, self.d
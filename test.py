from discrete import *
import random
import unittest


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
    
    def test_gcd(self):
        """Test cases for gcd function. Zero case and some static values."""
        self.assertEqual(12341234, gcd(12341234,0))
        self.assertEqual(100*10*55, gcd(100*10*55, 200*10*55))

    def test_lcm(self):
        self.assertEqual(0, lcm(5000, 0))
        for i in range(15):
            a, b = random.randint(i, 500), random.randint(i, 500)
            self.assertEqual(a * b / gcd(a, b), lcm(a, b))

    def test_rational(self):
        self.assertEqual(5, Rational(5, 2) * 2)
        self.assertEqual(Rational(5, 2), Rational(1, 2) * 5)
        self.assertEqual(Rational(10, 5), Rational(2) * Rational(3) / Rational(3))
        self.assertEqual(Rational(97, 10), Rational(13, 2) + Rational(16, 5))
        self.assertEqual(5, int(Rational(0) + Rational(10, 2)))
        for i in range(15):
            r = random.uniform(i, 500)
            self.assertEqual(r, float(Rational(r) + Rational(1, 1) - Rational(2, 2)))

    def test_powerset(self):
        foo = [[], [1], [5], [1, 5], [7], [1, 7], [5, 7], [1, 5, 7]]
        self.assertEqual(foo, [list(s) for s in powerset([1, 5, 7])])
        self.assertEqual([[]], [list(s) for s in powerset([])])


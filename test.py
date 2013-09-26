from main import *
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


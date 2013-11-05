from discrete import *
from volny_magic import random_length_pair, random_length
import random
import unittest


class MyTests(unittest.TestCase):
    """Unit tests for this project."""
    
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
        """Test case for lcm function. Zero case and random values."""
        self.assertEqual(0, lcm(5000, 0))
        for i in range(15):
            a, b = random.randint(i, 500), random.randint(i, 500)
            self.assertEqual(a * b / gcd(a, b), lcm(a, b))

    def test_rational(self):
        """Test case for Rational class. Static tests and random test."""
        self.assertEqual(5, Rational(5, 2) * 2)
        self.assertEqual(Rational(5, 2), Rational(1, 2) * 5)
        self.assertEqual(Rational(10, 5), Rational(2) * Rational(3) / Rational(3))
        self.assertEqual(Rational(97, 10), Rational(13, 2) + Rational(16, 5))
        self.assertEqual(5, int(Rational(0) + Rational(10, 2)))
        for i in range(15):
            r = random.uniform(i, 500)
            self.assertEqual(r, float(Rational(r) + Rational(1, 1) - Rational(2, 2)))

    def test_powerset(self):
        """Test case for powerset generator. Static and zero test."""
        foo = [[], [1], [5], [1, 5], [7], [1, 7], [5, 7], [1, 5, 7]]
        self.assertEqual(foo, [list(s) for s in powerset([1, 5, 7])])
        self.assertEqual([[]], [list(s) for s in powerset([])])

    def test_powermod(self):
        """Test case for iterative vs. powermod results."""
        for i in range(15):
            a, b = random_length_pair(3)
            self.assertEqual(powermod(a, b), rpowermod(a, b))
        for i in range(15):
            a, b = random_length_pair(10)
            for j in range(2, 15):
                self.assertEqual(powermod(a, b, j), rpowermod(a, b, j))

    def test_egcd(self):
        """Test case for random pairs against extended gcd function."""
        for i in range(15):
            a, b = random_length_pair(10)
            s, t = regcd(a, b)
            self.assertEqual(gcd(a, b), s*a+t*b)
            sp, tp = egcd(a, b)
            self.assertEqual((sp, tp), (s, t))

    def test_rsa(self):
        """Test case for classroom RSA functions. Generates 3 pairs and runs 5 tests each."""
        for x in range(3):
            d = generate_rsa()
            nlen = len(str(d['n']))
            for m in [random_length(nlen-1) for y in range(5)]:
                c = rsa_encrypt(m, d['a'], d['n'])
                mp = rsa_decrypt(c, d['b'], d['n'])
                self.assertEqual(m, mp)

    def test_prime(self):
        """Test if prime_generator actually generates prime numbers."""
        for i in range(15):
            j = 2*i
            print "%d:\t" % (j,),
            n = prime_generator(j, k=100)
            print n
            self.assertTrue(fprimality(n, k=1000))


if "__main__" == __name__:
    unittest.main()
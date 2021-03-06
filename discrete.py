# -*- coding: utf-8 -*-
from math import factorial
from operator import mul
import bisect
import copy
import math
import numbers
import string
import sys
import random
import unittest


# use this for large value testing in rfatorial(n) and rbinomial(n,k)
sys.setrecursionlimit(50000)

# simple alphabet for string encoding/decoding in base-100
alphabet = string.digits + string.ascii_letters + string.punctuation + string.whitespace


def prod(x):
    """Reduce elements of list using mul operator; like sum() for multiplication."""
    return reduce(mul, x, 1)


def random_length(n):
    """Return a string of digits of n-length."""
    v = str(random.randint(1, 9)) + ''.join(["{0}".format(random.randint(0, 9)) for n in range(1, n)])
    l = long(v)
    if l < sys.maxint - 1:
        return int(l)
    return l


def random_length_pair(n):
    """Returns a pair of numbers of length-n"""
    return random_length(n), random_length(n)


def digits(x, b, rev=False):
    """Returns list of digits in base-b from given base-10 number x."""
    v = []                          # results
    while x > 0:                    # loop so long as x is positive
        x, d = divmod(x, b)           # d <- x mod b, x <- x int-div b
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


def binomial(n, k):
    """Calculate the binomial coefficient of n choose k.
        result = n! / (k! * (n-k)!),
        using math.factorial(x)."""
    
    if n < 0 or k < 0:
        raise ValueError("n and k must be positive.")
    if k > n:
        raise ValueError("k must not be greater than n.")
    
    return factorial(n) / (factorial(k) * factorial(n-k))


def ibinomial(n, k):
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


def rbinomial(n, k):
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


def count_gcd(a, b):
    """Returns just the count from gcd(*,*,True)"""
    a, c = gcd(a, b, count=True)
    return c


def rpowermod(b, n, m=None):
    """Returns a = b^n or a = b^n mod m if m is specified; uses Indian powermod algorithm (recursively)."""
    if n == 0:
        return 1
    else:
        n, r = divmod(n, 2)
        x = rpowermod(b, n, m)**2
        if r > 0:
            x *= b
        if m:
            x %= m
        return x


def powermod(b, n, m=None):
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


def powerset(v):
    """generator for powerset of vector v (must be subscriptable like list/tuple). """
    l = len(v)
    m = 2**l
    i = 0
    while i < m:
        d = digits(i, 2)
        dl = len(d)
        j = 0
        r = set()
        while j < dl:
            if d[j]:
                r.add(v[j])
            j += 1
        i += 1
        yield r


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


class Vector(list):
    """Class to represent vectors of arbitrary dimension."""

    @staticmethod
    def versor(i, d):
        """static method to generate the versor in dimension-i in a d-dimension system."""
        r = [0] * d
        r[i - 1] = 1
        return Vector(r)

    def dim(self):
        """returns the dimensions with which this vector exists."""
        return len(self)

    def norm(self):
        """returns the norm or "length" of the vector."""
        return math.sqrt(sum([x ** 2 for x in self]))

    def unit(self):
        """returns the unit vector of the instance. u* = v / ||v||"""
        n = self.norm()
        return Vector([x / n for x in self])

    def __add__(self, other):
        """addition operator for vectors of same dimension."""
        # TODO: detect longer vector and extend shorter to fit, then perform addition.
        if self.dim() == other.dim():
            return Vector([self[i] + other[i] for i in range(self.dim())])
        raise ValueError("Dimension mismatch! {} != {}".format(self.dim(), other.dim()))

    def __sub__(self, other):
        """"subtraction operator relying on negation of elements and addition operator."""
        return self + [x * -1 for x in other]

    def __mul__(self, other):
        """"multiplication operator for multiplying the unit vector's components by a scalar value."""
        n = self.norm() * other
        return Vector([self.unit()[i] * n for i in range(self.dim())])

    def __div__(self, other):
        """"division operator for dividing the unit vector's components by a scalar value."""
        n = self.norm() * other
        return Vector([self.unit()[i] / n for i in range(self.dim())])

    def distance_to(self, other):
        """calculate the distance between two point vectors."""
        if self.dim() == other.dim():
            return math.sqrt(sum([(self[x] - other[x]) ** 2 for x in range(self.dim())]))
        raise ValueError("Dimension mismatch! {} != {}".format(self.dim(), other.dim()))

    def __str__(self):
        """return a string representation of the vector."""
        return "<{}>".format(",".join([str(x) for x in self]))

    def __repr__(self):
        """return a console compabitible string representation, relying on str."""
        return str(self)


def generate_rsa(plen=100, qlen=200):
    """Generate RSA public and private key information."""
    p = prime_generator(plen, k=100)
    q = prime_generator(qlen, k=100)
    n = p * q
    phi = (p - 1) * (q - 1)
    while 1:
        a = random.randint(1, n - 1)
        if gcd(phi, a) == 1:
            break
    b, c = egcd(a, phi)
    if b < 0:
        b %= phi
    return {'a': a, 'b': b, 'p': p, 'q': q, 'n': n, 'phi': phi, }


def string_encode(m):
    """Encode the string m to numeric value. This will need to be chunked to digits(,n) for RSA-crypto."""
    global alphabet    
    r = []
    for c in list(m):
        r.append(str(alphabet.index(c)).zfill(2))
    return long("".join(r))


def string_decode(c):
    """Decode the string represented by numeric value c."""
    global alphabet
    return "".join([alphabet[k] for k in digits(c, 100, rev=True)])


def prime_generator(x, k=5):
    """Generate a prime number of length x relying on k passes of Fermat's Little Theorem test."""
    n = random_length(x)
    if not n & 1:
        n += 1
    while not fprimality(n, k):
        n += 2
    return n


def dprimality(n):
    """Deterministric primality test from http://stackoverflow.com/a/15285588"""
    if n < 2:
        return False
    if n in (2, 3, 5, 7, 11, 13):
        return True
    for i in xrange(3, long(n**0.5)+1, 2):
        if n % i == 0:
            print n, i
            return False
    return True


def fprimality(p, k):
    """Use Fermat's Little Theorem to test primality for random cases k."""
    #print n, k
    if p < 2:
        return False
    for n in (2, 3, 5, 7, 11, 13):
        if not p % n:
            return False
    while k > 0:
        a = random.randrange(2, p)
        if powermod(a, p-1, p) != 1:
            return False
        k -= 1
    return True


def rsa_crypt(msg, a, n, encode):
    """RSA Encrypt msg using public key (a, n). Encode msg using encoding (callable)."""
    emsg = encode(msg)
    mblocks = digits(emsg, n)
    cblocks = []
    for mblock in mblocks:
        cblocks.append(powermod(mblock, *(a, n)))
    return horner(cblocks, n)


def rsa_decrypt(cipher, b, n, decode):
    """RSA Decrpyt cipher using private key (b, n). Decode that msg using decoding (callable)."""
    cblocks = digits(cipher, n,)
    mblocks = []
    for cblock in cblocks:
        mblocks.append(powermod(cblock, *(b, n)))
    emsg = horner(mblocks, n)
    return decode(emsg)


class Graph(dict):
    """Class to represent undirected graphs as a dictionary."""

    def add_node(self, k):
        """Add node with no edges to the graph. Throws KeyError if node already exists."""
        if k in self:
            raise KeyError("Node %s already defined." % k)
        self[k] = {}

    def del_node(self, k):
        """Delete node and all edges associated from graph."""
        if not k in self:
            raise KeyError("Node %s not defined." %k)
        for neighbor in self[k].keys():
            del self[neighbor][k]
        del self[k]

    def nodes(self):
        """Return a list of nodes."""
        return self.keys()

    def neighbors(self, k):
        """Return a list of neighbors to node k."""
        return self[k].keys()

    def degree(self, k):
        """Return the degree of the node k."""
        return sum(self[k].values())

    def extended_degree(self, k):
        """Return the degree of the node k, counting loops as a degree of 2."""
        s = 0
        for n in self.neighbors(k):
            if k == n:
                s += 2 * self[k][n]
            else:
                s += self[k][n]
        return s

    def add_edge(self, k1, k2, c=1):
        """Add an edge (or c edges) between nodes k1 and k2."""
        c += 0 if not k2 in self[k1] else self[k1][k2]
        self[k1][k2] = c
        self[k2][k1] = c

    def del_edge(self, k1, k2, c=1):
        """Delete an edge (or c edges) between nodes k1 and k2."""
        if c > self[k1][k2]:
            raise ValueError("Cannot remove %d edges between %s and %s; only %d exist." % (c, k1, k2, self[k1][k2]))
        if self[k1][k2] - c:
            self[k1][k2] -= c
            if not k1 == k2:
                self[k2][k1] -= c
        else:
            del self[k1][k2]
            if not k1 == k2:
                del self[k2][k1]

    def are_neighbors(self, k1, k2):
        """Determine whether nodes k1 and k2 are connected."""
        return k1 in self[k2]

    def del_loops(self):
        """Eliminate loops from the graph."""
        for k in self.nodes():
            if k in self[k].keys():
                self.del_edge(k, k, self[k][k])

    def simplify(self):
        for node in self.nodes():
            for neighbor, count in self[node].item():
                if node == neighbor:
                    self.del_edge(node, node, count)
                else:
                    self[node][neighbor] = 1

    def treeify(self):
        """ Perform in-place conversion to a spanning tree."""
        self.simplify()
        trees = []
        for node in self.nodes():
            t = None
            for tree in trees:
                if node in tree:
                    t = tree
                    break
            else:
                t = []
            for neighbor in self.neighbors(node):
                if neighbor in t:
                    del self[node][neighbor]
                    del self[neighbor][node]
                for tree in trees:
                    if neighbor in tree:
                        t += tree
                        trees.remove(tree)


def graph_epath_exists(g):
    """Determine if an Eulerian path exists in graph g. Returns odd degree nodes as a list."""
    odds = []
    for v in g.nodes():
        if 1 & g.extended_degree(v):
            odds.append(v)
    c = len(odds)
    if not c in (0, 2):
        raise ValueError("No Eulerian path exists in graph. %d nodes have odd degrees." % c)
    return odds


def graph_epath(g):
    """Find an Eulerian path, with loops, in graph g if one exists."""
    gp = copy.deepcopy(g)
    odds = graph_epath_exists(gp)
    r = gp.nodes()
    if odds:
        c, f = odds
    else:
        c, f = r[0], r[-1]
    p = [c]
    while not c == f:
        ns = gp.neighbors(c)
        n = f if f in ns else ns[0]
        gp.del_edge(c, n)
        p.append(n)
        c = n
    while r:
        if not c:
            c = [x for x in r if x in p][0]
        if gp.degree(c) == 0:
            r.remove(c)
            c = None
        else:
            if gp.are_neighbors(c, c):
                p = p[:p.index(c)] + ([c] * g[c][c]) + p[p.index(c):]
                gp.del_edge(c, c, g[c][c])
            n = gp.neighbors(c)[0]
            gp.del_edge(c, n)
            p.insert(p.index(c), n)
            c = n
    return p


class Tree(dict):
    """Dictionary represenation of a tree with sequential integers for keys and a child list as values."""

    def __init__(self):
        """Initialize with a single root element with label 0."""
        self[0] = []
        self.next_label = 1

    def add_leaf(self, parent):
        """Add a leaf under the specified parent node."""
        label = self.next_label
        if not parent in self.keys():
            raise ValueError("Parent '%s' does not exist." % parent)
        self[parent].append(label)
        self[label] = []
        self.next_label += 1
        return label

    def leaves(self):
        """Return a list of nodes with no children (leaves)."""
        r = []
        for node, children in self.items():
            if not children:
                r.append(node)
        return r

    def children(self, node):
        """Returns the list of children of the specified node."""
        return self[node]

    def parent(self, node):
        """Resolve the parent of the specified node."""
        if not node in self.keys():
            raise ValueError("Node '%s' does not exist." % node)
        for n, c in self.items():
            if node in c:
                return n

    def prune(self, leaf):
        """Prune a leaf from the tree."""
        if self[leaf]:
            raise ValueError("Node '%s' has children '[%s]' (not a leaf)." % (leaf, ",".join(self[leaf])))
        self[self.parent(leaf)].remove(leaf)
        del self[leaf]


def prufer(t):
    """Generate Prüfer code for a labeled Tree t."""
    t = copy.deepcopy(t)
    seq = []
    while 1:
        leaves = t.leaves()
        leaf = min(leaves)
        if leaf == 0:
            break
        parent = t.parent(leaf)
        seq.append(parent)
        t.prune(leaf)
    return seq[:-1]


def prufer_parse(seq):
    """ Parse Prüfer code and generate a labeled Tree. """
    top = []
    seq.append(0)
    n = len(seq) + 1
    leaves = range(n)
    for i in range(n):
        for j in leaves:
            if not j in seq[i:]:
                top.append(j)
                leaves.remove(j)
    top.pop()
    t = Tree()
    for i in range(1, n):
        t.add_leaf(0)
    t[0] = []
    for i in range(n - 1)[::-1]:
        bisect.insort(t[seq[i]], top[i])
    return t


def planar(t):
    """ Generate planar code for a Tree t. """
    r = []
    v = [0]
    s = [0]
    c = 0
    while s:
        todo = [x for x in t.children(c) if not x in v]
        if todo:
            r.append(1)
            s.append(c)
            c = min(todo)
            v.append(c)
        else:
            r.append(0)
            c = s.pop()
    return r[:-1]


def planar_parse(seq):
    """ Parse planar code to generate an arbitrarily labeled tree (arbitrary in that label info is lost in planar encoding)"""
    t = Tree()
    p = [0]
    for s in seq:
        s = str(s)
        if s == "1":
            p.append(t.add_leaf(p[-1]))
        elif s == "0":
            p.pop()
        else:
            raise ValueError("Invalid planar code character '%s', not a 1 or 0." % s)
    return t


# provided by instructor
class graph(dict):

    def add_node(self, x):
        if x in self:
            raise Exception("node named %s already exists" % x)
        else:
            self[x] = {}

    def del_node(self, x):
        for y in self.neighbors(x):
            del self[y][x]
        del self[x]

    def nodes(self):
        return self.keys()

    def neighbors(self, x):
        return [y for y in self[x] if y != x]

    def degree(self, x):
        d = sum(self[x].values())
        if x in self[x]:
            d += self[x][x]
        return d

    def add_edge(self, x, y):
        try:
            self[x][y] += 1
            if y != x:
                self[y][x] += 1
        except KeyError:
            self[x][y] = self[y][x] = 1

    def del_edge(self, x, y):
        if y not in self[x]:
            raise Exception("nodes %s and %s are not neighbors" %
                            (x, y))
        elif self[x][y] == 1:
            del self[x][y]
            if y != x:
                del self[y][x]
        else:
            self[x][y] -= 1
            if y != x:
                self[y][x] -= 1

    def are_neighbors(self, x, y):
        return y in self[x] and y != x


def eulerian_path(g):
    h = graph()
    h.update(g)
    v = h.nodes()
    t = [x for x in v if h.degree(x) % 2 == 1]
    if len(t) > 2:
        raise Exception("no eulerian path exists",
                        [(x, h.degree(x)) for x in t])
    elif len(t) == 2:
        w = [t[0]]
    else:
        w = [v[0]]
    i = 0
    while i < len(w):
        x = w[i]
        if h[x]:
            i += 1
        else:
            C = [x]
            while h[x]:
                if x in h[x]:
                    y = x
                else:
                    y = h.neighbors(x)[0]
                C.append(y)
                h.del_edge(x, y)
                x = y
            w[i:i + 1] = C
    return w


def dfs(g, r):
    t = graph()
    t.add_node(r)
    v = [r]
    while v:
        x = v[-1]
        U = [y for y in g[x] if y not in t]
        if U:
            y = U[0]
            t.add_node(y)
            t.add_edge(x, y)
            v.append(y)
        else:
            v.pop()
    return t


class MyTests(unittest.TestCase):
    """Unit tests for this project."""

    def test_bases(self):
        """Test cases for digits and horner functions against some values."""
        for x, b in [(10, 2), (1000, 3), (100000, 20)]:
            self.assertEqual(x, horner(digits(x, b), b))
            self.assertEqual(x, horner(digits(x, b, rev=True), b, rev=True))

    def test_factorial(self):
        """Test cases for factorial functions against prod([1,2,...,i,])."""
        for i in [0, 1, 10, 100, 1000]:
            x = prod(range(1, i + 1))
            self.assertEqual(x, ifactorial(i))
            self.assertEqual(x, rfactorial(i))

    def test_binomial(self):
        """Test cases for binomial coefficient functions against precomputed values."""
        a = {(10, 0): 1, (10, 10): 1, (10, 3): 120, (100, 4): 3921225}
        for n, k in a.keys():
            v = a[(n, k)]
            self.assertEqual(v, binomial(n, k))
            self.assertEqual(v, ibinomial(n, k))
            self.assertEqual(v, rbinomial(n, k))

    def test_gcd(self):
        """Test cases for gcd function. Zero case and some static values."""
        self.assertEqual(12341234, gcd(12341234, 0))
        self.assertEqual(100 * 10 * 55, gcd(100 * 10 * 55, 200 * 10 * 55))

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
            self.assertEqual(gcd(a, b), s * a + t * b)
            sp, tp = egcd(a, b)
            self.assertEqual((sp, tp), (s, t))

    def test_rsa(self):
        """Test case for classroom RSA functions. Generates 3 pairs and runs 5 tests each."""
        for x in range(1):
            d = generate_rsa()
            nlen = len(str(d['n']))
            for m in [random_length(nlen - 1) for y in range(5)]:
                c = powermod(m, d['a'], d['n'])
                mp = powermod(c, d['b'], d['n'])
                self.assertEqual(m, mp)

    def test_prime(self):
        """Test if prime_generator actually generates prime numbers."""
        for i in range(15):
            j = 2 * i
            n = prime_generator(j, k=100)
            self.assertTrue(fprimality(n, k=1000))

    def test_graph(self):
        gp = {
            1: {2: 1, 5: 1},
            2: {1: 1, 3: 1, 4: 1, 6: 1},
            3: {2: 1, 7: 2},
            4: {2: 1},
            5: {1: 1, 5: 1, 6: 1},
            6: {2: 1, 5: 1},
            7: {3: 2},
            8: {}}
        g = Graph()
        for k in gp.keys():
            g.add_node(k)
        for k, v in gp.iteritems():
            for kp, w in v.iteritems():
                if not g.are_neighbors(k, kp):  # double count otherwise...
                    g.add_edge(k, kp, w)
        self.assertEqual(g, gp)

    def test_path(self):
        g = Graph()
        g.update({
            1: {2: 1, 5: 1},
            2: {1: 1, 3: 1, 4: 1, 6: 1},
            3: {2: 1, 7: 2},
            4: {2: 1},
            5: {1: 1, 5: 5, 6: 1},
            6: {2: 1, 5: 1},
            7: {3: 2}})
        self.assertEqual(graph_epath(g), [3, 7, 3, 2, 6, 5, 5, 5, 5, 5, 5, 1, 2, 4])
        g.del_edge(5, 5, 5)
        self.assertEqual(graph_epath(g), [3, 7, 3, 2, 6, 5, 1, 2, 4])
        g.add_node(8)
        g.add_edge(1, 8)
        self.assertRaises(ValueError, graph_epath, g)

    def test_tree(self):
        t = Tree()
        n = 5
        for i in range(n):
            t.add_leaf(i)
        self.assertEqual(t, dict({x: [x + 1] for x in range(n)}.items() + {n: []}.items()))
        t = Tree()     # 0
        t.add_leaf(0)  # 1
        t.add_leaf(0)  # 2
        t.add_leaf(0)  # 3
        t.add_leaf(2)  # 4
        t.add_leaf(2)  # 5
        t.add_leaf(4)  # 6
        self.assertEqual(t, {0: [1, 2, 3], 2: [4, 5], 1: [], 3: [], 4: [6], 5: [], 6: []})

    def test_prufer(self):
        t = Tree()
        n = 5
        for i in range(n):
            t.add_leaf(i)
        self.assertEqual(prufer(t), range(n - 1, 0, -1))
        self.assertEqual(prufer_parse(range(n - 1, 0, -1)), t)
        p = [0, 0, 2, 4, 2]
        t = Tree()     # 0
        t.add_leaf(0)  # 1
        t.add_leaf(0)  # 2
        t.add_leaf(0)  # 3
        t.add_leaf(2)  # 4
        t.add_leaf(2)  # 5
        t.add_leaf(4)  # 6
        self.assertEqual(prufer(t), p)
        self.assertEqual(prufer_parse(p), t)

    def test_planar(self):
        t = Tree()
        n = 5
        for i in range(n):
            t.add_leaf(i)
        self.assertEqual(planar(t), [1] * n + [0] * n)
        self.assertEqual(planar_parse([1] * n + [0] * n), t)
        t = Tree()     # 0
        t.add_leaf(0)  # 1
        t.add_leaf(1)  # 2
        t.add_leaf(2)  # 3
        t.add_leaf(2)  # 4
        t.add_leaf(0)  # 5
        t.add_leaf(5)  # 6
        self.assertEqual("".join([str(x) for x in planar(t)]), "111010001100")
        self.assertEqual(planar_parse("111010001100"), t)


if "__main__" == __name__:
    unittest.main()
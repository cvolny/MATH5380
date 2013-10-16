from math import sqrt


class Vector(list):
    """Class to represent vectors of arbitrary dimension."""

    @staticmethod
    def versor(i, d):
        """static method to generate the versor in dimension-i in a d-dimension system."""
        r = [0] * d
        r[i-1] = 1
        return Vector(r)

    def dim(self):
        """returns the dimensions with which this vector exists."""
        return len(self)

    def norm(self):
        """returns the norm or "length" of the vector."""
        return sqrt(sum([x**2 for x in self]))

    def unit(self):
        """returns the unit vector of the instance. u* = v / ||v||"""
        n = self.norm()
        return Vector([x / n for x in self])

    def __add__(self, other):
        """addition operator for vectors of same dimension."""
        # TODO: detect longer vector and extend shorter to fit, then perform additon.
        if self.dim() == other.dim():
            return Vector([self[i] + other[i] for i in range(self.dim())])
        raise ValueError("Dimension mismatch! {} != {}".format(self.dim(), other.dim()))

    def __sub__(self, other):
        """"subtraction operator relying on negation of elements and addition operator."""
        return self + [x*-1 for x in other]

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
            return sqrt(sum([(self[x] - other[x])**2 for x in range(self.dim())]))
        raise ValueError("Dimension mismatch! {} != {}".format(self.dim(), other.dim()))

    def __str__(self):
        """return a string representation of the vector."""
        return "<{}>".format(",".join([str(x) for x in self]))

    def __repr__(self):
        """return a console compabitible string representation, relying on str."""
        return str(self)
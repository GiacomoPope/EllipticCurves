from gmpy2 import mpz, to_binary

class EllipticCurvePoint:
    def __init__(self, E, x, y, z, check=True):
      self.curve = E
      self.x = x
      self.y = y
      self.z = z

      # Removing this check saves time  
      if check:
        if not self.curve.is_on_curve(self):
          raise ValueError(f"Coordinates [{self.x}, {self.y}, {self.z}] do not define a point on {self.curve}")

    def is_inf(self):
      return self.z == 0

    def normalise_coordinates(self):
      if self.z == 1 or self.z == 0:
        return self
      try:
        z_inverse = pow(self.z, -1, self.curve.q)
      except:
        print(f"Point cannot be scaled as gcd({self.z},{self.curve.q}) != 1")
        return 0
      self.x = (self.x * z_inverse) % self.curve.q
      self.y = (self.y * z_inverse) % self.curve.q
      self.z = 1
      return self

    def compress(self):
      if self.is_inf():
        return bytes([0])
      self.normalise_coordinates()
      return bytes([2 + (self.y & 1)]) + to_binary(mpz(self.x))

    def to_tuple(self):
      if self.is_inf():
        return (0,0)
      self.normalise_coordinates()
      return (self.x, self.y)

    def __neg__(self):
      """
      returns -P
      """
      return self.curve._neg(self)

    def __add__(self, other):
      """
      Computes P + Q
      """
      # Check we're adding to a point
      # Removing this type check will save time
      if not isinstance(other, EllipticCurvePoint):
        raise TypeError(f"Cannot add an EllipticCurvePoint to type: {type(other)}")
      
      # Check the underlying points are on the same curve
      # Removing this type check will save time
      if not self.curve == other.curve:
        raise ValueError(f"Points are not defined over the same curve")

      # Easy cases when one point is the point at infinity
      if other.is_inf():
        return self
      elif self.is_inf():
        return other

      # Addition, logic based on Pz, Qz values
      if self == other:
        if self.z == 1:
          # Double when Z = 1
          return self.curve._mdouble(self)
        else:
          # Standard doubling
          return self.curve._double(self)

      if other.z == 1:
        if self.z == 1:
          # Addition when Z1 = Z2 = 1
          return self.curve._mmadd(self, other)
        else:
          # Addition when Z2 = 1
          return self.curve._madd(self, other)

      # Generic additon
      return self.curve._add(self, other)

    def __iadd__(self, other):
      self = self + other
      return self

    def __sub__(self, other):
      return self + (-other)

    def __isub__(self, other):
      self = self + (-other)
      return self

    def __mul__(self, n):
      # Removing this type check will save time.
      if not isinstance(n, int):
        raise TypeError(f"Scalar multiplication must be done using an integer.")

      Q = self
      R = self.curve.O
      # Deal with negative scalar multiplication
      if n < 0:
        n = -n
        Q = -Q
      while n > 0:
          if n % 2 == 1:
              R = R + Q
          Q = Q + Q
          n = n // 2
      return R.normalise_coordinates()

    def __rmul__(s, lhs):
      return s * lhs

    def __hash__(self):
      return hash(self.to_tuple())
      # return hash(str(self))


    def __eq__(self, other):
      # Removing this type check will save time.
      if isinstance(other, EllipticCurvePoint):
        return (self.x * other.y) % self.curve.q == (other.x * self.y) % self.curve.q
      return False

    def __str__(self):
      if self.is_inf():
        return "(0 : 1 : 0)"
      self.normalise_coordinates()
      return (f"({self.x} : {self.y} : 1)")


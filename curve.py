from point import EllipticCurvePoint
from gmpy2 import mpz

class EllipticCurve:
  """
  General Weierstrass curve 
  defined using projctive coordinates
  """
  def __init__(self, q, a, b):
    """
    Initalise Elliptic Curve
    in Weierstrass form
    y^2 = x^3 + ax + b mod q
    """
    self.point = EllipticCurvePoint
    self.a = mpz(a)
    self.b = mpz(b)
    self.q = mpz(q)
    self.O = self.point(self, 0, 1, 0, check=False)

    if self.determinant() == 0:
      raise ValueError(f"Invariants ({self.a}, {self.b}) define a singular curve mod {self.q}")

  def is_on_curve(self, point):
    """
    Is on curve `point`?
    """
    return self._is_on_curve(point.x, point.y, point.z)

  def _is_on_curve(self, x, y, z=1):
    """
    Is on curve (x,y,z)?
    """
    return (y**2 * z) % self.q == (x**3 + self.a * x * z**2 + self.b * z**3) % self.q

  def determinant(self):
    """
    Calculate Determinant of Curve.
    """
    return -16 * (4 * self.a**3 + 27 * self.b**2) % self.q

  def j_invariant(self):
    """
    Calculate j-Invariant of Curve.
    """
    return -1728 * ((4 * self.a)**3 * pow(self.determinant(), -1, self.q)) % self.q

  def _neg(self, P):
    """
    Return -P
    """
    if P == self.O:
      return self.O
    return self.point(self, P.x, -P.y % self.q, P.z, check=False)

  def _add(self, P, Q):
    # https://www.hyperelliptic.org/EFD/g1p/auto-shortw-projective.html#addition-add-1998-cmo-2
    y1z2 = P.y * Q.z               
    x1z2 = P.x * Q.z               
    z1z2 = P.z * Q.z               
    u    = (Q.y * P.z - y1z2) 
    v    = (Q.x * P.z - x1z2) 
    uu   = (u * u)     
    vv   = (v * v)     
    vvv  = (v * vv)    
    r    = (vv * x1z2) 
    a    = (uu*z1z2 - vvv - 2*r) 
    # New coordinates, now take modulus
    x3   = (v * a)               % self.q
    y3   = (u*(r-a) - vvv*y1z2)  % self.q
    z3   = (vvv * z1z2)          % self.q
    return self.point(self, x3, y3, z3, check=False)

  def _madd(self, P, Q):
    # https://www.hyperelliptic.org/EFD/g1p/auto-shortw-projective.html#addition-madd-1998-cmo
    u    = (Q.y * P.z - P.y) 
    v    = (Q.x * P.z - P.x) 
    uu   = (u * u)     
    vv   = (v * v)     
    vvv  = (v * vv)    
    r    = (vv * P.x) 
    a    = (uu*P.z - vvv - 2*r)  
    # New coordinates, now take modulus
    x3   = (v * a)               % self.q
    y3   = (u*(r-a) - vvv * P.y) % self.q
    z3   = (vvv * P.z)           % self.q
    return self.point(self, x3, y3, z3, check=False)

  def _mmadd(self, P, Q):
    # https://www.hyperelliptic.org/EFD/g1p/auto-shortw-projective.html#addition-mmadd-1998-cmo
    u    = (Q.y - P.y) 
    v    = (Q.x - P.x) 
    uu   = (u * u)     
    vv   = (v * v)     
    vvv  = (v * vv)
    r    = (vv * P.x) 
    a    = (uu - vvv - 2*r)      
    # New coordinates, now take modulus
    x3   = (v * a)               % self.q
    y3   = (u*(r-a) - vvv * P.y) % self.q
    z3   = vvv                   % self.q
    return self.point(self, x3, y3, z3, check=False)

  def _double(self, P):
    # This point will always have order 2
    if P.y == 0:
      return self.O

    # https://www.hyperelliptic.org/EFD/g1p/auto-shortw-projective.html#doubling-dbl-2007-bl
    xx  = (P.x * P.x)        
    zz  = (P.z * P.z)        
    w   = (self.a*zz + 3*xx) 
    s   = (2*P.y*P.z)        
    ss  = (s * s)            
    sss = (s * ss)
    r   = (P.y * s)          
    rr  = (r * r)            
    b   = (pow(P.x + r, 2, self.q) - xx - rr) 
    h   = (pow(w,2,self.q) - 2*b)             
    # New coordinates, now take modulus
    x3  = (h*s)               % self.q
    y3  = (w*(b - h) - 2*rr)  % self.q
    z3  = sss                 % self.q
    return self.point(self, x3, y3, z3, check=False)

  def _mdouble(self, P):

    # https://www.hyperelliptic.org/EFD/g1p/auto-shortw-projective.html#doubling-mdbl-2007-bl
    if P.y == 0:
      return self.O
    xx  = (P.x * P.x)     
    w   = (self.a + 3*xx) 
    yy  = (P.y * P.y)     
    r   = (2 * yy)        
    sss = (4*P.y*r)
    rr  = (r*r)           
    b   = (pow(P.x + r, 2, self.q) - xx - rr) 
    h   = (pow(w,2,self.q) - 2*b)             
    # New coordinates, now take modulus
    x3  = (2*h*P.y)           % self.q
    y3  = (w*(b - h) - 2*rr)  % self.q
    z3  = sss                 % self.q
    return self.point(self, x3, y3, z3, check=False)
    
  def __repr__(self):
    return f"EllipticCurve({self.q},{self.a},{self.b})"

  def __call__(self, x, y, z=1):
    """
    Define a point on the curve like sage

    E = EllipticCurve(11,2,5)
    P = E(3,7)
    """
    return self.point(self, x, y, z)

  def __str__(self):
    """
    Print info of the curve
    """
    info = f"Elliptic Curve defined by y^2 = x^3"
    if self.a:
      if self.a == 1:
        info += " + x"
      else:
        info += f" + {self.a}*x"
    if self.b:
      info += f" + {self.b}"
    info += f" over Finite Field of size {self.q}"
    return info






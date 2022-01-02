from math import ceil, sqrt, gcd
from gmpy2 import mpz
from collections import namedtuple
import time

# Create a simple Point class to represent the affine points.
Point = namedtuple("Point", "x y")

# The point at infinity (origin for the group law).
O = None

def check_point(P, curve):
    p, a, b = curve["p"], curve["a"], curve["b"]
    if P == O:
        return True
    else:
        return (P.y**2 - (P.x**3 + a*P.x + b)) % p == 0 and 0 <= P.x < p and 0 <= P.y < p

def point_inverse(P, curve):
    p = curve["p"]
    if (P == O or P.y == p or P.y == 0):
        return P
    return Point(P.x, p - P.y)

def point_addition(P, Q, curve):
    p, a, b = curve["p"], curve["a"], curve["b"]
    if P == O:
        return Q
    elif Q == O:
        return P
    elif Q == point_inverse(P, curve):
        return O
    else:
        if P == Q:
            lam = (3*P.x**2 + a)*pow(2*P.y, -1, p)
            lam %= p
        else:
            lam = (Q.y - P.y) * pow((Q.x - P.x), -1, p)
            lam %= p
    Rx = (lam**2 - P.x - Q.x) % p
    Ry = (lam*(P.x - Rx) - P.y) % p
    R = Point(Rx, Ry)
    return R

def double_and_add(P, n, curve):
    if n < 0:
        n = -n
        P = point_inverse(P, curve)
    Q = P
    R = O
    while n > 0:
        if n % 2 == 1:
            R = point_addition(R, Q, curve)
        Q = point_addition(Q, Q, curve)
        n = n // 2
    return R

def compress(P):
    if P == O:
        return bytes([0])
    bytes_x = int(P.x).to_bytes(32, byteorder='big')
    ybit = P.y & 1
    bytes_y = bytes([2 | ybit])
    return bytes_y + bytes_x

def bsgs(P, Q, curve, upper_bound=None, compress_points=False):
    if upper_bound:
        m = ceil(sqrt(upper_bound))
    else:
        m = ceil(sqrt(curve["n"]))

    if not hasattr(bsgs, 'baby_steps'):
        bsgs.baby_steps = dict()
        Pi = O
        for i in range(m):
            if compress_points:
                Pc = compress(Pi)
                bsgs.baby_steps[Pc] = i
            else:
                bsgs.baby_steps[Pi] = i
            Pi = point_addition(Pi, P, curve)
    
    C = double_and_add(P, m * (curve["n"] - 1), curve)
    Qi = Q

    # giant steps
    for j in range(m):
        if compress_points:
            Qc = compress(Qi)
        else:
            Qc = Qi
        if Qc in bsgs.baby_steps:
            return j * m + bsgs.baby_steps[Qc]
        Qi = point_addition(Qi, C, curve)
    # No solution
    return None

def crt(xs, ns_fac, n):
    x = 0
    ns = [p**e for p,e in ns_fac]
    common = gcd(*ns)
    ns = [n // common for n in ns]

    for xi, ni in zip(xs, ns):
        yi = n // ni
        zi = pow(yi, -1, ni)
        x += xi * yi * zi
    return x % n

def pohlig_hellman(P, Q, n_factors, curve, compress_points=False):
    n = curve["n"]
    dlogs = []
    for pi, ei in n_factors:
        # Set up for each step
        ni = pi**ei
        tmp = n // ni
        Pi = double_and_add(P, tmp, curve)
        Qi = double_and_add(Q, tmp, curve)

        # Groups of prime-power order
        xi = 0
        Qk_mul = ni // pi
        gamma = double_and_add(Pi, Qk_mul, curve)

        for k in range(ei):
            # Create hk in <γ>
            Pk = double_and_add(Pi, -xi, curve)
            PkQi = point_addition(Pk, Qi, curve)
            Qk = double_and_add(PkQi, Qk_mul, curve)

            # Solve partial dlog
            dk = bsgs(gamma, Qk, curve, upper_bound=pi, compress_points=compress_points)
            if dk == None:
                exit(f"No solution found for {pi=}, {k=}")

            # increment the secret
            xi += dk*(pi**k)
            
            # Reduce the exponent
            Qk_mul = Qk_mul // pi
        
        del bsgs.baby_steps
        dlogs.append(xi)
    return crt(dlogs, n_factors, n)



def easy(profile=False):
    curve = {
    "p"  : mpz(70626532935755249535015847300547144123),
    "a"  : mpz(53846105384463287779700510485213602312),
    "b"  : mpz(39488034705498452275235901953079958630),
    "n"  : mpz(70626532935755249533534472952715229049)
    }

    n_factors = [(3, 2), (7, 1), (103, 1), (149, 1), (2927, 1), (11383, 1), (19147411, 1), (157025399, 1), (729196241, 1)]
    d = 7925915577899419388989866332768730889
    P = Point(mpz(11485778132722977526438273953657454892), mpz(55353233819247962030145200182101892228))
    Q = Point(mpz(8282610078559603474288291323377077098), mpz(38703045175903081864811053665644938292))
    assert Q == double_and_add(P, d, curve)

    check_times = 10
    total_time = 0
    for _ in range(check_times):
        t = time.time()
        _d = pohlig_hellman(P, Q, n_factors, curve, compress_points=True)
        time_taken = time.time() - t
        total_time += time_taken
        assert _d == d

    total_time /= check_times
    print(f"dlog successfully found in: {total_time}s (Average of {check_times} computations)")

    if profile:
        import cProfile
        cProfile.runctx('pohlig_hellman(P, Q, n_factors, curve)', {'P' : P, 'Q' : Q, 'n_factors' : n_factors, 'curve' : curve}, {'pohlig_hellman' : pohlig_hellman})


def hard():
    curve = {
        "p"  : mpz(115792089210356248762697446949407573530086143415290314195533631308867097853951),
        "a"  : mpz(115792089210356248762697446949407573530086143415290314195533631308867097853948),
        "b"  : mpz(87141810357877800334735859453509209467794565735898098218969231306558751088856),
        "n"  : mpz(5263276782288920398304429406791253342296478557414290806433459571651589156874)
    }

    n_factors = [(2, 1), (11, 1), (103, 1), (9007, 1), (23251, 1), (2829341, 1), (12490680737, 1), (92928915967, 1), (390971098981, 1), (1056753725227, 1), (8173984130089, 1)]
    d = 3943544205328749264434177719074374035314915664326936412021520273127793155287
    P = Point(mpz(71240604556050345398966464559756938196778573228234842743790013676579385297801), mpz(60316620433133574305684204843273434175863163133594306844983613764544771974108))
    Q = Point(mpz(73603178013615315024061584560815809619225082394444494033618196279075556997083), mpz(63212696062746681459472418314686130004296932507725110671668786589609630338793))
    assert Q == double_and_add(P, d, curve)

    check_times = 1
    total_time = 0
    for _ in range(check_times):
        t = time.time()
        _d = pohlig_hellman(P, Q, n_factors, curve, compress_points=True)
        time_taken = time.time() - t
        total_time += time_taken
        assert _d == d
    total_time /= check_times
    print(f"dlog successfully found in: {total_time}s (Average of {check_times} computations)")

if __name__ == '__main__':
    easy(profile=True)
    # hard()



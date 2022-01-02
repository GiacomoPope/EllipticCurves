from math import ceil, sqrt, gcd
from functools import reduce
import random


def normalise_queue(queue):
    # optimise for non-zero inverses
    # optimise for our use case by generators
    # NOTE: 1-index prefix for optimization
    q = queue[0].curve.q
    n = len(queue)
    z_prod = 1
    prefix = [1] * (n + 1)
    for i, P in enumerate(queue):
        z_prod = z_prod * P.z % q
        prefix[i + 1] = prefix[i] * P.z % q
    z_prod_inverse = pow(z_prod, -1, q)
    # i = n - 1 separate
    P = queue[n - 1]
    cur_suffix = P.z
    P.x = P.x * prefix[n - 1] * z_prod_inverse % q
    P.y = P.y * prefix[n - 1] * z_prod_inverse % q
    P.z = 1
    yield P
    # 0 <= i <= n - 2
    for i in range(n - 2, -1, -1):
        P = queue[i]
        z = P.z
        cur_inverse = prefix[i] * cur_suffix * z_prod_inverse % q
        cur_suffix = cur_suffix * z % q
        P.x = P.x * cur_inverse % q
        P.y = P.y * cur_inverse % q
        P.z = 1
        yield P


def bsgs(P, Q, n, upper_bound=None, batched=True):
    if upper_bound:
        m = ceil(sqrt(upper_bound))
    else:
        m = ceil(sqrt(n))

    if not hasattr(bsgs, 'baby_steps'):
        baby_steps = dict()
        index, queue = [], []
        Pi = P.curve.O
        for i in range(m):
            if Pi == Q:
                return i
            if Pi.z == 0:
                baby_steps[Pi] = i
            else:
                index.append(i)
                queue.append(Pi)
                if len(queue) >= 100 or i == m - 1:
                    # NOTE: normalise_queue returns generator in reversed order
                    queue = normalise_queue(queue)
                    for j, Pj in zip(reversed(index), queue):
                        baby_steps[Pj] = j
                    index, queue = [], []
            Pi += P
        # update attribute at the end
        bsgs.baby_steps = baby_steps

    C = (m * (n - 1)) * P
    Qi = Q
    # giant steps
    for j in range(m):
        if Qi in bsgs.baby_steps:
            return j * m + bsgs.baby_steps[Qi]
        Qi += C
    # No solution
    # raise Exception(f"No solution found\nP = {P}\nQ = {Q}\nm, n = {m, n}\nupper_bound = {upper_bound}")
    return None


def discrete_log_rho(P, Q, n, upper_bound=None):
    PARTITION = 20
    MEMORY = 4

    if upper_bound:
        m = ceil(sqrt(upper_bound))
    else:
        m = ceil(sqrt(n))

    # setup to costly, use bsgs
    if m < PARTITION:
        return bsgs(P, Q, n, upper_bound=upper_bound)

    # margin for error
    reset_bound = 8 * m

    # to avoid infinite loops
    for s in range(10):
        # random walk function setup
        m = [random.randint(0, upper_bound-1) for i in range(PARTITION)]
        n = [random.randint(0, upper_bound-1) for i in range(PARTITION)]
        M = [m[i] * P + n[i] * Q for i in range(PARTITION)]

        ax = random.randint(0, upper_bound-1)
        bx = 0
        x = ax * P

        sigma = [(0, None)]*MEMORY
        H = {}  # memory
        i0 = 0
        nextsigma = 0

        # random walk, we need an efficient hash
        for i in range(reset_bound):
            s = hash(x) % PARTITION
            (x, ax, bx) = (x + M[s], ax + m[s], bx + n[s])
            # look for collisions
            if x in H:
                ay, by = H[x]
                if bx == by:
                    break
                else:
                    res = (ay - ax) * pow(bx - by, -1, upper_bound)
                    if res * P == Q:
                        return res
                    else:
                        break
            # should we remember this value?
            elif i >= nextsigma:
                if sigma[i0][1] is not None:
                    H.pop(sigma[i0][1])
                sigma[i0] = (i, x)
                i0 = (i0 + 1) % MEMORY
                nextsigma = 3 * sigma[i0][0]  # 3 seems a good choice
                H[x] = (ax, bx)

    exit("Algorithm failed...")


def crt(xs, ns_fac, n):
    x = 0
    ns = [p ** e for p, e in ns_fac]
    common = reduce(gcd, ns)
    ns = [n // common for n in ns]

    for xi, ni in zip(xs, ns):
        yi = n // ni
        zi = pow(yi, -1, ni)
        x += xi * yi * zi
    return x % n


def pohlig_hellman(P, Q, n, n_factors, dlog=bsgs):
    dlogs = []
    for pi, ei in n_factors:
        # Set up for each step
        ni = pi ** ei
        tmp = n // ni
        Pi = tmp * P
        Qi = tmp * Q

        # Groups of prime-power order
        xi = 0
        Qk_mul = ni // pi
        gamma = Qk_mul * Pi

        for k in range(ei):
            # Create hk in <γ>
            Pk = -xi * Pi
            Qk = Qk_mul * (Pk + Qi)

            # Solve partial dlog
            dk = dlog(gamma, Qk, n, upper_bound=pi)

            if dk is None:
                exit(f"Discrete log failed in bsgs step, for {str(gamma)}, {str(Qk)}, {pi=}")

            # increment the secret
            xi += dk*(pi**k)

            # Reduce the exponent
            Qk_mul = Qk_mul // pi

        if hasattr(bsgs, 'baby_steps'):
            del bsgs.baby_steps
        dlogs.append(xi)
    return crt(dlogs, n_factors, n)

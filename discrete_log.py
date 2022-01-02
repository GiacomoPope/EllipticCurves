from math import ceil, sqrt, gcd
import random

def normalise_queue(queue):
    n = len(queue)
    q = queue[0][1].curve.q
    z_prod = 1
    prefix = [-1] * n
    for i, (_, P) in enumerate(queue):
        z = P.z
        if z == 0: z = 1
        z_prod = z_prod * z % q
        if i == 0: prefix[0] = z
        else: prefix[i] = prefix[i - 1] * z % q
    z_prod_inverse = pow(z_prod, -1, q)
    cur_suffix = 1
    # going backwards
    # i = n - 1 separate
    P = queue[n - 1][1]
    cur_suffix = P.z
    if cur_suffix == 0:
        cur_suffix = 1
    P.x = P.x * prefix[n - 2] * z_prod_inverse % q
    P.y = P.y * prefix[n - 2] * z_prod_inverse % q
    P.z = 0 if P.z == 0 else 1
    # 1 <= i <= n - 2
    for i in range(n - 2, 0, -1):
        cur_inverse = prefix[i - 1] * cur_suffix % q
        P = queue[i][1]
        z = P.z
        if z != 0:
            cur_suffix = cur_suffix * z % q
            P.x = P.x * cur_inverse * z_prod_inverse % q
            P.y = P.y * cur_inverse * z_prod_inverse % q
            P.z = 1
    # i = 0 separate
    P = queue[0][1]
    P.x = P.x * cur_suffix * z_prod_inverse % q
    P.y = P.y * cur_suffix * z_prod_inverse % q
    P.z = 0 if P.z == 0 else 1
    return queue

def bsgs(P, Q, n, upper_bound=None, batched=False):
    if upper_bound:
        m = ceil(sqrt(upper_bound))
    else:
        m = ceil(sqrt(n))

    if batched:
        if not hasattr(bsgs, 'baby_steps'):
            bsgs.baby_steps = dict()
            queue = []
            Pi = P.curve.O
            for i in range(m):
                queue.append((i, Pi))
                Pi += P
                if len(queue) == m or len(queue) >= 500:
                    queue = normalise_queue(queue)
                    for j, Pj in queue:
                        bsgs.baby_steps[Pj] = j
                    queue = []
    
    else:
        if not hasattr(bsgs, 'baby_steps'):
            bsgs.baby_steps = dict()
            Pi = P.curve.O
            for i in range(m):
                bsgs.baby_steps[Pi] = i
                Pi += P
    
    C = (m * (n - 1))*P
    Qi = Q
    # giant steps
    for j in range(m):
        if Qi in bsgs.baby_steps:
            return j * m + bsgs.baby_steps[Qi]
        Qi += C
    # No solution
    return None

def discrete_log_rho(P, Q, n, upper_bound=None):
    partition_size = 20
    memory_size = 4

    if upper_bound:
        m = ceil(sqrt(upper_bound))
    else:
        m = ceil(sqrt(n))

    # setup to costly, use bsgs 
    if m < partition_size:
        return bsgs(P, Q, n, upper_bound=upper_bound)

    # margin for error
    reset_bound = 8*m

    # to avoid infinite loops
    for s in range(10):
        # random walk function setup 
        m = [random.randint(0,upper_bound-1) for i in range(partition_size)]
        n = [random.randint(0,upper_bound-1) for i in range(partition_size)]
        M = [m[i]*P + n[i]*Q for i in range(partition_size)]
         
        ax = random.randint(0,upper_bound-1)
        bx = 0
        x = ax*P
         
        sigma = [(0,None)]*memory_size 
        H = {} # memory 
        i0 = 0 
        nextsigma = 0

        # random walk, we need an efficient hash 
        for i in range(reset_bound):              
            s = hash(x) % partition_size 
            (x, ax, bx) = (x+M[s], ax+m[s], bx+n[s]) 
            # look for collisions
            if x in H:
                ay, by = H[x]
                if bx == by:
                    break 
                else: 
                    res = (ay-ax)*pow(bx-by, -1, upper_bound)
                    if res*P == Q:
                        return res
                    else:
                        break
            # should we remember this value?
            elif i >= nextsigma: 
                if sigma[i0][1] is not None: 
                    H.pop(sigma[i0][1])
                sigma[i0] = (i,x)
                i0 = (i0+1) % memory_size 
                nextsigma = 3*sigma[i0][0] #3 seems a good choice 
                H[x] = (ax, bx)

    exit("Algorithm failed...")

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

def pohlig_hellman(P, Q, n, n_factors, dlog=bsgs):
    dlogs = []
    for pi, ei in n_factors:
        # Set up for each step
        ni = pi**ei
        tmp = n // ni
        Pi = tmp*P
        Qi = tmp*Q

        # Groups of prime-power order
        xi = 0
        Qk_mul = ni // pi
        gamma = Qk_mul*Pi

        for k in range(ei):
            # Create hk in <γ>
            Pk = -xi*Pi
            Qk = Qk_mul*(Pk + Qi)

            # Solve partial dlog
            dk = dlog(gamma, Qk, n, upper_bound=pi)
            if dk is None:
                print(f"Discrete log failed for {gamma=}, {Qk=}, {pi=}")
                exit()

            # increment the secret
            xi += dk*(pi**k)
            
            # Reduce the exponent
            Qk_mul = Qk_mul // pi
        
        if hasattr(bsgs, 'baby_steps'): del bsgs.baby_steps
        dlogs.append(xi)
    return crt(dlogs, n_factors, n)
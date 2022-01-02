"""
def gen_challenge(p_bits=128, largest_factor=32):
    p = random_prime(2^p_bits)
    a, b = random.randint(1,p), random.randint(1,p)  
    E = EllipticCurve(GF(p), [a,b]) 
    n = E.order() 
    fs = ecm.factor(n)

    if int(fs[-1]).bit_length() < largest_factor: 
        P = E.gens()[0] 
        d = random.randint(1,n) 
        Q = d*P  
        print(fs)

        print(f'"p" : {p},') 
        print(f'"a" : {a},') 
        print(f'"b" : {b},') 
        print(f'"n" : {n},') 
        print(f'"Px" : {P[0]},') 
        print(f'"Py" : {P[1]},') 
        print(f'"Qx" : {Q[0]},') 
        print(f'"Qy" : {Q[1]},') 
        print(f'"n_factors" : {list(factor(n))},') 
        print(f'"d" : {d}') 
"""

import time
from tqdm import tqdm
from curve import EllipticCurve
from discrete_log import pohlig_hellman, bsgs, discrete_log_rho


def test(data, check_times, dlog=bsgs, profile=False, progress=False):
    p = data["p"]
    a = data["a"]
    b = data["b"]
    # dlog secret
    d = data["d"]

    # Set up curve
    E = EllipticCurve(p, a, b)
    n = data["n"]
    n_factors = data["n_factors"]

    P = E(data["Px"], data["Py"])
    Q = E(data["Qx"], data["Qy"])
    d = data["d"]
    assert d*P == Q

    total_time = 0
    if progress:
        tq = tqdm(range(check_times))
    else:
        tq = range(check_times)
    
    for _ in tq:
        t = time.time()
        _d = pohlig_hellman(P, Q, n, n_factors, dlog=dlog)
        time_taken = time.time() - t
        total_time += time_taken
        assert _d == d

    total_time /= check_times
    print(f"dlog successfully found in: {total_time}s (Average of {check_times} computations)")

    if profile:
        import cProfile
        gvars = {'P': P, 'Q': Q, 'n': n, 'n_factors': n_factors}
        lvars = {'pohlig_hellman': pohlig_hellman}
        cProfile.runctx('pohlig_hellman(P, Q, n, n_factors)', globals=gvars, locals=lvars)


easy = {
    "p": 70626532935755249535015847300547144123,
    "a": 53846105384463287779700510485213602312,
    "b": 39488034705498452275235901953079958630,
    "n": 70626532935755249533534472952715229049,
    "Px": 11485778132722977526438273953657454892,
    "Py": 55353233819247962030145200182101892228,
    "Qx": 8282610078559603474288291323377077098,
    "Qy": 38703045175903081864811053665644938292,
    "n_factors": [(3, 2), (7, 1), (103, 1), (149, 1), (2927, 1), (11383, 1), (19147411, 1), (157025399, 1), (729196241, 1)],
    "d": 7925915577899419388989866332768730889,
}

medium = {
    "p": 98906321313648462858319284505234548427,
    "a": 32145787080282355644144967255667048727,
    "b": 89548250861913899611424618886487180071,
    "n": 98906321313648462861838792221717503570,
    "Px": 26117803474791015119012614892802916918,
    "Py": 4572686300801370513052182829424865063,
    "Qx": 3147167679804035091862248740947924832,
    "Qy": 56854158179379733482731991597760459393,
    "n_factors": [(2, 1), (5, 1), (79, 1), (149, 1), (331, 1), (829, 1), (14557, 1), (2952361, 1), (3841283, 1), (18548573663, 1)],
    "d": 61740216832614097604827460809608306308
}

hard = {
    "p": 115792089210356248762697446949407573530086143415290314195533631308867097853951,
    "a": 115792089210356248762697446949407573530086143415290314195533631308867097853948,
    "b": 87141810357877800334735859453509209467794565735898098218969231306558751088856,
    "n": 5263276782288920398304429406791253342296478557414290806433459571651589156874,
    "Px": 71240604556050345398966464559756938196778573228234842743790013676579385297801,
    "Py": 60316620433133574305684204843273434175863163133594306844983613764544771974108,
    "Qx": 73603178013615315024061584560815809619225082394444494033618196279075556997083,
    "Qy": 63212696062746681459472418314686130004296932507725110671668786589609630338793,
    "n_factors": [(2, 1), (11, 1), (103, 1), (9007, 1), (23251, 1), (2829341, 1), (12490680737, 1), (92928915967, 1), (390971098981, 1), (1056753725227, 1), (8173984130089, 1)],
    "d": 3943544205328749264434177719074374035314915664326936412021520273127793155287,
}

if __name__ == '__main__':
    # (15) 0.568s
    # (15) 1.574s
    # (1)  92.07s
    test(easy, 15, dlog=bsgs, profile=False)
    # test(medium, 15, dlog=bsgs, profile=False)
    # test(hard, 1, dlog=bsgs, profile=False)

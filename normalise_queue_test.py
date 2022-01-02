import time
from point import EllipticCurvePoint as Point
from random import randint
from curve import EllipticCurve
from discrete_log import normalise_queue
from projective_ecdlp_test import easy, medium, hard

def generate_queue(n, data=hard):
    # data is from [easy, medium, hard]
    q, a, b = data['p'], data['a'], data['b']
    E = EllipticCurve(q, a, b)
    pts = []
    for i in range(n):
        x, y, z = randint(0, q - 1), randint(0, q - 1), randint(1, q - 1)
        pts.append((i, Point(E, x, y, z, check=False)))
    return pts

def test(n, data=hard):
    # average time to normalise 10^6 samples in n-batches
    SAMPLES = 10 ** 6
    start_time = time.time()
    total_time = 0
    test_data = generate_queue(SAMPLES, data)
    s = time.time()
    queue = []
    for i in range(SAMPLES):
        queue.append(test_data[i])
        if len(queue) == n or i == SAMPLES - 1:
            queue = normalise_queue(queue)
            queue = []
    t = time.time() - s
    return t

def main():
    cand = [1, 10, 50, 100, 300, 500, 750, 1000, 3000, 5000, 7500, 10000, 20000, 50000, 100000, 200000, 500000, 10000000]
    for n in cand:
        print(f'{n}-batches -> ', end='', flush=True)
        print(f'{test(n):.3f}ms')

if __name__ == '__main__':
    main()
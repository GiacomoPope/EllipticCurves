# ECDLP Benchmarks

Comparing the computation time of PH/BSGS with SageMath, an old script I made using affine coordinates and `gmpy2`, and the newer projective coordinate classes defined in this repo.

## My specs

```
MacBook Pro (Retina, 13-inch, Early 2015)
3.1 GHz Dual-Core Intel Core i7
16 GB 1867 MHz DDR3
```

## SageMath

### Setup

```py
# Curve parameters
p = 70626532935755249535015847300547144123
a = 53846105384463287779700510485213602312
b = 39488034705498452275235901953079958630
# dlog secret
d = 7925915577899419388989866332768730889

E = EllipticCurve(GF(p), [a,b])
P = E(11485778132722977526438273953657454892, 55353233819247962030145200182101892228)
Q = E(8282610078559603474288291323377077098, 38703045175903081864811053665644938292)

assert E.order() == 70626532935755249533534472952715229049
assert E.order() == P.order()
assert d*P == Q
assert P.order() == 3^2 * 7 * 103 * 149 * 2927 * 11383 * 19147411 * 157025399 * 729196241
```

### Benchmark

```py
sage: time P.discrete_log(Q)                                                                                            
CPU times: user 4.87 s, sys: 41.7 ms, total: 4.91 s
Wall time: 4.93 s
7925915577899419388989866332768730889
```


## Python (Messy impl. Affine Coordinates)

### Setup

See the file `affine_ecdlp_test.py` adapted from a solution I made for a CSAW challenge

### Benchmark

```
Jack: EllipticCurves % py affine_ecdlp_test.py
dlog successfully found in: 0.29899537563323975s (Average of 10 computations)
dlog successfully found in: 46.06622505187988s (Average of 1 computations)
```

## Golang

### Benchmark

Run `go test *.go -bench=.` to get the following output

Jack: EllipticCurves % go test -bench=.
goos: darwin
goarch: amd64
pkg: ecdlp
cpu: Intel(R) Core(TM) i7-5557U CPU @ 3.10GHz
BenchmarkPohligHellmanEasy-4           4     288281956 ns/op
BenchmarkPohligHellmanHard-4           1    66675495244 ns/op
PASS
ok      ecdlp   69.279s

Which is `0.278966777s`, for the easy test, and `58.087027854s`, putting it at the same time as python + gpmy2 (affine) for the easy challenge and slower for the hard one.

## Python (Projective Coordinates)

### Setup

See the file `projective_ecdlp_test.py`, using the classes defined in this repo

### Benchmark

```
Jack: EllipticCurves % py projective_ecdlp_test.py
dlog successfully found in: 0.4461967468261719s (Average of 20 computations)
dlog successfully found in: 96.60710620880127s (Average of 1 computations)
```

Python's `cProfile`:

```
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000  115.173  115.173 <string>:1(<module>)
     7673    0.034    0.000    0.045    0.000 curve.py:104(_double)
       66    0.000    0.000    0.001    0.000 curve.py:126(_mdouble)
     3750    0.017    0.000    0.018    0.000 curve.py:56(_add)
  7285327   24.965    0.000   34.686    0.000 curve.py:89(_mmadd)
        1    0.000    0.000    0.000    0.000 discrete_log.py:26(crt)
        1    0.000    0.000    0.000    0.000 discrete_log.py:28(<listcomp>)
       11    8.300    0.755  113.078   10.280 discrete_log.py:3(bsgs)
        1    0.000    0.000    0.000    0.000 discrete_log.py:30(<listcomp>)
        1    2.026    2.026  115.173  115.173 discrete_log.py:38(pohlig_hellman)
       66    0.006    0.000    0.104    0.002 point.py:102(__mul__)
       66    0.000    0.000    0.104    0.002 point.py:120(__rmul__)
  7285371    4.203    0.000   44.542    0.000 point.py:123(__hash__)
  7296838    6.888    0.000    7.588    0.000 point.py:126(__eq__)
 21879545    3.778    0.000    3.778    0.000 point.py:15(is_inf)
  7285426    9.816    0.000   32.124    0.000 point.py:21(scale)
  7285371    5.177    0.000   38.793    0.000 point.py:39(to_tuple)
  7296812    9.724    0.000    9.724    0.000 point.py:4(__init__)
  7297273   11.909    0.000   57.261    0.000 point.py:51(__add__)
  7285349    3.038    0.000   60.202    0.000 point.py:91(__iadd__)
        1    0.000    0.000  115.173  115.173 {built-in method builtins.exec}
       11    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
  7285371    1.547    0.000    1.547    0.000 {built-in method builtins.hash}
 14594177    1.428    0.000    1.428    0.000 {built-in method builtins.isinstance}
  7300840   22.317    0.000   22.317    0.000 {built-in method builtins.pow}
       11    0.000    0.000    0.000    0.000 {built-in method math.ceil}
        1    0.000    0.000    0.000    0.000 {built-in method math.gcd}
       11    0.000    0.000    0.000    0.000 {built-in method math.sqrt}
       11    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```


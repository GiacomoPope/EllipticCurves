# EllipticCurves

Implementation of elliptic curve arithematic for fun, and for use of plugging into cryptanalytic attacks for CTFs etc.

⚠️ Code is written to be fast rather than safe, so this is 100% not suitible for cryptographic implementations ⚠️

## To-Do

- Montgomery arithematic for fields
- Batch normalisation for giant steps
- Montgomery arithematic for curves, when suitible
- Pairings (Which also means divisors)
- More Benchmarks for point addion and scalar multiplication outside of dlog

# Discrete Logarithm Benchmarks

### Easy Challenge

```py
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
```

### Medium Challenge

```py
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
```

### Hard Challenge

```py
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
```

## Projective Coordinates

- dlog successfully found in: 0.4872660517692566s (Average of 20 computations)
- dlog successfully found in: 1.5874902725219726s (Average of 10 computations)
- dlog successfully found in: 93.61399602890015s (Average of 1 computations)

### Easy Challenge

```shell
dlog successfully found in: 0.4872660517692566s (Average of 20 computations)
         1144631 function calls in 0.750 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.750    0.750 <string>:1(<module>)
     3079    0.009    0.000    0.012    0.000 curve.py:107(_double)
       54    0.000    0.000    0.000    0.000 curve.py:128(_mdouble)
        1    0.000    0.000    0.000    0.000 curve.py:51(_neg)
     1511    0.004    0.000    0.004    0.000 curve.py:59(_add)
    43637    0.129    0.000    0.147    0.000 curve.py:77(_madd)
    14932    0.027    0.000    0.032    0.000 curve.py:92(_mmadd)
        1    0.000    0.000    0.000    0.000 discrete_log.py:136(crt)
        1    0.000    0.000    0.000    0.000 discrete_log.py:138(<listcomp>)
        1    0.000    0.000    0.000    0.000 discrete_log.py:140(<listcomp>)
        1    0.016    0.016    0.750    0.750 discrete_log.py:149(pohlig_hellman)
       10    0.104    0.010    0.714    0.071 discrete_log.py:37(bsgs)
    44539    0.071    0.000    0.072    0.000 discrete_log.py:6(normalise_queue)
       55    0.002    0.000    0.031    0.001 point.py:100(__mul__)
       55    0.000    0.000    0.031    0.001 point.py:118(__rmul__)
    58602    0.026    0.000    0.122    0.000 point.py:121(__hash__)
   107333    0.077    0.000    0.086    0.000 point.py:125(__eq__)
   185184    0.028    0.000    0.028    0.000 point.py:16(is_inf)
    58648    0.022    0.000    0.045    0.000 point.py:19(normalise_coordinates)
    58602    0.033    0.000    0.086    0.000 point.py:37(to_tuple)
        1    0.000    0.000    0.000    0.000 point.py:43(__neg__)
    63292    0.092    0.000    0.363    0.000 point.py:49(__add__)
    63214    0.025    0.000    0.025    0.000 point.py:5(__init__)
    58586    0.021    0.000    0.356    0.000 point.py:89(__iadd__)
        1    0.000    0.000    0.000    0.000 {built-in method _functools.reduce}
        1    0.000    0.000    0.750    0.750 {built-in method builtins.exec}
       19    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
    58602    0.010    0.000    0.010    0.000 {built-in method builtins.hash}
   170680    0.015    0.000    0.015    0.000 {built-in method builtins.isinstance}
    44539    0.005    0.000    0.005    0.000 {built-in method builtins.len}
    21235    0.026    0.000    0.026    0.000 {built-in method builtins.pow}
       10    0.000    0.000    0.000    0.000 {built-in method math.ceil}
       10    0.000    0.000    0.000    0.000 {built-in method math.sqrt}
    88193    0.009    0.000    0.009    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

### Medium Challenge

```shell
dlog successfully found in: 1.5874902725219726s (Average of 10 computations)
         3170998 function calls in 2.225 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    2.225    2.225 <string>:1(<module>)
     3465    0.011    0.000    0.014    0.000 curve.py:107(_double)
       57    0.000    0.000    0.000    0.000 curve.py:128(_mdouble)
     1766    0.005    0.000    0.005    0.000 curve.py:59(_add)
   138642    0.422    0.000    0.478    0.000 curve.py:77(_madd)
    22438    0.043    0.000    0.051    0.000 curve.py:92(_mmadd)
        1    0.000    0.000    0.000    0.000 discrete_log.py:136(crt)
        1    0.000    0.000    0.000    0.000 discrete_log.py:138(<listcomp>)
        1    0.000    0.000    0.000    0.000 discrete_log.py:140(<listcomp>)
        1    0.056    0.056    2.225    2.225 discrete_log.py:149(pohlig_hellman)
       10    0.408    0.041    2.145    0.214 discrete_log.py:37(bsgs)
   141465    0.232    0.000    0.237    0.000 discrete_log.py:6(normalise_queue)
       59    0.003    0.000    0.037    0.001 point.py:100(__mul__)
       59    0.000    0.000    0.037    0.001 point.py:118(__rmul__)
   161116    0.072    0.000    0.293    0.000 point.py:121(__hash__)
   306454    0.228    0.000    0.255    0.000 point.py:125(__eq__)
   494025    0.077    0.000    0.077    0.000 point.py:16(is_inf)
   161164    0.043    0.000    0.076    0.000 point.py:19(normalise_coordinates)
   161116    0.094    0.000    0.193    0.000 point.py:37(to_tuple)
   166456    0.248    0.000    1.001    0.000 point.py:49(__add__)
   166367    0.066    0.000    0.066    0.000 point.py:5(__init__)
   161098    0.060    0.000    1.027    0.000 point.py:89(__iadd__)
        1    0.000    0.000    0.000    0.000 {built-in method _functools.reduce}
        1    0.000    0.000    2.225    2.225 {built-in method builtins.exec}
       20    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
   161116    0.027    0.000    0.027    0.000 {built-in method builtins.hash}
   472969    0.042    0.000    0.042    0.000 {built-in method builtins.isinstance}
   141465    0.014    0.000    0.014    0.000 {built-in method builtins.len}
    29517    0.039    0.000    0.039    0.000 {built-in method builtins.pow}
       10    0.000    0.000    0.000    0.000 {built-in method math.ceil}
       10    0.000    0.000    0.000    0.000 {built-in method math.sqrt}
   280126    0.035    0.000    0.035    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

### Hard Challenge

```shell
dlog successfully found in: 93.61399602890015s (Average of 1 computations)
         134190329 function calls in 136.484 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000  136.484  136.484 <string>:1(<module>)
     7673    0.038    0.000    0.052    0.000 curve.py:107(_double)
       64    0.001    0.000    0.003    0.000 curve.py:128(_mdouble)
     3750    0.018    0.000    0.019    0.000 curve.py:59(_add)
  4881500   29.390    0.000   31.857    0.000 curve.py:77(_madd)
  2403827    6.427    0.000    7.327    0.000 curve.py:92(_mmadd)
        1    0.000    0.000    0.000    0.000 discrete_log.py:136(crt)
        1    0.000    0.000    0.000    0.000 discrete_log.py:138(<listcomp>)
        1    0.000    0.000    0.000    0.000 discrete_log.py:140(<listcomp>)
        1    2.974    2.974  136.484  136.484 discrete_log.py:149(pohlig_hellman)
       11   24.729    2.248  133.435   12.130 discrete_log.py:37(bsgs)
  4980136   13.803    0.000   14.139    0.000 discrete_log.py:6(normalise_queue)
       65    0.007    0.000    0.115    0.002 point.py:100(__mul__)
       65    0.000    0.000    0.115    0.002 point.py:118(__rmul__)
  7285368    3.723    0.000   21.725    0.000 point.py:121(__hash__)
 12227669   12.217    0.000   13.413    0.000 point.py:125(__eq__)
 21879166    3.691    0.000    3.691    0.000 point.py:16(is_inf)
  7285422    3.865    0.000   10.522    0.000 point.py:19(normalise_coordinates)
  7285368    4.712    0.000   16.464    0.000 point.py:37(to_tuple)
  7296899   11.935    0.000   62.108    0.000 point.py:49(__add__)
  7296812    3.373    0.000    3.373    0.000 point.py:5(__init__)
  7285348    3.043    0.000   65.043    0.000 point.py:89(__iadd__)
        1    0.000    0.000    0.000    0.000 {built-in method _functools.reduce}
        1    0.000    0.000  136.484  136.484 {built-in method builtins.exec}
       22    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
  7285368    1.537    0.000    1.537    0.000 {built-in method builtins.hash}
 19524633    1.894    0.000    1.894    0.000 {built-in method builtins.isinstance}
  4980136    0.573    0.000    0.573    0.000 {built-in method builtins.len}
  2419340    6.998    0.000    6.998    0.000 {built-in method builtins.pow}
       11    0.000    0.000    0.000    0.000 {built-in method math.ceil}
       11    0.000    0.000    0.000    0.000 {built-in method math.sqrt}
  9861657    1.534    0.000    1.534    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```


## Affine Coordinates

- dlog successfully found in: 0.2927542686462402s (Average of 20 computations)
- dlog successfully found in: 0.8004036188125611s (Average of 10 computations)
- dlog successfully found in: 48.72581100463867s (Average of 1 computations)


### Easy Challenge

```shell
dlog successfully found in: 0.2927542686462402s (Average of 20 computations)
         444914 function calls in 0.369 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   127040    0.029    0.000    0.054    0.000 <string>:1(<lambda>)
        1    0.000    0.000    0.369    0.369 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:100(<listcomp>)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:102(<listcomp>)
        1    0.010    0.010    0.369    0.369 affine_ecdlp_test.py:110(pohlig_hellman)
    63549    0.043    0.000    0.073    0.000 affine_ecdlp_test.py:19(point_inverse)
    63671    0.133    0.000    0.328    0.000 affine_ecdlp_test.py:25(point_addition)
       57    0.002    0.000    0.025    0.000 affine_ecdlp_test.py:45(double_and_add)
       10    0.029    0.003    0.343    0.034 affine_ecdlp_test.py:66(bsgs)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:98(crt)
   127040    0.025    0.000    0.025    0.000 {built-in method __new__ of type object at 0x10990a430}
        1    0.000    0.000    0.369    0.369 {built-in method builtins.exec}
       10    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
    63500    0.098    0.000    0.098    0.000 {built-in method builtins.pow}
       10    0.000    0.000    0.000    0.000 {built-in method math.ceil}
        1    0.000    0.000    0.000    0.000 {built-in method math.gcd}
       10    0.000    0.000    0.000    0.000 {built-in method math.sqrt}
        9    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

### Medium Challenge

```shell
dlog successfully found in: 0.8004036188125611s (Average of 10 computations)
         1164926 function calls in 1.040 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
   332713    0.076    0.000    0.163    0.000 <string>:1(<lambda>)
        1    0.000    0.000    1.040    1.040 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:100(<listcomp>)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:102(<listcomp>)
        1    0.040    0.040    1.040    1.040 affine_ecdlp_test.py:110(pohlig_hellman)
   166370    0.114    0.000    0.212    0.000 affine_ecdlp_test.py:19(point_inverse)
   166656    0.362    0.000    0.910    0.000 affine_ecdlp_test.py:25(point_addition)
       60    0.002    0.000    0.027    0.000 affine_ecdlp_test.py:45(double_and_add)
       10    0.088    0.009    0.983    0.098 affine_ecdlp_test.py:66(bsgs)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:98(crt)
   332713    0.087    0.000    0.087    0.000 {built-in method __new__ of type object at 0x10990a430}
        1    0.000    0.000    1.040    1.040 {built-in method builtins.exec}
       10    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
   166356    0.271    0.000    0.271    0.000 {built-in method builtins.pow}
       10    0.000    0.000    0.000    0.000 {built-in method math.ceil}
        1    0.000    0.000    0.000    0.000 {built-in method math.gcd}
       10    0.000    0.000    0.000    0.000 {built-in method math.sqrt}
       10    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

### Hard Challenge

```shell
dlog successfully found in: 48.72581100463867s (Average of 1 computations)
         51078262 function calls in 67.489 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
 14593615    3.782    0.000   10.246    0.000 <string>:1(<lambda>)
        1    0.000    0.000   67.489   67.489 <string>:1(<module>)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:100(<listcomp>)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:102(<listcomp>)
        1    1.703    1.703   67.489   67.489 affine_ecdlp_test.py:110(pohlig_hellman)
  7296816    5.566    0.000   12.504    0.000 affine_ecdlp_test.py:19(point_inverse)
  7297273   21.456    0.000   59.306    0.000 affine_ecdlp_test.py:25(point_addition)
       66    0.005    0.000    0.080    0.001 affine_ecdlp_test.py:45(double_and_add)
       11    6.475    0.589   65.732    5.976 affine_ecdlp_test.py:66(bsgs)
        1    0.000    0.000    0.000    0.000 affine_ecdlp_test.py:98(crt)
 14593615    6.465    0.000    6.465    0.000 {built-in method __new__ of type object at 0x10990a430}
        1    0.000    0.000   67.489   67.489 {built-in method builtins.exec}
       11    0.000    0.000    0.000    0.000 {built-in method builtins.hasattr}
  7296814   22.037    0.000   22.037    0.000 {built-in method builtins.pow}
       11    0.000    0.000    0.000    0.000 {built-in method math.ceil}
        1    0.000    0.000    0.000    0.000 {built-in method math.gcd}
       11    0.000    0.000    0.000    0.000 {built-in method math.sqrt}
       11    0.000    0.000    0.000    0.000 {method 'append' of 'list' objects}
        1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
```

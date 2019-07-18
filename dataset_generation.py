import numpy as np
import math
import random

##
# n is the number of tasks
# T parameter of the problem
# R is upper bound on r_n 
# C is upper bound on all c_i
# fun can be ='random' or ='polynomail'
##
def generate_bounds(n, T, fun='random'):
    c = np.zeros(n+1, dtype=int)
    d = np.zeros(n+1, dtype=int)
    r = np.zeros(n+1, dtype=int)
    f = [None]*(n+1)
    coefs = [None]*(n+1)
    interval = int(T/n)
    slack = int(interval/2.5)

    d[1] = random.randint(1, interval)
    
    for i in range(1, n):
        if i > 1:
            d[i] = random.randint(d[i-1] + slack, int(min(d[i-1] + interval + slack, T - interval)))
        r[i] = random.randint(r[i-1], d[i]-d[i-1]+r[i-1]-1)
        if r[i] == d[i]:
            r[i] = 0
        c[i] = random.randint(interval+slack, 2*interval)
        coefs[i], f[i] = generate_function(c[i]+1, fun)
    
    d[n] = T
    r[n] = T
    c[n] = T - d[n-1] + 1
    coefs[n], f[n] = generate_function(c[n]+1, fun)

    return d, r, c, f, coefs



def generate_function(c, fun):
    f = [None]*c
    coefs = np.random.randint(0, high=15, size=3)
    
    for i in range(c):
        #simple convex 2nd order polynomail is used
        if(fun == 'polynomail'):
            f[i] = coefs[0]*(i**2) + coefs[1]*i + coefs[2]

        #random non-decreasing convex function
        if(fun == 'random'):
            low = coefs[0] if i < 2 else f[i-1]-f[i-2]
            f[i] = 1 if i==0 else random.randint(f[i-1]+low, f[i-1]+low+10)
    
    return coefs.tolist(), f

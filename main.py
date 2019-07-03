import numpy as np
import math

def prime_relax(l, h, g, c, d, r):
    n = h - l + 1
    T = d - r
    delta = math.ceil(T/(2.0*n))
    t = np.zeros(n, dtype=int)

    while delta > 1:
        h = np.ones(n, dtype=int)
        t = greedy_alloc(delta, t, T, g, c)
        t = t - h*delta
        t *= (t>0)
        delta = math.ceil(delta/2.0)

    t = greedy_alloc(1, t, T, g, c)
    return t

def greedy_alloc(delta, t, T, g, c):
    n = np.size(c)
    D = T - np.sum(t)
    H = set(range(n))

    while D>0 and len(H) > 0 :
        
        #find min task
        min_i = 0
        min_val = np.iinfo(min_i).max
        for i in H:
            val = g[i][t[i]+1] - g[i][t[i]]
            if val < min_val:
                min_val = val
                min_i = i
        
        if t[min_i] + 1 > c[min_i]:
            H = H - {min_i}
        elif t[min_i] + delta > c[min_i] or delta > D:
            delta_prime = min(D, c[min_i]- t[min_i])
            t[min_i] += delta_prime
            D -= delta_prime
            H = H - {min_i}
        else:
            t[min_i] += delta
            D -= delta
    
    if delta > 1 or D == 0:
        return t
    else: 
        print("Failure!!!!")
        return np.ones(n) * -1

def naive_prime_relax(l, h, g, c, d, r):
    n = h - l + 1
    t = np.zeros(n, dtype=int)
    T = d - r
    t = greedy_alloc(1, t, T, g, c)
    return t

def generate_funs_and_bounds(n, d, r):
    c = np.random.randint(1, high=d-r, size=n)
    g = [None]*n
    
    for i in range(n):
        g[i] = generate_convex_lut(c[i]+3)
    
    return g, c


def generate_convex_lut(size):
    f = np.zeros(size, dtype=int)
    coefs = np.random.randint(0, high=size, size=3)
    
    for i in range(size):
        #simple convex 2nd order polynomail is used
        f[i] = coefs[0]*(i**2) + coefs[1]*i + coefs[2]

        #1/x 
        #f[i] = math.ceil((coefs[0]+size)/(i+1))

        #random non-decreasing convex function
        # low = 1 if i < 2 else math.ceil(f[i-1]**2/f[i-2])
        # f[i] = np.random.randint(low, high=low*2, size=1)[0]
    
    return f

def get_value(t, g):
    s = 0
    for i in range(len(t)):
        s += g[i][t[i]]
    return s

def test(n, d, r):
    g, c = generate_funs_and_bounds(n, d, r)

    t_fast = prime_relax(1, n, g, c, d, r)
    t_naive = naive_prime_relax(1, n, g, c, d, r)

    val_fast = get_value(t_fast, g)
    val_naive = get_value(t_naive, g)

    if np.array_equal(t_naive, t_fast) or val_fast == val_naive:
        print("They are equal!")
    else:
        print("Test failed!")
        print(n, d, r)
        print(c)
        for i in range(n):
            print(g[i])
        print(t_fast)
        print(t_naive)
        print(val_fast)
        print(val_naive)


test(11, 20, 2)
test(13, 40, 1)
test(7, 20, 5)
test(14, 15, 4)
test(25, 30, 3)
test(57, 42, 1)
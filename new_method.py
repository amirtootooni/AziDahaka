import numpy as np
from heapq import heappush, heappop
import math

def primal(l, h, f, c, d, r):
    if(l==h):
        t = np.zeros(1, dtype=int)
        t[0] = d[l] - r[l-1]
        return t
    elif h-l >= 1:
        t = primal_relax(l, h, f, c, d, r)
        max_violation = 0
        m = 0
        t_sum = 0
        upper_violation = False

        for i in range(l, h+1):
            t_sum += t[i-l]
            ub = t_sum-d[i]+r[l-1]
            lb = r[i]-r[l-1]-t_sum
            val = max(ub, lb)
            if (val >= max_violation):
                max_violation = val
                m = i
                upper_violation = ub >= lb

        if max_violation == 0:
            return t
        elif upper_violation:
            r[m] = d[m]
        else:
            d[m] = r[m]

        t_lh = primal(l, m, f, c, d, r)
        t_uh = primal(m+1, h, f, c, d, r)
        return np.concatenate((t_lh, t_uh),axis=0)
    else: 
       raise ValueError('l greater than h')

##
# l, h are the lower and higher indexes between 1 and n
# f, c, d, r are arrays of all the problem parameters of size n+1 (from 1 to n)
# r[0], d[0], c[0] = 0 as they are not used in the problem
##
def primal_relax(l, h, f, c, d, r):
    n = h - l + 1
    T = d[h] - r[l-1]
    delta = int(math.ceil(T/(2.0*n)))
    t = np.zeros(n, dtype=int) #note that t will have an l offset
    v = np.ones(n, dtype=int)

    while delta > 1:
        t = greedy_alloc(delta, t, T, f, c, l, h)
        t = t - v*delta
        t *= (t>0) #equivalent to t = max{t-delta, 0}
        delta = int(math.ceil(delta/2.0))

    t = greedy_alloc(1, t, T, f, c, l, h)
    return t

def greedy_alloc(delta, t, T, f, c, l, h):
    D = T - np.sum(t)
    H = []

    # create heap of all h_i(t_i)
    for i in range(l, h+1):
        if(t[i-l] < c[i]):
            heappush(H, (f[i][t[i-l]+1] - f[i][t[i-l]], i))

    while D>0 and len(H) > 0 :
        
        # find min task
        min_i = heappop(H)[1]
        
        if t[min_i-l] + delta > c[min_i] or delta > D:
            delta_prime = min(D, c[min_i]- t[min_i-l])
            t[min_i-l] += delta_prime
            D -= delta_prime
        else:
            t[min_i-l] += delta
            D -= delta
            if(t[min_i-l] < c[min_i]):
                heappush(H, (f[min_i][t[min_i-l]+1] - f[min_i][t[min_i-l]], min_i))
    
    if D == 0:
        return t
    else: 
        raise ValueError('Problem infeasible')
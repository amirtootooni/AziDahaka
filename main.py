from dataset_generation import generate_bounds
from new_method import primal 
from general_solver import gurobi_solve
import numpy as np
import time
import os
import re

def test(n, T, fun='polynomail'):
    d, r, c, f = generate_bounds(n, T, fun=fun)

    ex_new = time.time()
    t = primal(1, n, f, c, d, r)
    ex_new = time.time() - ex_new

    print('t = ', t)

    obj_new = show_details(n, t, d, r, c, f, T)

    ex_general, obj_general = gurobi_solve(n, f, c, d, r)

    print('---------------------------------------')
    print('execution time of new method: ', ex_new)
    print('objective of new method: ', obj_new)
    print('execution time of gurobi: ', ex_general)
    print('objective of gurobi: ', obj_general)

def show_details(n, t, d, r, c, f, T, detailed=False):
    correct = True
    sumT = 0
    sumObj = 0

    if detailed:
        print('t = ', t)
        print('d = ', d)
        print('c = ', c)
        print('r = ', r)

    for i in  range(1, n+1):
        sumT += t[i-1]
        sumObj += f[i][t[i-1]]

        if detailed:
            print('0<=t_', i,'<=', c[i], ' t=', t[i-1], ' ', t[i-1] <= c[i] and t[i-1] >= 0)
            print(r[i], '<=t_1:', i,'<=', d[i], ' sum=', sumT, ' ', sumT >= r[i] and sumT <= d[i])
        
        correct = correct if sumT >= r[i] and sumT <= d[i] and t[i-1] <= c[i] and t[i-1] >= 0 else False

    if(sumT == T and correct):
        print('Solved correctly with objective = ', sumObj)
    else:
        print('incorrect solution')
    
    return sumObj


def save_datasets():
    while (input('What to continue? y/n ') == 'y'):
        n = int(input('What n? '))
        T = int(input('What T? '))
        fun = 'random' if input('What function? r/p ')== 'r' else 'polynomail'

        try:
            d, r, c, f = generate_bounds(n, T, fun=fun)
            ex, obj = gurobi_solve(n, f, c, d, r)
        except:
            print('Got an exception')
            continue
        
        print('execution time of gurobi: ', ex)
        print('objective of gurobi: ', obj)
        print('-------------------------------')

        if(input('Do you want to save this example? y/n ') == 'y'):
            base_path = 'data/n_' + str(n) + '_T_' + str(T) + '/'

            if not os.path.exists(base_path):
                os.makedirs(base_path)

            np_f = np.asarray(f)
            np.save(base_path + 'f.npy', np_f)
            np.save(base_path + 'c.npy', c)
            np.save(base_path + 'r.npy', r)
            np.save(base_path + 'd.npy', d)

def save_results():
    files = [x[0] for x in os.walk('data/')]
    
    for i in range(1, len(files)):
        base_path = files[i]
        n = int(re.search('n_(.*)_T', files[i]).group(1))
        T = int(re.search('T_(.*)', files[i]).group(1))

        f = np.load(base_path + '/f.npy').tolist()
        c = np.load(base_path + '/c.npy')
        r = np.load(base_path + '/r.npy')
        d = np.load(base_path + '/d.npy')
        result = np.zeros((2,20))

        for j in range(40):
            if j < 20:
                ex_new = time.time()
                primal(1, n, f, c, d, r)
                ex_new = time.time() - ex_new
                result[0][j] = ex_new
            else:
                ex, _ = gurobi_solve(n, f, c, d, r)
                result[1][j-20] = ex_new
        
        np.save('results/n_' + str(n) + '_T_' + str(T) +'.npy', result)


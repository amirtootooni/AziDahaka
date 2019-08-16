from dataset_generation import generate_bounds
from new_method import primal 
from general_solver import gurobi_solve_lut, gurobi_solve_poly
import numpy as np
import time
import os
import re
import matplotlib
import matplotlib.pyplot as plt

def test(n, T, fun='polynomail'):
    d, r, c, f, coefs = generate_bounds(n, T, fun=fun)

    ex_new = time.time()
    t = primal(1, n, f, c, d, r)
    ex_new = time.time() - ex_new

    print('t = ', t)

    obj_new = show_details(n, t, d, r, c, f, T)

    ex_general, obj_general = gurobi_solve_poly(n, coefs, c, d, r)

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

def generate_plots(func= 'polynomail'):
    ns = [50, 100, 200, 500, 1000, 2000]
    Ts = [100000]
    breaks = 0
    exceptions = 0
    for T in Ts:
        means_new = []
        stds_new = []
        means_gen = []
        stds_gen = []
        lables = []
        for n in ns:
            if T/n < 10:
                continue
            
            try:
                d, r, c, f, coefs = generate_bounds(n, T, fun=func)
                obj_new = primal(1, n, f, c, d, r)
            except:
                continue

            iterations = 20 # if n < 5000 and T < 20000 else 2
            results = np.zeros((2, iterations))
            for i in range(iterations):
                ex = time.time()
                primal(1, n, f, c, d, r)
                results[0][i] = time.time() - ex
                results[1][i], _ = gurobi_solve_poly(n, coefs, c, d, r)

            lables.append('n='+ str(n))
            means_new.append(round(results[0, :].mean(), 4))
            stds_new.append(results[0, :].std())
            means_gen.append(round(results[1, :].mean(), 4))
            stds_gen.append(results[1, :].std())
            
        ind = np.arange(len(lables))  # the x locations for the groups
        width = 0.30  # the width of the bars

        fig, ax = plt.subplots(figsize=(len(lables), 12))
        rects1 = ax.bar(ind - width/2, means_new, width, yerr=stds_new, label='Our Method')
        rects2 = ax.bar(ind + width/2, means_gen, width, yerr=stds_gen, label='Gurobi Solver with explicit polynomials')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Execution times (s)')
        ax.set_title('Performance comparison for T = ' + str(T) + ' and different n for quadratic objectives')
        ax.set_xticks(ind)
        ax.set_xticklabels(lables)
        ax.legend()

        autolabel(ax, rects1, "left")
        autolabel(ax, rects2, "right")
        fig.tight_layout()
        plt.show()

    print('Number of times the objectives were not equal: ', breaks)

        

def autolabel(ax, rects, xpos='center'):
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}
    
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')

def showSpeedUp():
    ns = [10, 50, 100, 200, 500, 1000, 2000, 5000, 8000, 10000]
    Ts = [50, 100, 200, 500, 1000, 2000, 5000, 8000, 10000, 20000, 50000, 100000]
    results = [None]
    for n in ns:
        for T in Ts:
            if T/n < 5:
                continue
            problemSU = np.zeros(10)
            problem = 0
            while problem < 10:
                d, r, c, f, coefs = None
                try:
                    d, r, c, f, coefs = generate_bounds(n, T, fun='random')
                    primal(1, n, f, c, d, r)
                    problem = problem + 1
                except:
                    continue
                trailSU = np.zeros(10)
                for trial in range(10):
                    ex1 = time.time()
                    primal(1, n, f, c, d, r)
                    ex1 = time.time() - ex1
                    # ex2, _ = gurobi_solve_poly(n, coefs, c, d, r)
                    ex2, _ = gurobi_solve_poly(n, f, c, d, r)
                    trailSU[trial] = ex2 * 1.0 / ex1

                problemSU[problem] = np.mean(trailSU)

            result = 'T = ' + str(T) + ', n = ' + str(n) + ' speedup = ' + str(np.mean(problemSU))
            results.append(result)
    
    print(results)




# test(10, 2000, fun='polynomail')
# generate_plots(func='polynomail')

# useless functions:

# def save_datasets():
#     while (input('What to continue? y/n ') == 'y'):
#         n = int(input('What n? '))
#         T = int(input('What T? '))
#         fun = 'random' if input('What function? r/p ')== 'r' else 'polynomail'

#         try:
#             d, r, c, f = generate_bounds(n, T, fun=fun)
#             ex, obj = gurobi_solve(n, f, c, d, r)
#         except:
#             print('Got an exception')
#             continue
        
#         print('execution time of gurobi: ', ex)
#         print('objective of gurobi: ', obj)
#         print('-------------------------------')

#         if(input('Do you want to save this example? y/n ') == 'y'):
#             base_path = 'data/n_' + str(n) + '_T_' + str(T) + '/'

#             if not os.path.exists(base_path):
#                 os.makedirs(base_path)

#             np_f = np.asarray(f)
#             np.save(base_path + 'f.npy', np_f)
#             np.save(base_path + 'c.npy', c)
#             np.save(base_path + 'r.npy', r)
#             np.save(base_path + 'd.npy', d)

# def save_results():
#     files = [x[0] for x in os.walk('data/')]
    
#     for i in range(1, len(files)):
#         base_path = files[i]
#         n = int(re.search('n_(.*)_T', files[i]).group(1))
#         T = int(re.search('T_(.*)', files[i]).group(1))

#         f = np.load(base_path + '/f.npy').tolist()
#         c = np.load(base_path + '/c.npy')
#         r = np.load(base_path + '/r.npy')
#         d = np.load(base_path + '/d.npy')
#         result = np.zeros((2,20))

#         for j in range(40):
#             if j < 20:
#                 ex_new = time.time()
#                 primal(1, n, f, c, d, r)
#                 ex_new = time.time() - ex_new
#                 result[0][j] = ex_new
#             else:
#                 ex, _ = gurobi_solve(n, f, c, d, r)
#                 result[1][j-20] = ex_new
        
#         np.save('results/n_' + str(n) + '_T_' + str(T) +'.npy', result)

for i in range(1,10):
    d, r, c, f, coefs = generate_bounds(50, 200, fun='random')
    print(f)
    try:
        t = primal(1, 50, f, c, d, r)
        s = 0
        for i in range(50):
            s += t[i]
        print(t)
        print(s)
    except:
        print("infeasible")
from gurobipy import *
from math import exp
import time

def gurobi_solve(n, f, c, d, r):
    try:
        m = Model()

        t = [None]*n
        for i in range(1, n+1):
            t[i-1] = m.addVar(lb=0, ub=c[i], obj=0, vtype=GRB.INTEGER, name='t_' + str(i))
        
        expr = LinExpr(1*t[0])
        for i in range(1, n):
            m.addConstr(lhs=expr, sense=GRB.GREATER_EQUAL, rhs=r[i], name='clb_'+str(i))
            m.addConstr(lhs=expr, sense=GRB.LESS_EQUAL, rhs=d[i], name='cub_'+str(i))
            expr.add(1*t[i])
        
        m.addConstr(lhs=expr, sense=GRB.EQUAL, rhs=d[n], name='c_n')

        for i in range(1, n+1):
            m.setPWLObj(t[i-1], list(range(len(f[i]))), f[i])

        # timer here
        ex = time.time()
        m.optimize()
        ex = time.time() - ex

        return ex, m.ObjVal

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')
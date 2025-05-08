from enum import Enum
import matplotlib.pyplot as plt
from .lpStateVar import LPStateVar

class Solver(Enum):
    GUROBI=0
    SCIPY=1
    CPLEX=2

class Obj(Enum):
    MINIMIZE=0
    MAXIMIZE=1

def plot_sum(var1:LPStateVar,var2:LPStateVar,name=''):
    '''Plots the difference between the optimized time series of two stateVars'''
    if var1.result is None or var2.result is None:
        print('The optimization must be performed first')
        return
    summe = var1.result - var2.result
    plt.plot(summe)
    plt.title(name)
    plt.ylabel(var1.unit)
    plt.xlabel('steps')
    plt.show()
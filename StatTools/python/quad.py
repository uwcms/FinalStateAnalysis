'''
Function to sum in quadrature, avoid replication everywhere
'''
import math

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

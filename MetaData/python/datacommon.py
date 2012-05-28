'''

Common definitions and helpers used by the dataset definitions.

Author: Evan K. Friis, UW Madison

'''

import math

# Conversions to pico barns
millibarns = 1.0e+9
microbarns = 1.0e+6
nanobarns  = 1.0e+3
picobarns =  1.0
femtobarns = 1.0e-3

# Branching ratios
br_w_leptons =  0.1075+0.1057+0.1125

def square(x):
    return x*x

def cube(x):
    return x*x*x

def quad(*xs):
    # Add stuff in quadrature
    return math.sqrt(sum(x*x for x in xs))

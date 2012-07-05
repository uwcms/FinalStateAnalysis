'''

RooFunctorFromWS

Builds a functor from a function in a RooWorkspace.

This could be improved with cython.

Author: Evan K. Friis, UW Madison

>>> import ROOT
>>> file = ROOT.TFile('../test/test_RooFunctorFromWS.root')
>>> ws = file.Get('fit_efficiency')
>>> functor = RooFunctorFromWS(ws, 'efficiency')
>>> '%0.2f' % functor(120)
'0.02'

'''

import ROOT

class RooFunctorFromWS(ROOT.RooFunctor):
    def __init__(self, workspace, functionname, var='x'):
        # Get the RooFormulaVar
        self.function = workspace.function(functionname)
        # Get the ind. var and the parameters
        self.x = workspace.var(var)
        #parameters = workspace.allVars()
        #parameters.remove(x)
        #parameters.Print('v')
        #self.functor = self.function.functor(ROOT.RooArgList(x), ROOT.RooArgList(parameters))

    def __call__(self, x):
        self.x = x
        return self.function.getVal()

def build_roofunctor(filename, wsname, functionname, var='x'):
    ''' Build a functor from a filename '''
    file = ROOT.TFile.Open(filename)
    ws = file.Get(wsname)
    return RooFunctorFromWS(ws, functionname, var)

if __name__ == "__main__":
    import doctest; doctest.testmod()

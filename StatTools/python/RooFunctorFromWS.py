'''

RooFunctorFromWS

Builds a functor from a function in a RooWorkspace.

This could be improved with cython.

Author: Evan K. Friis, UW Madison

>>> import ROOT
>>> file = ROOT.TFile('../test/test_RooFunctorFromWS.root')
>>> ws = file.Get('fit_efficiency')
>>> functor = RooFunctorFromWS(ws, 'efficiency')
>>> '%0.4f' % functor(60)
'0.0244'
>>> '%0.4f' % functor(140)
'0.0138'

'''

import ROOT

class RooFunctorFromWS(ROOT.RooFunctor):
    def __init__(self, workspace, functionname, var='x'):
        # Get the RooFormulaVar
        self.function = workspace.function(functionname)
        # Get the ind. var and the parameters
        #self.x = workspace.var(var)
        self.x = self.function.getParameter(var)
        self.x.setRange(0, 1e99)

    def __call__(self, x):
        self.x.setVal(x)
        return self.function.getVal()

def build_roofunctor(filename, wsname, functionname, var='x'):
    ''' Build a functor from a filename '''
    file = ROOT.TFile.Open(filename)
    if not file:
        raise IOError("Can't open file: %s" % filename)
    ws = file.Get(wsname)
    return RooFunctorFromWS(ws, functionname, var)

def make_corrector_from_th2(filename, path):
    tfile = ROOT.TFile.Open(filename)
    if not tfile:
        raise IOError("Can't open file: %s" % filename)
    hist  = tfile.Get(path).Clone()
    #print hist
    binsx = hist.GetNbinsX()
    binsy = hist.GetNbinsY()
    def refFun(xval,yval):
        #print hist
        xbin = hist.GetXaxis().FindBin(xval)
        xbin = (xbin if xbin <= binsx else binsx ) if xbin >= 1 else 1 #Compute underflow and overflow as first and last bin
        ybin = hist.GetYaxis().FindBin(yval)
        ybin = (ybin if ybin <= binsy else binsy ) if ybin >= 1 else 1 #Compute underflow and overflow as first and last bin
        prob = hist.GetBinContent(xbin,ybin)
        try:
            return prob 
        except ZeroDivisionError:
            raise ZeroDivisionError(" catched trying to return weight for (%.3f,%.3f) ==> (%i,%i) bin out of (%i,%i). Prob: %.3f. Hist: %s : %s. " % (xval, yval, xbin, ybin, binsx, binsy , prob, filename, path))
    return refFun


if __name__ == "__main__":
    import doctest; doctest.testmod()

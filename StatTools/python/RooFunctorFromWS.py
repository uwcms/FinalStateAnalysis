'''

RooFunctorFromWS

Builds a functor from a function in a RooWorkspace.

This could be improved with cython.

Author: Evan K. Friis, UW Madison

>>> from FinalStateAnalysis.Utilities.rootbindings import ROOT
>>> file = ROOT.TFile('../test/test_RooFunctorFromWS.root')
>>> ws = file.Get('fit_efficiency')
>>> functor = RooFunctorFromWS(ws, 'efficiency')
>>> '%0.4f' % functor(60)
'0.0244'
>>> '%0.4f' % functor(140)
'0.0138'

'''

from FinalStateAnalysis.Utilities.rootbindings import ROOT
import array
from FinalStateAnalysis.PlotTools.decorators import memo_last

#ROOT.gSystem.Load("libFinalStateAnalysisStatTools")

TMVA_tools = ROOT.TMVA.Tools.Instance()

class RooFunctorFromWS(ROOT.RooFunctor):
    def __init__(self, workspace, functionname, var='x'):
        # Get the RooFormulaVar
        self.function = workspace.function(functionname)
        # Get the ind. var and the parameters
        #self.x = workspace.var(var)
        self.x = self.function.getParameter(var) if hasattr(self.function, 'getParameter') else self.function.getVariables().find(var)
        self.x.setRange(0, 1e99)

    def __call__(self, x):
        self.x.setVal(x)
        return self.function.getVal()

class FunctorFromMVA(object):
    def __init__(self, name, xml_filename, *variables, **kwargs):
        self.reader    = ROOT.TMVA.Reader( "!Color:Silent=%s:Verbose=%s" % (kwargs.get('silent','T'), kwargs.get('verbose','F')))
        self.var_map   = {}
        self.name      = name
        self.variables = variables
        self.xml_filename = xml_filename
        for var in variables:
            self.var_map[var] = array.array('f',[0]) 
            self.reader.AddVariable(var, self.var_map[var])
        self.reader.BookMVA(name, xml_filename)

    def evaluate_(self): #so I can profile the time needed
        return self.reader.EvaluateMVA(self.name)

    @memo_last
    def __call__(self, **kvars):
        #kvars enforces that we use the proper vars
        if not ( 
                 all(name in self.variables for name in kvars.keys()) and \
                 all(name in kvars.keys() for name in self.variables)
                ):
            raise Exception("Wrong variable names. Available variables: %s" % self.variables.__repr__())
        for name, val in kvars.iteritems():
            self.var_map[name][0] = val
        retval = self.evaluate_() #reader.EvaluateMVA(self.name)
        if retval == 1:
            print "returning 1 in %s, kvars: %s" % (self.xml_filename, kvars.items()) 
        return retval

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
        xbin = hist.GetXaxis().FindFixBin(xval) #Faster than FindBin
        xbin = (xbin if xbin <= binsx else binsx ) if xbin >= 1 else 1 #Compute underflow and overflow as first and last bin
        ybin = hist.GetYaxis().FindFixBin(yval)
        ybin = (ybin if ybin <= binsy else binsy ) if ybin >= 1 else 1 #Compute underflow and overflow as first and last bin
        prob = hist.GetBinContent(xbin,ybin)
        if prob:
            return prob
        else:
            return 10**-8
           # raise ZeroDivisionError(" catched trying to return weight for (%.3f,%.3f) ==> (%i,%i) bin out of (%i,%i). Prob: %.3f. Hist: %s : %s. " % (xval, yval, xbin, ybin, binsx, binsy , prob, filename, path))
    return refFun

def build_uncorr_2Droofunctor(functor_x, functor_y, filename, num='numerator', den='denominator'):
    ''' Build a functor from a filename '''
    file = ROOT.TFile.Open(filename)
    num_int = file.Get(num).Integral()
    den_int = file.Get(den).Integral()
    scale   = num_int/den_int
    def _f(x, y):
        print scale
        return functor_x(x)*functor_y(y)/scale
    return _f



if __name__ == "__main__":
    import doctest; doctest.testmod()

'''

Wrapper around the th1fmorph library.

Inspired by code by R. Wolf, C. Veelken & J. Swanson

Author: Evan K. Friis, UW Madison

'''

from FinalStateAnalysis.Utilities.rootbindings import ROOT
# Load the library with th1fmorph
#ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so')
from ROOT import th1fmorph

def interpolate(x1, y1, x2, y2, x):
    ''' Linearly interpolate the y value for <x> between two 2D points

    The two 2D points are described by <x1>, <y1> and <x2>, <y2>
    >>> interpolate(1, 1, 3, 3, 2)
    2.0
    '''
    # If the two x-values are the same, average the two values
    if (x2 == x1):
        return 0.5*(y1 + y2)
    intercept = (y2 - y1)*1./(x2 - x1)
    return y1 + intercept*(x - x1)


def morph(name, title, x, hist1, x1, hist2, x2):
    '''
    Given to histograms, <hist1> and <hist2>, which correspond to the parameters
    <x1> and <x2>, return a TH1 with the given name and title, morphed to
    correspond to parameter <x>.

    The total yield for the target histogram is interpolated between the two
    base histograms.
    '''

    yield1 = hist1.Integral()
    yield2 = hist2.Integral()

    interp_yield = interpolate(x1, yield1, x2, yield2, x)

    return th1fmorph(name, title, hist1, hist2, x1, x2, x, interp_yield, 0)

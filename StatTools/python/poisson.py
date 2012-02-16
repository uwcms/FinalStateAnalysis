'''

Convert a TH1 histogram into a TGraphAsymmErrors, with the proper poisson
statistics.

These use the Neyman construction, instead of simply sqrt(N).

Code taken from:
    https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars

'''

import ROOT

def convert(histogram):
    ''' Convert a histogram into a TGraphAsymmErrors with Poisson errors '''
    output = ROOT.TGraphAsymmErrors(histogram)

    for i in xrange(output.GetN()):
        yield_in_bin = output.GetY()[i]
        N = ROOT.TMath.Nint(yield_in_bin)
        if abs(yield_in_bin - N) < 1e-4:
            raise ValueError("Bin %i has non-integer value %0.5f" % yield_in_bin)

        alpha = 1.0-0.6827
        L, U = 0, 0
        if N > 0:
            L = ROOT.Math.gamma_quantile(alpha/2, N, 1.)

        if N == 0:
            U =  ROOT.Math.gamma_quantile_c(alpha,N+1,1)
        else:
            U = ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)

        output.SetPointEYlow(i, N - L)
        output.SetPointEYhigh(i, U - N)

    return output

'''

Convert a TH1 histogram into a TGraphAsymmErrors, with the proper poisson
statistics.

These use the Neyman construction, instead of simply sqrt(N).

Code taken from:
    https://twiki.cern.ch/twiki/bin/view/CMS/PoissonErrorBars



   double gamma_quantile_c(double z, double alpha, double theta) {

      return theta * ROOT::Math::Cephes::igami( alpha, z);

   }

   double gamma_quantile(double z, double alpha, double theta) {
      // if possible, should use MathMore function ROOT::Math::gamma_quantile for z close to zero
      // otherwise will always return zero for z  value smaller than eps
      return theta * ROOT::Math::Cephes::igami( alpha, 1.- z);
   }


Command line usage:

   python poisson.py N

prints the upper and lower confidence interval to stdout.

'''
import sys
import ROOT

def poisson_errors(N, coverage=0.6827):
    alpha = 1.0-coverage
    L, U = 0, 0
    if N > 0:
        # WORKAROUND (see above)
        #L = ROOT.Math.gamma_quantile(alpha/2, N, 1.)
        L = ROOT.Math.gamma_quantile_c((1. - alpha/2), N, 1.)
    if N == 0:
        U =  ROOT.Math.gamma_quantile_c(alpha,N+1,1)
    else:
        U = ROOT.Math.gamma_quantile_c(alpha/2,N+1,1)
    return L, U


def convert(histogram, x_err=True, set_zero_bins=None, is_scaled=False):
    ''' Convert a histogram into a TGraphAsymmErrors with Poisson errors '''
    output = ROOT.TGraphAsymmErrors(histogram)

    for i in xrange(output.GetN()):
        multiplier = 1.
        if is_scaled:
            multiplier = output.GetErrorXhigh(i) + output.GetErrorXlow(i)
        yield_in_bin = output.GetY()[i] * multiplier
        N = ROOT.TMath.Nint(yield_in_bin)
        if abs(yield_in_bin - N) > 1e-4:
            raise ValueError("Bin %i has non-integer value %0.5f" %
                             (i, yield_in_bin))

        if set_zero_bins is not None and N == 0:
            output.SetPoint(i, output.GetX()[i], set_zero_bins)
            output.SetPointEYhigh(i, 0)
            output.SetPointEYlow(i, 0)

        alpha = 1.0-0.6827
        L, U = poisson_errors(N)

        output.SetPointEYlow( i, (N - L) / multiplier )
        output.SetPointEYhigh(i, (U - N) / multiplier )
        if not x_err:
            output.SetPointEXlow(i, 0)
            output.SetPointEXhigh(i, 0)

    return output

if __name__ == "__main__":
    arg = sys.argv[-1]
    print poisson_errors(int(arg))

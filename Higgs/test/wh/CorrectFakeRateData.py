'''

Subtract expected WZ and ZZ contamination from FR numerator and denominators.

Author: Evan K. Frii

'''

from RecoLuminosity.LumiDB import argparse
import fnmatch
import logging
import glob
import os
import sys

log = logging.getLogger("CorrectFakeRateData")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+')
    parser.add_argument('--lumifiles', nargs='+')
    parser.add_argument('--outputfile', required=True)
    parser.add_argument('--denom', required=True, help='Path to denom')
    parser.add_argument('--numerator', required=True, help='Path to numerator')
    parser.add_argument('--rebin', type=int, default=1)

    args = parser.parse_args()

    from rootpy import io
    import rootpy.plotting.views as views
    import rootpy.plotting as plotting
    from FinalStateAnalysis.MetaData.data_views import data_views

    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    files = []
    for pattern in args.files:
        files.extend(glob.glob(pattern))

    log.info("Loading data from %i files", len(files))

    lumifiles = []
    for pattern in args.lumifiles:
        lumifiles.extend(glob.glob(pattern))

    the_views = data_views(files, lumifiles)

    outputdir = os.path.dirname(args.outputfile)
    if outputdir and not os.path.exists(outputdir):
        os.makedirs(outputdir)

    log.info("Rebinning with factor %i", args.rebin)
    def rebin_view(x, rebin):
        ''' Make a view which rebins histograms '''
        if rebin > 1:
            rebinner = lambda x: x.Rebin(rebin)
            output = views.FunctorView(x, rebinner)
            return output
        else:
            return x

    def all_bins_positive(x):
        ''' Set all bins to be > 0 '''
        for i in range(1, x.GetNbinsX()+1):
            if x.GetBinContent(i) < 0:
                x.SetBinContent(i, 0)
        return x

    def postive_view(x):
        ''' Make a view where all bins > 0 '''
        return views.FunctorView(x, all_bins_positive)

    def get_view(sample_pattern):
        for sample, sample_info in the_views.iteritems():
            if fnmatch.fnmatch(sample, sample_pattern):
                return rebin_view(sample_info['view'], args.rebin)
        raise KeyError("I can't find a view that matches %s, I have: %s" % (
            sample_pattern, " ".join(the_views.keys())))

    wz_view = get_view('WZ*')
    zz_view = get_view('ZZ*')
    data = rebin_view(the_views['data']['view'], args.rebin)

    diboson_view = views.SumView(wz_view, zz_view)
    inverted_diboson_view = views.ScaleView(diboson_view, -1)
    corrected_view = postive_view(views.SumView(data, inverted_diboson_view))

    output = io.open(args.outputfile, 'RECREATE')
    output.cd()

    corr_numerator = corrected_view.Get(args.numerator)
    corr_denominator = corrected_view.Get(args.denom)

    log.info("Corrected:   %0.2f/%0.2f = %0.1f%%",
             corr_numerator.Integral(),
             corr_denominator.Integral(),
             100*corr_numerator.Integral()/corr_denominator.Integral()
             if corr_denominator.Integral() else 0
            )

    uncorr_numerator = data.Get(args.numerator)
    uncorr_denominator = data.Get(args.denom)

    log.info("Uncorrected: %0.2f/%0.2f = %0.1f%%",
             uncorr_numerator.Integral(),
             uncorr_denominator.Integral(),
             100*uncorr_numerator.Integral()/uncorr_denominator.Integral()
             if uncorr_denominator.Integral() else 0
            )

    corr_numerator.SetName('numerator')
    corr_denominator.SetName('denominator')

    uncorr_numerator.SetName('numerator_uncorr')
    uncorr_denominator.SetName('denominator_uncorr')

    corr_numerator.Write()
    corr_denominator.Write()
    uncorr_numerator.Write()
    uncorr_denominator.Write()

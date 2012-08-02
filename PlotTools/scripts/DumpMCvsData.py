#!/usr/bin/env python
'''

Walk a ROOT file directory structure, and compare MC and DATA in all
distributions.

Author: Evan K. Friis, UW

'''

from RecoLuminosity.LumiDB import argparse
import fnmatch
import glob
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+')
    parser.add_argument('--lumifiles', nargs='+')
    parser.add_argument('--outputdir', required=True)
    parser.add_argument('--rebin', type=int, default=1)
    parser.add_argument('--mc-samples', dest='mclist', nargs='+',
                        default=[
                            'Zjets_M50',
                            'WplusJets_madgraph',
                            'TTplusJets_madgraph',
                            'WZJetsTo3LNu*',
                            'ZZJetsTo4L*',
                        ])

    args = parser.parse_args()

    from rootpy import io
    import rootpy.plotting.views as views
    import rootpy.plotting as plotting
    from FinalStateAnalysis.MetaData.data_views import data_views

    files = []
    for pattern in args.files:
        files.extend(glob.glob(pattern))

    lumifiles = []
    for pattern in args.lumifiles:
        lumifiles.extend(glob.glob(pattern))

    the_views = data_views(files, lumifiles)

    outputdir = args.outputdir

    if outputdir and not os.path.exists(outputdir):
        os.makedirs(outputdir)

    def rebin_view(x, rebin):
        ''' Make a view which rebins histograms '''
        if rebin > 1:
            rebinner = lambda x: x.Rebin(rebin)
            output = views.FunctorView(x, rebinner)
            return output
        else:
            return x

    def get_view(sample_pattern):
        for sample, sample_info in the_views.iteritems():
            if fnmatch.fnmatch(sample, sample_pattern):
                return rebin_view(sample_info['view'], args.rebin)
        raise KeyError("I can't find a view that matches %s, I have: %s" % (
            sample_pattern, " ".join(the_views.keys())))

    # Build data and MC views
    mc_stack = views.StackView(*[get_view(x) for x in args.mclist])
    data = rebin_view(the_views['data']['view'], args.rebin)

    canvas = plotting.Canvas(name='adsf', title='asdf')
    keep = []

    def save(name):
        canvas.SetLogy(False)
        canvas.SaveAs(os.path.join(outputdir, name) + '.png')
        canvas.SetLogy(True)
        canvas.SaveAs(os.path.join(outputdir, name) + '_log.png')
        keep = []

    # Walk the histogram layout
    for path, subdirs, histos in io.open(files[0]).walk(class_pattern='TH1F'):
        for histo in histos:
            full_path = os.path.join(path, histo)
            clean_path = full_path.replace('/', '-')
            mc_hist = mc_stack.Get(full_path)
            data_hist = data.Get(full_path)

            mc_hist.Draw()
            data_hist.Draw('same')
            mc_hist.SetMaximum(2*mc_hist.GetMaximum())
            # Make sure we can see everything
            #if data_hist.GetMaximum() > mc_hist.GetHistogram().GetMaximum():
                #mc_hist.SetMaximum(2*data_hist.GetMaximum())
            keep.append( (mc_hist, data_hist) )
            save(clean_path)


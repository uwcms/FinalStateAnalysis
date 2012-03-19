#!/usr/bin/env python
'''

Fit the fake measured fake rates an write out a RooWorkspace

Author: Evan K. Friis, UW

'''


from RecoLuminosity.LumiDB import argparse
from FinalStateAnalysis.PatTools.data_views import get_views
import glob
import json
import logging
import os
import pdb
from rootpy.plotting import views
import rootpy.io as io
import sys

# Steal the args so ROOT doesn't mess them up!
parser = argparse.ArgumentParser()
args = sys.argv[:]
sys.argv = []

import ROOT

if __name__ == "__main__":
    log = logging.getLogger("fit_fakerates")
    logging.basicConfig(level=logging.DEBUG)

    parser.add_argument('meta', help='File with meta information')

    parser.add_argument('cfg', help='Configuration python file')

    parser.add_argument('fit_models', help='Fit models file')

    parser.add_argument('output', help='Output workspace file')

    parser.add_argument('files', metavar='file', nargs='+',
                        help = 'Histogram files')

    args = parser.parse_args(args[1:])

    meta_info = None
    with open(args.meta) as meta_file:
        meta_info = json.load(meta_file)

    files = []
    for file_glob in args.files:
        log.debug("Expanding file: %s", file_glob)
        files.extend(glob.glob(file_glob))

    log.info("Got %i data files", len(files))

    log.info("Importing configuration")
    cfg = __import__(args.cfg.replace('.py', ''))

    log.info("Building views")
    mu_fr_views = get_views(
        files,
        # How to get the sample from the file name
        lambda x: os.path.basename(x).replace('.all.root', ''),
        meta_info,
        4700
    )

    # Get view of double muon data
    data = mu_fr_views[cfg.data_sample]['view']

    # Get the different regions where we measure the stuff
    log.info("Getting regions from cfg")
    regions = cfg.make_regions(data)

    log.info("Loading workspace")
    fit_models_file = io.open(args.fit_models, 'READ')
    # fit_modles is a RooWorkspace
    fit_models = fit_models_file.fit_models

    x = fit_models.var('x')
    cut = fit_models.cat('cut')

    # Make pass and fail views
    def make_path_mangler(to_insert):
        def functor(path):
            print path
            dir = os.path.dirname(path)
            var = os.path.basename(path)
            newpath = os.path.join(dir, to_insert, var)
            return newpath
        return functor

    # Wrap the views of the histograms to translate to RooDataHists
    def roodatahistizer(hist):
        ''' Turn a hist into a RooDataHist '''
        return ROOT.RooDataHist(hist.GetName(), hist.GetTitle(),
                                ROOT.RooArgList(x), hist)
    # Now a Get() will return a RooDataHist
    for type in regions.keys():
        # Rebin the histograms.  Make this smarter later
        regions[type] = views.FunctorView(regions[type], lambda x: x.Rebin(5))
        # Make views of the numerator and denominator.
        # For RooFit we have to split into Pass & Fail
        # So subtract the numerator from the denominator
        num_view = views.PathModifierView(regions[type], make_path_mangler('pass'))
        all_view = views.PathModifierView(regions[type], make_path_mangler('all'))
        negative_num_view = views.ScaleView(num_view, -1)
        fail_view = views.SumView(all_view, negative_num_view)

        # Now make RooDataHistViews of the numerator & denominator
        regions[type] = (
            views.FunctorView(num_view, roodatahistizer),
            views.FunctorView(fail_view, roodatahistizer),
        )

    log.info("Making output workspace")
    ws = ROOT.RooWorkspace("fit_results")
    def ws_import(*args):
        getattr(ws, 'import')(*args)

    # Fit each region
    for region, folder in regions.iteritems():
        # Figure out what to fit
        for path, options in cfg.things_to_fit.iteritems():
            log.info("Computing fake rates for region: %s path: %s",
                     region, '/'.join(path))

            # Path is (folder1, folder2, var)
            # need to convert this to all/pass to get num denominator
            num = folder[0].Get(os.path.join(*path))
            fail = folder[1].Get(os.path.join(*path))
            log.info("Num/fail have %f/%f entries", num.sumEntries(),
                     fail.sumEntries())

            log.info("Constructing composite roo data hist")
            roo_data = ROOT.RooDataHist(
                'data', 'data',
                ROOT.RooArgList(x),  ROOT.RooFit.Index(cut),
                ROOT.RooFit.Import('accept', num),
                ROOT.RooFit.Import('reject', fail),
            )
            log.info("Putting fit data in workspace")
            ws_import(roo_data, ROOT.RooFit.Rename('_'.join((region,) + path)))

            # Which function to fit
            function_name = options['func']
            log.info("Getting fit function: %s", function_name)
            function = fit_models.function(function_name)

            # Clone and rename
            function = function.Clone(
                '_'.join(('func', region,) + path)
            )

            ws_import(function)

            log.info("Making RooEfficiency")
            roo_eff = ROOT.RooEfficiency(
                '_'.join((region,) + path + ('pdf',)),
                "Fake rate", function, cut, "accept")

            log.info("Doing fit for %s!", region +  '/'.join(path))
            fit_result = roo_eff.fitTo(
                roo_data,
                ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(x)),
                ROOT.RooFit.Save(True),
                #ROOT.RooFit.PrintLevel(-1)
            )
            ws_import(
                fit_result,
                '_'.join(('result', region,) + path)
            )


    ws.writeToFile(args.output)

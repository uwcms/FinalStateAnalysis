#!/usr/bin/env python

'''

Fit the functional form of an efficiency.

Usage:
    fit_efficiency.py input.root output.root path/to/num path/to/denom "eff"

Where [efficiency] is a RooFit factory command.

'''

from RecoLuminosity.LumiDB import argparse
import logging
import sys
args = sys.argv[:]
sys.argv = [sys.argv[0]]
from rootpy.plotting import views
import rootpy.io as io
import ROOT

log = logging.getLogger("fit_efficiency")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('output', metavar='output.root', help='Output root file')
    parser.add_argument('num', metavar='/path/to/num',
                        help='Path to numerator object')
    parser.add_argument('denom', metavar='/path/to/denom',
                        help='Path to denominator object')
    parser.add_argument('efficiency',
                        help='RooFactory command to build eff. function')
    parser.add_argument('parameters',
                        help='RooFactory command to build eff. parameters')

    parser.add_argument('input', nargs='+', metavar='input.root',
                        help='Input root files - will be summed')

    args = parser.parse_args(args[1:])

    # Build view of input histograms
    log.info("Merging input files")
    input_view = views.SumView(*[io.open(x) for x in args.input])

    log.info("Getting histograms")
    pass_histo = input_view.Get(args.input)
    all_histo = input_view.Get(args.output)
    log.info("pass/all = %0.0f/%0.0f = %0.2f%%", pass_histo.Integral(),
             all_histo.Integral(), pass_histo.Integral()/all_histo.Integral())
    fail_histo = all_histo - pass_histo

    log.info("Converting data to RooFit format")
    # Build the X variable
    x = ROOT.RooRealVar('x', 'x', 0)
    cut = ROOT.RooCategory("cut", "cutr")
    cut.defineType("accept", 1)
    cut.defineType("reject", 0)

    def roodatahistizer(hist):
        ''' Turn a hist into a RooDataHist '''
        return ROOT.RooDataHist(hist.GetName(), hist.GetTitle(),
                                ROOT.RooArgList(x), hist)

    pass_data = roodatahistizer(pass_histo)
    fail_data = roodatahistizer(fail_histo)
    combined_data = ROOT.RooDataHist(
        'data', 'data',
        ROOT.RooArgList(x),  ROOT.RooFit.Index(cut),
        ROOT.RooFit.Import('accept', pass_data),
        ROOT.RooFit.Import('reject', fail_data),
    )

    log.info("Creating workspace and importing data")
    ws = ROOT.RooWorkspace("fit_efficiency")
    # Import is a reserved word
    def ws_import(*args):
        getattr(ws, 'import')(*args)
    ws_import(combined_data)

    command = "expr::efficiency('%s', x, %s)" % (
        args.efficiency, args.parameters)
    log.info("Building efficiency function: %s", command)
    ws.factory(command)
    function = ws.function('efficiency')

    eff = ROOT.RooEfficiency(
        'rooefficiency', 'Efficiency', function, cut, "accept")

    log.info("Doing fit!")
    fit_result = eff.fitTo(
        combined_data,
        ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(x)),
        ROOT.RooFit.Save(True),
        ROOT.RooFit.PrintLevel(-1)
    )

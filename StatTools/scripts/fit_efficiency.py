#!/usr/bin/env python

'''

Fit the functional form of an efficiency.

Usage:
    fit_efficiency.py input.root output.root path/to/num path/to/denom "eff"

Where [efficiency] is a RooFit factory command.

'''

import array
from RecoLuminosity.LumiDB import argparse
from FinalStateAnalysis.PlotTools.RebinView import RebinView
from FinalStateAnalysis.PlotTools.THBin import zipBins
import logging
import sys
args = sys.argv[:]
sys.argv = [sys.argv[0]]

log = logging.getLogger("fit_efficiency")

def get_th1f_binning(histo):
    bin_edges = []
    for i in range(histo.GetNbinsX()+1):
        bin_edges.append(histo.GetBinLowEdge(i+1))
    return array.array('d', bin_edges)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('output', metavar='output.root', help='Output root file')
    parser.add_argument('num', metavar='/path/to/num',
                        help='Path to numerator object')
    parser.add_argument('denom', metavar='/path/to/denom',
                        help='Path to denominator object')
    parser.add_argument('efficiency',
                        help='RooFactory command to build eff. function'
                        ' (see: http://root.cern.ch/root/html/RooFactoryWSTool.html#RooFactoryWSTool:process)')
    parser.add_argument('parameters',
                        help='RooFactory command to build eff. parameters')

    parser.add_argument('input', nargs='+', metavar='input.root',
                        help='Input root files - will be summed')

    parser.add_argument('--verbose', action='store_true',
                        help='More log output')

    parser.add_argument('--rebin', metavar='N', type=str, required=False,
                        help='Rebin histograms before fitting. '
                        'Can be either an integer or a list of bin edges.'
                        ' If variable binning is used, the numbers should '
                        ' be specified as a comma separated list w/o spaces.')

    plot_grp = parser.add_argument_group('plotting')
    plot_grp.add_argument('--plot', action='store_true',
                          help='Plot fit result')

    plot_grp.add_argument('--xrange', nargs=2, type=float, help='x-axis range')

    plot_grp.add_argument('--min', type=float, default=1e-3,
                          help='y-axis minimum')
    plot_grp.add_argument('--max', type=float, default=1,
                          help='y-axis maximum')

    args = parser.parse_args(args[1:])

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    from rootpy.plotting import views
    import rootpy.io as io
    from FinalStateAnalysis.Utilities.rootbindings import ROOT
    ROOT.gROOT.SetBatch(True)
    #ROOT.gSystem.Load("libFinalStateAnalysisStatTools")

    # Build view of input histograms
    log.info("Merging input files")
    input_view = views.SumView(*[io.open(x) for x in args.input])

    if args.rebin and args.rebin > 1:
        binning = None
        if ',' in args.rebin:
            binning = tuple(int(x) for x in args.rebin.split(','))
        else:
            binning = int(args.rebin)
        input_view = RebinView(input_view, binning)

    log.info("Getting histograms")
    pass_histo = input_view.Get(args.num)
    all_histo = input_view.Get(args.denom)
    if not all_histo.Integral():
        log.info("no entries in denominator!")
    else:
        log.info("pass/all = %0.0f/%0.0f = %0.2f%%",
                 pass_histo.Integral(), all_histo.Integral(),
                 pass_histo.Integral()/all_histo.Integral())
    # Fill the data.
    print type(pass_histo)
    ## for binp, bina in zipBins(pass_histo, all_histo):
    ##     bratio = binp.content/bina.content if bina.content <> 0 else 0
    ##     print "bin #%s: passed %s     all %s  ratio: %s" % (binp._binNum, binp.content, bina.content, bratio)
    graph = ROOT.TGraphAsymmErrors(pass_histo, all_histo)
    ## graph.SetMarkerColor(2)
    ## graph.GetYaxis().SetRangeUser(0,1)
    ## graph.SetMarkerStyle(20)
    ## graph.SetMarkerSize(1)
    ## canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)
    ## graph.Draw('ap')
    ## canvas.Print( plot_name = args.output.replace('.root', 'TGraph.png') )
    ## canvas.Delete()
    log.info("Building x-y RooDataSet")
    x = ROOT.RooRealVar('x', 'x', 0)
    x.setMin(graph.GetX()[0]-graph.GetEXlow()[0])
    x.setMax(graph.GetX()[graph.GetN()-1]+graph.GetEXhigh()[graph.GetN()-1])
    y = ROOT.RooRealVar('y', 'y', 0)
    xy_data = ROOT.RooDataSet(
        "xy_data", "xy_data",
        ROOT.RooArgSet(x, y),
        ROOT.RooFit.StoreAsymError(ROOT.RooArgSet(y)),
        ROOT.RooFit.StoreError(ROOT.RooArgSet(x))
    )
    # Convert TGraph into x-y datasets
    for bin in range(graph.GetN()):
        xval = graph.GetX()[bin]
        yval = graph.GetY()[bin]
        xdown = graph.GetEXlow()[bin]
        xup = graph.GetEXhigh()[bin]
        ydown = graph.GetEYlow()[bin]
        yup = graph.GetEYhigh()[bin]
        x.setVal(xval)
        y.setVal(yval)
        x.setError(xup)
        #x.setError(1)
        y.setAsymError(-ydown, yup)
        xy_data.add(ROOT.RooArgSet(x, y))


    log.info("Creating workspace and importing data")
    ws = ROOT.RooWorkspace("fit_efficiency")
    # Import is a reserved word
    def ws_import(*args):
        getattr(ws, 'import')(*args)
    ws_import(xy_data)

    command = "expr::efficiency('%s', x, %s)" % (
        args.efficiency, args.parameters)
    log.info("Building efficiency function: %s", command)
    ws.factory(command)
    function = ws.function('efficiency')
    #import pdb; pdb.set_trace()

    log.info("Doing fit!")
    fit_result = function.chi2FitTo(
        xy_data,
        ROOT.RooFit.YVar(y),
        # Integrate fit function across x-error width, don't just use center
        # This doesn't work... I don't know why.
        ROOT.RooFit.Integrate(False),
        #ROOT.RooFit.Integrate(True),
        ROOT.RooFit.Save(True),
        ROOT.RooFit.PrintLevel(-1),
    )

    log.info("Fit result status: %i", fit_result.status())
    fit_result.Print()
    ws_import(fit_result)
    log.info("Saving workspace in %s", args.output)
    ws.writeToFile(args.output)

    if args.plot:
        canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)
        try:
            frame = None
            if args.xrange:
                frame = x.frame(ROOT.RooFit.Title("Efficiency"),
                                ROOT.RooFit.Range(args.xrange[0], args.xrange[1]))
            else:
                frame = x.frame(ROOT.RooFit.Title("Efficiency"))

            function.plotOn(
                frame,
                ROOT.RooFit.LineColor(ROOT.EColor.kBlack),
                ROOT.RooFit.VisualizeError(fit_result, 1.0),
                ROOT.RooFit.FillColor(ROOT.EColor.kAzure - 9)
            )
            function.plotOn(frame, ROOT.RooFit.LineColor(ROOT.EColor.kAzure))
            xy_data.plotOnXY(
                frame,
                ROOT.RooFit.YVar(y),
            )
            frame.SetMinimum(args.min)
            frame.SetMaximum(args.max)
            frame.GetYaxis().SetTitle("Efficiency")
            frame.GetXaxis().SetTitle(pass_histo.GetTitle())
            frame.Draw()
            canvas.SetLogy(True)
            canvas.Draw()
            plot_name = args.output.replace('.root', '.png')
            log.info("Saving fit plot in %s", plot_name)
            canvas.SaveAs(plot_name)
            canvas.SaveAs(plot_name.replace('.png', '.pdf'))
        finally:
            # If we don't explicitly delete this, we get a segfault in the dtor
            frame.Delete()

#!/usr/bin/env python

'''

Fit the functional form of an efficiency.

Usage:
    fit_efficiency.py input.root output.root path/to/num path/to/denom "eff"

Where [efficiency] is a RooFit factory command.

'''

import array
from RecoLuminosity.LumiDB import argparse
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

    parser.add_argument('--rebin', metavar='N', type=int, required=False,
                        help='Rebin histograms before fitting')

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
    import ROOT
    ROOT.gSystem.Load("libFinalStateAnalysisStatTools")

    # Build view of input histograms
    log.info("Merging input files")
    input_view = views.SumView(*[io.open(x) for x in args.input])

    if args.rebin and args.rebin > 1:
        rebinner = lambda x: x.Rebin(args.rebin)
        input_view = views.FunctorView(input_view, rebinner)

    log.info("Getting histograms")
    pass_histo = input_view.Get(args.num)
    all_histo = input_view.Get(args.denom)
    if not all_histo.Integral():
        log.info("no entries in denominator!")
    else:
        log.info("pass/all = %0.0f/%0.0f = %0.2f%%",
                 pass_histo.Integral(), all_histo.Integral(),
                 pass_histo.Integral()/all_histo.Integral())
    fail_histo = all_histo - pass_histo

    log.info("Converting data to RooFit format")
    # Build the X variable
    x = ROOT.RooRealVar('x', 'x', 0)
    x_bins = get_th1f_binning(fail_histo)
    x_binning = ROOT.RooBinning(len(x_bins)-1, x_bins)
    x.setBinning(x_binning)
    cut = ROOT.RooCategory("cut", "cutr")
    cut.defineType("accept", 1)
    cut.defineType("reject", 0)

    def roodatahistizer(hist):
        ''' Turn a hist into a RooDataHist '''
        return ROOT.RooDataHist(hist.GetName(), hist.GetTitle(),
                                ROOT.RooArgList(x), hist)

    pass_data = roodatahistizer(pass_histo)
    fail_data = roodatahistizer(fail_histo)

    canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)

    log.info("Building combined data")
    combined_data_factory = ROOT.RooDataHistEffBuilder(
        'data', 'data', ROOT.RooArgList(x), cut
    )
    log.info("Adding pass histo")
    combined_data_factory.addHist('accept', pass_histo)
    log.info("Adding fail histo")
    combined_data_factory.addHist('reject', fail_histo)

    #combined_data = ROOT.RooDataHist(
        #'data', 'data',
        #ROOT.RooArgList(x),  ROOT.RooFit.Index(cut),
        #ROOT.RooFit.Import('accept', pass_data),
        #ROOT.RooFit.Import('reject', fail_data),
    #)
    log.info("Calling build()")
    combined_data = combined_data_factory.build()

    #comb_frame = x.frame(ROOT.RooFit.Title("Efficiency"))
    #combined_data.plotOn(comb_frame, ROOT.RooFit.Efficiency(cut))
    #comb_frame.Draw()
    #plot_name = args.output.replace('.root', '.debug_comb.png')
    #log.info("Saving fit plot in %s", plot_name)
    #canvas.SaveAs(plot_name)

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
        ROOT.RooFit.PrintLevel(-1),
        ROOT.RooFit.SumW2Error(False)
    )
    log.info("Fit result status: %i", fit_result.status())
    fit_result.Print()
    ws_import(fit_result)
    log.info("Saving workspace in %s", args.output)
    ws.writeToFile(args.output)

    if args.plot:
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
            combined_data.plotOn(frame, ROOT.RooFit.Efficiency(cut))
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

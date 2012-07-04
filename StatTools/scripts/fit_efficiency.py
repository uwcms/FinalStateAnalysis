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

log = logging.getLogger("fit_efficiency")


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
                          help='Optionally plot the result in [output].png')

    args = parser.parse_args(args[1:])

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    from rootpy.plotting import views
    import rootpy.io as io
    import ROOT

    # Build view of input histograms
    log.info("Merging input files")
    input_view = views.SumView(*[io.open(x) for x in args.input])

    if args.rebin:
        rebinner = lambda x: x.Rebin(args.rebin)
        input_view = views.FunctorView(input_view, rebinner)

    log.info("Getting histograms")
    pass_histo = input_view.Get(args.num)
    all_histo = input_view.Get(args.denom)
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
    log.info("Fit result status: %i", fit_result.status())
    fit_result.Print()
    ws_import(fit_result)
    log.info("Saving workspace in %s", args.output)
    ws.writeToFile(args.output)

    if args.plot:
        canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)
        try:
            frame = x.frame(ROOT.RooFit.Title("Efficiency"))
            function.plotOn(
                frame,
                ROOT.RooFit.LineColor(ROOT.EColor.kBlack),
                ROOT.RooFit.VisualizeError(fit_result, 1.0),
                ROOT.RooFit.FillColor(ROOT.EColor.kAzure - 9)
            )
            function.plotOn(frame, ROOT.RooFit.LineColor(ROOT.EColor.kAzure))
            combined_data.plotOn(frame, ROOT.RooFit.Efficiency(cut))
            frame.SetMinimum(1e-4)
            frame.SetMaximum(1)
            frame.GetYaxis().SetTitle("Efficiency")
            frame.GetXaxis().SetTitle(pass_histo.GetTitle())
            frame.Draw()
            canvas.SetLogy(True)
            canvas.Draw()
            plot_name = args.output.replace('.root', '.pdf')
            log.info("Saving fit plot in %s", plot_name)
            canvas.SaveAs(plot_name)
        finally:
            # If we don't explicitly delete this, we get a segfault in the dtor
            frame.Delete()

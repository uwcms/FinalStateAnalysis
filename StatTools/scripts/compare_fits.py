#!/usr/bin/env python
'''

Stupid script to compare fits made by fit_efficiency.py

Un-copypaste later

'''

import atexit
from RecoLuminosity.LumiDB import argparse
import logging
import sys
args = sys.argv[:]
sys.argv = [sys.argv[0]]

log = logging.getLogger("compare_fits")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('output', help='Output plot file')

    parser.add_argument('workspaces', nargs='+', metavar='ws.root',
                        help='Input root files with workspaces')

    parser.add_argument('--names', metavar='ZTT', nargs='+',
                        help = "Sample names in legend - must be same size"
                        " as [workspaces]")

    parser.add_argument('--verbose', action='store_true',
                        help='More log output')

    plot_grp = parser.add_argument_group('plotting')
    plot_grp.add_argument('--linear', action='store_true',
                          help='Plot in linear scale')
    plot_grp.add_argument('--min', type=float, default=5e-3,
                          help='y-axis minimum')
    plot_grp.add_argument('--max', type=float, default=1,
                          help='y-axis maximum')
    plot_grp.add_argument('--label', type=float, default=1,
                          help='y-axis maximum')

    args = parser.parse_args(args[1:])

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    from rootpy.plotting import views
    import rootpy.io as io
    import ROOT

    canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)

    workspaces = [io.open(x).Get("fit_efficiency") for x in args.workspaces]


    x = workspaces[0].var('x')

    frame = x.frame(ROOT.RooFit.Title("Efficiency"))

    # Always Delete the frame, otherwise we get a segfault
    @atexit.register
    def cleanup_frame():
        if frame:
            frame.Delete()


    ecolor = ROOT.EColor

    colors = [ecolor.kAzure, ecolor.kViolet, ecolor.kOrange]

    legend = None

    if args.names:
        legend = ROOT.TLegend(0.7, 0.8, 0.9, 0.9, "", "brNDC")
        legend.SetBorderSize(0)
        legend.SetFillStyle(0)

    keep = []
    for i, (color, ws) in enumerate(zip(colors, workspaces)):
        function = ws.function('efficiency')
        fit_result = ws.genobj("fitresult_rooefficiency_data")
        function.plotOn(
                frame,
                ROOT.RooFit.LineColor(ROOT.EColor.kBlack),
                ROOT.RooFit.VisualizeError(fit_result, 1.0),
                ROOT.RooFit.FillColor(color - 9)
            )
        function.plotOn(frame, ROOT.RooFit.LineColor(color))
        if args.names:
            # Make a dummy thing for the legend
            stupid = ROOT.TGraph(1)
            stupid.SetLineColor(color)
            stupid.SetFillColor(color-9)
            stupid.SetLineWidth(3)
            keep.append(stupid)
            # Add the dummy to the legend
            legend.AddEntry(stupid, args.names[i], "lf")

    frame.SetMinimum(args.min)
    frame.SetMaximum(args.max)
    if not args.linear:
        canvas.SetLogy(True)
    frame.GetYaxis().SetTitle("Efficiency")

    frame.Draw()

    if legend:
        legend.Draw()

    canvas.SaveAs(args.output)

    #frame.Delete()


#!/usr/bin/env python

'''

Make a limit plot given a set of json limit data files.

'''

import sys
import glob
from RecoLuminosity.LumiDB import argparse
from rootpy.utils import asrootpy

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    plots = parser.add_argument_group('plot data', 'Limit data and color options')
    plots.add_argument('--plot1', nargs=4, required=True,
                        metavar=('jsonglob', 'title', 'exp/obs', 'color'),
                        help='First limit to plot')

    plots.add_argument('--plot2', nargs=4, required=True,
                        metavar=('jsonglob', 'title', 'exp/obs', 'color'),
                        help='Second limit to plot')

    plots.add_argument('--plot3', nargs=4, required=False,
                        metavar=('jsonglob', 'title', 'exp/obs', 'color'),
                        help='Third limit to plot')

    plots.add_argument('--plot4', nargs=4, required=False,
                        metavar=('jsonglob', 'title', 'exp/obs', 'color'),
                        help='Fourth limit to plot')

    plots.add_argument('--method', type=str, default='cls',
                        help='Limit method to use.  Default: cls')

    plots.add_argument('--label', type=str, default='',
                        help='Limit label to use.  Default: None')

    blurb = parser.add_argument_group('blurb options')
    blurb.add_argument('--blurb', type=str, default='',
                        help='Blurb to use at [blurbpos].  Default: None')

    blurb.add_argument('--blurbpos', type=str, default="0.5,0.12,0.9,0.25",
                        help='[blurb] position, separated by commas.  '
                        ' Default: %(default)s')

    blurb.add_argument('--blurbalign', type=int, default=31,
                        help='[blurb] alignment. Default: %(default)i')

    blurb.add_argument('--blurbsize', type=float, default=0.05,
                        help='[blurb] text size. Default: %(default)i')

    style = parser.add_argument_group('style options')
    style.add_argument('--canvas-x', dest="cx", type=int, default=800,
                        help="Canvas width (pixels).  Default: 800")

    style.add_argument('--canvas-y', dest="cy", type=int, default=600,
                        help="Canvas height (pixels).  Default: 600")

    style.add_argument('--max-y', dest="maxy", type=float, default=30,
                        help="Max on the y axis")

    style.add_argument('--max-x', dest="maxx", type=float, default=-1,
                        help="Max on the x axis, if less than 0 take from max limits")

    style.add_argument('--lumi', dest="lumi", type=int, default=4684,
                        help="Integrated lumi: picobarns")

    parser.add_argument('-o', '--output', dest="output",
                        type=str, default="output.pdf",
                        help="Output plot file")

    parser.add_argument('--legendpos', type=str, default="0.7,0.17,0.9,0.45",
                        help="Comma separated corners of legend."
                        " default: %(default)s")

    parser.add_argument('--showpoints', action='store_true',
                        help="Put dots at the actual mass values where"
                        " the limit is set")
    parser.add_argument('--preliminary', action='store_true',
                        help="Add 'preliminary' to CMS label")

    args = parser.parse_args()

    sys.argv[:] = []
    import ROOT
    import FinalStateAnalysis.StatTools.limitplot as limitplot
    import FinalStateAnalysis.Utilities.styling as styling

    print args.plot1, args.plot4

    plots_to_comp = []

    key = (args.method, args.label)
    xmin = 1e9
    xmax = -1e9

    for plot in [args.plot1, args.plot2, args.plot3, args.plot4]:
        if plot:
            the_glob, title, type, color = tuple(plot)
            limit_data = limitplot.get_limit_info(glob.glob(the_glob))
            tgraph = asrootpy(limitplot.build_line(limit_data, key, type))
            print tgraph
            tgraph.SetLineColor(color)
            plots_to_comp.append((tgraph, title))
            xmin = min(min(limit_data[key].keys()), xmin)
            xmax = max(max(limit_data[key].keys()), xmax)

    canvas = ROOT.TCanvas("c", "c", args.cx, args.cy)

    if args.maxx > 0:
        xmax = args.maxx

    frame = ROOT.TH1F("frame", "frame", 1, xmin, xmax)

    frame.Draw()
    #frame.SetTitle("WH(#tau#tau) limits [4.6 fb^{-1}]")
    frame.GetYaxis().SetTitle("95% CL upper limit on #sigma/#sigma_{SM}")
    frame.GetXaxis().SetTitle("M_{H} (GeV)")

    frame.SetMaximum(args.maxy)

    draw_option = 'l'
    if args.showpoints:
        draw_option += 'p'

    cms_label = styling.cms_preliminary(
        args.lumi,
        is_preliminary=args.preliminary,
        lumi_on_top = True,
    )

    # Add legend
    legend_args = [ float(x) for x in args.legendpos.split(',') ] + ["", "NDC"]

    legend = ROOT.TLegend(*legend_args)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)

    for graph, title in plots_to_comp:
        legend.AddEntry(graph, title, 'l')
        graph.Draw(draw_option)
    legend.Draw()

    blurb = None
    if args.blurb:
        blurbargs = [float(x) for x in args.blurbpos.split(',')] + ['brNDC']
        blurb = ROOT.TPaveText(*blurbargs)
        blurb.SetFillStyle(0)
        blurb.SetBorderSize(0)
        blurb.SetTextAlign(args.blurbalign)
        blurb.AddText(args.blurb)
        blurb.SetTextSize(args.blurbsize)
        blurb.Draw()

    canvas.RedrawAxis()

    canvas.RedrawAxis()

    # Add some extra lines on the border to make it look nice
    top_frame_line = ROOT.TLine(xmin, args.maxy, xmax, args.maxy)
    top_frame_line.SetLineWidth(2)
    top_frame_line.Draw()

    right_frame_line = ROOT.TLine(xmax, 0, xmax, args.maxy)
    right_frame_line.SetLineWidth(2)
    right_frame_line.Draw()

    left_frame_line = ROOT.TLine(xmin, 0, xmin, args.maxy)
    left_frame_line.SetLineWidth(2)
    left_frame_line.Draw()

    bottom_frame_line = ROOT.TLine(xmin, 0, xmax, 0)
    bottom_frame_line.SetLineWidth(2)
    bottom_frame_line.Draw()

    canvas.SaveAs(args.output)

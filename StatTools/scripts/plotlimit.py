#!/usr/bin/env python

'''

Make a limit plot given a set of json limit data files.

'''

import glob
from RecoLuminosity.LumiDB import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    input_grp = parser.add_argument_group('input/output')
    input_grp.add_argument('data', nargs='*', help='JSON files with limit data')
    input_grp.add_argument('--method', type=str, default='cls',
                        help='Limit method to use.  Default: cls')
    input_grp.add_argument('--label', type=str, default='',
                        help='Limit label to use.  Default: None')
    input_grp.add_argument('--smooth', default = -1, type = int,
                           help="Smooth using N order poly. -1 => no smoothing")

    input_grp.add_argument('-o', '--output', dest="output",
                        type=str, required=True,
                        help="Output plot file")

    blurb_grp = parser.add_argument_group('blurb')
    blurb_grp.add_argument('--blurb', type=str, default='',
                        help='Blurb to use at [blurbpos].  Default: None')
    blurb_grp.add_argument('--blurbpos', type=str, default="0.5,0.12,0.9,0.25",
                        help='[blurb] position, separated by commas.  '
                        ' Default: %(default)s')
    blurb_grp.add_argument('--blurbalign', type=int, default=31,
                        help='[blurb] alignment. Default: %(default)i')

    blurb_grp.add_argument('--blurbsize', type=float, default=0.05,
                        help='[blurb] text size. Default: %(default)f')


    style_grp = parser.add_argument_group('style')
    style_grp.add_argument('--canvas-x', dest="cx", type=int, default=800,
                        help="Canvas width (pixels).  Default: 800")
    style_grp.add_argument('--canvas-y', dest="cy", type=int, default=800,
                        help="Canvas height (pixels).  Default: 800")
    style_grp.add_argument('--max-y', dest="maxy", type=float, default=30,
                        help="Max on the y axis")
    style_grp.add_argument('--max-x', dest="maxx", type=float, default=-1,
                        help="Max on the x axis, if less than 0 take from max limits")
    style_grp.add_argument('--legendpos', type=str, default="0.7,0.17,0.9,0.45",
                        help="Comma separated corners of legend."
                        " default: %(default)s")
    style_grp.add_argument('--legendnudge', type=str, default="0,0",
                           help="Translate the legend by X,Y in NDC")

    style_grp.add_argument('--showpoints', action='store_true',
                        help="Put dots at the actual mass values where"
                        " the limit is set")
    style_grp.add_argument('--no-obs', dest='noobs', action='store_true',
                        help="Don't show the observed limit")
    style_grp.add_argument('--show-sm', dest='showsm', action='store_true',
                        help="Draw a dashed line at Y=1")
    style_grp.add_argument('--debug', action='store_true',
                        help="Draw boxes around the Paves")

    label_grp = parser.add_argument_group('labeling')
    label_grp.add_argument('--lumi', dest="lumi", type=int, default=4684,
                           help="Integrated lumi: picobarns")
    label_grp.add_argument('--preliminary', action='store_true',
                           help="Add 'preliminary' to CMS label")
    label_grp.add_argument('--ytitle', type=str,
                           default="95% CL upper limit on #sigma/#sigma_{SM}",
                           help="y-axis title.  Default: '%(default)s'")
    label_grp.add_argument('--xtitle', type=str,
                           default="m_{H} (GeV)",
                           help="x-axis title.  Default: '%(default)s'")


    args = parser.parse_args()

    import FinalStateAnalysis.Utilities.styling as styling

    import FinalStateAnalysis.StatTools.limitplot as limitplot
    import ROOT

    all_files = []
    for file in args.data:
        all_files.extend(glob.glob(file))

    limit_data = limitplot.get_limit_info(all_files)

    key = (args.method, args.label)

    canvas = ROOT.TCanvas("c", "c", args.cx, args.cy)
    canvas.SetRightMargin(0.05)
    canvas.SetLeftMargin(1.1*canvas.GetLeftMargin())

    xmin = min(limit_data[key].keys())
    xmax = max(limit_data[key].keys())

    if args.maxx > 0:
        xmax = args.maxx

    frame = ROOT.TH1F("frame", "frame", 1, xmin, xmax)

    frame.Draw()
    #frame.SetTitle("WH(#tau#tau) limits [4.6 fb^{-1}]")
    frame.GetYaxis().SetTitle(args.ytitle)
    frame.GetXaxis().SetTitle(args.xtitle)

    frame.SetMaximum(args.maxy)

    exp, onesig, twosig = limitplot.build_expected_band(limit_data, key,
                                                       args.smooth)
    twosig.Draw("3")
    onesig.Draw("3")

    exp_draw_option = 'l'
    if args.noobs and args.showpoints:
        exp_draw_option += 'p'

    exp.Draw(exp_draw_option)

    if not args.noobs:
        obs = limitplot.build_obs_line(limit_data, key)
        obs_draw_option = 'l'
        if args.showpoints:
            obs_draw_option += 'p'
        obs.Draw(obs_draw_option)

    cms_label = styling.cms_preliminary(
        args.lumi,
        is_preliminary=args.preliminary,
        lumi_on_top = True,
    )

    # Add legend
    legend_args = [ float(x) for x in args.legendpos.split(',') ] + ["", "NDC"]

    # Translate the legend in X,Y, if desired.
    nudge = [ float(x) for x in args.legendnudge.split(',') ]
    legend_args[0] += nudge[0]
    legend_args[2] += nudge[0]
    legend_args[1] += nudge[1]
    legend_args[3] += nudge[1]

    legend = ROOT.TLegend(*legend_args)
    legend.SetBorderSize(1)
    legend.SetFillStyle(1001)
    legend.SetFillColor(0)
    if not args.noobs:
        legend.AddEntry(obs,"Observed",  'lp')
    legend.AddEntry(exp, "Median Expected", 'l')
    legend.AddEntry(onesig, "#pm 1#sigma Expected",  'f')
    legend.AddEntry(twosig, "#pm 2#sigma Expected",  'f')
    legend.Draw()

    blurb = None
    if args.blurb:
        blurbargs = [float(x) for x in args.blurbpos.split(',')] + ['brNDC']
        blurb = ROOT.TPaveText(*blurbargs)
        blurb.SetFillStyle(0)
        if not args.debug:
            blurb.SetBorderSize(0)
        blurb.SetTextAlign(args.blurbalign)
        blurb.AddText(args.blurb)
        blurb.SetTextSize(args.blurbsize)
        blurb.Draw()

    canvas.RedrawAxis()
    canvas.RedrawAxis()

    legend.Draw()

    sm_line = None
    if args.showsm:
        sm_line = ROOT.TLine(xmin, 1.0, xmax, 1.0)
        sm_line.SetLineStyle(1)
        sm_line.SetLineColor(ROOT.EColor.kRed)
        sm_line.SetLineWidth(1)
        sm_line.Draw()

    # Add some extra lines on the border to make it look nice
    top_frame_line = ROOT.TLine(xmin, args.maxy, xmax, args.maxy)
    top_frame_line.SetLineWidth(3)
    top_frame_line.Draw()

    right_frame_line = ROOT.TLine(xmax, 0, xmax, args.maxy)
    right_frame_line.SetLineWidth(2)
    right_frame_line.Draw()

    left_frame_line = ROOT.TLine(xmin, 0, xmin, args.maxy)
    left_frame_line.SetLineWidth(3)
    left_frame_line.Draw()

    bottom_frame_line = ROOT.TLine(xmin, 0, xmax, 0)
    bottom_frame_line.SetLineWidth(3)
    bottom_frame_line.Draw()

    canvas.SaveAs(args.output)

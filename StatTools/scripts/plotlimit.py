#!/usr/bin/env python

'''

Make a limit plot given a set of json limit data files.

'''

import glob
from RecoLuminosity.LumiDB import argparse
import FinalStateAnalysis.StatTools.limitplot as limitplot
import FinalStateAnalysis.Utilities.styling as styling
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs='*', help='JSON files with limit data')
    parser.add_argument('--method', type=str, default='cls',
                        help='Limit method to use.  Default: cls')

    parser.add_argument('--label', type=str, default='',
                        help='Limit label to use.  Default: None')

    parser.add_argument('--blurb', type=str, default='',
                        help='Blurb to use at [blurbpos].  Default: None')

    parser.add_argument('--blurbpos', type=str, default="0.5,0.12,0.9,0.25",
                        help='[blurb] position, separated by commas.  '
                        ' Default: %(default)s')

    parser.add_argument('--blurbalign', type=int, default="31",
                        help='[blurb] alignment. Default: %(default)i')

    parser.add_argument('--no-obs', dest='noobs', action='store_true',
                        help="Don't show the observed limit")

    parser.add_argument('--canvas-x', dest="cx", type=int, default=800,
                        help="Canvas width (pixels).  Default: 800")

    parser.add_argument('--canvas-y', dest="cy", type=int, default=600,
                        help="Canvas height (pixels).  Default: 600")

    parser.add_argument('--max-y', dest="maxy", type=float, default=30,
                        help="Max on the y axis")

    parser.add_argument('--lumi', dest="lumi", type=int, default=4684,
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

    print sys.argv
    args = parser.parse_args()

    import ROOT

    all_files = []
    for file in args.data:
        all_files.extend(glob.glob(file))

    limit_data = limitplot.get_limit_info(all_files)

    key = (args.method, args.label)

    canvas = ROOT.TCanvas("c", "c", args.cx, args.cy)

    xmin = min(limit_data[key].keys())
    xmax = max(limit_data[key].keys())

    frame = ROOT.TH1F("frame", "frame", 1, xmin, xmax)

    frame.Draw()
    #frame.SetTitle("WH(#tau#tau) limits [4.6 fb^{-1}]")
    frame.GetYaxis().SetTitle("95% CL upper limit on #sigma/#sigma_{SM}")
    frame.GetXaxis().SetTitle("M_{H} (GeV)")

    frame.SetMaximum(args.maxy)

    exp, onesig, twosig = limitplot.build_expected_band(limit_data, key)
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

    legend = ROOT.TLegend(*legend_args)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    if not args.noobs:
        legend.AddEntry(obs,"Observed",  'lp')
    legend.AddEntry(exp, "Expected", 'l')
    legend.AddEntry(onesig, "#pm 1 #sigma",  'f')
    legend.AddEntry(twosig, "#pm 2 #sigma",  'f')
    legend.Draw()

    blurb = None
    if args.blurb:
        blurbargs = [float(x) for x in args.blurbpos.split(',')] + ['brNDC']
        blurb = ROOT.TPaveText(*blurbargs)
        blurb.SetFillStyle(0)
        blurb.SetBorderSize(0)
        blurb.SetTextAlign(args.blurbalign)
        blurb.AddText(args.blurb)
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

#!/usr/bin/env python

'''

Make a limit plot given a set of json limit data files.

'''

import glob
from RecoLuminosity.LumiDB import argparse
import FinalStateAnalysis.StatTools.limitplot as limitplot
import FinalStateAnalysis.Utilities.styling as styling
import ROOT

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('data', nargs='*', help='JSON files with limit data')
    parser.add_argument('--method', type=str, default='cls',
                        help='Limit method to use.  Default: cls')
    parser.add_argument('--label', type=str, default='',
                        help='Limit label to use.  Default: None')
    parser.add_argument('--no-obs', action='store_false',
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

    args = parser.parse_args()

    all_files = []
    for file in args.data:
        all_files.extend(glob.glob(file))

    limit_data = limitplot.get_limit_info(all_files)

    key = (args.method, args.label)

    canvas = ROOT.TCanvas("c", "c", args.cx, args.cy)

    frame = ROOT.TH1F("frame", "frame", 1,
                      min(limit_data[key].keys()),
                      max(limit_data[key].keys()))
    frame.Draw()
    #frame.SetTitle("WH(#tau#tau) limits [4.6 fb^{-1}]")
    frame.GetYaxis().SetTitle("95% CL upper limit on #sigma/#sigma_{SM}")
    frame.GetXaxis().SetTitle("M_{H} (GeV)")

    frame.SetMaximum(args.maxy)

    exp, onesig, twosig = limitplot.build_expected_band(limit_data, key)
    twosig.Draw("3")
    onesig.Draw("3")
    exp.Draw("l")

    obs = limitplot.build_obs_line(limit_data, key)
    obs.Draw("l")

    cms_label = styling.cms_preliminary(args.lumi)

    canvas.RedrawAxis()
    canvas.SaveAs(args.output)

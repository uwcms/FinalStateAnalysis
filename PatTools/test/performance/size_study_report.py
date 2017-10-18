#!/usr/bin/env python

'''

Generates a web page with skim info images.

Usage:

    After creating a directory with

        ./size_study.sh THE_DIR,

    run

        ./size_study_report.py THE_DIR

'''


import glob
import os
import sys
import ROOT

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetPalette(1)

if __name__ == "__main__":
    input_dir = sys.argv[1]
    canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)
    for sample_root in glob.glob(os.path.join(input_dir, "*.root")):
        sample = os.path.basename(sample_root)
        sample_name = sample.replace('.root', '')
        # Get skim efficiency images
        skim_info = ROOT.TFile(sample_root, "READ")
        passed = skim_info.Get("skimEfficiency/passed")
        passed.Draw()
        canvas.SaveAs(input_dir + "/%s-passed.png" % sample_name)
        passed = skim_info.Get("skimEfficiency/pathExlcusivePass")
        passed.Draw()
        canvas.SaveAs(input_dir + "/%s-excl_passed.png" % sample_name)
        passed = skim_info.Get("skimEfficiency/pathCorrelation")
        passed.Draw('colz')
        canvas.SaveAs(input_dir + "/%s-correlation.png" % sample_name)


        with open(os.path.join(input_dir,
                               sample_name + '-report.html'), 'w') as webpage:
            def writeln(x):
                webpage.write(x)
                webpage.write('\n')

            writeln("<html>")
            writeln("<head>")
            writeln("<title>%s-%s size report</title>" % (input_dir, sample_name))
            writeln("</head>")
            writeln("<body>")
            writeln("<h1>%s</h1>" % sample_name)
            writeln("<img src='%s-passed.png'>" % sample_name)
            writeln("<img src='%s-excl_passed.png'>" % sample_name)
            writeln("<img src='%s-correlation.png'>" % sample_name)
            writeln("<pre>")
            with open(os.path.join(input_dir,
                                   'sizes_%s.txt' % sample_name), 'r') as size_rep:
                writeln(size_rep.read())
            writeln("</pre>")
            writeln("</body>")
            writeln("</html>")

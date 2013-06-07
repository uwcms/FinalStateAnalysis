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
import logging
import sys
args = sys.argv[:]
sys.argv = [sys.argv[0]]

log = logging.getLogger("fit_efficiency")


def get_th1f_binning(histo):
    bin_edges = []
    for i in range(histo.GetNbinsX() + 1):
        bin_edges.append(histo.GetBinLowEdge(i + 1))
    return array.array('d', bin_edges)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('output', metavar='output.root',
                        help='Output root file')
    parser.add_argument('num', metavar='/path/to/num',
                        help='Path to numerator object')
    parser.add_argument('denom', metavar='/path/to/denom',
                        help='Path to denominator object')
    parser.add_argument('efficiency',
                        help='RooFactory command to build eff. function'
                        ' (see: http://root.cern.ch/root/html/'
                        'RooFactoryWSTool.html#RooFactoryWSTool:process)')
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
    plot_grp.add_argument('--xtitle', type=str, help='Override x-axis range')

    plot_grp.add_argument('--min', type=float, default=1e-3,
                          help='y-axis minimum')
    plot_grp.add_argument('--max', type=float, default=1,
                          help='y-axis maximum')
    plot_grp.add_argument('--grid', action='store_true', help="Draw grid")
    plot_grp.add_argument('--noFit', action='store_true',
                          help="Do not perform fit")

    plot_grp.add_argument('--show-error', dest='showerror',
                          action='store_true', help='Plot fit error band')

    args = parser.parse_args(args[1:])

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
    else:
        logging.basicConfig(level=logging.INFO, stream=sys.stderr)

    from rootpy.plotting import views
    import rootpy.io as io
    from FinalStateAnalysis.Utilities.rootbindings import ROOT

    # Build view of input histograms
    log.info("Merging input files")
    input_view = views.SumView(*[io.open(x) for x in args.input])

    if args.rebin and args.rebin > 1:
        binning = None
        # if ',' in args.rebin:
        # print args.rebin.split(',')
        if args.rebin:
            binning = eval(args.rebin)
            if  isinstance(binning,float) or isinstance(binning,int) :
                newbinning = int(binning)
            elif isinstance(binning,list) and isinstance(binning[0],float) or isinstance(binning[0],int)  :
                newbinning= tuple(float(x) for x in binning)
            elif isinstance(binning,list) and isinstance(binning[0],list):
                # print   args.rebin
                #print binning[0]
                binningx= tuple(float(x) for x in binning[0])
                #print binningx
                binningy= tuple(float(x) for x in binning[1])
                newbinning = tuple([binningx, binningy]) 

        input_view = RebinView(input_view, newbinning)
        
    from math import *
    #log.info("Getting histograms")
    #from pdb import set_trace; set_trace()
    pass_histo = input_view.Get(args.num)
    all_histo = input_view.Get(args.denom)
    new_histo =  pass_histo.Clone()
    new_histo.Sumw2()
    new_histo.Divide( all_histo) 
    for binx in range(1, new_histo.GetNbinsX()+1):
        for biny in range(1, new_histo.GetNbinsY()+1):
            olderr = new_histo.GetBinError(binx, biny)
            eff = new_histo.GetBinContent(binx,biny) 
            erreff = sqrt(eff*(1.-eff)/all_histo.GetBinContent(binx,biny))
            new_histo.SetBinError(binx, biny, erreff)

            
    myeff = ROOT.TEfficiencyBugFixed(pass_histo, all_histo)
    myeff.SetStatisticOption(0) # 0 means  ClopperPearson
    ROOT.SetOwnership( myeff, False )
    
    myf = ROOT.TF2('myf', 'xylandau', 10, 200, 0, 50)
    myf.SetParameters(30, 12.5, 5, 0.5, 0.05)
    myf.SetParLimits(0, 0, 50)
    myf.SetParLimits(1, 0, 30)
    myf.SetParLimits(2, 0, 10)
    myf.SetParLimits(3, 0, 5)
    myf.SetParLimits(4, 0, 10)

    ROOT.SetOwnership( myf, False )
    myeff.Fit(myf, "LMI") # fitta con l'esponenziale ma crasha    

    if args.plot:
        canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)
        canvas.SetLogz(1)
        myeff.Draw("LEGO")
        #new_histo.Draw("LEGO")
        myf.Draw("SURFSAME")
   # import pdb; pdb.set_trace()
        canvas.SaveAs(args.output)
        plot_name = args.output.replace('.root', '.png')
#        log.info("Saving fit plot in %s", plot_name)
        canvas.SaveAs(plot_name)
        canvas.SaveAs(plot_name.replace('.png', '.pdf'))
   

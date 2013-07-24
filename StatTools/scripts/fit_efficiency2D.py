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
from FinalStateAnalysis.Utilities.struct import struct
import rootpy.plotting as plotting
import logging
import sys
import re
from rootpy.utils import asrootpy

args = sys.argv[:]
sys.argv = [sys.argv[0]]

log = logging.getLogger("fit_efficiency")


def get_th1f_binning(histo):
    bin_edges = []
    for i in range(histo.GetNbinsX() + 1):
        bin_edges.append(histo.GetBinLowEdge(i + 1))
    return array.array('d', bin_edges)

def parse_formula(fcn_string, pars_string):
    pars       = []
    formula    = fcn_string
    for par_num, match in enumerate(re.finditer("(?P<name>\w+)(?P<boundaries>\[[^\]]+\]),? ?", pars_string)):
        par        = struct()
        par.num    = par_num
        par.name   = match.group('name')
        par.bounds = eval( match.group('boundaries') )
        formula    = formula.replace(par.name, '[%i]' % par.num)
        pars.append(par)

    print "parsed formula: %s" % formula
    ret = ROOT.TF2('ret', formula, 0, 200, 0, 200)
    for par in pars:
        ret.SetParName(par.num, par.name)
        if len(par.bounds) == 1:
            ret.FixParameter(par.num, par.bounds[0])
        else:
            ret.SetParameter(par.num, par.bounds[0])
            ret.SetParLimits(par.num, par.bounds[1], par.bounds[2])
    return ret


def bins_projectionsY(histo2D):
    projections = []
    oldbiny = [float(histo2D.GetYaxis().GetBinLowEdge(1))]
    oldbiny.extend(float(histo2D.GetYaxis().GetBinUpEdge(y)) for y in xrange(1, histo2D.GetNbinsY()+1))
    for i in range(1, histo2D.GetNbinsX()+1):
        projections.append(plotting.Hist(oldbiny))
        projections[-1].markerstyle = 19+i
        for j in range(1, histo2D.GetNbinsY()+1):
            projections[-1].SetBinContent(j, histo2D.GetBinContent(i,j))
            projections[-1].SetBinError(j, histo2D.GetBinError(i,j))
    return projections
            
def bins_projectionsX(histo2D):
    projections = []
    oldbinx = [float(histo2D.GetXaxis().GetBinLowEdge(1))]
    oldbinx.extend(float(histo2D.GetXaxis().GetBinUpEdge(x)) for x in xrange(1, histo2D.GetNbinsX()+1))
    for i in range(1, histo2D.GetNbinsY()+1):
        projections.append(plotting.Hist(oldbinx))
        projections[-1].markerstyle = 19+i
        for j in range(1, histo2D.GetNbinsX()+1):
            projections[-1].SetBinContent(j, histo2D.GetBinContent(j,i))
            projections[-1].SetBinError(j, histo2D.GetBinError(j,i))
    return projections


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
    plot_grp.add_argument('--ytitle', type=str, help='Override y-axis range')
    plot_grp.add_argument('--fineBinnedDen', type=str, help='')

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
        
    #from math import *
    #log.info("Getting histograms")
    #from pdb import set_trace; set_trace()
    pass_histo = input_view.Get(args.num)
    all_histo  = input_view.Get(args.denom)
    all_histo_fine_bin = None
    if args.fineBinnedDen:
        all_histo_finebin = input_view.Get(args.fineBinnedDen)
        all_histo_finebin.Smooth(1,"k5a")
#
#    clone = pass_histo.Clone('cazzoneso')
#    clone.Divide(all_histo)
#    canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)
#    projectionsy = bins_projectionsY(clone)
#    projectionsy[0].Draw()
#    for i in projectionsy[1:]:
#        i.Draw('same')
#    canvas.SaveAs('projectionsY.png')
#
#    projectionsx = bins_projectionsX(clone)
#    projectionsx[0].Draw()
#    for i in projectionsx[1:]:
#        i.Draw('same')
#    canvas.SaveAs('projectionsX.png')
#    
#    raise Exception
#
    myeff = ROOT.TEfficiencyBugFixed(pass_histo, all_histo)
    myeff.SetStatisticOption(0) # 0 means  ClopperPearson
    ROOT.SetOwnership( myeff, False )

    efficiency = parse_formula(args.efficiency, args.parameters)
    efficiency.SetName('efficiency')
    efficiency.SetTitle('efficiency')

    ROOT.SetOwnership( efficiency, False)
    myeff.Fit(efficiency, "LMI") # fitta con l'esponenziale ma crasha    

    if args.plot:
        canvas = ROOT.TCanvas("asdf", "asdf", 800, 600)
        canvas.SetLogz(True)
        myeff.Draw("LEGO")
        efficiency.Draw("SURFSAME")
   # import pdb; pdb.set_trace()
        canvas.SaveAs(args.output)
        plot_name = args.output.replace('.root', '.png')
#        log.info("Saving fit plot in %s", plot_name)
        canvas.SaveAs(plot_name)
        canvas.SaveAs(plot_name.replace('.png', '.pdf'))
        
        canvas.SetLogz(False)
        canvas.SetLogy(True)
        graph_proj_x = asrootpy( myeff.Projection(ROOT.TEfficiencyBugFixed.xaxis) )
        graph_proj_x.SetMarkerStyle(20)
        graph_proj_x.title = 'data'
        fcn_proj_x   = asrootpy( myeff.ProjectFunction(ROOT.TEfficiencyBugFixed.xaxis, all_histo_finebin) ) \
                       if all_histo_finebin else \
                       asrootpy( myeff.ProjectFunction(ROOT.TEfficiencyBugFixed.xaxis) )
        print graph_proj_x, fcn_proj_x
        fcn_proj_x.SetName('fcn_proj_x')
        fcn_proj_x.SetFillStyle(0)
        fcn_proj_x.Draw('AL')
        graph_proj_x.Draw('P SAME')
        plot_name = plot_name.replace('.png', '_projX.png')
        canvas.SaveAs(plot_name)
        canvas.SaveAs(plot_name.replace('.png', '.pdf'))

        graph_proj_y = asrootpy( myeff.Projection(ROOT.TEfficiencyBugFixed.yaxis) )
        graph_proj_y.SetMarkerStyle(20)
        fcn_proj_y   = asrootpy( myeff.ProjectFunction(ROOT.TEfficiencyBugFixed.yaxis, all_histo_finebin) ) \
                       if all_histo_finebin else \
                       asrootpy( myeff.ProjectFunction(ROOT.TEfficiencyBugFixed.xaxis) )
        fcn_proj_y.SetName('fcn_proj_y')
        fcn_proj_y.SetFillStyle(0)
        fcn_proj_y.Draw('AL')
        graph_proj_y.Draw('P SAME')
        plot_name = plot_name.replace('projX', 'projY')
        canvas.SaveAs(plot_name)
        canvas.SaveAs(plot_name.replace('.png', '.pdf'))
#

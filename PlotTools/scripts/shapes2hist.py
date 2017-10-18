#! /bin/env python

import os
import sys
import rootpy.plotting.views as views
import rootpy.plotting as plotting
from rootpy import io
from FinalStateAnalysis.MetaData.data_styles import data_styles
from FinalStateAnalysis.PlotTools.DifferentialView import DifferentialView
from fnmatch import fnmatch
from optparse import OptionParser
import logging

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


__author__  = "Mauro Verzetti (mauro.verzetti@cern.ch)"
__doc__ = "reads a shapefile and outputs a histogram, in multiple categories are given they are automatically summed"
usage   = "shape2hist.py [rootfile] [categories] [options]"


def match_to_style(sample):
    best_pattern = ''
    for pattern, style_dict in data_styles.iteritems():
        logging.debug("Checking pattern: %s against %s", pattern, sample)
        if fnmatch(sample, pattern):
            logging.debug("-> it matches!")
            if len(pattern) > len(best_pattern):
                best_pattern = pattern
                logging.info("Found new best style for %s: %s", sample, pattern)
    if best_pattern:
        return data_styles[best_pattern]
    else:
        return {}

def remove_name_entry(dictionary):
    return dict( [ i for i in dictionary.iteritems() if i[0] != 'name'] )

def apply_style(histo, key):
    style = match_to_style(key)
    histo.decorate( **remove_name_entry(style) )
    #histo.SetTitle( style['name'] )
    return histo
    

if __name__ == '__main__':
    parser = OptionParser(description=__doc__, usage=usage)
    parser.add_option('-o','--output', metavar='output', type=str, default = 'out.png',
                     help='name of the output picture',dest='out')
    parser.add_option('-e','--exclude', metavar='pattern', type=str, default = '',
                     help='pattern of shape to be excluded',dest='excluded')
    parser.add_option('-n','--nuisance', metavar='pattern', type=str, default = '*CMS_*',
                     help='pattern of nuisances to be excluded',dest='nuisances')
    parser.add_option('-x','--x-title', metavar='name', type=str, default = '',
                     help='x axis title',dest='xtitle')
    parser.add_option('-y','--y-title', metavar='name', type=str, default = '',
                     help='y axis title',dest='ytitle')
    parser.add_option('-d','--differential', type=int, default = 0,
                     help='makes a differential plot',dest='differential')
    parser.add_option('--show-errors', dest='show_errors', action='store_true')

    (options,arguments) = parser.parse_args()
    
    tfile_name = arguments.pop(0)
    categories = arguments

    tfile = io.open(tfile_name)
    logging.info("Opened file %s" % tfile_name)
    
    #get a directory and look into that
    keys = [i.GetName() for i in tfile.Get(categories[0]).GetListOfKeys() if not fnmatch(i.GetName(), options.nuisances)]
    if options.excluded:
        keys = [ i for i in keys if not fnmatch(i, options.excluded)]
    data = [i for i in keys if i.startswith('data')][0]
    keys = [i for i in keys if not i.startswith('data')]

    logging.debug("These shapes will be plotted: %s" % keys.__repr__())
    
    input_view = views.SumView(
        *[ views.SubdirectoryView( tfile, category ) 
           for category in categories]
        )
    
    if options.differential == 1:
        input_view = DifferentialView( input_view )

    histograms = [ apply_style(input_view.Get(i), i) for i in keys ]
    histograms = sorted(histograms, key=lambda x: x.Integral())
    observed   = apply_style(input_view.Get(data), data)

    logging.debug("debugging histos:")
    for histo in histograms:
        logging.debug("    %s: style: %s, integral: %.2f" % ( histo.GetTitle(), histo.drawstyle, histo.Integral() ) )

    stack = plotting.HistStack()
    for obj in histograms:
        stack.Add(obj)

    maximum = max(list(observed)+[stack.GetMaximum()])
    
    canvas = plotting.Canvas(name='adsf', title='asdf')
    canvas.cd()
    stack.SetMaximum(maximum*1.8)
    stack.Draw()
    stack.GetXaxis().SetTitle(options.xtitle)
    stack.GetYaxis().SetTitle(options.ytitle)
 
    #from pdb import set_trace; set_trace()
    bkg_sum = None
    if options.show_errors:
        bkg_sum = sum(stack.GetHists())
        print [bkg_sum.GetBinError(i) for i in range(bkg_sum.GetNbinsX()+1)]
        bkg_sum.SetMarkerSize(0)
        bkg_sum.SetFillColor(1)
        bkg_sum.SetFillStyle(3013)
        bkg_sum.legendstyle = 'f'
        bkg_sum.SetTitle("Bkg. Unc.")
        bkg_sum.Draw('pe2,same')

    observed.Draw('same')

    #tries to figure which side the legend goes
    obslist = list(observed)
    sx_mean = obslist[:len(obslist) / 2]
    dx_mean = obslist[len(obslist) / 2:]
    sx_mean = sum(sx_mean) / float(len(sx_mean))
    dx_mean = sum(dx_mean) / float(len(dx_mean))

    num_entries = len(histograms)+1 if bkg_sum else len(histograms)+2
    legend = plotting.Legend(num_entries, rightmargin=0.03, topmargin=0.02, leftmargin=0.45) \
             if sx_mean > dx_mean else \
             plotting.Legend(num_entries, leftmargin=0.03, topmargin=0.02, rightmargin=0.45)
    
    #for sample in samples:
    legend.AddEntry(stack)
    if bkg_sum:
        legend.AddEntry(bkg_sum)
    legend.AddEntry(observed)
    legend.SetEntrySeparation(0.0)
    legend.SetMargin(0.35)
    legend.Draw()
    canvas.Update()

    outfile = os.path.join(os.getcwd(), options.out)
    canvas.SaveAs(outfile )
    logging.info("%s created" % outfile)
    
    
    

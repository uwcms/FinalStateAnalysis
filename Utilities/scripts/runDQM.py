#!/usr/bin/env python
'''
Run the DQM plotting script. The script will run over all variables found in the first root file.

Usage:
    ./runDQM.py [-h] [options] <ntuple root file> [...]

Author: Devin N. Taylor, UW-Madison
'''

import sys
import os
import errno
import ROOT

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)

def python_mkdir(dir):
    '''A function to make a unix directory as well as subdirectories'''
    try:
        os.makedirs(dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else: raise

def get_events(trees):
    '''Get the list of events common to all trees'''
    print 'Getting common events'
    events = []
    for tree in trees:
        tree_events = []
        for row in tree:
            event = row.evt
            lumi = row.lumi
            run = row.run
            event_tuple = (run, lumi, event)
            tree_events.append(event_tuple)
        events.append(tree_events)
        print '  Events: %i' % len(tree_events)
    events_intersection = set(events[0]).intersection(*events)
    print '  Union: %i' % len(events_intersection)
    return events_intersection

def plot_hist(variable,hists):
    '''Plot a single variable with a set of trees'''
    colors = [ROOT.EColor.kRed, ROOT.EColor.kBlue, ROOT.EColor.kGreen]
    names = ['UW PAT-tuple', 'MiniAOD']
    legend = ROOT.TLegend(0.7, 0.78, 0.89, 0.89, "", "brNDC")
    legend.SetFillColor(ROOT.EColor.kWhite)
    legend.SetBorderSize(1)
    min = 0
    max = 0
    for h in range(len(hists)):
        if not hists[h]: continue
        hists[h].SetLineColor(colors[h])
        min_temp = hists[h].GetMinimum(0)
        max_temp = hists[h].GetMaximum()
        if not min or min<min_temp: min = min_temp
        if not max or max>max_temp: max = max_temp
        if h==0:
            hists[h].SetTitle('')
            hists[h].GetXaxis().SetTitle(variable)
            hists[h].Draw('ph')
        else:
            hists[h].Draw('phsame')
        legend.AddEntry(hists[h],names[h],'p')
    legend.Draw('same')
    if min:
        if max/min > 500:
            canvas.SetLogy(1)
        else:
            canvas.SetLogy(0)
    else:
        canvas.SetLogy(0)

def plot_helper(trees,events,savepath,channel):
    '''A helper script for plotting a given channel'''
    # book histograms for each variable
    print 'Booking histograms'
    leaves = trees[0].GetListOfLeaves()
    variables = []
    for leaf in leaves:
        variables.append(leaf.GetName())
    hists = {}
    for v in range(len(variables)):
        var = variables[v]
        hists[var] = []
        for t in range(len(trees)):
            histname = "h%s%s%i" % (var, channel, t)
            print "  "+histname
            if hists[var]:
                hists[var].append(hists[var][0].Clone(histname))
            else:
                tree = trees[t]
                tree.Draw(var+">>"+histname+'temp')
                histtemp = ROOT.gDirectory.Get(histname+'temp')
                min = histtemp.GetXaxis().GetBinLowEdge(histtemp.FindFirstBinAbove(50))
                max = histtemp.GetXaxis().GetBinUpEdge(histtemp.FindLastBinAbove(10))
                if min>0: min = min*0.8
                else: min = min*1.2
                if max>0: max = max*1.2
                else: max = max*0.8
                binning = [100, min, max]
                drawstring = var+">>"+histname+"("+", ".join(str(x) for x in binning)+")"
                tree.Draw(drawstring)
                hist = ROOT.gDirectory.Get(histname)
                if type(hist) is not ROOT.TObject:
                    hist.Reset()
                    hists[var].append(hist)
                else:
                    hists[var].append(0)
    # fill histograms
    print "Filling histograms"
    for t in range(len(trees)):
        print "  Tree %i" % t
        eventnum = 0
        for row in trees[t]:
            if eventnum % 1000 == 0:
                print "    Event %i" % eventnum
            eventnum += 1
            event = row.evt
            lumi = row.lumi
            run = row.run
            event_tuple = (run, lumi, event)
            if event_tuple in events:
                for v in variables:
                    if hists[v][t]:
                        try:
                            attr = getattr(row,v)
                            hists[v][t].Fill(attr)
                        except AttributeError:
                            pass
    # plot histograms and save
    print "Saving histograms"
    python_mkdir(savepath)
    for v in range(len(variables)):
        var = variables[v]
        plot_hist(var,hists[var])
        canvas.SaveAs(savepath+'/'+var+'.png')

def plot_all(filenames,channels,savepath):
    '''A function to plot all variables in a given ntuple'''
    # get the files and channels
    files = []
    for filename in filenames:
        files.append(ROOT.TFile(filename))
    if channels=='all':
        channels = []
        for key in files[0].GetListOfKeys():
            channels.append(key.GetTitle())
    events = []
    for channel in channels:
        channelsave = savepath+'/DQM/'+channel
        # extract each ntuple
        trees = []
        for file in files:
            trees.append(file.Get(channel+'/final/Ntuple'))
        # get common events
        if not events: events = get_events(trees)
        print 'Running over channel: '+ channel
        plot_helper(trees,events,channelsave,channel)


    
            
    print "and save in: "+savepath

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Run DQM plotting script.')
    parser.add_argument('ntuples',metavar='ntuples',type=str,nargs='+',
                        help='Ntuples output from FSA make_ntuples')
    parser.add_argument('--channels',type=str,
                        help='Comma separated list of final states to run over (default all). ex: "e,m,em"')
    parser.add_argument('--savepath',type=str,
                        help='Path to save directory (default pwd)')
    options = parser.parse_args()

    savepath = options.savepath
    if options.savepath==None:
        savepath = os.getcwd()
    if options.channels==None:
        channels = 'all'
    else:
        channels = [x.strip() for x in options.channels.split(',')]

    plot_all(options.ntuples,channels,savepath)

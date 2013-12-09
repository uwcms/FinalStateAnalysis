#! /bin/env python

#import logging
#import sys
#logging.basicConfig(stream=sys.stderr, level=logging.INFO)
from RecoLuminosity.LumiDB import argparse
from progressbar import ETA, ProgressBar, FormatLabel, Bar
from pdb import set_trace
import glob
import os
import ROOT

ROOT.gROOT.SetBatch(True)
#log = logging.getLogger("CorrectFakeRateData")

def txt2tuple(line):
    return tuple([ int(i.strip()) for i in line.split(':') ])

def row2tuple(row):
    return int(row.run), int(row.lumi), int(row.evt)

def GetDbsInfo(query):
    "Interface with the DBS API to get the whatever you want of a requirements. ALWAYS RETURN A LIST OF STRINGS"
    from xml.dom.minidom import parseString
    from DBSAPI.dbsApi import DbsApi
    args = {}
    args['url']='http://cmsdbsprod.cern.ch/cms_dbs_prod_global/servlet/DBSServlet'
    args['version']='DBS_2_0_9'
    args['mode']='POST'
    api = DbsApi(args)
    data = api.executeQuery(query)#"find %s where %s" % (toFind, requirements))
    domresults = parseString(data)
    dbs = domresults.getElementsByTagName('dbs')
    result = dbs[0].getElementsByTagName('results')
    rows=result[0].getElementsByTagName('row')
    retList = []
    for row in rows:
        resultXML = row.getElementsByTagName(toFind)[0]
        node=(resultXML.childNodes)[0] #childNodes should be a one element array
        retList.append(str(node.nodeValue))
    return retList


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infiles', nargs='+')
    parser.add_argument('--pickfile', required=True)
    parser.add_argument('--treepath', required=True)
    parser.add_argument('--outputfile', type=str, default="", help='by default is pickfile_name.root')
    parser.add_argument('--verbose', action='store_true', default=False, help='tell in which file the event was found')
    parser.add_argument('--needle-mode', dest='needle_mode', action='store_true', default=False, help='makes it faster when looking for few events in a lot of files')
    parser.add_argument('--infer-run-epoch', dest='infer_run_epoch', action='store_true', default=False, help='infers the run period, data only!') #HARDCODED!

    args = parser.parse_args()
    input_files = args.infiles

    print "loading events to pick..."
    evts_to_pick = dict([(txt2tuple(line), False) for line in open(args.pickfile).readlines() if line.strip()])
    run_periods  = {
        '2012A' : [190456, 193621], 
        '2012B' : [193833, 196531],
        '2012C' : [198022, 203742],
        '2012D' : [203768, 208686],
        }
    def assign_epoch(evt):
        runno = evt[0]
        for period, runs in run_periods.iteritems():
            if runs[0] <= runno <= runs[1]:
                return period

    if args.infer_run_epoch:
        periods = []
        for event in evts_to_pick:
            periods.append( assign_epoch( event ) )
        if periods:
            periods = list(set(periods))
            print 'restricting to following epochs: %s' % periods
            input_files = filter(lambda x: any(y in x for y in periods), input_files)

    if args.needle_mode:
        good_files = []
        progress= ProgressBar(
            widgets = [
                ETA(),
                Bar('>')],
            maxval = len(input_files) ).start()

        for i, tfile_name in enumerate(input_files):
            progress.update(i+1)
            tfile = ROOT.TFile.Open(tfile_name)
            in_tree = tfile.Get(args.treepath)
            in_tree.GetEntry(0)
            first = row2tuple(in_tree)
            in_tree.GetEntry(in_tree.GetEntries() -1)
            last  = row2tuple(in_tree)
            if any(first <= i <= last for i in evts_to_pick):
                good_files.append( tfile_name )
            tfile.Close()
        print 'restricting to following files: %s' % good_files
        input_files = good_files
            

    print "loading trees..."
    in_tree  = ROOT.TChain(args.treepath) #'mmt/final/Ntuple')
    progress= ProgressBar(
        widgets = [
            ETA(),
            Bar('>')],
        maxval = len(input_files) ).start()
    for n, i in enumerate(input_files):
        progress.update(n+1)
        in_tree.Add(i)

    del progress
    out_name = args.pickfile.split('.')[0]+'.root' if not args.outputfile else args.outputfile
    new_file = ROOT.TFile(out_name,"recreate")
    new_tree = in_tree.CloneTree(0)
    
    evt_in_file  = dict([(i,[]) for i in evts_to_pick])
    picked = 0

    entries = in_tree.GetEntries()
    progress= ProgressBar(
        widgets = [
            ETA(),
            Bar('>')],
        maxval = entries ).start()

    for i, row in enumerate( in_tree ):
        progress.update(i+1)
        etv_tuple = row2tuple(row)
        if etv_tuple in evts_to_pick:
            picked += 1
            evt_in_file[etv_tuple].append(in_tree.GetFile().GetName())
            in_tree.GetEntry(i)
            new_tree.Fill()
            evts_to_pick[etv_tuple] = True

    print "\npicked %i entries" % picked
    print "picked %i events" % len([i for i, j in evts_to_pick.iteritems() if j])
    not_found = [i for i, j in evts_to_pick.iteritems() if not j]
    if len(not_found) > 0:
        print "Following %i events were not found in the files!:" % len(not_found)
        for i in not_found:
            print "%i:%i:%i" % i

    if args.verbose:
        for evt, files in evt_in_file.iteritems():
            print '%i:%i:%i found in ' % evt
            print '%s' % list(set(files))

    new_tree.AutoSave()
    del in_tree
    del new_file

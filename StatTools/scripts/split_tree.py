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
import time
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


ROOT.gROOT.SetBatch(True)
#log = logging.getLogger("CorrectFakeRateData")

def mkdir(obj, name):
    if name not in [i.GetName() for i in obj.GetListOfKeys()]:
        return obj.mkdir(name)
    else:
        return obj.Get(name)

def mkdir_p(obj, path):
    obj.cd()
    newdir = obj
    for i in path.split('/'): 
        newdir = mkdir(newdir, i)
        newdir.cd()
    return newdir
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--infiles' , nargs='+', required=True)
    parser.add_argument('--treepath', type=str, required=True)
    parser.add_argument('--parity'  , type=str, required=True)
    parser.add_argument('--outputfile', type=str, default="goofy.root", help='by default is pickfile_name.root')
    parser.add_argument('--verbose', action='store_true', default=False, help='tell in which file the event was found')

    args = parser.parse_args()
    input_files = args.infiles

    if not (args.parity == 'even' or args.parity == 'odd'):
        raise ValueError("parity argument must be 'even' or 'odd', not %s" % args.parity)
           
    logging.info( "loading trees..." )
    in_tree  = ROOT.TChain(args.treepath)
    for i in input_files:
        in_tree.Add(i)

    
    new_file = ROOT.TFile(args.outputfile, "recreate")
    new_tree = in_tree.CloneTree(0)
    
    entries = in_tree.GetEntries()
    progress= ProgressBar(
        widgets = [
            ETA(),
            Bar('>')],
        maxval = entries ).start()

    for i, row in enumerate( in_tree ):
        progress.update(i+1)
        if args.parity == 'even' and (i % 2) == 0:
            in_tree.GetEntry(i)
            new_tree.Fill()
        elif args.parity == 'odd' and (i % 2) == 1:
            in_tree.GetEntry(i)
            new_tree.Fill()

    new_tree.AutoSave()
    del in_tree
    del new_file

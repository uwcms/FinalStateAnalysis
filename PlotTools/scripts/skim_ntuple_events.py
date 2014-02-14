#!/usr/bin/env python

""" Skim events (rows) using a string cut.

The event list should be passed in via stdin.  The list should be formatted
with one run:lumi:event per line, separated by colon.


Example:

    cat events.txt | skim_ntuple_events.py path/to/tree out.root inputs/*.root

"""

from RecoLuminosity.LumiDB import argparse
import logging

log = logging.getLogger(__name__)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("tree", metavar="path/to/TTree",
                        help="Path in root file to TTree to skim")
    parser.add_argument("output", metavar="output.root",
                        help="Output ROOT file with skimmed Tree")
    parser.add_argument("inputs", metavar="in.root", nargs='+',
                        help="Input ROOT files to skim")
    parser.add_argument("--filter", default="") 

                        #default="/dev/stdin",
                        #metavar='/dev/stdin', dest='evts',
                        #help="Event list .txt file. Default: /dev/stdin")

    args = parser.parse_args()

    import ROOT
    #ROOT.SetBatch(True)

    logging.basicConfig(level=logging.INFO)

    chain = ROOT.TChain(args.tree)

    log.info("Adding %i files", len(args.inputs))

    for in_file in args.inputs:
        chain.Add(in_file)

    #run_lumis = []
    #run_lumi_set = set([])
    #with open(args.evts, 'r') as evts:
    #    for evt in evts:
    #        if not evt.strip():
    #            # skip blank lines
    #            continue
    #        datum = tuple(evt.strip().split(':'))
    #        run_lumis.append(
    #            "(run == %s && lumi == %s && evt == %s)" %
    #            datum
    #        )
    #        run_lumi_set.add(
    #            tuple(int(x) for x in datum)
    #        )
    #
    #log.info("Skimming %i vents", len(run_lumis))

    # Make a huge cut string
    the_cut = args.filter #" || ".join(run_lumis)

    output = ROOT.TFile(args.output, "RECREATE")
    output.cd()

    log.info("Trimming tree...")
    new_tree = chain.CopyTree(the_cut)

    log.info("Trimmed tree has %i entries", new_tree.GetEntries())

    final_run_lumi_set = set()

    log.info("picked %i events" % new_tree.GetEntries())
    #for row in new_tree:
    #    final_run_lumi_set.add((int(row.run), int(row.lumi), int(row.evt)))
    #
    #log.info("corresponding to %i unique events", len(final_run_lumi_set))
    #
    #difference = run_lumi_set - final_run_lumi_set
    #if difference:
    #    log.warning("I couldn't find %i events!", len(difference))
    #    for run, lumi, evt in difference:
    #        print run, lumi, evt

    new_tree.Write()

#!/usr/bin/env python

'''

Given an input directory, find the input ntuple files and put them in one
.txt filelist for each discovered sample.

Filter out duplicate run-lumis in data, optionally in MC as well.

Author: Evan K. Friis, UW

'''

from RecoLuminosity.LumiDB import argparse
import logging
import glob
import os
import sys

log = logging.getLogger("discover_ntuples")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('jobid', help='Job ID')
    parser.add_argument('directory', help='Base directory')
    parser.add_argument('outputdir', help='Output directory')
    parser.add_argument('--meta', default='mm/metaInfo',
                        help='Path to a meta tree, default: mm/metaInfo')
    parser.add_argument('--filtermc', default=False,
                        help='If true, skip MC files with run-lumis that exist'
                        ' in other files.  Might not be correct...')

    args = parser.parse_args()
    import ROOT

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    log.info("Finding input files for job: %s in %s"
             % (args.jobid, args.directory))

    for sample_dir in glob.glob(os.path.join(args.directory, args.jobid, '*')):
        sample_name = os.path.basename(sample_dir)
        log.info("Finding files for sample %s" % sample_name)

        run_lumis = set([])

        with open(os.path.join(
            args.outputdir, sample_name + '.txt'), 'w') as flist:
            for file in glob.glob(os.path.join(sample_dir, '*', '*.root')):
                tfile = ROOT.TFile.Open(file)
                if not tfile:
                    log.warning("Can't open file: %s" % file)
                    flist.write('# corrupt %s\n' % file)
                    continue
                ntuple = tfile.Get(args.meta)
                if not ntuple:
                    log.warning("Can't read ntuple in file: %s" % file)
                    flist.write('# corrupt %s\n' % file)
                    tfile.Close()
                    continue

                # Check to make sure this file doesn't have any lumi dupes
                has_dupes = None
                if 'data' in sample_name or args.filtermc:
                    for row in ntuple:
                        run_lumi = (int(row.run), int(row.lumi))
                        if run_lumi in run_lumis:
                            has_dupes = run_lumi
                            break
                        run_lumis.add(run_lumi)

                if has_dupes:
                    log.error("Duplicate run lumi %s found in file: %s",
                              repr(has_dupes), file)
                    flist.write('# dupe %s\n' % file)
                    tfile.Close()
                    continue
                # Made it!
                flist.write(file + '\n')
                tfile.Close()

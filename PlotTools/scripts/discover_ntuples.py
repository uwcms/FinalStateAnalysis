#!/usr/bin/env python

'''

Given an input directory, find the input ntuple files and put them in one
.txt filelist for each discovered sample.

Author: Evan K. Friis, UW

'''

from RecoLuminosity.LumiDB import argparse
import glob
from hashlib import sha1
import logging
import os
from progressbar import ETA, ProgressBar, FormatLabel, Bar
import shutil
import sys

log = logging.getLogger("discover_ntuples")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


# From http://stackoverflow.com/questions/6963610/
# how-in-python-check-if-two-files-string-and-file-have-same-content
def shafile(filename):
    with open(filename, "rb") as f:
        return sha1(f.read()).hexdigest()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('jobid', help='Job ID')
    parser.add_argument('directory', help='Base directory')
    parser.add_argument('outputdir', help='Output directory')
    parser.add_argument('--meta', default='mm/metaInfo',
                        help='Path to a meta tree, default: mm/metaInfo')
    parser.add_argument('--force', default=False, action='store_true',
                        help='If specified, check files even if they '
                        ' have an older timestamp than previously output')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='More output')

    args = parser.parse_args()
    print args
    if args.verbose:
        log.setLevel(logging.DEBUG)

    import ROOT

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    log.info("Finding input files for job: %s in %s"
             % (args.jobid, args.directory))

    for sample_dir in glob.glob(os.path.join(args.directory, args.jobid, '*')):
        sample_name = os.path.basename(sample_dir)
        if not os.path.isdir(sample_dir):
            log.info("skipping object %s" % sample_name)
            continue
        log.info("Finding files for sample %s" % sample_name)
        log.info("Looking for  %s" % args.meta)

        output_txt = os.path.join(args.outputdir, sample_name + '.txt')
        # Do work in a temporary directory
        output_tmp = output_txt.replace('.txt', '.tmp')

        previous_files = set([])
        if os.path.exists(output_txt):
            log.debug("-- Output already exists - "
                      "finding new and re-checking broken.")
            with open(output_txt, 'r') as current:
                for line in current.readlines():
                    if '#' not in line:
                        previous_files.add(line.strip())

        with open(output_tmp, 'w') as flist:
            all_files = glob.glob(os.path.join(sample_dir, '*', '*.root')) + \
                glob.glob(os.path.join(sample_dir, '*.root'))
            pbar = ProgressBar(widgets=[FormatLabel(
                'Checked %(value)i/' + str(len(all_files)) + ' files. '),
                ETA(), Bar('>')], maxval=len(all_files)).start()

            for i, file in enumerate(all_files):
                pbar.update(i)
                # Always write if we have found + checked it OK before
                if args.force or file not in previous_files:
                    tfile = ROOT.TFile.Open(file)
                    if not tfile:
                        log.warning("-- Can't open file: %s" % file)
                        flist.write('# corrupt %s\n' % file)
                        continue
                    ntuple = tfile.Get(args.meta)
                    if not ntuple:
                        log.warning("-- Can't read ntuple in file: %s" % file)
                        flist.write('# corrupt %s\n' % file)
                        continue
                    tfile.Close()
                # Made it!
                flist.write(file + '\n')

        # Check if we found anything new in the .txt file
        # Don't update if we didn't, so rake knows nothing has changed
        if not os.path.exists(output_txt):
            shutil.move(output_tmp, output_txt)
            log.debug("-- Completed sample %s", sample_dir)
        elif shafile(output_txt) != shafile(output_tmp):
            # content has changed
            shutil.move(output_tmp, output_txt)
            log.debug("-- Completed sample %s - new files found", sample_dir)
        else:
            # Nothing has changed, remove the tmp
            log.debug("-- Completed sample %s - no new files found",
                      sample_dir)
            os.remove(output_tmp)

        log.info('Finished finding files for %s' % sample_name)

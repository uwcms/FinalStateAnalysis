#!/usr/bin/env python

'''

Given an input directory, find the input ntuple files and put them in one
.txt filelist for each discovered sample.

Author: Evan K. Friis, UW

'''

from RecoLuminosity.LumiDB import argparse
import contextlib
import glob
from hashlib import sha1
import logging
import os
import tempfile
import shutil
import sys

from progressbar import ETA, ProgressBar, FormatLabel, Bar

log = logging.getLogger("discover_ntuples")
logging.basicConfig(stream=sys.stderr, level=logging.INFO)


def get_previous_files(output_txt):
    """ Returns the set of valid files in the output_txt list. """
    previous_files = set()
    if os.path.exists(output_txt):
        log.debug("-- Output already exists - "
                  "finding new and re-checking broken.")
        with open(output_txt, 'r') as current:
            for line in current.readlines():
                if '#' not in line:
                    previous_files.add(line.strip())
    return previous_files


@contextlib.contextmanager
def open_update_if_changed(output_txt, sample):
    """ Yields a smart-updating file object.

    The file at output_file will be written with the new content if it does not
    exist or if the new content differs from what is currently in output_file.

    """
    # From http://stackoverflow.com/questions/6963610/
    # how-in-python-check-if-two-files-string-and-file-have-same-content
    def shafile(filename):
        with open(filename, "rb") as f:
            return sha1(f.read()).hexdigest()

    with tempfile.NamedTemporaryFile() as output_tmp:
        yield output_tmp
        output_tmp.flush()
        # Check if we found anything new in the .txt file
        # Don't update if we didn't, so rake knows nothing has changed
        if not os.path.exists(output_txt):
            shutil.copyfile(output_tmp.name, output_txt)
            log.debug("-- Completed sample %s", sample)
        elif shafile(output_txt) != shafile(output_tmp.name):
            # content has changed
            shutil.copyfile(output_tmp.name, output_txt)
            log.debug("-- Completed sample %s - new files found", sample)
        else:
            # Nothing has changed, remove the tmp
            log.debug("-- Completed sample %s - no new files found", sample)


def find_sample_dirs(search_dirs, jobid):
    """ Find all samples and files for a given job ID and search path.

    For each sample, yields a tuple with (sample, search_dir, list_of_files).
    A sample is returned only the first time it is found in the search path.

    """
    samples_found = set()
    for search_dir in search_dirs:
        log.info("Searching for samples in %s", search_dir)
        for sample_dir in glob.glob(os.path.join(search_dir, args.jobid, '*')):
            sample_name = os.path.basename(sample_dir)
            # Take the sample from the first match in the search path
            if sample_name in samples_found:
                continue
            if not os.path.isdir(sample_dir):
                log.info("skipping object %s" % sample_name)
                continue
            log.info("Finding files for sample %s" % sample_name)
            all_files = glob.glob(os.path.join(sample_dir, '*', '*.root'))
            all_files += glob.glob(os.path.join(sample_dir, '*.root'))
            if not all_files:
                log.info("No files in %s, skipping" % sample_dir)
                continue
            samples_found.add(sample_name)
            yield (sample_name, search_dir, all_files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('jobid', help='Job ID')
    parser.add_argument('directory',
                        help='Base directory(ies).  If this is a colon (:) '
                        'separated list of directories, it is used as a'
                        ' search path (like $MEGAPATH)')
    parser.add_argument('outputdir', help='Output directory')
    parser.add_argument('--meta', default='mm/metaInfo',
                        help='Path to a meta tree, default: mm/metaInfo')
    parser.add_argument('--histo', default='mt/summedWeights',
                        help='Path to a meta histo, default: mt/summedWeights')
    parser.add_argument('--relative', default=False, action='store_true',
                        help='Output paths relative to input directory(ies)')
    parser.add_argument('--force', default=False, action='store_true',
                        help='If specified, check files even if they '
                        ' have an older timestamp than previously output')
    parser.add_argument('--no-check', dest='nocheck', default=False,
                        action='store_true',
                        help='If specified, never check files for corruption.')
    parser.add_argument('--verbose', default=False, action='store_true',
                        help='More output')

    args = parser.parse_args()
    print args
    if args.verbose:
        log.setLevel(logging.DEBUG)

    override_keyword   = 'OVERRIDE_META_TREE_'
    meta_override_keys = filter(lambda x: x.startswith(override_keyword), os.environ.keys())
    meta_override      = [(i.replace(override_keyword,''), os.environ[i]) for i in meta_override_keys]
    def get_meta_treename(sample):
        for key, value in meta_override:
            if sample.startswith(key):
                return value
        return args.meta
    def get_meta_histoname(sample):
        for key, value in meta_override:
            if sample.startswith(key):
                return value
        return args.histo

    # We do this here to prevent ROOT from messing with sys.argv
    import ROOT

    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)

    log.info("Finding input files for job: %s in %s"
             % (args.jobid, args.directory))

    for sample_name, search_dir, all_files in find_sample_dirs(
            args.directory.split(':'), args.jobid):

        sumEventsAll=0 

        tree_name   = get_meta_treename( sample_name )
        histo_name   = get_meta_histoname( sample_name )

        log.info("Finding files for sample %s" % sample_name)
        log.info("Looking for tree  %s" %  tree_name)
        log.info("Looking for histo %s" %  histo_name)
   
        print histo_name
        print tree_name
        print "!!!!!!!!!!!!!!!!!"

        output_txt = os.path.join(args.outputdir, sample_name + '.txt')
        output_weights_txt  = os.path.join(args.outputdir, sample_name + '_weight.log')
        previous_files = get_previous_files(output_txt)
        with open_update_if_changed(output_txt, sample_name) as flist:
            pbar = ProgressBar(widgets=[FormatLabel(
                'Checked %(value)i/' + str(len(all_files)) + ' files. '),
                ETA(), Bar('>')], maxval=len(all_files)).start()

            sumEventsAll=0
            for i, file in enumerate(all_files):
                pbar.update(i)
                filepath = file
                if args.relative:
                    filepath = os.path.relpath(file, search_dir)
                # Always write if we have found + checked it OK before
                if not args.nocheck and (args.force
                                         or file not in previous_files):
                    tfile = ROOT.TFile.Open(file)
                    if not tfile:
                        log.warning("-- Can't open file: %s" % file)
                        flist.write('# corrupt %s\n' % filepath)
                        continue
                    ntuple = tfile.Get(tree_name)
                    histo = tfile.Get(histo_name)
                    sumEventsAll+=histo.Integral()
                    if not ntuple:
                        log.warning("-- Can't read ntuple in file: %s"
                                    % file)
                        flist.write('# corrupt %s\n' % filepath)
                        continue
                    tfile.Close()
                # Made it!
                flist.write(filepath + '\n')

        fweight=open(output_weights_txt,"a")
        fweight.write("Weights: %f \n" %sumEventsAll )       
        log.info('\nFinished finding files for %s' % sample_name)

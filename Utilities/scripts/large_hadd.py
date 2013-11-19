#!/usr/bin/env python
"""
Enables running hadd on a large number of files w/out crashing hadd.

Author: D. Austin Belknap, UW-Madison
"""

import sys
import os
import argparse

from Queue import Queue
from threading import Thread


def hadd(outfile, infiles):
    """This makes a simple call to hadd"""
    cmd = "hadd " + outfile + " " + " ".join(infiles)
    os.system(cmd)


def worker(q):
    """
    Runs a single instance of hadd from the job queue.
    """
    while True:
        outfile, infiles = q.get()
        print outfile
        hadd(outfile, infiles)
        q.task_done()


def batch_hadd(outfile, infiles, n_files=200, n_threads=1):
    """
    This runs hadd on smaller chunks of files and merges them into intermediate
    files. Then hadd is run to merge the intermidate files into the final file.
    """

    # split the list of input files into sublists
    split_infiles = [infiles[x:x+n_files]
                     for x in xrange(0, len(infiles), n_files)]

    intermediate_files = []

    user_name = os.environ['USER']

    q = Queue()

    # Create worker threads
    for i in range(n_threads):
        t = Thread(target=worker, args=(q,))
        t.daemon = True
        t.start()

    # Queue up the individual hadd jobs
    for i, file_list in enumerate(split_infiles):
        # Use unique names for the intermediate files to avoid collisions
        intm_file = ("/tmp/tmp_" + user_name + "_" + str(i) + "_" +
                     os.path.basename(outfile))
        intermediate_files.append(intm_file)
        q.put((intm_file, file_list))

    # Block until all hadd threads have completed
    q.join()

    # merge the intermediate files together
    hadd(outfile, intermediate_files)

    # remove the intermediate files
    os.system("rm " + " ".join(intermediate_files))


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Run hadd on a large number '
                                                 'of ROOT files')
    parser.add_argument('outfile', type=str,
                        help='The name of the output ROOT file.')
    parser.add_argument('infiles', nargs='+',
                        help='A list of input ROOT files to merge.')
    parser.add_argument('--files-per-job', type=int, default=200,
                        help='Number of files to merge with hadd at one time. '
                             'Default is 200.')
    parser.add_argument('--n-threads', type=int, default=1,
                        help='Number of instances of hadd to run at one time. '
                             'Default is 1.')
    args = parser.parse_args(argv)

    return args


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    batch_hadd(args.outfile, args.infiles, args.files_per_job, args.n_threads)

    return 0


if __name__ == "__main__":
    status = main()
    sys.exit(status)

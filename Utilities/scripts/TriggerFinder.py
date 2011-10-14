#!/usr/bin/env python

'''

Parses prescales of triggers for a given JSON file.

'''

import os
import sys
import json
import logging
import copy
from RecoLuminosity.LumiDB import argparse, lumiCalcAPI, sessionManager

log = logging.getLogger("TriggerFinder")

def average(items):
    return sum(items)*1./len(items)


def flatten_json(run_lumis):
    output = {}
    for run, ls_ranges in run_lumis.iteritems():
        flattened_ls = []
        for ls_range in ls_ranges:
            flattened_ls.extend(xrange(ls_range[0], ls_range[1]+1))
        output[int(run)] = flattened_ls
    return output

def trim_json(run_lumis, first_run, last_run, max_lumis=3):
    log.info("Trimming json to use %i lumis per run, from %i-%i",
             max_lumis, first_run, last_run)
    # Trim a run/ls list to take sample fewer lumis per run
    output = {}
    for run, ls_list in run_lumis.iteritems():
        if run < first_run:
            continue
        if last_run > 0 and run > last_run:
            continue
        n_ls = len(ls_list)
        take_every = max(int(n_ls/max_lumis), 1)
        output[run] = []
        for i, ls in enumerate(ls_list):
            if i % take_every == 0:
                output[run].append(ls)
    return output

def collapse_runs(run_hlt_infos):
    first_run = None
    current_hlt_info = None
    current_hlt_prescales = {}
    last_identical_run = None
    for run, hlt_info in run_hlt_infos:
        if first_run is None:
            first_run = run
            last_identical_run = run
            current_hlt_info = sorted(hlt_info.keys())
            current_hlt_details = {}
            for path, path_info in hlt_info.iteritems():
                # Get the list of prescales
                current_hlt_details[path] = path_info[2]

        elif current_hlt_info == sorted(hlt_info.keys()):
            last_identical_run = run
            for path, path_info in hlt_info.iteritems():
                # Get the list of prescales
                current_hlt_details[path].extend(path_info[2])
        else:
            yield (first_run, last_identical_run, current_hlt_details)
            first_run = run
            last_identical_run = run
            current_hlt_info = sorted(hlt_info.keys())
            current_hlt_details = {}
            for path, path_info in hlt_info.iteritems():
                # Get the list of prescales
                current_hlt_details[path] = path_info[2]
    yield (first_run, last_identical_run, current_hlt_details)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description = "Find the best trigger for a series of runs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', dest='inputfile',action='store',
                        required=True,
                        help='run/lumi json file')

    parser.add_argument('-p', dest='pattern',action='store',
                        required=True, nargs='+', type=str,
                        help='One or more HLT path patterns')

    parser.add_argument('-t', dest='trim',action='store',
                        required=False, type=int,
                        default = -1,
                        help='How many LS to sample per run. -1 = all')

    parser.add_argument('-firstRun', dest='first',action='store',
                        required=False, type=int,
                        default = 1, help='First run to use')

    parser.add_argument('-lastRun', dest='last',action='store',
                        required=False, type=int,
                        default = -1, help='Last run to use')

    parser.add_argument('-c',dest='connect',action='store',
                        required=False,
                        help='connect string to lumiDB,optional',
                        default='frontier://LumiCalc/CMS_LUMI_PROD')
    parser.add_argument('-P',dest='authpath',action='store',
                        required=False,
                        help='path to authentication file (optional)')
    parser.add_argument('--debug',dest='debug',action='store_true',
                        help='debug')

    options=parser.parse_args()
    if options.authpath:
        os.environ['CORAL_AUTH_PATH'] = options.authpath

    svc=sessionManager.sessionManager(
        options.connect, authpath=options.authpath, debugON=options.debug)
    session=svc.openSession(isReadOnly=True, cpp2sqltype=[
        ('unsigned int','NUMBER(10)'), ('unsigned long long','NUMBER(20)')])

    input_json_file = open(options.inputfile, 'r')
    run_ls = flatten_json(json.loads(input_json_file.read()))
    run_ls = trim_json(run_ls, options.first, options.last, options.trim)

    withL1Pass = False
    withHLTAccept = False

    pattern_results = {}

    for pattern in options.pattern:
        for run in sorted(run_ls.keys()):
            small_run_ls = { run : run_ls[run] }
            sys.stdout.write("Querying pattern: %s in run %i" % (pattern, run))
            sys.stdout.write("                     ")
            sys.stdout.write('\r')
            try:
                session.transaction().start(True)
                result = lumiCalcAPI.hltForRange(
                    session.nominalSchema(),
                    small_run_ls,
                    hltpathname=None,
                    hltpathpattern=pattern,
                    withL1Pass=withL1Pass,
                    withHLTAccept=withHLTAccept)
                pattern_results.setdefault(pattern, {}).update(result)
            except:
                sys.stderr.write(
                    "\nException detected processing run %i, skipping\n" % run)
            finally:
                session.transaction().commit()

    # Now we want tto find, for each run, all the unprescaled triggers.
    # Just go through each run, and check what the lowest prescale is for each
    # pattern.
    run_info = {}
    for pattern, run_ls in pattern_results.iteritems():
        # Check which paths had what prescales in each LS
        for run, lumilist in run_ls.iteritems():
            path_prescales = {}
            for ls, path_list in lumilist:
                for path, prescale, l1pass, hltaccept in path_list:
                    path_prescales.setdefault(path, []).append(prescale)
            path_results = run_info.setdefault(run, {})
            # Get the avg. prescale and dead time for each path
            for path, prescale_list in path_prescales.iteritems():
                if not prescale_list or max(prescale_list) == 0:
                    continue
                dead_ls = len([x for x in prescale_list if x == 0])
                avg_prescale = sum(prescale_list)/(len(prescale_list) - dead_ls)
                nom_prescale = min(x for x in prescale_list if x != 0)
                path_results[path] = (dead_ls, nom_prescale, prescale_list)

    clean_run_info = {}
    # Filter by prescale
    for run, paths in run_info.iteritems():
        clean_paths = {}
        for path, path_info in paths.iteritems():
            dead_ls, nom_prescale, prescale_list = path_info
            if nom_prescale == 1:
                clean_paths[path] = path_info
        clean_run_info[run] = clean_paths

    # Now collapse the runs
    sorted_runs = sorted(clean_run_info.keys())
    collapsed = collapse_runs((run, clean_run_info[run]) for run in sorted_runs)

    sys.stdout.write('\n\n')
    for x in collapsed:
        paths = sorted(x[2].keys())
        path_info = ', '.join('%s[%0.1f]' % (path, average(x[2][path])) for
                              path in paths)
        output = '%i-%i : %s' % (x[0], x[1], path_info)
        sys.stdout.write(output + '\n')

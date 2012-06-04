#!/usr/bin/env python

'''

Build a condor_submit file to compute the grid of CLs points.

Run with --help for options.

'''

import json
import logging
import math
import os
import shutil
import sys

from RecoLuminosity.LumiDB import argparse

# Setup logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO, filemode='w'
)
log = logging.getLogger("make_grid_submission")

prelude_template = '''

X509UserProxy        = /tmp/x509up_u{UID}
Universe             = vanilla
Executable           = {executable}
GetEnv               = true
Environment          = "dboard_taskId=efriis-login06.hep.wisc.edu-$(Cluster) dboard_jobId=$(Process) dboard_sid=efriis-login06.hep.wisc.edu-$(Cluster).$(Process) dboard_application=Analysis dboard_exe=fwklite dboard_tool=farmout dboard_scheduler=local-condor dboard_taskType=analysis dboard_broker=local-condor-login06.hep.wisc.edu dboard_user=efriis dboard_SyncCE=cmsgrid02.hep.wisc.edu CMS_DASHBOARD_REPORTER=/afs/hep.wisc.edu/cms/sw/cmsdashboard_reporter FARMOUT_DASHBOARD_REPORTER=/afs/hep.wisc.edu/cms/cmsprod/bin/farmout_dashboard.sh   FARMOUT_VSIZE_LIMIT=3000 "
Copy_To_Spool        = false
Notification         = never
WhenToTransferOutput = On_Exit
+IsFastQueueJob      = True
ImageSize            = 921600
+DiskUsage           = 2048000
Requirements         = TARGET.Arch == "X86_64" && TARGET.HasAFS_OSG && IsSlowSlot=!=true && TARGET.UWCMS_CVMFS_Exists && TARGET.UWCMS_CVMFS_Revision >= 1215 && TARGET.Memory > 900
# stop jobs from running if they blow up
periodic_hold        = DiskUsage/1024 > 10.0*2000
'''

submit_template = '''
InitialDir           = {submit_dir}
Arguments            = "{card_file_base} {exclusion_point} {output_file} --toys={toys} --iter={iter} --seed={seed} --job=$(Process) --mass={mass}"
Transfer_Input_Files = {card_file_full_path}
output               = {log_name}.$(Process).out
error                = {log_name}.$(Process).err
Log                  = {log_name}.$(Process).log
Queue {njobs}

'''

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog=os.path.basename(sys.argv[0]),
        description = "Make a condor submission file to make CLs grids",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-i', dest='cardfile', action='store',
                        required=True, help='path to card file')

    parser.add_argument('-toys', dest='toys',action='store',
                        required=False, type=int,
                        default = 100, help='Number of toys per iteration')

    parser.add_argument('-iter', dest='iter',action='store',
                        required=False, type=int,
                        default = 10, help='Number of iterations per job')

    parser.add_argument('-jobs', dest='jobs',action='store',
                        required=False, type=int,
                        default = 25,
                        help='Number of jobs to queue for each point')

    range_grp = parser.add_mutually_exclusive_group( required=True)

    range_grp.add_argument('-r', '--range', nargs=2, dest='range',action='store',
                        type=float,
                        help='Min and max exclusion to scan')

    range_grp.add_argument('-g', '--guess-limits', dest='guess', type=str,
                           required=False, default='',
                           help='An asymptotic CLs file to get the min and max')

    parser.add_argument('-mass', dest='mass',action='store',
                        required=True, type=int,
                        help='Mass of signal in card')

    parser.add_argument('-seed', dest='seed',action='store',
                        default=123456,
                        required=False, type=int,
                        help='Base random seed')

    parser.add_argument('-steps', dest='steps',action='store',
                        required=False, type=int, default=20,
                        help='N exclusion points to check')

    parser.add_argument('-log', dest='log',action='store_true',
                        required=False, default=False,
                        help='If true, step logarithmically')

    parser.add_argument('-submitdir', dest='submitdir', action='store',
                        required=True, type=str,
                        help='Folder to submit files jobs in')

    options=parser.parse_args()

    # Create submit direcotry
    if not os.path.exists(options.submitdir):
        log.info("Creating submit directory %s", options.submitdir)
        os.makedirs(options.submitdir)

    submit_file_path = os.path.join(options.submitdir, 'submit')
    log.info("Creating submit file %s", submit_file_path)
    submit_file = open(submit_file_path, 'w')

    if not os.path.exists(options.cardfile):
        raise IOError("Can't open input card file %s" % options.cardfile)

    card_source = options.cardfile
    card_dest = os.path.join(options.submitdir,
                             os.path.basename(options.cardfile))
    shutil.copy(card_source, card_dest)

    submit_file.write(prelude_template.format(
        UID = os.geteuid(),
        executable=os.path.expandvars(
            '$CMSSW_BASE/bin/$SCRAM_ARCH/run_grid_point.sh'),
    ))

    # Figure out max and min
    min = None
    max = None
    if options.range:
        min = options.range[0]
        max = options.range[1]
        assert(max > min)
    elif options.guess:
        log.info("Getting asymptotic range")
        with open(options.guess, 'r') as asymp_guess:
            asymp = json.load(asymp_guess)
            min = asymp['-2']*0.3
            max = asymp['+2']*1.3
        log.info("Got asymptotic range: [%0.2f, %0.2f]", min, max)
    else:
        raise ValueError("Must specify either guess or range!")

    # Build signal strength points to scan
    points = None
    if options.log:
        dx = math.log(max/min)/(options.steps-1)
        points = [ min * math.exp(dx*i) for i in range(options.steps) ]
    else:
        points = [ min + i*(max - min)/(options.steps-1) for i in range(options.steps) ]

    # Run along grid points
    for i, point in enumerate(points):
        seed = options.mass*options.seed + i
        submit_statement = submit_template.format(
            submit_dir = options.submitdir,
            card_file_base = os.path.basename(card_dest),
            card_file_full_path = card_dest,
            exclusion_point = point,
            toys = options.toys,
            iter = options.iter,
            mass = options.mass,
            log_name = "point_%i" % i,
            output_file = 'point_%i_$(Process).root' % i,
            seed = seed,
            njobs = options.jobs,
        )
        submit_file.write(submit_statement + '\n')
    log.info("Generated %i points x %i jobs/point = %i condor jobs",
             options.steps, options.jobs, options.steps*options.jobs)
    log.info("At each point, %i jobs x %i iterations x %i toys per call: %i toys/point",
             options.jobs, options.iter, options.toys,
             options.jobs*options.iter*options.toys)

    print "Now run:"
    print "condor_submit %s/submit" % options.submitdir

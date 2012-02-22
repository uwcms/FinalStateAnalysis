#!/usr/bin/env python

'''

Build a condor_submit file to compute the grid of CLs points.

Run with --help for options.

'''

import logging
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

    parser.add_argument('-min', dest='min',action='store',
                        required=True, type=float,
                        help='Min exclusion to scan')

    parser.add_argument('-max', dest='max',action='store',
                        required=True, type=float,
                        help='Max exclusion to scan')

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


    # Run along grid points
    for i in range(options.steps):
        seed = options.mass*options.seed + i
        point = options.min + i*(options.max - options.min)/(options.steps-1.)
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
    log.info("Generated %i x %i jobs = %i",
             options.steps, options.jobs, options.steps*options.jobs)
    log.info("Total combine calls: %i x %i x %i = %i",
             options.steps, options.jobs, options.iter,
             options.steps*options.jobs*options.iter)
    log.info("Toys per call: %i", options.toys)

    print "Now run condor_submit %s/submit" % options.submitdir

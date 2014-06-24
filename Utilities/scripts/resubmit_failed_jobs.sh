#!/bin/sh

# Description of Unix script:
#  - list dag.status files
#  - find files with errors
#  - replace dag.status with dag.rescue
#  - select lines that match rescue files available 
#  - reverse sort (so we get rescue002 before rescue001)
#  - sort by first column deliminated by '/' and select first unique (rescue002 not rescue001)
#  - pass latest rescue file to farmoutAnalysisJobs for resubmission

if [ $# -lt 1 ]
then
    echo "Usage: bash resubmit_failed_jobs.sh JOB_ID"
    exit 1
fi

JOBID=$1
SCRATCH_PATH=/nfs_scratch/$USER/$JOBID

EXISTING_RESCUE_DAGS=$(ls -1 $SCRATCH_PATH/*/dags/*dag.rescue*)
ls $SCRATCH_PATH/*/dags/*dag.status | xargs grep -lir ERR | sed -e "s|status|rescue|" | sed 's/^/^/' | grep -f- $EXISTING_RESCUE_DAGS | sort -r | sort -u -t/ -k1,1 | xargs -I{} -n 1 farmoutAnalysisJobs --rescue-dag-file={}

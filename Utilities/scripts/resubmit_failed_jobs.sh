#!/bin/sh

if [ $# -lt 1 ]
then
    echo "Usage: resubmit_failed_jobs.sh JOB_ID"
    exit 1
fi

JOBID=$1
SCRATCH_PATH=/scratch/$USER/$JOBID

ls $SCRATCH_PATH/*/dags/dag.dag.status | xargs grep -lir ERR | sed -e "s|status|rescue001|" | xargs -I{} -n 1 farmoutAnalysisJobs --rescue-dag-file={}

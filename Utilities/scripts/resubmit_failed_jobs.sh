#!/bin/sh

if [ $# -lt 1 ]
then
    echo "Usage: resubmit_failed_jobs.sh JOB_ID"
    exit 1
fi

JOBID=$1
SCRATCH_PATH=/nfs_scratch/$USER/$JOBID

#ls $SCRATCH_PATH/*/dags/*dag.status | xargs grep -lir ERR | sed -e "s|status|rescue001|" | xargs -I{} -n 1 farmoutAnalysisJobs --rescue-dag-file={}
ls $SCRATCH_PATH/*/dags/*dag.status | xargs grep -lir ERR | sed -e "s|status|rescue|" | sed 's/^/^/' | grep -f- <(ls -1 $SCRATCH_PATH/*/dags/*dag.rescue*) | sort -r | sort -u -t/ -k1,1 | xargs -I{} -n 1 farmoutAnalysisJobs --rescue-dag-file={}
# what this does:
# list dag.status files
# find files with errors
# replace dag.status with dag.rescue
# select lines that match rescue files available 
# reverse sort (so we get rescue002 before rescue001)
# sort by first column deliminated by '/' and select first unique (rescue002 not rescue001)
# pass latest rescue file to farmoutAnalysisJobs for resubmission

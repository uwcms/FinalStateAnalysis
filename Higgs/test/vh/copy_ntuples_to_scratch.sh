#!/bin/bash

# Copy ntuples from HDFS to scratch
# Usage: ./copy_ntuples_to_scratch.sh jobid 

JOBID=$1

OUTPUTDIR=$scratch/data/$JOBID

mkdir -p $OUTPUTDIR

# http://stackoverflow.com/questions/3231804/in-bash-how-to-add-are-you-sure-y-n-to-any-command-or-alias
read -p "Copy everything in $hdfs/$JOBID/ to $OUTPUTDIR? <y/N> " prompt
if [[ $prompt == "y" || $prompt == "Y" || $prompt == "yes" || $prompt == "Yes" ]]
then
  find $hdfs/$JOBID/* -name "*.root" | xargs -n 1 -P 3 -I {} cp -r -u -v {} $OUTPUTDIR
else
  exit 0
fi

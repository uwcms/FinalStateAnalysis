#!/bin/bash

# Parse the job reports for the inputs to get the luminosity
# Usage: ./get_processed_lumis.sh jobid submit_dir
# The script should be able to find the job report xml files in
# 
# <submit_dir>/<jobid>/<sample>/submit/*/*.xml
# 
# The output is inputs/<jobid>/<sample>.lumimask.json

JOBID=$1
SOURCE=$2
SAMPLE=$3

echo "Finding job reports for $SAMPLE with id $JOBID in $SOURCE"

OUTPUTDIR=inputs/$JOBID/

mkdir -p $OUTPUTDIR

sampledir=$SOURCE/$JOBID/$SAMPLE/
sample=`basename $sampledir`
echo -n "Getting xml files for $sample - got "
count=`ls $sampledir/submit/*/*xml | wc -l`
echo "$count files"
jobReportSummary --json-out $OUTPUTDIR/$sample.lumimask.json $sampledir/submit/*/*xml 

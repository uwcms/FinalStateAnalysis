#!/bin/bash

# A stupid script for discovering the input ntuple files.
# Usage: ./get_inputs.sh jobid $hdfs
# Generates inputs/[jobid]/[sample1].txt
#           inputs/[jobid]/[sample2].txt
#           etc

JOBID=$1 
SOURCE=$2

echo "Finding input files for job: $JOBID in $SOURCE"

OUTPUTDIR=inputs/$JOBID

mkdir -p $OUTPUTDIR

for sampledir in `ls -d $SOURCE/$JOBID/*`
do
  sample=`basename $sampledir`
  echo -n "Getting data files for $sample - got "
  ls $sampledir/*/*root | sed "s|^|file:|" | root_file_check.py > $OUTPUTDIR/${sample}.txt
  echo -n `cat $OUTPUTDIR/${sample}.txt | wc -l `
  echo " files"
done

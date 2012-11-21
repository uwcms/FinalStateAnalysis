#!/bin/bash

# Run me once.

set -o errexit
set -o nounset

export jobid=2012-07-19-7TeV-Higgs
export s=/scratch/efriis

# Make cython wrapper
export afile=`find /scratch/efriis/data/$jobid | grep root | head -n 1`
echo $afile
rake "make_wrapper[$afile, mt/final/Ntuple, MuTauTree]"
rake MuTauTree.so

# Figure out what inputs we have
rake "meta:getinputs[$jobid, $s/data]"
# Only care about VH for now.
ls inputs/$jobid/*txt | grep -v -e "VH_120" -e "TT" | xargs rm 
rake "meta:getmeta[inputs/$jobid, mm/metaInfo, 7]"

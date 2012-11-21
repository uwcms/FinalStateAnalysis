#!/bin/bash

# Setup the cython proxies, find input ntuple files, and compute luminosity.

source jobid.sh
export datasrc=/scratch/efriis/data/
export jobid=$jobid7
export afile=`find $datasrc/$jobid | grep root | head -n 1`

rake "make_wrapper[$afile, eet/final/Ntuple, EETauTree]"
rake "make_wrapper[$afile, emt/final/Ntuple, EMuTauTree]"
rake "make_wrapper[$afile, mmt/final/Ntuple, MuMuTauTree]"
rake "make_wrapper[$afile, mmm/final/Ntuple, MuMuMuTree]"
rake "make_wrapper[$afile, mm/final/Ntuple, MuMuTree]"
rake "make_wrapper[$afile, em/final/Ntuple, EMuTree]"
rake "make_wrapper[$afile, ee/final/Ntuple, EETree]"

ls *pyx | sed "s|pyx|so|" | xargs rake 

rake "meta:getinputs[$jobid, $datasrc]"
rake "meta:getmeta[inputs/$jobid, mm/metaInfo, 7]"

export jobid=$jobid8
rake "meta:getinputs[$jobid, $datasrc]"
# Use the 7TeV WH samples for 8TeV
pushd inputs/$jobid/
# Symlink the list of input files and the counts of the number of events.
# For the effectively lumis, we have to recompute using the 8 TeV x-section.
ls ../../inputs/$jobid7/WH_*HWW* | grep -v lumicalc | xargs -n 1 ln -s 
popd
rake "meta:getmeta[inputs/$jobid, mm/metaInfo, 8]"


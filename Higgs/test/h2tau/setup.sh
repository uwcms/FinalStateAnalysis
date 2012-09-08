#!/bin/bash

# Get the data
export jobid=2012-07-29-7TeV-Higgs
export datasrc=/scratch/efriis/data/
export jobid7TeV=$jobid
export afile=`find $datasrc/$jobid | grep root | head -n 1`

# Build the cython wrappers
rake "make_wrapper[$afile, em/final/Ntuple, EMuTree]"
ls *pyx | sed "s|pyx|so|" | xargs rake 

rake "meta:getinputs[$jobid, $datasrc]"
rake "meta:getmeta[inputs/$jobid, mm/metaInfo, 7]"

export jobid=2012-07-29-8TeV-Higgs
rake "meta:getinputs[$jobid, $datasrc]"
rake "meta:getmeta[inputs/$jobid, mm/metaInfo, 8]"


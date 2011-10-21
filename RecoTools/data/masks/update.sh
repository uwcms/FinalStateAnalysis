#!/bin/bash

# Update the local directory to match the official one at:
# /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/

base=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/

# Get 2011 prompt jsons
rsync -v -n -a --exclude="*CMSSW*" --exclude="*/*" --include="*.txt" $base/Collisions11/7TeV/Prompt/ .
# Get 2011 reprocessing jsons
rsync -v -n -a --exclude="*CMSSW*" --exclude="*/*" --include="*.txt" $base/Collisions11/7TeV/Reprocessing/ .

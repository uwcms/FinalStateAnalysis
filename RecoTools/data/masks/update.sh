#!/bin/bash

# Update the local directory to match the official one at:
# Just run it.  ./update.sh
# /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/

base=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/

# Get 2011 prompt jsons
rsync -v -a --exclude="*CMSSW*" --exclude="*/" --exclude="*/*" --include="Cert*.txt" --exclude="*" $base/Collisions11/7TeV/Prompt/ .
# Get 2011 reprocessing jsons
rsync -v -a --exclude="*CMSSW*" --exclude="*/" --exclude="*/*" --include="Cert*.txt" --exclude="*" $base/Collisions11/7TeV/Reprocessing/ .

#!/bin/bash

# Update the local directory to match the official one at:
# Just run it.  ./update.sh
# /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/

base=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/

# Get 2011 prompt jsons
rsync -v -a --exclude="*CMSSW*" --exclude="*/" --exclude="*/*" --include="Cert*.txt" --exclude="*" $base/Collisions11/7TeV/Prompt/ .
# Get 2011 reprocessing jsons
rsync -v -a --exclude="*CMSSW*" --exclude="*/" --exclude="*/*" --include="Cert*.txt" --exclude="*" $base/Collisions11/7TeV/Reprocessing/ .
# Get 2011 DCSOnly jsons
rsync -v -a --exclude="*CMSSW*" --exclude="*/" --exclude="*/*" --include="*json*DCSOnly*.txt" --exclude="*" $base/Collisions11/7TeV/DCSOnly/ .

# Get 2012 prompt jsons
rsync -v -a --exclude="*CMSSW*" --exclude="*/" --exclude="*/*" --include="Cert*.txt" --exclude="*" $base/Collisions12/8TeV/Prompt/ .
# Get 2012 reprocessing jsons
rsync -v -a --exclude="*CMSSW*" --exclude="*/" --exclude="*/*" --include="Cert*.txt" --exclude="*" $base/Collisions12/8TeV/Reprocessing/ .
# Get 2012 DCSOnly jsons
rsync -v -a --exclude="*CMSSW*" --exclude="*/" --exclude="*/*" --include="*json*DCSOnly*.txt" --exclude="*" $base/Collisions12/8TeV/DCSOnly/ .

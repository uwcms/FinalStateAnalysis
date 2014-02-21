#!/bin/bash

# Install the MVA MET

set -o errexit
set -o nounset

: ${CMSSW_BASE:?"CMSSW_BASE is not set! Run cmsenv before recipe.sh"}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`

pushd $CMSSW_BASE/src

if [ "$MAJOR_VERSION" -eq "5" ]; then
  # https://hypernews.cern.ch/HyperNews/CMS/get/met/333.html
  git cms-addpkg PhysicsTools/PatAlgos
  git cms-merge-topic cms-analysis-tools:5_3_14-updateSelectorUtils
  git cms-merge-topic cms-analysis-tools:5_3_13_patch2-testNewTau
  git cms-merge-topic -u TaiSakuma:53X-met-131120-01
  git-cms-merge-topic -u cms-met:53X-MVaNoPuMET-20131217-01
else
  echo "Sorry, 42X not ported yet. For 7 TeV, we should move to the rereco"
fi

popd

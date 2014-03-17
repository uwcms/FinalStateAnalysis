#!/bin/bash

# Install the MVA MET

set -o errexit
set -o nounset

: ${CMSSW_BASE:?"CMSSW_BASE is not set! Run cmsenv before recipe.sh"}
pushd $CMSSW_BASE/src

if [ "$CMSSW_VERSION" == "CMSSW_5_3_14" ]; then
  # https://hypernews.cern.ch/HyperNews/CMS/get/met/333.html
  git cms-addpkg PhysicsTools/PatAlgos
  git cms-merge-topic cms-analysis-tools:5_3_14-updateSelectorUtils
  git cms-merge-topic cms-analysis-tools:5_3_13_patch2-testNewTau
  git cms-merge-topic -u TaiSakuma:53X-met-131120-01
  git-cms-merge-topic -u cms-met:53X-MVaNoPuMET-20131217-01
else
  echo "MVAMET recipe not available for releases other than 5_3_14."
fi

popd

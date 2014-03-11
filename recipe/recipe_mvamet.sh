#!/bin/bash

echo Install the MVA MET

set -o errexit
set -o nounset

: ${CMSSW_BASE:?"CMSSW_BASE is not set! Run cmsenv before recipe.sh"}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`
LEAST_VERSION=`echo $CMSSW_VERSION | awk -F_ '{print $4}'`

pushd $CMSSW_BASE/src

if [ "$MAJOR_VERSION" -eq "5" ]; then
  # Add MVA MET
  if [ "$LEAST_VERSION" -lt 14 ] && [ "$MINOR_VERSION" -eq "3" ]; then
      echo "The mva met stuff will ONLY work in version > 5.3.14! If you want to stay in 539, you need CSV access."
  else
      #from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SWGuideCMSDataAnalysisSchoolJetMetAnalysis#Step_2_Checkout_additional_softw
      git cms-addpkg PhysicsTools/PatAlgos
      git cms-merge-topic -u TaiSakuma:53X-met-131120-01
      git cms-merge-topic -u cms-analysis-tools:5_3_14-updateSelectorUtils
      git cms-merge-topic -u cms-analysis-tools:5_3_13_patch2-testNewTau
      git cms-merge-topic -u cms-met:53X-MVaNoPuMET-20131217-01
  fi
else
  echo "Sorry, 42X not ported yet. For 7 TeV, we should move to the rereco"
fi

popd

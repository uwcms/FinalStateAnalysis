#!/bin/bash
set -o errexit
set -o nounset

pushd $CMSSW_BASE/src

if [ "$PATPROD" = "1" ]
then
  # https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATReleaseNotes52X#Fix_jet_tools_CMSSW_5_3_14
  if [ "$MVAMET" = "1" ]; then
      echo "PAT recipe already done in recipe_mvamet.sh"
  else
      echo "Applying PAT recipe"
      git cms-addpkg PhysicsTools/PatAlgos
      git cms-merge-topic cms-analysis-tools:5_3_13_patch2-testNewTau
  fi

  # https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#53X
  # need to re-run HPS reco, but no tags needed

  echo "Quark/Gluon Tagger v1-2-6"
  git clone https://github.com/amarini/QuarkGluonTagger.git
  pushd $CMSSW_BASE/src/QuarkGluonTagger
  git checkout v1-2-6
  pushd $CMSSW_BASE/src

  echo "Checking out EGamma POG recipe for electron corrections"
  git clone https://github.com/cms-analysis/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools
  pushd $CMSSW_BASE/src/EgammaAnalysis/ElectronTools
  git checkout EgammaAnalysis-ElectronTools-FB_4Jun2013
  pushd $CMSSW_BASE/src

  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/Egamma_PassAll.patch
  set -o errexit

  #Get weight files
  pushd $CMSSW_BASE/src/EgammaAnalysis/ElectronTools/data
  cat download.url | xargs wget
  popd

  #echo "Patching data format"
  ##git cms-addpkg DataFormats/PatCandidates  # done already in recipe_common.sh
  #set +o errexit
  #patch -N -p0 < FinalStateAnalysis/recipe/patches/PATObject.h.patch
  #set -o errexit

  #echo "Applying Marias b-tag patch"   
  ##doubtful that we need it now... but just in case...
  #set +o errexit
  #patch -N -p0 < FinalStateAnalysis/recipe/patches/PhysicsToolsPatAlgos_fix_btags_52X.patch
  #set -o errexit
fi

popd

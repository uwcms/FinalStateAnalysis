#!/bin/bash
set -o errexit
set -o nounset


# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`


# Tags for 7XX

pushd $CMSSW_BASE/src

echo "Checking out PAT dataformats"

if [ "$LIMITS" = "1" ]
then
   echo ""     
   echo "======================================="
   echo "You shouldnt run limits/fits from here." 
   echo "LIMITS should be run from 6XX, and do not require the rest of the machinery. Please, change area."
   echo "Check https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideHiggsAnalysisCombinedLimit for updates"
   echo "======================================="
   echo ""     
fi


if [ "$PATPROD" = "1" ]
then
  echo "Checking out tuple production tags"

  echo "Need to update recipe for Quark Gluon Jet ID - which is the correct tag?"
  #echo "Downloading Quark Gluon Jet ID"
  #cvs co -r v1-2-3 -d QuarkGluonTagger/EightTeV UserCode/tomc/QuarkGluonTagger/EightTeV
  # Quark-gluon tagging
  git clone https://github.com/amarini/QuarkGluonTagger.git
  pushd $CMSSW_BASE/src/QuarkGluonTagger
  git checkout v1-2-6
  pushd $CMSSW_BASE/src

#   echo "Checking out Tau POG recipe" # https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePFTauID#Tau_ID_2014_preparation_for_Run
#   if [ "$MINOR_VERSION" -eq "0" ]; then
#     git cms-merge-topic -u cms-tau-pog:CMSSW_7_0_X_taus  
#   fi
#   if [ "$MINOR_VERSION" -eq "1" ]; then
#     git cms-merge-topic -u cms-tau-pog:CMSSW_7_1_X_taus  
#   fi  

  echo "Checking out EGamma MVA ID for miniAOD"
  if [ "$MINOR_VERSION" -eq "0" ]
  then
    git cms-merge-topic HuguesBrun:addTheElecIDMVAoutputCSA14 #needed until mva added by default
  elif [ "$MINOR_VERSION" -eq "2" ]
  then
    git cms-merge-topic HuguesBrun:trigElecIdInCommonIsoSelection720
  fi

  echo "Checking out EGamma POG recipe for electron corrections"
  #Following Volker's instructions
  #git cms-cvs-history import V09-00-01 RecoEgamma/EgammaTools
  #git clone https://github.com/cms-analysis/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools
  #pushd $CMSSW_BASE/src/EgammaAnalysis/ElectronTools
  #git checkout EgammaAnalysis-ElectronTools-FB_4Jun2013
  #pushd $CMSSW_BASE/src
  git cms-addpkg EgammaAnalysis/ElectronTools

  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/Egamma_PassAll.patch
  set -o errexit

  #Get weight files
  pushd $CMSSW_BASE/src/EgammaAnalysis/ElectronTools/data
  cat download.url | xargs wget
  popd
  #apply some pathces to make everythin work
  #set +o errexit
  #patch -N -p0 < FinalStateAnalysis/recipe/patches/PATObject.h.patch
  #set -o errexit

fi

popd


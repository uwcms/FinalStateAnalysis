#!/bin/bash
set -o errexit
set -o nounset

# Tags for 52X

pushd $CMSSW_BASE/src

echo "Checking out PAT dataformats"

# these 3 could be updated easily - well documented 
git cms-cvs-history import V06-05-06-10 DataFormats/PatCandidates
git cms-cvs-history import V08-09-58  PhysicsTools/PatAlgos
git cms-cvs-history import  V03-09-28 PhysicsTools/PatUtils

# These conflict with the MVA MET RecoMET tags.
rm -f PhysicsTools/PatAlgos/plugins/PATMHTProducer.*
rm -f PhysicsTools/PatAlgos/plugins/PATMHTProducer.*

git cms-cvs-history import V03-03-12-02 RecoMET/METProducers
git cms-cvs-history import V00-02-14 DataFormats/StdDictionaries
git cms-cvs-history import V00-03-16 CommonTools/ParticleFlow

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
  git cms-cvs-history import V02-05-11 DataFormats/CaloRecHit
  git cms-cvs-history import V00-00-70 FWCore/GuiBrowsers
  git cms-cvs-history import V03-03-12-02 RecoMET/METProducers
  #24/10/2012 LAG -- PF Isolation for Photons
  git cms-cvs-history import V15-02-06 RecoParticleFlow/PFProducer
  git cms-cvs-history import V00-00-12  CommonTools/RecoUtils
  #    V00-00-12, cvs up -r 1.4 CommonTools/RecoUtils/BuildFile.xml
  git cms-cvs-history import V02-06-05 DataFormats/HLTReco
  git cms-cvs-history import V04-06-09 JetMETCorrections/Type1MET
  git cms-cvs-history import V01-08-00 RecoBTag/SecondaryVertex
  git cms-cvs-history import V02-02-00 RecoVertex/AdaptiveVertexFinder

  echo "Need to update recipe for Quark Gluon Jet ID - which is the correct tag?"
  #echo "Downloading Quark Gluon Jet ID"
  #cvs co -r v1-2-3 -d QuarkGluonTagger/EightTeV UserCode/tomc/QuarkGluonTagger/EightTeV
  # Quark-gluon tagging
  git clone https://github.com/amarini/QuarkGluonTagger.git
  pushd $CMSSW_BASE/src/QuarkGluonTagger
  git checkout v1-2-6
  pushd $CMSSW_BASE/src

  echo "Checking out Tau POG recipe"
  git cms-cvs-history import V01-04-25 RecoTauTag/RecoTau
  git cms-cvs-history import V01-04-13 RecoTauTag/Configuration
  git cms-cvs-history import V00-04-00 CondFormats/EgammaObjects

  #git cms-addpkg RecoTauTag/RecoTau  # recipe from christian, the merge topic complained in 539, it will probably work in 5314
  # to be checked
  #git cms-merge-topic -u cms-tau-pog:CMSSW_5_3_X


  echo "Checking out EGamma POG recipe for electron corrections"
  #cvs co -r V09-00-01 RecoEgamma/EgammaTools
  #cvs co -r FB_4Jun2013 EgammaAnalysis/ElectronTools
  git cms-cvs-history import V09-00-01 RecoEgamma/EgammaTools
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
  #apply some pathces to make everythin work
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/PATObject.h.patch
  set -o errexit

  echo "Applying Marias b-tag patch"   
  #doubtful that we need it now... but just in case...
  set +o errexit
  patch -N -p0 < FinalStateAnalysis/recipe/patches/PhysicsToolsPatAlgos_fix_btags_52X.patch
  set -o errexit
fi

popd


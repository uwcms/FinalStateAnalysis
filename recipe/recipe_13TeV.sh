#!/bin/bash
set -o errexit
set -o nounset

HZZ=${HZZ:-0}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`


# Tags for 7XX

pushd $CMSSW_BASE/src

echo "Need to update recipe for Quark Gluon Jet ID - which is the correct tag?"
#echo "Downloading Quark Gluon Jet ID"
# Quark-gluon tagging
git clone https://github.com/amarini/QuarkGluonTagger.git
pushd $CMSSW_BASE/src/QuarkGluonTagger
git checkout v1-2-6
popd


# These recipes are sort of "hacky" at the moment, pending updates to the official EGM ID framework
# From https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Working_points_for_PHYS14_sample (cut based)
# and  https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateElectronIdentificationRun2 (MVA)
echo "Checking out electron IDs for miniAOD in CMSSW_7_2_X"
git cms-merge-topic HuguesBrun:trigElecIdInCommonIsoSelection720
cp /afs/cern.ch/user/i/ikrav/public/EGMCode/GsfEleFull5x5SigmaIEtaIEtaCut72X.cc RecoEgamma/ElectronIdentification/plugins/cuts/
cp /afs/cern.ch/user/i/ikrav/public/EGMCode/cutBasedElectronID_PHYS14_PU20bx25_V0_miniAOD_cff.py RecoEgamma/ElectronIdentification/python/Identification/
cp /afs/cern.ch/user/i/ikrav/public/EGMCode/cutBasedElectronID_PHYS14_PU20bx25_V1_miniAOD_cff.py RecoEgamma/ElectronIdentification/python/Identification/

echo "Checking out EGamma POG recipe for electron corrections"
git cms-addpkg EgammaAnalysis/ElectronTools

set +o errexit
patch -N -p0 < FinalStateAnalysis/recipe/patches/Egamma_PassAll.patch
set -o errexit

#Get weight files
pushd $CMSSW_BASE/src/EgammaAnalysis/ElectronTools/data
cat download.url | xargs wget
popd

# echo "Checking out recipe for mvamet"
# # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MVAMet#CMSSW_7_2_X_requires_slc6_MiniAO
# git-cms-merge-topic -u cms-met:72X-13TeV-Training-30Jan15
# pushd $CMSSW_BASE/src/RecoMET/METPUSubtraction
# git clone https://github.com/rfriese/RecoMET-METPUSubtraction data -b 72X-13TeV-Phys14_25_V4-26Mar15
# popd

# HZZ MELA, MEKD etc.
if [ "$HZZ" = "1" ]; then
    echo "Checking out ZZ MELA and Higgs combine"
    git clone https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
fi

popd


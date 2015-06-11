#!/bin/bash
set -o errexit
set -o nounset

HZZ=${HZZ:-0}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`


# Tags for 7XX

pushd $CMSSW_BASE/src

# recipe for electron cutbased ids (https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Recipe_for_regular_users_for_74X)
git cms-merge-topic 9003 #this is the version that is in CMSSW_7_4_X
rm -rf RecoEgamma/ElectronIdentification/data
git clone https://github.com/cms-data/RecoEgamma-ElectronIdentification.git RecoEgamma/ElectronIdentification/data
rm -rf RecoEgamma/PhotonIdentification/data
git clone https://github.com/cms-data/RecoEgamma-PhotonIdentification.git RecoEgamma/PhotonIdentification/data

# HZZ MELA, MEKD etc.
if [ "$HZZ" = "1" ]; then
    echo "Checking out ZZ MELA and Higgs combine"
    git clone https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement
    git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
fi

popd


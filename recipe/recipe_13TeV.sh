#!/bin/bash
set -o errexit
set -o nounset

HZZ=${HZZ:-0}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`


# Tags for 7XX

pushd $CMSSW_BASE/src

# electron and photon id
git cms-merge-topic ikrav:egm_id_7.4.12_v1
# and energy scale and resolution corrections
git cms-merge-topic gpetruc:ElectronRun2PromptCalib-74X

# HZZ MELA, MEKD etc.
if [ "$HZZ" = "1" ]; then
    echo "Checking out ZZ MELA and Higgs combine"
    git clone https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement
    git clone -b 74x-root6 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
fi

echo "Checking out mva met and svFit material:"
# svFit packaged checked out for everyone so that svFit code in FSA compiles
git clone git@github.com:veelken/SVFit_standalone.git TauAnalysis/SVfitStandalone
pushd TauAnalysis/SVfitStandalone
git checkout svFit_2015Apr03
popd


git cms-addpkg RecoMET/METPUSubtraction
pushd RecoMET/METPUSubtraction/
git clone https://github.com/rfriese/RecoMET-METPUSubtraction data -b 74X-13TeV-Summer15-July2015
git clone https://github.com/cms-data/RecoMET-METPUSubtraction.git
popd

echo "####################################################################"
echo "###   Before using mva MEt make sure to do the following...      ###"
echo "###   Go Edit: RecoMET/METPUSubtraction/python/mvaPFMET_cff.py   ###"
echo "###   Add at line 41:    etaBinnedWeights = cms.bool(False),     ###"
echo "###   And await a real fix...                                    ###"
echo "####################################################################"

popd


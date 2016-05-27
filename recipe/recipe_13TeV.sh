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
#git cms-merge-topic ikrav:egm_id_7.4.12_v1

# and energy scale and resolution corrections
#git cms-merge-topic gpetruc:ElectronRun2PromptCalib-74X

# 74X met corrections (no HF)
#git cms-merge-topic -u cms-met:METCorUnc74X

# HZZ MELA, MEKD etc.
if [ "$HZZ" = "1" ]; then
    echo "Checking out ZZ MELA and Higgs combine"
    git clone https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement
    pushd ZZMatrixElement
    git checkout -b from-V00-02-01-patch1 V00-02-01-patch1
    popd
    git clone -b 74x-root6 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
fi

echo "Checking out mva met and svFit material:"
# svFit packaged checked out for everyone so that svFit code in FSA compiles
git clone git@github.com:veelken/SVFit_standalone.git TauAnalysis/SVfitStandalone
pushd TauAnalysis/SVfitStandalone
git checkout svFit_2015Apr03
popd

# Checkout mva met code
git cms-addpkg RecoMET/METPUSubtraction
git cms-addpkg DataFormats/METReco
#add the MVA MET when it is working in CMSSW8XY
#git remote add -f mvamet https://github.com/rfriese/cmssw.git
#git checkout MVAMET2_beta_0.6 -b mvamet


popd


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

# HZZ MELA, MEKD etc.
if [ "$HZZ" = "1" ]; then
    echo "Checking out ZZ MELA and Higgs combine"
    git clone https://github.com/cms-analysis/HiggsAnalysis-ZZMatrixElement.git ZZMatrixElement
    git clone -b 74x-root6 https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
fi

if [ "$HTT" = "1" ]; then
    echo "Checking out HTT material: mva met and svFit"
    git cms-addpkg RecoMET/METPUSubtraction/
    git clone https://github.com/cms-data/RecoMET-METPUSubtraction RecoMET/METPUSubtraction/data -b 74X-13TeV-Summer15-July2015
    echo "######################################"
    echo "### Now go edit XXXX              ###"
    echo "######################################"
fi

popd


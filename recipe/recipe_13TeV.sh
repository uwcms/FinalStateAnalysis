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

echo "Checking out material to run new tau MVA ID"
pushd $CMSSW_BASE/src
git cms-addpkg DataFormats/PatCandidates
git cms-addpkg PhysicsTools/PatAlgos
git cms-addpkg RecoTauTag/Configuration
git cms-addpkg RecoTauTag/RecoTau

cd RecoTauTag/RecoTau
git remote add tau-pog git@github.com:cms-tau-pog/cmssw.git
git fetch tau-pog
git merge tau-pog/CMSSW_8_0_X_tau-pog_miniAOD-backport-tauID
popd

echo "Checking out MET Filters"
git cms-merge-topic -u cms-met:fromCMSSW_8_0_20_postICHEPfilter

echo "Checking out bad muon filter stuff"
git cms-merge-topic gpetruc:badMuonFilters_80X_v2

echo "Checking out mva met and svFit material:"
# svFit packaged checked out for everyone so that svFit code in FSA compiles
git clone git@github.com:veelken/SVFit_standalone.git TauAnalysis/SVfitStandalone
pushd TauAnalysis/SVfitStandalone
git checkout svFit_2015Apr03
popd

git cms-merge-topic cms-met:METRecipe_8020
git cms-merge-topic ikrav:egm_id_80X_v2
git cms-merge-topic rafaellopesdesa:RegressionCheckNegEnergy
git cms-merge-topic cms-egamma:EGM_gain_v1

pushd EgammaAnalysis/ElectronTools/data
git clone -b Moriond17_gainSwitch_unc https://github.com/ECALELFS/ScalesSmearings.git
popd

echo "Checking out Rivet Tools for Higgs Template Cross Section"
pushd $CMSSW_BASE/src
git cms-merge-topic -u perrozzi:HTXS_clean
popd

# Checkout mva met code
#git cms-addpkg RecoMET/METPUSubtraction
#git cms-addpkg DataFormats/METReco
#git remote add -f mvamet https://github.com/rfriese/cmssw.git
#git checkout mvamet/mvamet8020 -b mvamet
#mkdir RecoMET/METPUSubtraction/data
#cd RecoMET/METPUSubtraction/data
#wget https://github.com/rfriese/cmssw/raw/MVAMET2_beta_0.6/RecoMET/METPUSubtraction/data/weightfile.root
cd $CMSSW_BASE/src



popd


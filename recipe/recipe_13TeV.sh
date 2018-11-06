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

pushd $CMSSW_BASE/src
git cms-addpkg GeneratorInterface/RivetInterface
cd GeneratorInterface/RivetInterface/plugins
rm HTXSRivetProducer.cc
wget https://raw.githubusercontent.com/perrozzi/cmssw/HTXS_clean/GeneratorInterface/RivetInterface/plugins/HTXSRivetProducer.cc
cd -

### Merge-topics ###

# Get code for electron V2 ID's (trained on 94X MC's)
git cms-merge-topic guitargeek:EgammaID_949

# Get code for electron scale & smear corrections
git cms-merge-topic cms-egamma:EgammaPostRecoTools_940

# Get recipes to re-correct MET (also for ECAL noise)
git cms-merge-topic cms-met:METFixEE2017_949_v2

# Get deep Tau & DPF based Tau ID (and Tau ID Embedder) (deep Tau & DPF Tau optional)
git cms-merge-topic ocolegro:dpfisolation # consists updated version of runTauIdMVA.py (RecoTauTag/RecoTau/python/runTauIdMVA.py). Originally, this .py file comes from https://raw.githubusercontent.com/greyxray/TauAnalysisTools/CMSSW_9_4_X_tau-pog_RunIIFall17/TauAnalysisTools/python/runTauIdMVA.py

# Get latest anti-e discriminator MVA6v2 (2017 training) (optional)
#TODO some files need to be copied from afs. A proper integration of the files will be done by Tau POG. To be followed up.
git cms-merge-topic cms-tau-pog:CMSSW_9_4_X_tau-pog_updateAntiEDisc


#echo "Checking out material to run new tau MVA ID"
#pushd $CMSSW_BASE/src
#git cms-addpkg DataFormats/PatCandidates
#git cms-addpkg PhysicsTools/PatAlgos
#git cms-addpkg RecoTauTag/Configuration
#git cms-addpkg RecoTauTag/RecoTau
#
#git cms-addpkg RecoMET/METFilters
#git cms-addpkg EgammaAnalysis/ElectronTools
#git cms-addpkg RecoEgamma/EgammaTools
#git cms-addpkg RecoEgamma/ElectronIdentification
#git cms-addpkg RecoJets/JetProducers
#
###waiting CMSSW9XY directions
##cd RecoTauTag/RecoTau
##git remote add tau-pog git@github.com:cms-tau-pog/cmssw.git
##git fetch tau-pog
##git merge tau-pog/CMSSW_8_0_X_tau-pog_miniAOD-backport-tauID
##popd
#
##echo "Checking out MET Filters"
##git cms-merge-topic -u cms-met:fromCMSSW_8_0_20_postICHEPfilter
#
##echo "Checking out bad muon filter stuff"
##git cms-merge-topic gpetruc:badMuonFilters_80X_v2
#
echo "Checking out mva met and svFit material:"
# svFit packaged checked out for everyone so that svFit code in FSA compiles
git clone git@github.com:veelken/SVFit_standalone.git TauAnalysis/SVfitStandalone
pushd TauAnalysis/SVfitStandalone
git checkout svFit_2015Apr03
popd
#
##git cms-merge-topic cms-met:METRecipe_8020
##git cms-merge-topic ikrav:egm_id_80X_v2
##git cms-merge-topic rafaellopesdesa:RegressionCheckNegEnergy
##git cms-merge-topic cms-egamma:EGM_gain_v1
#
#
###Doesn't work. Need to clone and modify my version
##pushd $CMSSW_BASE/src
##git remote add cms-egamma git@github.com:cms-egamma/cmssw.git
##git fetch cms-egamma
###git checkout cms-egamma/CMSSW_9_0_X -- EgammaAnalysis/ElectronTools
##git checkout cms-egamma/EGM_gain_v1 -- EgammaAnalysis/ElectronTools/python/regressionWeights_cfi.py
##git checkout cms-egamma/EGM_gain_v1 -- EgammaAnalysis/ElectronTools/python/regressionApplication_cff.py
##popd
#
###cd EgammaAnalysis/ElectronTools/data
###git clone https://github.com/ECALELFS/ScalesSmearings.git
###cd - 
##pushd EgammaAnalysis/ElectronTools/data
##git clone -b Moriond17_gainSwitch_unc https://github.com/ECALELFS/ScalesSmearings.git
##popd
#
###echo "Checking out Rivet Tools for Higgs Template Cross Section"
###pushd $CMSSW_BASE/src
##cd $CMSSW_BASE/src
###git cms-addpkg SimDataFormats/HTXS
##git remote add perozzi https://github.com/perrozzi/cmssw.git
##git fetch perozzi
##git checkout perozzi/HTXS_clean -- SimDataFormats/HTXS
##git remote rm perozzi
####git cms-merge-topic -u perrozzi:HTXS_clean
##popd
#
#
#cd $CMSSW_BASE/src
#git cms-merge-topic guitargeek:ElectronID_MVA2017_940pre3
#git cms-merge-topic lsoffi:CMSSW_9_4_0_pre3_TnP
#scram b -j 9
#
#
#cd $CMSSW_BASE/external
## below, you may have a different architecture, this is just one example from lxplus
#cd slc6_amd64_gcc630/
#git clone https://github.com/lsoffi/RecoEgamma-PhotonIdentification.git data/RecoEgamma/PhotonIdentification/data
#cd data/RecoEgamma/PhotonIdentification/data
#git checkout CMSSW_9_4_0_pre3_TnP
#cd $CMSSW_BASE/external
#cd slc6_amd64_gcc630/
#git clone https://github.com/lsoffi/RecoEgamma-ElectronIdentification.git data/RecoEgamma/ElectronIdentification/data
#cd data/RecoEgamma/ElectronIdentification/data
#git checkout CMSSW_9_4_0_pre3_TnP
# Go back to the src/
cd $CMSSW_BASE/src

popd


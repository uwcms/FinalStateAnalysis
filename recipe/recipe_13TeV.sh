#!/bin/bash
set -o errexit
set -o nounset

HZZ=${HZZ:-0}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-10]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-10]\)_\([0-9]\)_.*|\2|"`


pushd $CMSSW_BASE/src

cd $CMSSW_BASE/src
git cms-merge-topic cms-egamma:EgammaPostRecoTools
git cms-addpkg EgammaAnalysis/ElectronTools
rm EgammaAnalysis/ElectronTools/data -rf
git clone git@github.com:cms-egamma/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data
cd EgammaAnalysis/ElectronTools/data
git checkout ScalesSmearing2018_Dev
cd -
git cms-merge-topic cms-egamma:EgammaPostRecoTools_dev

cd $CMSSW_BASE/src

#Add DeepTau code from Tau POG repository (note "-u" option preventing checkout of unnecessary stuff)
#git cms-merge-topic -u cms-tau-pog:CMSSW_10_2_X_tau-pog_DeepTau2017v2
#git cms-merge-topic -u cms-tau-pog:CMSSW_10_2_X_tau-pog_DeepTau2017v2p1_nanoAOD
git cms-merge-topic -u cms-tau-pog:CMSSW_10_2_X_tau-pog_DeepTau2017v2
git cms-merge-topic -u cms-tau-pog:CMSSW_10_2_X_tau-pog_deepTauVetoPCA
#Add 2017v2 training file by using "git clone" or wget
# git clone -b DeepTau2017v2_alone https://github.com/cms-tau-pog/RecoTauTag-TrainingFiles.git RecoTauTag/TrainingFiles/data
#wget https://github.com/cms-tau-pog/RecoTauTag-TrainingFiles/raw/DeepTau2017v2/DeepTauId/deepTau_2017v2p6_e6_core.pb -P RecoTauTag/TrainingFiles/data/DeepTauId
#wget https://github.com/cms-tau-pog/RecoTauTag-TrainingFiles/raw/DeepTau2017v2/DeepTauId/deepTau_2017v2p6_e6_inner.pb -P RecoTauTag/TrainingFiles/data/DeepTauId
#wget https://github.com/cms-tau-pog/RecoTauTag-TrainingFiles/raw/DeepTau2017v2/DeepTauId/deepTau_2017v2p6_e6_outer.pb -P RecoTauTag/TrainingFiles/data/DeepTauId

# MET filter
git cms-addpkg RecoMET/METFilters

cd $CMSSW_BASE/src
git cms-addpkg SimDataFormats/HTXS
git cms-addpkg GeneratorInterface/RivetInterface

popd


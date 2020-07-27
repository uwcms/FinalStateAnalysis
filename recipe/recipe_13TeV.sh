#!/bin/bash
set -o errexit
set -o nounset

HZZ=${HZZ:-0}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-10]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-10]\)_\([0-9]\)_.*|\2|"`


pushd $CMSSW_BASE/src

cd $CMSSW_BASE/src
git cms-merge-topic cms-egamma:EgammaPostRecoTools #just adds in an extra file to have a setup function to make things easier 
git cms-merge-topic cms-egamma:PhotonIDValueMapSpeedup1029 #optional but speeds up the photon ID value module so things fun faster
git cms-merge-topic cms-egamma:slava77-btvDictFix_10210 #fixes the Run2018D dictionary issue, see https://github.com/cms-sw/cmssw/issues/26182, may not be necessary for later releases, try it first and see if it works
#now to add the scale and smearing for 2018 (eventually this will not be necessary in later releases but is harmless to do regardless)
git cms-addpkg EgammaAnalysis/ElectronTools
rm EgammaAnalysis/ElectronTools/data -rf
git clone git@github.com:cms-data/EgammaAnalysis-ElectronTools.git EgammaAnalysis/ElectronTools/data
cd $CMSSW_BASE/src

#Add DeepTau code from Tau POG repository (note "-u" option preventing checkout of unnecessary stuff)
git cms-merge-topic -u cms-tau-pog:CMSSW_10_2_X_tau-pog_DeepTau2017v2p1_nanoAOD

# MET filter
git cms-addpkg RecoMET/METFilters

cd $CMSSW_BASE/src
git cms-addpkg SimDataFormats/HTXS
git cms-addpkg GeneratorInterface/RivetInterface

##cov met fix embedded
#cp -r RecoEgamma/EgammaTools temporary
#git cms-merge-topic -u KIT-CMS:embedded_metcov_fix
#rm -rf RecoEgamma/EgammaTools
#cp -r temporary RecoEgamma/EgammaTools
#rm -rf temporary
#
#jet pu ID new training
git cms-addpkg  RecoJets/JetProducers 
git clone -b 94X_weights_DYJets_inc_v2 git@github.com:cms-jet/PUjetID.git PUJetIDweights/
cp PUJetIDweights/weights/pileupJetId_{94,102}X_Eta* $CMSSW_BASE/src/RecoJets/JetProducers/data/
rm -rf PUJetIDweights/  ### If needed
git cms-merge-topic -u alefisico:PUID_102X


popd


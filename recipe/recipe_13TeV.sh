#!/bin/bash
set -o errexit
set -o nounset

HZZ=${HZZ:-0}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-10]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-10]\)_\([0-9]\)_.*|\2|"`


pushd $CMSSW_BASE/src

git cms-addpkg SimDataFormats/HTXS
git cms-addpkg GeneratorInterface/RivetInterface
cd GeneratorInterface/RivetInterface/plugins/
rm HTXSRivetProducer.cc 
wget https://raw.githubusercontent.com/amarini/cmssw/htxs_stage1p1_cmssw949_v2/GeneratorInterface/RivetInterface/plugins/HTXSRivetProducer.cc

cd $CMSSW_BASE/src
cd SimDataFormats/HTXS/interface/
rm HiggsTemplateCrossSections.h 
wget https://raw.githubusercontent.com/amarini/cmssw/htxs_stage1p1_cmssw949_v2/SimDataFormats/HTXS/interface/HiggsTemplateCrossSections.h

cd $CMSSW_BASE/src
cd GeneratorInterface/RivetInterface/src/
rm HiggsTemplateCrossSections.cc 
wget https://raw.githubusercontent.com/amarini/cmssw/htxs_stage1p1_cmssw949_v2/GeneratorInterface/RivetInterface/src/HiggsTemplateCrossSections.cc


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

popd


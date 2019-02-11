#!/bin/bash
set -o errexit
set -o nounset

HZZ=${HZZ:-0}

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-10]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-10]\)_\([0-9]\)_.*|\2|"`


pushd $CMSSW_BASE/src

#pushd $CMSSW_BASE/src
#git cms-addpkg GeneratorInterface/RivetInterface
#cd GeneratorInterface/RivetInterface/plugins
#rm HTXSRivetProducer.cc
#wget https://raw.githubusercontent.com/perrozzi/cmssw/HTXS_clean/GeneratorInterface/RivetInterface/plugins/HTXSRivetProducer.cc
#cd -

cd $CMSSW_BASE/src

popd


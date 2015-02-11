#!/bin/bash
set -o errexit
set -o nounset

pushd $CMSSW_BASE/src

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`

# To install lumiCalc.py
if [ "$LUMI" = "1" ]
then
git clone https://github.com/cms-sw/RecoLuminosity-LumiDB.git RecoLuminosity/LumiDB
pushd $CMSSW_BASE/src/RecoLuminosity/LumiDB
git checkout V04-02-10
pushd $CMSSW_BASE/src
fi

# Only checkout PAT tuple production dependencies if requested.
if [ "$PATPROD" = "1" ]
then
    # Set the compile time flag which enables PAT modules that have external
    # dependencies.
    cat > $CMSSW_BASE/src/FinalStateAnalysis/PatTools/interface/PATProductionFlag.h << EOF
#define ENABLE_PAT_PROD
EOF

else
    cat > $CMSSW_BASE/src/FinalStateAnalysis/PatTools/interface/PATProductionFlag.h << EOF
//#define ENABLE_PAT_PROD
EOF

fi

popd

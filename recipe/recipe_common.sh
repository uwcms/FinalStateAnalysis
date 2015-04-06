#!/bin/bash
set -o errexit
set -o nounset

pushd $CMSSW_BASE/src

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`

#for standalone version of svfit
git clone git@github.com:veelken/SVfit_standalone.git TauAnalysis/SVfitStandalone
pushd $CMSSW_BASE/src/TauAnalysis/SVfitStandalone
git checkout svFit_2015Mar28
popd

# Tags that work in any release

# To install lumiCalc.py
if [ "$LUMI" = "1" ]
then
git clone https://github.com/cms-sw/RecoLuminosity-LumiDB.git RecoLuminosity/LumiDB
pushd $CMSSW_BASE/src/RecoLuminosity/LumiDB
git checkout V04-02-10
pushd $CMSSW_BASE/src
fi

# Add and patch to way speed up trigger matching
# Don't crash if patch already applied.
set +o errexit
echo "Applying pat trigger matching speedup"
git cms-addpkg DataFormats/PatCandidates
git apply FinalStateAnalysis/recipe/patches/DataFormats_PatCandidates_TriggerEvent.cc.patch
set -o errexit


# Only checkout PAT tuple production dependencies if requested.
if [ "$PATPROD" = "1" ]
then
    #PU Jet ID Weights -- yes this way sucks
    if [ "$MAJOR_VERSION" -eq "7" ] 
    then
        echo "No RecoJets yet"
    else
        git clone https://github.com/violatingcp/Jets_Short.git
        rm -r RecoJets/
        mv Jets_Short/RecoJets .
        mv Jets_Short/JetMETCorrections/Modules JetMETCorrections/.
        rm -rf Jets_Short
    fi
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

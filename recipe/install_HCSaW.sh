#!/bin/bash

# Installs the HCSaW package into MetaData

pushd $CMSSW_BASE/src
cvs co -P -d HCSaW UserCode/Snowball/Higgs

mkdir -p FinalStateAnalysis/MetaData/interface/
mkdir -p FinalStateAnalysis/MetaData/src/
mkdir -p FinalStateAnalysis/MetaData/data/HCSaW

cp -v HCSaW/*/include/*.h FinalStateAnalysis/MetaData/interface/
cp -v HCSaW/*/src/*.cc FinalStateAnalysis/MetaData/src/
cp -v HCSaW/*/txtFiles/*txt FinalStateAnalysis/MetaData/data/HCSaW

rm -r HCSaW

pushd FinalStateAnalysis/MetaData/
patch -N -p0 < ../recipe/patches/HCSaW_sanity.patch
popd
popd

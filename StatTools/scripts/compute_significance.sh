#!/bin/bash

# Compute a significance point for the VH PAS

echo $@
INPUT_DIR=$1
BLINDED=$2

pushd $PWD/$INPUT_DIR

if [[ $BLINDED == "YES" ]];
then
    echo "RUNNING BLIND"
    text2workspace.py -b vhtt_*.txt -o ./tmp.root -m $INPUT_DIR --default-morphing shape2
    combine -M ProfileLikelihood -m $INPUT_DIR --significance tmp.root -t -1 --expectSignal=1
    mv higgsCombineTest.ProfileLikelihood.mH$INPUT_DIR.root higgsCombine-sig.ProfileLikelihood.mH$INPUT_DIR.root
    rm tmp.root
else
    text2workspace.py -b vhtt_*.txt -o ./tmp.root -m $INPUT_DIR --default-morphing shape2
    combine -M ProfileLikelihood -m $INPUT_DIR --significance tmp.root -t -1 --expectSignal=1 --toysFreq
    mv higgsCombineTest.ProfileLikelihood.mH$INPUT_DIR.root higgsCombine-sig.ProfileLikelihood.mH$INPUT_DIR.root
    rm tmp.root
fi
exit 0

popd
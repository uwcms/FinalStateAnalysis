#!/bin/bash
set -o errexit
set -o nounset

echo "Checking out HZZ4L KD recipe"
pushd $CMSSW_BASE/src
cvs co -r V00-03-01 -d Higgs/Higgs_CS_and_Width UserCode/Snowball/Higgs/Higgs_CS_and_Width 
cvs co -r bonato_supermela_20121107 -d HZZ4L_Combination/CombinationPy UserCode/HZZ4L_Combination/CombinationPy
cvs co -r V00-02-03 -d ZZMatrixElement/MELA UserCode/CJLST/ZZMatrixElement/MELA
cvs co -r V00-02-00 -d ZZMatrixElement/MEKD UserCode/UFL/ZZMatrixElement/MEKD
cvs co -r V00-00-12 -d ZZMatrixElement/MEMCalculators UserCode/HZZ4l_MEM/ZZMatrixElement/MEMCalculators
popd

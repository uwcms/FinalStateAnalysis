#!/bin/bash

label=$1

echo $label

gghFile=/store/mc/Fall11/GluGluToHToTauTau_M-125_7TeV-powheg-pythia6/AODSIM/PU_S6_START42_V14B-v1/0000/12628F24-31FB-E011-883A-90E6BA19A248.root
vbfFile=/store/mc/Fall11/VBF_HToTauTau_M-125_7TeV-powheg-pythia6-tauola/AODSIM/PU_S6_START42_V14B-v1/0000/668A54D7-53F8-E011-9D81-E0CB4E29C502.root

echo "Tuplizing ggH sample - will write log to ggH_tuplization.log"
./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$gghFile reportEvery=100 maxEvents=500\
  outputFile=/scratch/$LOGNAME/h2tau_ggh_xcheck.$label.root dataset=Fall11 &> ggH_tuplization.log &

#echo "Tuplizing VBF sample - will write log to vbf_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$vbfFile reportEvery=100 \
  #outputFile=/scratch/$LOGNAME/h2tau_vbf_xcheck.$label.root dataset=Fall11 &> vbf_tuplization.log &

echo "Waiting for both jobs to finish"
wait

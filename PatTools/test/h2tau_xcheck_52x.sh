#!/bin/bash

label=$1

echo $label

vbfFile=/store/mc/Summer12/VBF_HToTauTau_M-125_8TeV-powheg-pythia6/AODSIM/PU_S7_START52_V9-v1/0000/CE37860C-6196-E111-B574-002481A60370.root

dataFile=/store/data/Run2012A/TauPlusX/AOD/PromptReco-v1/000/191/226/CEF49C35-0488-E111-91DD-0025901D6288.root 

#echo "Tuplizing VBF sample - will write log to vbf_8TeV_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$vbfFile reportEvery=100 \
  #outputFile=/scratch/$LOGNAME/h2tau_vbf_8TeV_xcheck.$label.root dataset=Fall11 &> vbf_8TeV_tuplization.log &

echo "Tuplizing data sample - will write log to data_8TeV_tuplization.log"
./patTuple_cfg.py isMC=0 globalTag=$datagt inputFiles=$dataFile reportEvery=100 \
  outputFile=/scratch/$LOGNAME/h2tau_data_8TeV_xcheck.$label.root dataset=Prompt &> data_8TeV_tuplization.log &

wait

#!/bin/bash

label=$1

echo $label

vbfFile=/store/data/Run2012A/DoubleMu/AOD/PromptReco-v1/000/190/456/D0478E94-0681-E111-82A4-0019B9F72F97.root

dataFile=/store/data/Run2012A/DoubleMu/AOD/PromptReco-v1/000/190/456/D0478E94-0681-E111-82A4-0019B9F72F97.root

#echo "Tuplizing VBF sample - will write log to vbf_8TeV_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$vbfFile reportEvery=100 \
  #outputFile=/scratch/$LOGNAME/h2tau_vbf_8TeV_xcheck.$label.root dataset=Fall11 &> vbf_8TeV_tuplization.log &

outputData=/scratch/$LOGNAME/h2tau_data_8TeV_xcheck.$label.root 

echo "Tuplizing data sample - will write log to data_8TeV_tuplization.log"
echo "Output root file: $outputData"
./patTuple_cfg.py isMC=0 globalTag=$datagt inputFiles=$dataFile reportEvery=100 \
  outputFile=$outputData dataset=Prompt &> data_8TeV_tuplization.log &

wait

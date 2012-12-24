#!/bin/bash

label=$1
echo $label

wjfile=/store/mc/Fall11/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S6_START42_V14B-v1/0000/000D1C75-14F2-E011-A53D-003048678B1A.root
ttbarfile=/store/mc/Fall11/TTJets_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S6_START42_V14B-v2/0000/0040932D-A80F-E111-BBF7-00304867BFAA.root

../patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$wjfile reportEvery=100 \
  outputFile=/scratch/$LOGNAME/smb_wjets.$label.root dataset=Fall11 &> wjets_tuplization.$label.log &

../patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$ttbarfile reportEvery=100 \
  outputFile=/scratch/$LOGNAME/smb_ttbar.$label.root dataset=Fall11 &> ttbar_tuplization.$label.log &

wait

echo "done"

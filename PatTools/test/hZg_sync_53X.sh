#!/bin/bash

label=$1

echo $label

#2012 data : /store/data/Run2012B/DoubleMu/AOD/29Jun2012-v1/0001/C46FD2A9-3FC3-E111-A1A8-485B39800C00.root
#2011 data : /store/data/Run2011A/DoubleMu/AOD/16Jan2012-v1/0001/E8EFCAFA-3F44-E111-A9DF-0026189438BC.root
#2011 MC Signal (44X): /store/mc/Fall11/GluGluToHToZG_M-125_7TeV-powheg-pythia6/AODSIM/PU_S6_START44_V9B-v1/0000/2263742A-48BA-E111-ADCB-003048678BF4.root
#2011 MC Signal (42X): /store/mc/Fall11/GluGluToHToZG_M-125_7TeV-powheg-pythia6/AODSIM/PU_S6_START42_V14B-v1/0000/4E7D0288-43BA-E111-B933-0026189438F7.root
#2012 MC BG: /store/mc/Summer12/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/0003/EAF43999-8D9B-E111-A418-003048D4610E.root

muonSync[0]='Data_52X:/store/data/Run2012B/DoubleMu/AOD/29Jun2012-v1/0001/C46FD2A9-3FC3-E111-A1A8-485B39800C00.root'
muonSync[1]='MCSignal_52X:/store/mc/Summer12/GluGluToHToZG_M-125_8TeV-powheg-pythia6/AODSIM/PU_S7_START52_V9-v1/0000/422A59C9-CFEF-E111-9BB5-00266CFFCC7C.root'
muonSync[2]='MCBackground_52X:/store/mc/Summer12/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/0003/EAF43999-8D9B-E111-A418-003048D4610E.root'

echo "Tuplizing ggH sample - will write log to ggH_tuplization.log"
./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$gghFile reportEvery=100 maxEvents=500\
  outputFile=/scratch/$LOGNAME/h2tau_ggh_xcheck.$label.root dataset=Fall11 &> ggH_tuplization.log &

#echo "Tuplizing VBF sample - will write log to vbf_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$vbfFile reportEvery=100 \
  #outputFile=/scratch/$LOGNAME/h2tau_vbf_xcheck.$label.root dataset=Fall11 &> vbf_tuplization.log &

echo "Waiting for both jobs to finish"
wait

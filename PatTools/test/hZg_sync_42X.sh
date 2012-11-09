#!/bin/bash

label=$1

echo $label



#muons
#2012 data : /store/data/Run2012B/DoubleMu/AOD/29Jun2012-v1/0001/C46FD2A9-3FC3-E111-A1A8-485B39800C00.root
#2011 data : /store/data/Run2011A/DoubleMu/AOD/16Jan2012-v1/0001/E8EFCAFA-3F44-E111-A9DF-0026189438BC.root
#2011 MC Signal (44X): /store/mc/Fall11/GluGluToHToZG_M-125_7TeV-powheg-pythia6/AODSIM/PU_S6_START44_V9B-v1/0000/2263742A-48BA-E111-ADCB-003048678BF4.root
#2011 MC Signal (42X): 
#2012 MC BG: /store/mc/Summer12/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/0003/EAF43999-8D9B-E111-A418-003048D4610E.root
#electron
#2011 Data : /store/data/Run2011A/DoubleElectron/AOD/16Jan2012-v1/0000/FC8A17E2-1644-E111-9276-0018F3D096D4.root
#Fall 11 MC: /store/mc/Fall11/GluGluToHToZG_M-125_7TeV-powheg-pythia6/AODSIM/PU_S6_START42_V14B-v1/0000/4E7D0288-43BA-E111-B933-0026189438F7.root
#2012 Data : /store/data/Run2012B/DoubleElectron/AOD/29Jun2012-v1/0000/00507372-79C2-E111-B41C-003048FFCB6A.root
#Sum12 Bkg : /store/mc/Summer12/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/0002/002C5B35-519B-E111-862D-001E67398025.root
#Sum12 Sig : /GluGluToHToZG_M-125_8TeV-powheg-pythia6/Summer12-PU_S7_START52_V9-v1/AODSIM

sync_42X=()
sync_42X+=('DataMuon;root://cmsxrootd.hep.wisc.edu//store/data/Run2011A/DoubleMu/AOD/16Jan2012-v1/0001/E8EFCAFA-3F44-E111-A9DF-0026189438BC.root')
sync_42X+=('DataElectron;root://cmsxrootd.hep.wisc.edu//store/data/Run2011A/DoubleElectron/AOD/16Jan2012-v1/0000/FC8A17E2-1644-E111-9276-0018F3D096D4.root')
sync_42X+=('MCSignalMuo;root://cmsxrootd.hep.wisc.edu//store/mc/Fall11/GluGluToHToZG_M-125_7TeV-powheg-pythia6/AODSIM/PU_S6_START42_V14B-v1/0000/4E7D0288-43BA-E111-B933-0026189438F7.root')
sync_42X+=('MCSignalEle;root://cmsxrootd.hep.wisc.edu//store/mc/Fall11/GluGluToHToZG_M-125_7TeV-powheg-pythia6/AODSIM/PU_S6_START42_V14B-v1/0000/4E7D0288-43BA-E111-B933-0026189438F7.root')

for sync_test in ${sync_42X[@]}
do
  parts=(`echo $sync_test | tr ';' ' '`)
  echo ${parts[0]} ${parts[1]}

  if [[ "${parts[0]}" == *Data* ]]
      then
      ./patTuple_cfg.py isMC=0 globalTag=$datagt inputFiles=${parts[1]} reportEvery=100 maxEvents=-1\
	  outputFile=/scratch/$LOGNAME/hZg_sync42X.$label.${parts[0]}.root dataset=ReReco\
	  calibrationTarget=Jan16ReReco passThru=1 &> HZG_${parts[0]}_42X_sync.log & 
      else
      ./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=${parts[1]} reportEvery=100 maxEvents=-1\
	  outputFile=/scratch/$LOGNAME/hZg_sync42X.$label.${parts[0]}.root dataset=Fall11\
	  calibrationTarget=Fall11 passThru=1 &> HZG_${parts[0]}_42X_sync.log &
  fi  
done
#echo "Tuplizing ggH sample - will write log to ggH_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$gghFile reportEvery=100 maxEvents=500\
#  outputFile=/scratch/$LOGNAME/h2tau_ggh_xcheck.$label.root dataset=Fall11 &> ggH_tuplization.log &

#echo "Tuplizing VBF sample - will write log to vbf_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$vbfFile reportEvery=100 \
  #outputFile=/scratch/$LOGNAME/h2tau_vbf_xcheck.$label.root dataset=Fall11 &> vbf_tuplization.log &

echo "Waiting for ${#sync_42X[@]} jobs to finish"
wait

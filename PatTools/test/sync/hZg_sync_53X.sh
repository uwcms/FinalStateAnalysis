#!/bin/bash

label=$1

echo $label



#electrons and muons
#/GluGluToHToZG_M-125_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM

hzg_list=`dbs lsf --path=/GluGluToHToZG_M-125_8TeV-powheg-pythia6/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM | head -16 | tail -13 | tr -d ' ' | sed 's/\/store/root\:\/\/cmsxrootd\.hep\.wisc\.edu\/\/store/'`

hzg_list_arr=()
for item in $hzg_list
do
  hzg_list_arr+=($item)
done

sync_53X=()
for idx in "${!hzg_list_arr[@]}"
do
  sync_53X+=("MCSignalEle${idx};${hzg_list_arr[$idx]}")
done

for sync_test in ${sync_53X[@]}
do
  parts=(`echo $sync_test | tr ';' ' '`)
  echo ${parts[0]} ${parts[1]}

  if [[ "${parts[0]}" == *Data* ]]
      then
      ../patTuple_cfg.py isMC=0 globalTag=$datagt inputFiles=${parts[1]} reportEvery=1 maxEvents=-1\
	  outputFile=/scratch/$LOGNAME/hZg_sync53X.$label.${parts[0]}.root dataset=ReReco #&> ${part[0]}_sync.log  & 
      else
      ../patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=${parts[1]} reportEvery=1 maxEvents=-1\
	  outputFile=/scratch/$LOGNAME/hZg_sync53X.$label.${parts[0]}.root dataset=Summer12 #&> ${part[0]}_sync.log  &
  fi  
done
#echo "Tuplizing ggH sample - will write log to ggH_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$gghFile reportEvery=100 maxEvents=500\
#  outputFile=/scratch/$LOGNAME/h2tau_ggh_xcheck.$label.root dataset=Fall11 &> ggH_tuplization.log &

#echo "Tuplizing VBF sample - will write log to vbf_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$vbfFile reportEvery=100 \
  #outputFile=/scratch/$LOGNAME/h2tau_vbf_xcheck.$label.root dataset=Fall11 &> vbf_tuplization.log &

echo "Waiting for ${#sync_53X[@]} jobs to finish"
wait

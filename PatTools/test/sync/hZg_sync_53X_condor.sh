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

hdfsOutDir=srm://cmssrm.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/store/user/lgray/HZG_sync/${label}/53X 

mcOpts="isMC=1 globalTag=$mcgt dataset=Summer12 calibrationTarget=Summer12_DR53X_HCP2012"
dataOpts="isMC=0 globalTag=$datagt dataset=ReReco calibrationTarget=2012Jul13ReReco"

for sync_test in ${sync_53X[@]}
do
  parts=(`echo $sync_test | tr ';' ' '`)
  echo
  echo ${parts[0]} ${parts[1]}

  jobName=hZg_sync_53X.${label}.${parts[0]}
  fajOpts="--assume-input-files-exist --infer-cmssw-path --express-queue --job-generates-output-name --output-dir=${hdfsOutDir} --input-dir=${parts[1]%/*}/ --input-file-list=${jobName}.input.txt"
  patTupleOpts="reportEvery=100 maxEvents=-1 outputFile=${jobName}.root passThru=1"

  echo ${parts[1]##*/} > ${jobName}.input.txt

  if [[ "${parts[0]}" == *Data* ]]
      then
      farmoutAnalysisJobs $fajOpts $jobName ../patTuple_cfg.py inputFiles='$inputFileNames' $patTupleOpts $dataOpts
      else
      farmoutAnalysisJobs $fajOpts $jobName ../patTuple_cfg.py inputFiles='$inputFileNames' $patTupleOpts $mcOpts
  fi  
done
#echo "Tuplizing ggH sample - will write log to ggH_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$gghFile reportEvery=100 maxEvents=500\
#  outputFile=/scratch/$LOGNAME/h2tau_ggh_xcheck.$label.root dataset=Fall11 &> ggH_tuplization.log &

#echo "Tuplizing VBF sample - will write log to vbf_tuplization.log"
#./patTuple_cfg.py isMC=1 globalTag=$mcgt inputFiles=$vbfFile reportEvery=100 \
  #outputFile=/scratch/$LOGNAME/h2tau_vbf_xcheck.$label.root dataset=Fall11 &> vbf_tuplization.log &

#echo "Waiting for ${#sync_53X[@]} jobs to finish"
#wait

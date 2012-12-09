#!/bin/bash

# Get information about the size of the pat tuple on different samples

label=$1

function sizeup {
   # arguments AODfile, isMC, globalTag, name
   outputdir=$5
   echo $outputdir
   mkdir -p $outputdir
   name=$1
   echo "Creating size report $name"
   $fsa/PatTools/test/patTuple_cfg.py isMC=$2 globalTag=$3 inputFiles=file:$4 maxEvents=500 \
     outputFile=/tmp/tuple_$name.root analyzeSkimEff=$outputdir/$name.root &> $outputdir/stdoutput_$name.txt
   edmEventSizeReport.py /tmp/tuple_$name.root --wrt $4 > $outputdir/sizes_$name.txt
   rm -f /tmp/tuple_$name.root 
}

echo "Putting reports in " $label
sizeup singleElec 0 $datagt /hdfs/store/data/Run2012B/SingleElectron/AOD/13Jul2012-v1/0000/361F28D2-6DD7-E111-9E2B-003048678B5E.root $label &
sizeup singleMu 0 $datagt /hdfs/store/data/Run2012B/SingleMu/AOD/13Jul2012-v1/0000/FEE38669-ADD3-E111-957A-00259073E3C0.root $label &
sizeup ttbar 1 $mcgt /hdfs/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FED775BD-B8E1-E111-8ED5-003048C69036.root $label &

wait

./size_study_report.py $label

echo "done!"

 
export varname="lundi_0121"

#cmsRun ./PatTools/test/patTuple_cfg.py reportEvery=1 isMC=1 globalTag=$mcgt inputFiles=root://cmsxrootd.hep.wisc.edu//store/mc/Summer12_DR53X/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7C-v1/20000/5ACBC7A4-7D84-E211-A0B6-782BCB27B958.root outputFile="tt_"$varname"_5ACBC7A4-7D84-E211-A0B6-782BCB27B958.root" maxEvents=30 dumpCfg="tt_"$varname"_5ACBC7A4-7D84-E211-A0B6-782BCB27B958.py"

cmsRun ./PatTools/test/patTuple_cfg.py reportEvery=1 isMC=1 globalTag=$mcgt inputFiles=file:5ACBC7A4-7D84-E211-A0B6-782BCB27B958.root outputFile="tt_"$varname"_5ACBC7A4-7D84-E211-A0B6-782BCB27B958.root" maxEvents=6 dumpCfg="tt_"$varname"_5ACBC7A4-7D84-E211-A0B6-782BCB27B958.py"

edmDumpEventContent "tt_"$varname"_5ACBC7A4-7D84-E211-A0B6-782BCB27B958.root" > "tt_"$varname"_5ACBC7A4-7D84-E211-A0B6-782BCB27B958.content" 

./printMet_corrMet_FSAPattuples.py --inputPath="tt_"$varname"_5ACBC7A4-7D84-E211-A0B6-782BCB27B958.root" > "tt_"$varname"_5ACBC7A4-7D84-E211-A0B6-782BCB27B958.mets"

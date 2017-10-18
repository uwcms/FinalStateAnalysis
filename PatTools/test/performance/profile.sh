valgrind --tool=callgrind --combine-dumps=yes --instr-atstart=no \
  --dump-instr=yes --separate-recs=1 cmsRun \
  ./patTuple_cfg.py isMC=1 globalTag=$mcgt \
  inputFiles=/store/mc/Fall11/WJetsToLNu_TuneZ2_7TeV-madgraph-tauola/AODSIM/PU_S6_START42_V14B-v1/0004/FECD1F53-09F3-E011-A327-001A92811720.root \
  maxEvents=100 reportEvery=1 outputFile=profile.root profile=1 

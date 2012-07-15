#!/bin/bash 

# Setup the environment for the FinalStateAnalysis software

echo "Setting up CMSSW runtime environment"
cmsenv

export FSAHOME=$CMSSW_BASE/src/FinalStateAnalysis/
echo "Setting variable FSAHOME=$FSAHOME"
# easier to type
export fsa=$FSAHOME

export vpython=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/vpython
echo "Activating python virtualenv from $vpython"

export tests=$CMSSW_BASE/test/$SCRAM_ARCH/

# Define shortcuts for the relevant global tags 

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`

if [ "$MAJOR_VERSION" -eq "4" ]; then
  echo "Setting up CMSSW 4 global tags"
  export datagt=GR_R_42_V24::All
  export mcgt=START42_V17::All
fi

if [ "$MAJOR_VERSION" -eq "5" ]; then
  echo "Setting up CMSSW 5 global tags"
  export datagt=GR_R_52_V8::All
  export mcgt=START52_V10::All
fi

echo "Data global tag: $datagt"
echo "MC global tag: $mcgt"

# Define some shortcuts to HDFS and scratch areas
export hdfs=/hdfs/store/user/$LOGNAME/
export scratch=/scratch/$LOGNAME/

if [ -d "$vpython" ]; then
  echo "Activating python virtual environment"
  export VIRTUAL_ENV_DISABLE_PROMPT=1
  cd $vpython
  source bin/activate
  cd -
fi

# Put the PWD into the PYTHONPATH
export PYTHONPATH=.:$PYTHONPATH
# Make sure we prefer our virtualenv packages
export PYTHONPATH=$fsa/recipe/external/vpython/lib/python2.6/site-packages/:$PYTHONPATH

# Don't require a scram build to get updated scripts
export PATH=$fsa/Utilities/scripts:$PATH
export PATH=$fsa/StatTools/scripts:$PATH
export PATH=$fsa/PlotTools/scripts:$PATH
export PATH=$fsa/MetaData/scripts:$PATH
export PATH=$fsa/PatTools/scripts:$PATH
export PATH=$fsa/RecoTools/scripts:$PATH

# Add some shortcuts to example files for testing
if [ "$MAJOR_VERSION" -eq "4" ]; then
  export mcAODFile=/hdfs/store/mc/Fall11/WH_ZH_TTH_HToTauTau_M-130_7TeV-pythia6-tauola/AODSIM/PU_S6_START42_V14B-v1/0000/08400E05-880C-E111-9E78-90E6BA0D0987.root
  export dataAODFile=/hdfs/store/data/Run2011B/MuEG/AOD/PromptReco-v1/000/175/832/08252A90-35DD-E011-B45A-485B3989721B.root
  export patTupleFile=/hdfs/store/user/friis/WH_ZH_TTH_HToTauTau_M-130_7TeV-pythia6-tauola/VH_130_2012-05-29-7TeV-PatTuple-b08cf9d/c7f0540d247deade88c2d29ec1211eaf/output_10_2_sbE.root
fi

if [ "$MAJOR_VERSION" -eq "5" ]; then
  export mcAODFile=/hdfs/store/mc/Summer12/WH_ZH_TTH_HToTauTau_M-130_8TeV-pythia6-tauola/AODSIM/PU_S7_START52_V9-v2/0000/04BF9EBD-D19E-E111-86A3-00215E221FDA.root
  export dataAODFile=/hdfs/store/data/Run2012B/SingleMu/AOD/PromptReco-v1/000/193/752/B66332A3-789B-E111-939C-5404A63886B2.root
  export patTupleFile=/hdfs/store/user/friis/WH_ZH_TTH_HToTauTau_M-130_8TeV-pythia6-tauola/VH_H2Tau_M-130_2012-05-28-8TeV-PatTuple-8a107b9/4729152ae17d7e4009729a1d0d9e952d/output_1_3_47m.root
fi

# Define the current most-informative PU information JSONs
export pu2011JSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/PileUp/pileup_2011_JSON_pixelLumi.txt
export pu2012JSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_JSON_DCSONLY_190389-196531_patch2.txt

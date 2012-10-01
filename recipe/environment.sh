#!/bin/bash 

# Setup the environment for the FinalStateAnalysis software

echo "Setting up CMSSW runtime environment"
cmsenv

export fsa=$CMSSW_BASE/src/FinalStateAnalysis/
echo "Setting variable \$fsa=$FSAHOME"

export base=$CMSSW_BASE/src

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
  export datagt=GR_P_V41_AN1::All
  export mcgt=START53_V10::All
fi
#  export datagt=GR_R_52_V8::All
#  export mcgt=START52_V10::All

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
  export mcAODFile=/hdfs/store/mc/Summer12_DR53X/WH_ZH_TTH_HToTauTau_M-125_lepdecay_8TeV-pythia6-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/04E2F0AA-09E1-E111-B2BC-0018F3D096C8.root
  export dataAODFile=/hdfs/store/data/Run2012B/DoubleMu/AOD/13Jul2012-v4/00000/FC8B75AE-A6DD-E111-B81F-20CF3027A611.root
  export patTupleFile=/hdfs/store/user/tapas/2012-09-18-8TeV-53X-PatTuple/data_TauPlusX_Run2012C_PromptReco_v2_Run198934_201264/patTuple_cfg-0001908A-8BE3-E111-9C6D-BCAEC53296F3.root
fi

# Define the current most-informative PU information JSONs
export pu2011JSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/PileUp/pileup_2011_JSON_pixelLumi.txt
# Valid up to the September 12 technical stop, see https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/1882.html
export pu2012JSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_JSON_DCSONLY_190389-203002_corr.txt

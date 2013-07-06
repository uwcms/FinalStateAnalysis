#!/bin/bash 

# Setup the environment for the FinalStateAnalysis software

echo "Setting up CMSSW runtime environment"
eval `scramv1 ru -sh`

export fsa=$CMSSW_BASE/src/FinalStateAnalysis/
echo "Setting variable \$fsa=$fsa"

export base=$CMSSW_BASE/src

export vpython=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/vpython
export hdf5=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/hdf5
echo "Activating python virtualenv from $vpython"

export tests=$CMSSW_BASE/test/$SCRAM_ARCH/

# Define shortcuts for the relevant global tags 

# Check CMSSW version
MAJOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_.*|\1|"`
MINOR_VERSION=`echo $CMSSW_VERSION | sed "s|CMSSW_\([0-9]\)_\([0-9]\)_.*|\2|"`

if [ "$MAJOR_VERSION" -eq "4" ]; then
  echo "Setting up CMSSW 4 global tags"
  export datagt=FT_R_42_V24::All
  export mcgt=START42_V17::All
fi

if [ "$MAJOR_VERSION" -eq "5" ]; then
  echo "Setting up CMSSW 5_3_X global tags"
  export datagt=FT_53_V21_AN4::All
  export mcgt=START53_V23::All
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

if [ -d "$hdf5" ]
then
    export LD_LIBRARY_PATH=$hdf5/lib:$LD_LIBRARY_PATH
    export HDF5_DIR=$hdf5
fi


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
  export dataAODFile=/hdfs/store/data/Run2011B/DoubleMu/AOD/16Jan2012-v1/0000/0036326C-C244-E111-BF09-00261894397D.root
  export patTupleFile=/hdfs/store/user/tapas/GluGluToHToTauTau_M-100_7TeV-powheg-pythia6/Fall11-PU_S6_START42_V14B-v1/AODSIM/2013-03-06-7TeV-42X-PatTuple_Master/patTuple_cfg-0E4D5BE2-9DF0-E011-BCEC-0019BB3FE352.root
fi

if [ "$MAJOR_VERSION" -eq "5" ]; then
  export mcAODFile=/hdfs/store/mc/Summer12_DR53X/WH_ZH_TTH_HToWW_M-140_lepdecay_8TeV-pythia6/AODSIM/PU_S10_START53_V7A-v1/0000/1022798A-5AE1-E111-956C-002618943865.root
  export dataAODFile=/hdfs/store/data/Run2012D/DoubleMu/AOD/PromptReco-v1/000/204/705/8ADDD20D-8413-E211-BBD9-003048D2BF1C.root
  export patTupleFile=/hdfs/store/user/tapas/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/Summer12_DR53X-PU_S10_START53_V7A-v1/AODSIM/2013-03-13-8TeV-53X-PatTuple_Master/patTuple_cfg-00037C53-AAD1-E111-B1BE-003048D45F38.root
fi

# Define the current most-informative PU information JSONs
export pu2011JSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/PileUp/pileup_2011_JSON_pixelLumi.txt
# Valid up to the September 12 technical stop, see https://hypernews.cern.ch/HyperNews/CMS/get/physics-validation/1882.html
export pu2012JSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions12/8TeV/PileUp/pileup_JSON_DCSONLY_190389-208686_corr.txt 

#check if dev area is up to date
pushd $fsa
check_git_updates.sh
popd

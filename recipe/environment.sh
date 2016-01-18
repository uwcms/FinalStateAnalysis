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

# Define some shortcuts to HDFS and scratch areas
export hdfs=/hdfs/store/user/$LOGNAME/
export scratch=/scratch/$LOGNAME/

if [ -d "$vpython" ]; then
  echo "Activating python virtual environment"
  export VIRTUAL_ENV_DISABLE_PROMPT=1
  cd $vpython
  # See https://github.com/pypa/virtualenv/issues/150
  source bin/activate
  cd -
  # Make sure we prefer our virtualenv packages
  export PYTHONPATH=$fsa/recipe/external/vpython/lib/python2.7/site-packages/:$PYTHONPATH
fi

# Put the PWD into the PYTHONPATH
export PYTHONPATH=.:$PYTHONPATH

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

# Some tight compiler flags should be relaxed
export USER_CXXFLAGS="-Wno-delete-non-virtual-dtor -Wno-error=unused-but-set-variable -Wno-error=unused-variable -Wno-error=sign-compare -Wno-error=reorder"

# Only use the ZZ MELA packages if we actually need them (they take a long time to compile)
if [ -d $CMSSW_BASE/src/ZZMatrixElement ]; then
    echo "Using HZZ Matrix Element packages."
    export USER_CXXFLAGS="$USER_CXXFLAGS -D HZZMELA"
fi

echo "Will compile with flags:"
echo $USER_CXXFLAGS

export pu2015JSON=/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions15/13TeV/PileUp/pileup_latest.txt

#check if dev area is up to date
### Removed by Nate 31 March 2015. Can be put back in when we're following master again.
# pushd $fsa
# check_git_updates.sh
# popd

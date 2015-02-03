FinalStateAnalysis Package Description (miniAOD_dev version)
============================================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

**Documentation:** https://github.com/uwcms/FinalStateAnalysis/wiki


Installation
------------

Current CMSSW version: ``7_2_3_patch1``.

Get a supported CMSSW release area:

```bash
  scram pro -n MyWorkingAreaName CMSSW CMSSW_VERSION
  cd MyWorkingAreaName/src
  # Setup your CMSSW environment
  cmsenv
  # Run this before doing ANYTHING else in src
  git cms-init
```

Checkout the FinalStateAnalysis repository:

```bash
  git clone --recursive -b miniAOD_dev https://github.com/uwcms/FinalStateAnalysis.git
  cd FinalStateAnalysis
```

Checkout the needed CMSSW tags:

```bash
  cd recipe/
  # Checkout needed packages and apply patches
  # This enables all options.  You can turn off things you don't need.
  # NB that in the hcp2012 changes the options won't do anything.
  PATPROD=1 LUMI=1 LIMITS=0 ./recipe.sh
  # Compile
  cd ../../
  # Avoid the new strict version of the compiler by relaxing some flags
  export USER_CXXFLAGS="-Wno-delete-non-virtual-dtor -Wno-error=unused-but-set-variable -Wno-error=unused-variable -Wno-error=sign-compare -Wno-error=reorder"
  scram b -j 8
```

You must always set up the CMSSW environment + some extra variables from FinalStateAnalysis:

```bash
  cmsenv
  source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh
```

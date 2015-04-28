FinalStateAnalysis Package Description (miniAOD_dev version)
============================================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

**Documentation:** https://github.com/uwcms/FinalStateAnalysis/wiki


Installation
------------

Current CMSSW version: ``7_4_1``.

Get a supported CMSSW release area:

```bash
  scram pro -n MyWorkingAreaName CMSSW <CMSSW_VERSION>
  cd MyWorkingAreaName/src
  # Setup your CMSSW environment
  cmsenv
  # SSH agent is optional, but will save you from typing your password many times
  eval `ssh-agent -s`
  ssh-add
  # Run this before doing ANYTHING else in src
  git cms-init
```

Checkout the FinalStateAnalysis repository:

```bash
  git clone --recursive -b miniAOD_dev_74X git@github.com:uwcms/FinalStateAnalysis.git
  cd FinalStateAnalysis
```

Checkout the needed CMSSW tags:

```bash
  cd recipe/
  # Checkout needed packages and apply patches
  # do >> HZZ=1 ./recipe.sh  instead if you want H->ZZ MELA stuff.
  ./recipe.sh
  cd ..
  # Setup FSA environment
  source environment.sh
  # Compile
  pushd ..
  scram b -j 8
  popd
```

You must always set up the CMSSW environment + some extra variables from FinalStateAnalysis:

```bash
  cmsenv
  source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh
```

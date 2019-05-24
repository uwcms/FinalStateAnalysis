FinalStateAnalysis Package Description (miniAOD_dev version)
============================================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

**Documentation:** https://github.com/uwcms/FinalStateAnalysis/wiki

This is for the 2018 data, but should work with 2016 miniAODv3 and 2017 94X samples too.


Installation
------------

Current CMSSW version: ``CMSSW_10_2_14``.

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
  git clone --recursive -b miniAOD_10_2_5 https://github.com/uwcms/FinalStateAnalysis.git
  cd FinalStateAnalysis
  source environment.sh
```

Checkout extra needed code:

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

It is highly recommended to set up a python virtualenv with a number of nice tools:
```bash
  ./recipe/install_python.sh
```
The virtualenv is automatically activated by `environment.sh`.

You must always set up the CMSSW environment + some extra variables from FinalStateAnalysis:

```bash
  cmsenv
  source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh
```


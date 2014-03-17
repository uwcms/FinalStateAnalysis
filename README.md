FinalStateAnalysis Package Description
======================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  
The package contains a complete implementatation to build a POG-approved 
PAT tuple, and utilities for generating plain ROOT ntuples from the PAT tuple.

**Documentation:** https://github.com/uwcms/FinalStateAnalysis/wiki

**Automated tests:**
<table>
    <tr>
        <td>53X PAT + Ntuple</td> 
        <td><a href='http://login06.hep.wisc.edu:8080/job/FinalStateAnalysis/'><img src='https://www.hep.wisc.edu/~efriis/badges/FSA.jpg' width='100'></a></td>
    </tr>
    <tr>
        <td>42X PAT + Ntuple</td> 
        <td><a href='http://login06.hep.wisc.edu:8080/job/FinalStateAnalysis-42X/'><img src='https://www.hep.wisc.edu/~efriis/badges/FSA-42X.jpg' width='100'></a></td>
    </tr>
    <tr>
        <td>53X Ntuple Only</td> 
        <td><a href='http://login06.hep.wisc.edu:8080/job/FinalStateAnalysis-NoPAT/'><img src='https://www.hep.wisc.edu/~efriis/badges/FSA-NoPAT.jpg' width='100'></a></td>
    </tr>
</table>

Installation for SL6 (abridged)
---------------------
```
scram project CMSSW_5_3_14
cd CMSSW_5_3_14/src
cmsenv
git cms-init # needs to be done before ANYTHING else
git clone --recursive https://github.com/uwcms/FinalStateAnalysis.git
cd FinalStateAnalysis/recipeGIT
kinit [cern_username]@CERN.CH
./recipe.sh
USER_CXXFLAGS="-Wno-delete-non-virtual-dtor -Wno-error=unused-but-set-variable -Wno-error=unused-variable" scram b -j 8
```
Now, you need to set the relevant environment variables and such

```bash
cmsenv
source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh
```

Installation for SL6 (detailed)
--------------------

Current CMSSW versions: ``5_3_14``.
The installation instructions are the same for both.  

Get a supported CMSSW release area::

```bash
  scram pro -n MyWorkingAreaName CMSSW CMSSW_VERSION
  cd MyWorkingAreaName/src
  # Setup your CMSSW environment
  cmsenv
  # Run this before doing ANYTHING else in src
  git cms-init
```

Checkout the FinalStateAnalysis repository::

```bash
  git clone --recursive https://github.com/uwcms/FinalStateAnalysis.git
  cd FinalStateAnalysis
```

This will checkout the lastest and greatest version of the code.  You might also want the Summer 2013 compatible branch, if so you should additionally run:
```bash
git checkout 53X_SLC6_Dev
```
and then proceed as normal.

Checkout the needed CMSSW tags:

```bash
  cd recipe/
  # You need to have CVS access -- Actually not, but do it anyway
  kinit me@CERN.CH
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

You must always set up the CMSSW environment + some extra variables from FinalStateAnalysis::

```bash
  cmsenv
  source $CMSSW_BASE/src/FinalStateAnalysis/environment.sh
```

For python plotting enhancements, install the custom python virtualenv and extra
packages (note this is *not* necessary for PAT tuple production)::

```bash
  ./install_python.sh
  yolk -l # List installed packages
```


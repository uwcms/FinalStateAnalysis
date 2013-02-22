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
        <td>52X PAT + Ntuple</td> 
        <td><a href='http://login06.hep.wisc.edu:8080/job/FinalStateAnalysis-52X/'><img src='https://www.hep.wisc.edu/~efriis/badges/FSA-52X.jpg' width='100'></a></td>
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

Installation
------------

Current CMSSW versions: ``4_2_8_patch7`` or ``5_3_7``.  
The installation instructions are the same for both.  

Get a supported CMSSW release area::

```bash
  scram pro -n MyWorkingAreaName CMSSW CMSSW_VERSION
```

Checkout the FinalStateAnalysis repository::

```bash
  cd MyWorkingAreaName/src
  git clone https://github.com/uwcms/FinalStateAnalysis.git
```

This will checkout the lastest and greatest version of the code.  You might also want the HCP2012 compatible branch, if so you should additionally run:
```bash
cd FinalStateAnalysis
git checkout hcp2012
```
and then proceed as normal.

Checkout the needed CMSSW tags:

```bash
  cd FinalStateAnalysis/recipe/
  # You need to have CVS access
  kinit me@CERN.CH
  # Make sure your CMSSW environment is set up
  cmsenv
  # Checkout needed packages and apply patches
  # This enables all options.  You can turn off things you don't need.
  # NB that in the hcp2012 changes the options won't do anything.
  PATPROD=1 LUMI=1 LIMITS=1 ./recipe.sh
  # Compile
  cd ../../
  scram b -j 8
```

You must always set up the environment::

```bash
  source FinalStateAnalysis/environment.sh
```

For python plotting enhancements, install the custom python virtualenv and extra
packages (note this is *not* necessary for PAT tuple production)::

```bash
  ./install_python.sh
  yolk -l # List installed packages
```

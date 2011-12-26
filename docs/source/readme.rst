======================================
FinalStateAnalysis Package Description
======================================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  Common
utilities are organized as subpackages.  Each analysis (Higgs to tau, SSDL, etc)
should exists as a separate subpackage.

The full documentation is available at http://readthedocs.org/docs/final-state-analysis/en/latest/. 

DataFormats
-----------

Definitions of custom, EDM persist-able data formats used by the framework.

DataAlgos
---------

The DataAlgos package defines the algorithm implementations used by the member
functions of the DataFormats package.  This improves code reuse, eases backward
compatibility, and improves compilation speed.

RecoTools
---------

The RecoTools package contains plugin modules and utilities for dealing with
RECO and AOD content.  This package is **not** FWKLITE compatible.

PatTools
--------

The PAT tools package contains everything needed to build the FSA pat tuple.  It
is standalone.  

Selectors
---------

The Selectors package defines the "analyzeFinalStates" FWKLITE binary, which is
the final analysis builder.  It additionally contains additional helper classes
to analyze PATFinalStates, as well as the python definitions of common cuts to
be applied.  New selections and plots should be defined in
``Selectors/python/selectors`` and ``Selectors/python/plotting``, respectively.

Utilities
---------

Contains various command--line tools and C++ functionality.  

docs and recipe
---------------

The recipe section contains scripts which automate installation of related
packages.  The docs folder just contains all the documentation.

==========================
Analysis Specific Packages
==========================

Each analysis, which uses the above packages, is configued in a separate
sub--package.  In general, an analysis can/should have some variation of following content:

python/selection.py 
  Defines the selections and plots (from the Selectors_ package) used in the
  analysis.  
 
test/analyze_cfg.py
  Defines the final ntuple production cfg.  This is the steering file for the
  analyzeFinalStatesBinary.
 
test/submit_analysis.py
  Submits the analyze_cfg.py jobs to condor/GRID/etc.

test/plotting/*
  Tools to analyze the final level ntuple and produces plots.

TagAndProbe
-----------

Tools for generating Tag and Probe like analysis for muons and taus.


VHiggs
------

Associated Higgs to tau analysis.

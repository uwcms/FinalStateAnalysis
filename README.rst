======================================
FinalStateAnalysis Package Description
======================================

Documentation: https://github.com/uwcms/FinalStateAnalysis/wiki

[![Build Status](http://login06.hep.wisc.edu:8080/job/FinalStateAnalysis/badge/icon)](http://login06.hep.wisc.edu:8080/job/FinalStateAnalysis/)

The Final State Analysis (FSA) package is a CMSSW analysis framework.  Common
utilities are organized as subpackages.  

DataFormats
-----------

Definitions of custom, EDM persist-able data formats used by the framework.

DataAlgos
---------

The DataAlgos package defines the algorithm implementations used by the member
functions of the DataFormats package.  This improves code reuse, eases backward
compatibility, and improves compilation speed.

MetaData 
--------

This package holds "data about data."  It knows what samples exist, how to find
them in DBS, and what their cross sections are.  It also holds the central
definition of plot styles used for different data samples.  Also, reference type
code (such as getting Higgs boson properties from lookup tables, etc, are hosted
here).

NtupleTools
-----------

The NtupleTools package defines the "analyzeFinalStates" binary, which is
the final analysis builder, used to build flat TTrees from PATFinalState
objects in the PAT tuple.  New selections and ntuple columns should be defined
in
``NtupleTools/python/templates.``  Ntuples designed for Higgs multi-lepton final 
states can be produced by make_ntuples_cfg.py, in test/.

PatTools
--------

The PAT tools package contains everything needed to build the FSA pat tuple.  

PlotTools
--------

Tools and helpers for making plots from ntuples created by NtupleTools.

RecoTools
---------

The RecoTools package contains plugin modules and utilities for dealing with
RECO and AOD content.  

StatTools
---------

Various statistical/limit setting tools.

Utilities
---------

Contains various command--line tools and C++ functionality.  

TagAndProbe
-----------

Tools for generating Tag and Probe studies.  Classes for querying Tag and Probe
results provided by other groups (eg Muon POG) are kept here as well.

recipe
---------------

The recipe section contains scripts which automate installation of related
packages.  


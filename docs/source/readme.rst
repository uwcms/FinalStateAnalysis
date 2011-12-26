FinalStateAnalysis Package
==========================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  Common
utilities are organized as subpackages.  Each analysis (Higgs to tau, SSDL, etc)
should exists as a separate subpackage.

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
RECO and AOD content.  This package is not FWKLITE compatible.

PatTools
--------

The PAT tools package contains everything needed to build the FSA pat tuple.  It
is standalone.  


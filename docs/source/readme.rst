FinalStateAnalysis Package
==========================

The Final State Analysis (FSA) package is a CMSSW analysis framework.  Common
utilities are organized as subpackages.  Each analysis (Higgs to tau, SSDL, etc)
should exists as a separate subpackage.

The full `Final State Analysis documentation
<http://readthedocs.org/docs/final-state-analysis/en/latest/>`_ is available
online.

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

Selectors
---------

The Selectors package defines the "analyzeFinalStates" FWKLITE binary, which is
the final analysis builder.  It additionally contains additional helper classes
to analyze PATFinalStates, as well as the python definitions of common cuts to
be applied.  New selections and plots should be defined in
``Selectors/python/selectors`` and ``Selectors/python/plotting``, respectively.

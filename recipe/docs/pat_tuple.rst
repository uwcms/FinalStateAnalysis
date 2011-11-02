Philosophy
==========

The final state analysis package is built around the data format PATFinalState.
This abstract which encapsulates all of the interesting information needed by
the analyst.   Another way of imagining the PATFinalState is that it represents
a single row in an ntuple.  The advantage of the single object is that is both
lightweight and that it holds references to all of the interesting information
in the event.  Thus you can compose complex observables using only a single
object, enabling many tasks to use the string cut parser.  This allows new cuts
to be implemented quickly, and without writing an C++ code.
 
Workflow
========

The analysis proceeds in three steps.  First, a pat tuple containing the final
states is produced from AOD content.  The PAT tuple can then be analyzed
(selections + plots) directly, using the PATFinalStateAnalysis tool.  The
analysis typically runs at about 500+ events/second.
As an optional third step, the PATFinalStateAnalysis can produce a bare ROOT
ntuple at any stage of the processing.  One then apply additional selections.


PAT Tuple production
--------------------
 
The pat tuple production runs on sod events and runs at about two events per
second.  The PAT tuplization does the following:

* Compute and embed all object Ids
* Apply corrections and embed systematics
* Produce event weights
* Compose all possible final states of interest.  Example: DoubleMu + Tau
 
The tuplization only needs to be done occasionally.  The PAT tuple is configured
in four places.

* PatTools/python/datadefs.py provides a global defintion of all MC and data
     samples.

* PatTools/python/patTupleProduction.py defines the PAT production sequence,
  the corrections applied to different objects, and the PATFinalState
  production.

* PatTools/test/patTuple_cfg.py is the top-level cfg which builds the tuple.

* PatTools/test/submit_tuplization.py submits the jobs to condor.

PAT Final State Analysis
------------------------
 
Secondly, the analysis is run.  A series of selections and plots can be made on
the chosen set of final states.  At any point in the selection, plots or bare
ntuples can be produced.
  
Optionally, the final stage can be the production of a bar root ntuple.  Plots
can then be made from this ntuple. 
 
PAT Tuple Content
=================

Muons
-----

The ``cleanPatElectrons`` collection is defined as electrons
which have ``pt > 8``. 

The following muon IDs are embedded:
* ``userInt('WWID')``
* ``userInt('VBTF')``

The following isolation quantities are embedded as userFloats (no DB correction)

* ``pfLooseIsoPt03``
* ``pfLooseIsoPt04``
* ``pfLooseIsoPt06``

The impact parameter to the PV is embedded as userFloat: ``vertexDXY``

The following systematics candidates are embedded (as userCands)

* ``uncorr`` (no muon energy scale)
* ``nom`` (nominal ES correction, same as pat::Muon p4)
* ``mes-`` (down 1 sigma)
* ``mes+`` (up 1 sigma)


Electrons
---------

The ``cleanPatElectrons`` collection is defined as electrons
which have ``pt > 8``. 

Electrons which overlap a ``cleanPatMuon``, or overlap 
a tau candidate which has ``pt > 15``, passes decay mode
finding, loose combined isolation, and ``againstElectronTight`` are removed.

The following electron IDs are embedded as userFloats:

* ``wp80``
* ``wp90``
* ``wp95``
* ``WWID``

Jets
----

The following jet IDs are embedded into the PFJets.
They correspond to the official PFJet IDs listed on the `JetMET twiki`_.

.. _JetMET twiki: https://twiki.cern.ch/twiki/bin/view/CMS/JetID

* ``idLoose``
* ``idMedium``
* ``idTight``

Corrections
'''''''''''

The L1FastJet, L2Relative, L3Absolute corrections are applied to MC & Data.  The
L2L3Residual corrections are additionally applied to Data. Reference:
`IntroToJEC twiki`_.

.. _IntroToJEC twiki: https://twiki.cern.ch/twiki/bin/view/CMS/IntroToJEC

The uncorrected, and 1 sigma uncertainties on the JEC are available from the
``pat::Jets`` via;

* ``userCand("uncorr")``
* ``userCand("jes+")``
* ``userCand("jes-")``


Taus
----

The seed jets are available via the ``userCand('patJet')`` function.



Utilities
=========

Scripts
-------
    
* ``trimJSON.py`` apply a run selection to a JSON file




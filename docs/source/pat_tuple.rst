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

The following IP information is embedded as userFloats: 

* ``ipDXY``
* ``dz``
* ``ip3D``
* ``ip3DS`` - significance
* ``tip`` 
* ``tipS``  - significance

The following systematics candidates are embedded (as userCands)

* ``uncorr`` (no muon energy scale)
* ``nom`` (nominal ES correction, same as pat::Muon p4)
* ``mes-`` (down 1 sigma)
* ``mes+`` (up 1 sigma)

The closest PF patJet is available via the ``userCand('patJet')`` function.
This ref may be null!  The jet pt is stored as ``userFloat('jetPt')``.

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

The following electron IDs are embedded as as eIDs (pat defaults):

* ``cicHyperTight1 --> eidHyperTight1``
* ``cicTight --> eidTight``
* ``cicHyperTight3 --> eidHyperTight3``
* ``cicHyperTight2 --> eidHyperTight2``
* ``cicHyperTight4 --> eidHyperTight4``
* ``cicVeryLoose --> eidVeryLoose``
* ``cicLoose --> eidLoose``
* ``cicSuperTight --> eidSuperTight``
* ``cicMedium --> eidMedium``

The following electron MVA ID related information is embedded:

* ``hasConversion``
* ``missingHits`` - number of missing hits 
* ``idDZ`` - dz used for MVA id
* ``MVA`` - raw MVA value
* ``MITID`` - MIT MVA ID working point binary value

The following IP information is embedded as userFloats: 

* ``ipDXY``
* ``dz``
* ``ip3D``
* ``ip3DS`` - significance
* ``tip`` 
* ``tipS``  - significance

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
`IntroToJEC twiki`_.  In simulation, a smearing correction (see PAS JME-10-014)
is additionally applied to correct the simulated jet energy resolution.
The energy corrections are applied after the smearing is done.

.. _IntroToJEC twiki: https://twiki.cern.ch/twiki/bin/view/CMS/IntroToJEC

The uncorrected, and 1 sigma uncertainties on the JEC are available from the
``pat::Jets`` via;

* ``userCand("uncorr")`` - no corrections or smearing applied
* ``userCand("unsmeared")`` - the same as above...
* ``userCand("smear+")`` - smear error up
* ``userCand("smear-")`` - smear error down
* ``userCand("jes+")`` - using the JES uncertainty from the CondDB
* ``userCand("jes-")`` - using the JES uncertainty from the CondDB
* ``userCand("ues+")`` - using the UES uncertainty of 10%
* ``userCand("ues-")`` - using the UES uncertainty of 10%

The closest PF patJet is available via the ``userCand('patJet')`` function.
This ref may be null!  The jet pt is stored as ``userFloat('jetPt')``.

Taus
----

The taus are HPS PFTaus.


Discriminators
''''''''''''''
The standard complement of discriminators are available.

* ``decayModeFinding``
* ``byVLooseIsolation``
* ``byLooseIsolation``
* ``byMediumIsolation``
* ``byTightIsolation``
* ``byVLooseIsolationDeltaBetaCorr``
* ``byLooseIsolationDeltaBetaCorr``
* ``byMediumIsolationDeltaBetaCorr``
* ``byTightIsolationDeltaBetaCorr``
* ``byVLooseCombinedIsolationDeltaBetaCorr``
* ``byLooseCombinedIsolationDeltaBetaCorr``
* ``byMediumCombinedIsolationDeltaBetaCorr``
* ``byTightCombinedIsolationDeltaBetaCorr``
* ``againstElectronLoose``
* ``againstElectronMedium``
* ``againstElectronTight``
* ``againstElectronMVA``
* ``againstMuonLoose``
* ``againstMuonMedium``
* ``againstMuonTight``

The seed jets are available via the ``userCand('patJet')`` function.
The corrected jet pt is stored as ``userFloat('jetPt')``.

The following IP information is embedded as userFloats: 

* ``ipDXY``
* ``dz``
* ``ip3D``
* ``ip3DS`` - significance
* ``tip`` 
* ``tipS``  - significance

Utilities
=========

Scripts
-------
    
* ``trimJSON.py`` apply a run selection to a JSON file




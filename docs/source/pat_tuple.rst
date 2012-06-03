PAT Tuple Content
=================

Skim
----

Before tuplization, the events are skimmed at the AOD level.  The OR of the
following requirements is applied:

* One global muon with pt > 20 and eta < 2.4
* One electron with pt > 20 and eta < 2.5
* One global muon with pt > 14, eta < 2.4 and one tau pt > 18, eta < 2.3
* One electron with pt > 17, eta < 2.5 and one tau pt > 18, eta < 2.3
* One electron with pt > 17, eta < 2.5 and one tau pt > 18, eta < 2.3

PF Isolation
------------

The PF isolation values (0.4) are available for electrons and muons via:

* ``chargedHadronIso()``
* ``neutralHadronIso()``
* ``photonIso()``
* ``pfPUChargedHadrons()`` - for applying the Delta Beta correction

The H2Tau analysis uses custom veto cones, defined at the `H2Tau working twiki`_.  
You can get the H2Tau isolations by:

.. _H2Tau working twiki: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012 

Electrons:

* ``userIso(0)`` - all PF charged particles vetos: EB 0.01, EE 0.01 
* ``userIso(1)`` - PF photon isolation vetos: EE + EB 0.08 
* ``userIso(2)`` - PF PU isolation vetos: none (maybe this isn't right??)

Muons:

* ``userIso(0)`` - all PF charged particles vetos: EB 0.001, EE 0.001 

Note that you probably need to update your `PAT tags in 42X`_ to get the
required version of DataFormats/PatCandidates.

.. _PAT tags in 42X: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATReleaseNotes42X#V08_06_55

For convenience, the fastjet energy is embedded in electrons and muons:

* ``userFloat('rho')``  - uses determinstic Voronoi rho produced during tau ID
* ``userFloat('zzRho')`` - uses ZZ recipe

Muons
-----

The following cut-based muon IDs are embedded:

* ``userInt('WWID')``
* ``userInt('WWID2011')``
* ``userInt('VBTF')``
* ``userInt('tightID')`` - 2012 Muon POG recommendation

The WWID2011 is the same as defined in the UWAnalysis packages.  The following
MVA IDs (see the `MuonId twiki`_).

.. _MuonId twiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateMuonSelection


* ``userFloat('isomva')``
* ``userFloat('idmva')`` - just rings
* ``userFloat('isoringsradmva')`` - rings + radial

Three isolation (rings) MVA working points are embedded, from the `H2Tau 2012
twiki`_.  Note that WP2 is the loosest. :|

.. _H2Tau 2012 twiki: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#Object_ID_AN1

* ``userInt('mvaisowp1')``
* ``userInt('mvaisowp2')``
* ``userInt('mvaisowp3')``

You can get a ref to to the associated PFMuon via:

* ``pfCandidateRef()``,

if this ref ``isNull()``, there is no muon ID'd by PF.

The following IP information is embedded as userFloats: 

* ``ipDXY``
* ``dz``
* ``vz``
* ``ip3D``
* ``ip3DS`` - significance
* ``tip`` 
* ``tipS``  - significance

The following systematics candidates are embedded (as userCands).  The energy
scale uncertainty is taken from the muon MuscleFit.

* ``uncorr`` (no muon energy scale, same as pat::Muon p4)
* ``corr`` (nominal ES correction)
* ``mes-`` (down 1 sigma)
* ``mes+`` (up 1 sigma)

The closest PF patJet is available via the ``userCand('patJet')`` function.
This ref may be null if the closest jet is farther than DR=0.5!  
The jet pt is stored as ``userFloat('jetPt')``.  If the 
jet doesn't exist, the "jet pt" is equal to the muon Pt.  
The distance to the jet is ``userFloat('jetDR')``.

The "effective area" for different isolation types is available:

* ``userFloat("EAGamma04")``
* ``userFloat("EANeuHadron04")``
* ``userFloat("EAGammaNeuHadron04")``

Electrons
---------

The following electron IDs are embedded as userFloats:

* ``wp80``
* ``wp90``
* ``wp95``
* ``WWID``
* ``MITID`` - the 2011 MVA ID by the MIT people

The following 2012 electron MVA IDs (see `EGamma ID Recipe`_.) and RECO IDs
 are embedded as as eIDs:

.. _EGamma ID Recipe: https://twiki.cern.ch/twiki/bin/view/CMS/MultivariateElectronIdentification

* ``cicTight --> eidTight``
* ``cicLoose --> eidLoose``
* ``cicMedium --> eidMedium``
* ``electronID('mvaNonTrigV0')``
* ``electronID('mvaTrigV0')``

The following 2011 electron MVA ID related information is embedded:

* ``userFloat("hasConversion")``
* ``userInt("missingHits")`` - number of missing hits 
* ``userFloat("idDZ")`` - dz used for MVA id
* ``userFloat("MVA")`` - raw MVA value
* ``userFloat("MVApreID")`` - pre-ID cuts used for the MVA
* ``userFloat("MITID")`` - MIT MVA ID working point binary value

The following 2012 electron MVA ISOs (see `EGamma Iso Recipe`_) are available:

.. _EGamma Iso Recipe: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMultivariateIsoElectrons

* ``userFloat('isomva')``

An MVA working point for the electron ID and Iso are embedded, again from the `H2Tau 2012
twiki`_.   The ID working point is based on the "NonTrig" MVA.

.. _H2Tau 2012 twiki: https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#Object_ID_AN1

* ``userInt('mvaidwp')``
* ``userInt('mvaisowp')``

The "effective area" for different isolation types is available:

* ``userFloat("EAGamma04")``
* ``userFloat("EANeuHadron04")``
* ``userFloat("EAGammaNeuHadron04")``

The `EGamma rho correction`_ is then: ``chargedHadronIso + max(photonIso + neutralHadronIso - userFloat('EAGammaNeuHadron04')*userFloat('rho'), 0)``

.. _EGamma rho correction: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaEARhoCorrection

The following IP information is embedded as userFloats: 

* ``ipDXY``
* ``dz``
* ``vz``
* ``ip3D``
* ``ip3DS`` - significance
* ``tip`` 
* ``tipS``  - significance

The following systematics candidates are embedded (as userCands).  The electron
energy scale uncertainty is currently configured to be 6% (I think this is a
fixme)

* ``uncorr`` (no muon energy scale)
* ``ees-`` (down 1 sigma)
* ``ees+`` (up 1 sigma)

References to the calibrated GSF electrons are embedded as user cands:  

* ``userCand("calibrated")``

returns a reco::CandidatePtr pointing to a reco::GsfElectron.

Jets
----

The following jet IDs are embedded into the PFJets as userFloats.
They correspond to the official PFJet IDs listed on the `JetMET twiki`_.

.. _JetMET twiki: https://twiki.cern.ch/twiki/bin/view/CMS/JetID

* ``idLoose``
* ``idMedium``
* ``idTight``

The raw MVA-based PU jet IDs (see `MVAMet`_) are embedded as:

.. _MVAMet: https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet

* ``userFloat('fullDiscriminant')``
* ``userFloat('philv1Discriminant')``
* ``userFloat('simpleDiscriminant')``

and the integer working points as:

* ``userInt('fullIdXXX')``
* ``userInt('philv1IdXXX')``
* ``userInt('simpleIdXXX')``

where XXX is Loose, Medium or Tight.

Available b-tag discriminators:

* ``jetBProbabilityBJetTagsAOD``
* ``jetProbabilityBJetTagsAOD``
* ``trackCountingHighPurBJetTagsAOD``
* ``trackCountingHighEffBJetTagsAOD``
* ``simpleSecondaryVertexNegativeBJetTagsAOD``
* ``simpleSecondaryVertexHighEffBJetTagsAOD``
* ``simpleSecondaryVertexHighPurBJetTagsAOD``
* ``combinedSecondaryVertexBJetTagsAOD``
* ``combinedSecondaryVertexMVABJetTagsAOD``
* ``softMuonBJetTagsAOD``
* ``softMuonByPtBJetTagsAOD``
* ``softMuonByIP3dBJetTagsAOD``

Corrections
'''''''''''

The L1FastJet, L2Relative, L3Absolute corrections are applied to MC & Data.  The
L2L3Residual corrections are additionally applied to Data. Reference:
`IntroToJEC twiki`_.  

In simulation, a smearing correction (see PAS JME-10-014)
is additionally computed to correct the simulated jet energy resolution.
The energy corrections are applied after the smearing is done.

.. _IntroToJEC twiki: https://twiki.cern.ch/twiki/bin/view/CMS/IntroToJEC

The uncorrected, and 1 sigma uncertainties on the JEC are available from the
``pat::Jets`` via;

* ``userCand("uncorr")`` - no corrections or smearing applied
* ``userCand("smeared")`` - applying GEN-DATA resolution correction
* ``userCand("smear+")`` - smear error up
* ``userCand("smear-")`` - smear error down
* ``userCand("jes+")`` - using the JES uncertainty from the CondDB
* ``userCand("jes-")`` - using the JES uncertainty from the CondDB
* ``userCand("ues+")`` - using the UES uncertainty of 10%
* ``userCand("ues-")`` - using the UES uncertainty of 10%

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
* ``byIsolationMVAraw``
* ``byLooseIsolationMVA``
* ``byMediumIsolationMVA``
* ``byTightIsolationMVA``
* ``againstElectronLoose``
* ``againstElectronMedium``
* ``againstElectronTight``
* ``againstElectronMVA``
* ``againstElectronMVA2raw``
* ``againstElectronVLooseMVA2``
* ``againstElectronLooseMVA2``
* ``againstElectronMediumMVA2``
* ``againstElectronTightMVA2``
* ``againstMuonLoose``
* ``againstMuonMedium``
* ``againstMuonTight``

The seed jets are available via the ``userCand('patJet')`` function.
The corrected jet pt is stored as ``userFloat('jetPt')``.  This always exists,
as taus are seeded by jets.

The following IP information is embedded as userFloats: 

* ``ipDXY``
* ``dz``
* ``vz``
* ``ip3D``
* ``ip3DS`` - significance
* ``tip`` 
* ``tipS``  - significance

The following systematics candidates are embedded (as userCands).  The tau
energy scale uncertainty is currently configured to be 3% 

* ``uncorr`` (no tau energy scale)
* ``tes-`` (down 1 sigma)
* ``tes+`` (up 1 sigma)

Information regarding the tau preselection (used in the TNP measurement is
added) - note these quantities refer to the PFJet, *not* the tau:

* ``userCand("leadPFCH")`` - ref to leading PF CH in *jet* (dropped in output)
* ``userInt("ps_ldTrk")`` - the lead PF CH exists
* ``userFloat("ps_ldTrkPt")`` - lead PF CH pT
* ``userFloat("ps_ldTrkQ")`` - lead PF CH charge
* ``userFloat("ps_lsPFIsoPt")`` - loose isolation pT sum
* ``userFloat("ps_elMVA")`` - electron MVA value for lead PFCH
* ``userFloat("ps_drMuon")`` - Delta R to nearest pat::Muon
* ``userFloat("numTracks")`` - number of tracks in jet
* ``userInt("ps_crk_nom")`` - is in ECAL crack


MET
---

The following four-vector systematics are embedded as userCands:

* ``userCand("type1")`` - Type 1 correct MET (jets only)
* ``userCand("mes+")`` - Muon scale uncertainty
* ``userCand("tes+")`` - Tau scale uncertainty
* ``userCand("jes+")`` - Jet scale uncertainty
* ``userCand("ues+")`` - Unclustered energy scale uncertainty

Charge conjugation is implied.


'''

Ntuple branch template sets for muon objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# ID and isolation
id = PSet(
    objectVBTFID = '{object}.userInt("VBTF")',
    objectWWID = '{object}.userInt("WWID")',
    objectPFIDTight = '{object}.userInt("tightID")',

    # For charged, we use ALL charged particles
    objectRelPFIsoDB = cms.string(
        "({object}.userIso(0)"
        "+max({object}.photonIso()"
        "+{object}.neutralHadronIso()"
        "-0.5*{object}.puChargedHadronIso,0.0))"
        "/{object}.pt()"
    ),
    objectIsGlobal = '{object}.isGlobalMuon',
    objectIsTracker = '{object}.isTrackerMuon',
    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}).isAvailable && getDaughterGenParticleMotherSmart({object_idx}).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}).pdgId() : -999',
    objectComesFromHiggs = 'comesFromHiggs({object_idx})',        
)

# Information about the associated track
tracking = PSet(
    objectPtUncorr = '{object}.userCand("uncorr").pt',
    objectPixHits = '? {object}.combinedMuon.isNonnull ? '
        '{object}.combinedMuon.hitPattern.numberOfValidPixelHits :-1',
    objectGlbTrkHits = '? {object}.globalTrack.isNonnull ? '
        '{object}.globalTrack.hitPattern.numberOfHits :-1',
    objectNormTrkChi2 = "? {object}.combinedMuon.isNonnull ? "
        "{object}.combinedMuon.chi2/{object}.combinedMuon.ndof : 1e99",
    objectD0 = '{object}.dB("PV3D")',
)

# Trigger matching
trigger = PSet(
    objectDiMuonL3p5PreFiltered8 = 'matchToHLTFilter({object_idx}, "hltDiMuonL3(p5|)PreFiltered8")',
    objectDiMuonL3PreFiltered7 = 'matchToHLTFilter({object_idx}, "hltDiMuonL3PreFiltered7")',
    objectSingleMu13L3Filtered13 = 'matchToHLTFilter({object_idx}, "hltSingleMu13L3Filtered13")',
    objectSingleMu13L3Filtered17 = 'matchToHLTFilter({object_idx}, "hltSingleMu13L3Filtered17")',
    objectDiMuonMu17Mu8DzFiltered0p2 = 'matchToHLTFilter({object_idx}, "hltDiMuonMu17Mu8DzFiltered0p2")',
    objectL1Mu3EG5L3Filtered17 = 'matchToHLTFilter({object_idx}, "hltL1Mu3EG5L3Filtered17")',
    objectMu17Ele8dZFilter  = 'matchToHLTFilter({object_idx}, "hltMu17Ele8dZFilter")',
    objectL3fL1DoubleMu10MuOpenL1f0L2f10L3Filtered17  = 'matchToHLTFilter({object_idx}, "hltL3fL1DoubleMu10MuOpenL1f0L2f10L3Filtered17")',# missing ) on purpose
    objectMatchesDoubleMu2011Paths = r'matchToHLTPath({object_idx}, "HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+,HLT_Mu17_Mu8_v\\d+")', #DoubleMu7_v* Mu13_Mu8 Mu17_Mu8 wichever least prescaled
    objectMatchesMu17TrkMu8Path    = r'matchToHLTPath({object_idx}, "HLT_Mu17_TrkMu8_v\\d+")',
    objectMatchesMu17Ele8Path      = r'matchToHLTPath({object_idx}, "HLT_Mu17_Ele8_CaloIdL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+")',
    objectMatchesMu8Ele17Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_Ele17_CaloIdL_v\\d+,HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v\\d+")',
)



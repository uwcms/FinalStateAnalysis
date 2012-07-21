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
    objectDiMuonL3p5PreFiltered8 = 'matchToHLTFilter(${object_idx}, "hltDiMuonL3(p5|)PreFiltered8")',
    objectDiMuonL3PreFiltered7 = 'matchToHLTFilter(${object_idx}, "hltDiMuonL3PreFiltered7")',
    objectSingleMu13L3Filtered13 = 'matchToHLTFilter(${object_idx}, "hltSingleMu13L3Filtered13")',
    objectSingleMu13L3Filtered17 = 'matchToHLTFilter(${object_idx}, "hltSingleMu13L3Filtered17")',
    objectDiMuonMu17Mu8DzFiltered0p2 = 'matchToHLTFilter(${object_idx}, "hltDiMuonMu17Mu8DzFiltered0p2")',
    objectL1Mu3EG5L3Filtered17 = 'matchToHLTFilter(${object_idx}, "hltL1Mu3EG5L3Filtered17")',
)



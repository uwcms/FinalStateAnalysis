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
    objectWWID = '{object}.userInt("WWID")',
    # Use cms.string so we get the parentheses formatting bonus
    objectRelPFIsoDB = cms.string(
        "({object}.chargedHadronIso"
        "+max({object}.photonIso()"
        "+{object}.neutralHadronIso()"
        "-0.5*{object}.userIso(0),0.0))"
        "/{object}.pt()"
    ),
)

# Information about the associated track
tracking = PSet(
    objectPixHits = '? {object}.combinedMuon.isNonnull ? '
        '{object}.combinedMuon.hitPattern.numberOfValidPixelHits :-1',
    objectNormTrkChi2 = "? {object}.combinedMuon.isNonnull ? "
        "{object}.combinedMuon.chi2/{object}.combinedMuon.ndof : 1e99",
    objectD0 = '{object}.dB("PV3D")',
)

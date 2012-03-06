'''

Ntuple branch template sets for muon objects

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import TPSet

# ID and isolation
id = TPSet(
    objectWWID = '{object}.userInt("WWID")',
    objectRelPFIsoDB = cms.string(
        "({object}.chargedHadronIso"
        "+max({object}.photonIso()"
        "+{object}.neutralHadronIso()"
        "-0.5*{object}.userIso(0),0.0))"
        "/{object}.pt()"
    ),
)

# Information about the associated track
tracking = TPSet(
    objectPixHits = '? {object}.combinedMuon.isNonnull ? '
        '{object}.combinedMuon.hitPattern.numberOfValidPixelHits :-1',
    objectNormTrkChi2 = "? {object}.combinedMuon.isNonnull ? "
        "{object}.combinedMuon.chi2/{object}.combinedMuon.ndof : 1e99",
    objectD0 = '{object}.dB("PV3D")',
)

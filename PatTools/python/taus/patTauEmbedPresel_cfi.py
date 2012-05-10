import FWCore.ParameterSet.Config as cms
from RecoTauTag.RecoTau.PFRecoTauQualityCuts_cfi import PFTauQualityCuts

'''
Embed the Tag & Probe preselection into pat taus
'''

patTauEmbedPresel = cms.EDFilter(
    "PATTauPreselectionEmbedder",
    src = cms.InputTag("fixme"),
    #minJetPt = cms.double(20.0),
    minJetPt = cms.double(15), # lower for systematics reasons
    maxJetEta = cms.double(2.3),
    trackQualityCuts = PFTauQualityCuts.signalQualityCuts,
    minLeadTrackPt = cms.double(5.0),
    maxDzLeadTrack = cms.double(0.2),
    maxLeadTrackPFElectronMVA = cms.double(0.6),
    #applyECALcrackVeto = cms.bool(True),
    applyECALcrackVeto = cms.bool(False),
    minDeltaRtoNearestMuon = cms.double(0.5),
    muonSelection = cms.string("isGlobalMuon() | isTrackerMuon() | isStandAloneMuon()"),
    srcMuon = cms.InputTag('patMuons'),
    pfIsolation = cms.PSet(
        chargedHadronIso = cms.PSet(
            ptMin = cms.double(1.0),
            dRvetoCone = cms.double(0.15),
            dRisoCone = cms.double(0.6)
        ),
        neutralHadronIso = cms.PSet(
            ptMin = cms.double(1000.),
            dRvetoCone = cms.double(0.15),
            dRisoCone = cms.double(0.)
        ),
        photonIso = cms.PSet(
            ptMin = cms.double(1.5),
            dPhiVeto = cms.double(-1.),  # asymmetric Eta x Phi veto region
            dEtaVeto = cms.double(-1.),  # to account for photon conversions in electron isolation case
            dRvetoCone = cms.double(0.15),
            dRisoCone = cms.double(0.6)
        )
    ),
    maxPFIsoPt = cms.double(2.5),
    srcPFIsoCandidates = cms.InputTag('pfNoPileUpIso'),
    srcBeamSpot = cms.InputTag('offlineBeamSpot'),
    srcVertex = cms.InputTag('offlinePrimaryVertices'),
    filter = cms.bool(False)
)

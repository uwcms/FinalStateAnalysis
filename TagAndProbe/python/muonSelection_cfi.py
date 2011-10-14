import FWCore.ParameterSet.Config as cms

signalMuonSelection = cms.PSet(
    sysTag = cms.string("nom"),
    muonPt = cms.double(20),
    muonEta = cms.double(2.1),
    maxDXY = cms.double(0.05),
    isoCut = cms.string('userFloat("pfLooseIsoPt04")/pt < 0.1'),
)

# Version where muon is anti-isolated to enrich QCD
antiIsoMuonSelection = signalMuonSelection.clone(
    isoCut = cms.string(
        'userFloat("pfLooseIsoPt04")/pt > 0.1 && '
        'userFloat("pfLooseIsoPt04")/pt < 0.3'
    )
)

def updateSystematicsTags(pset, systematic):
    # Only use the non-nominal value if the systematic is MES
    cloned = pset.clone()
    if 'mes' in systematic:
        cloned.sysTag = systematic
    return cloned

import FWCore.ParameterSet.Config as cms

signalTauSelection = cms.PSet(
    # Don't apply tau ID per default
    cutsToIgnore = cms.vstring("Tau ID"),
    sysTag = cms.string("nom"),
    minDRMuon = cms.double(0.3),
    jetPt = cms.double(20),
    jetEta = cms.double(2.3),
    leadTrackPt = cms.double(5),
    preselCut = cms.string('userFloat("ps_lsPFIsoPt") < 2.5'),
    antiMuonCut = cms.string('tauID("againstMuonTight") > 0.5'),
    antiElectronCut = cms.string('tauID("againstElectronLoose") > 0.5'),
    discrimCut = cms.string('tauID("decayModeFinding") & tauID("byLooseIsolation") > 0.5'),
)

signalTauSelectionPassing = signalTauSelection.clone(
    cutsToIgnore = cms.vstring(),
)

signalTauSelectionFailing = signalTauSelection.clone(
    cutsToIgnore = cms.vstring(),
    discrimCut = signalTauSelection.discrimCut.value().replace('>', '<')
)

# We always use the jet pt, so TES doesn't affect it
def updateSystematicsTags(pset, systematic):
    cloned = pset.clone()
    if 'jes' in pset:
        pset.sysTag = systematic
    return pset

import FWCore.ParameterSet.Config as cms

signalTopoSelection = cms.PSet(
    cutsToIgnore = cms.vstring(''),
    muSysTag = cms.string("nom"),
    tauSysTag = cms.string("jet_nom"),
    metSysTag = cms.string("nom"),

    visPZetaFactor = cms.double(-1.5),
    pZetaDiffMin = cms.double(-20.),
    pZetaDiffMax = cms.double(1e9),
    charge = cms.string('OS'),
    #topoCut = cms.string('mt1MEt("nom", "nom") < 40'),
    topoCut = cms.string(''),
    deltaPhiMax = cms.double(3.2),
)

invertedPZetaTopoSelection = signalTopoSelection.clone(
    pZetaDiffMin = cms.double(-1e9),
    pZetaDiffMax = cms.double(-20.0),
    #topoCut = cms.string('mt1MEt("nom", "nom") > 40'),
    topoCut = cms.string(''),
)

def updateSystematicsTags(pset, systematic):
    cloned = pset.clone()
    if 'mes' in systematic:
        cloned.muSysTag = systematic
        cloned.metSysTag = systematic
    if 'jes' in systematic:
        cloned.metSysTag = systematic
        cloned.tauSysTag = systematic
    if 'tes' in systematic:
        # FIXME is this right?
        cloned.metSysTag = systematic
    return cloned

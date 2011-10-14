import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.TagAndProbe.muonSelection_cfi as muon_cfg
import FinalStateAnalysis.TagAndProbe.tauSelection_cfi as tau_cfg
import FinalStateAnalysis.TagAndProbe.topoSelection_cfi as topo_cfg
from FinalStateAnalysis.TagAndProbe.plots_cfi import all_histos

signalRegionOS = cms.PSet(
    muonSelection = muon_cfg.signalMuonSelection.clone(),
    tauSelection = tau_cfg.signalTauSelection.clone(),
    topoSelection = topo_cfg.signalTopoSelection.clone(),
    folders = cms.PSet(
        histos = all_histos,
        realTau = cms.PSet(
            SELECT = cms.string('daughter2.userInt("genDecayMode") > -1'),
            histos = all_histos
        ),
        fakeTau = cms.PSet(
            SELECT = cms.string('daughter2.userInt("genDecayMode") < 0'),
            histos = all_histos
        ),
    )
)


signalRegionSS = signalRegionOS.clone()
signalRegionSS.topoSelection.charge = 'SS'

# Signal region, passing tau ID
signalRegionOSPassing = signalRegionOS.clone(
    tauSelection = tau_cfg.signalTauSelectionPassing,
)
signalRegionSSPassing = signalRegionOSPassing.clone()
signalRegionSSPassing.topoSelection.charge = 'SS'

signalRegionTightOSPassing = signalRegionOSPassing.clone()
signalRegionTightOSPassing.muonSelection.isoCut = cms.string(
    'userFloat("pfLooseIsoPt04")/pt < 0.01')
signalRegionTightOSPassing.topoSelection.topoCut = cms.string(
    'mt1MEt("nom", "nom") < 40 && mt2MEt("jet_nom", "nom") > 30')
signalRegionTightSSPassing = signalRegionTightOSPassing.clone()
signalRegionTightSSPassing.topoSelection.charge = 'SS'

# Signal region, failing tau ID
signalRegionOSFailing = signalRegionOS.clone(
    tauSelection = tau_cfg.signalTauSelectionFailing,
)
signalRegionSSFailing = signalRegionOSFailing.clone()
signalRegionSSFailing.topoSelection.charge = 'SS'

# Signal region, but without preselection
signalNoPreselOSPassing = signalRegionOSPassing.clone()
signalNoPreselOSPassing.tauSelection.preselCut = ''

signalNoPreselSSPassing = signalNoPreselOSPassing.clone()
signalNoPreselSSPassing.topoSelection.charge = 'SS'

qcdEnrichedRegionOS = cms.PSet(
    muonSelection = muon_cfg.antiIsoMuonSelection.clone(),
    tauSelection = tau_cfg.signalTauSelection.clone(),
    topoSelection = topo_cfg.signalTopoSelection.clone(),
    folders = cms.PSet(
        histos = all_histos
    )
)

qcdEnrichedRegionSS = qcdEnrichedRegionOS.clone()
qcdEnrichedRegionSS.topoSelection.charge = 'SS'

qcdEnrichedRegionSSPassing = qcdEnrichedRegionSS.clone(
    tauSelection = tau_cfg.signalTauSelectionPassing,
)
qcdEnrichedRegionSSFailing = qcdEnrichedRegionSS.clone(
    tauSelection = tau_cfg.signalTauSelectionFailing,
)

qcdEnrichedRegionOSPassing = qcdEnrichedRegionOS.clone(
    tauSelection = tau_cfg.signalTauSelectionPassing,
)
qcdEnrichedRegionOSFailing = qcdEnrichedRegionOS.clone(
    tauSelection = tau_cfg.signalTauSelectionFailing,
)

wjetsEnrichedRegionOS = cms.PSet(
    muonSelection = muon_cfg.signalMuonSelection.clone(),
    tauSelection = tau_cfg.signalTauSelection.clone(),
    topoSelection = topo_cfg.invertedPZetaTopoSelection.clone(),
    folders = cms.PSet(
        histos = all_histos
    )
)

wjetsEnrichedRegionSS = wjetsEnrichedRegionOS.clone()
wjetsEnrichedRegionSS.topoSelection.charge = 'SS'

wjetsEnrichedRegionSSPassing = wjetsEnrichedRegionSS.clone(
    tauSelection = tau_cfg.signalTauSelectionPassing,
)
wjetsEnrichedRegionSSFailing = wjetsEnrichedRegionSS.clone(
    tauSelection = tau_cfg.signalTauSelectionFailing,
)

wjetsEnrichedRegionOSPassing = wjetsEnrichedRegionOS.clone(
    tauSelection = tau_cfg.signalTauSelectionPassing,
)
wjetsEnrichedRegionOSFailing = wjetsEnrichedRegionOS.clone(
    tauSelection = tau_cfg.signalTauSelectionFailing,
)

def updateSystematicsTags(pset, systematic):
    cloned = pset.clone()
    cloned.muonSelection = muon_cfg.updateSystematicsTags(cloned.muonSelection)
    cloned.tauSelection = tau_cfg.updateSystematicsTags(cloned.tauSelection)
    cloned.topoSelection = topo_cfg.updateSystematicsTags(cloned.topoSelection)
    return cloned

# Garbage
nunuTauTauRegion = signalRegionOSPassing.clone()
nunuTauTauRegion.topoSelection.pZetaDiffMin = cms.double(-1e9)
nunuTauTauRegion.topoSelection.pZetaDiffMax = cms.double(-20)
#nunuTauTauRegion.topoSelection.deltaPhiMax = cms.double(2.5)
nunuTauTauRegion.topoSelection.deltaPhiMax = cms.double(3.5)
nunuTauTauRegion.topoSelection.topoCut = cms.string(
    #'abs(deltaPhi(visP4("nom", "jet_nom").phi, met().userCand("nom").phi)) > 2'
    #'&& met().userCand("nom").et > 30'
    'visP4("nom", "jet_nom").mass > 40'
    '&& visP4("nom", "jet_nom").mass < 120'
)

nunuTauTauRegionPZeta = signalRegionOSPassing.clone()
nunuTauTauRegionPZeta.topoSelection.pZetaDiffMin = cms.double(-20)
nunuTauTauRegionPZeta.topoSelection.pZetaDiffMax = cms.double(1e9)
nunuTauTauRegionPZeta.topoSelection.deltaPhiMax = cms.double(2.5)
nunuTauTauRegionPZeta.topoSelection.topoCut = cms.string(
    'abs(deltaPhi(visP4("nom", "jet_nom").phi, met().userCand("nom").phi)) > 2'
    '&& met().userCand("nom").et > 30'
    #'&& visP4("nom", "jet_nom").mass > 40'
    #'&& visP4("nom", "jet_nom").mass < 120'
)



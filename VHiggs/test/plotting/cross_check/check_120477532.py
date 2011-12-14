
from PhysicsTools.PatAlgos.patTemplate_cfg import *
process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration/StandardSequences/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        'file:/scratch/efriis/results/infn_mmt_events.root'
    ),
    eventsToProcess = cms.untracked.VEventRange('175990:120477532')
)

process.GlobalTag.globaltag = cms.string('GR_R_42_V21::All')

import PhysicsTools.PatAlgos.tools.tauTools as tautools
import PhysicsTools.PatAlgos.tools.coreTools as coreTools
tautools.switchToPFTauHPS(process)
coreTools.runOnData(process)
process.patJetCorrFactors.useRho = False

process.selectOurWeirdTau = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("patTaus"),
    cut = cms.string('eta <  -0.1 & eta > -0.12 & pt > 36 & pt < 38'),
    filter = cms.bool(True)
)

process.ourTauPassesDecayMode = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("selectOurWeirdTau"),
    cut = cms.string('tauID("decayModeFinding")'),
    filter = cms.bool(True)
)

process.ourTauPassesLooseIso = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("selectOurWeirdTau"),
    cut = cms.string('tauID("byLooseCombinedIsolationDeltaBetaCorr")'),
    filter = cms.bool(True)
)

process.p = cms.Path(
    process.PFTau*
    process.patDefaultSequence*
    process.selectOurWeirdTau*
    process.ourTauPassesDecayMode*
    process.ourTauPassesLooseIso
)

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

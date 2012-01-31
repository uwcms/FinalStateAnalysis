import FWCore.ParameterSet.Config as cms

process = cms.Process("USER")

import FWCore.ParameterSet.VarParsing as VarParsing
options = VarParsing.VarParsing ('analysis')
options.parseArguments()

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
)

process.printElectrons = cms.EDAnalyzer(
    "CandInfoPrinter",
    src = cms.InputTag("cleanPatElectrons"),
    pt = cms.string("pt"),
    eta = cms.string("eta"),
    superclusterEta = cms.string("superCluster.eta"),
    mva = cms.string("userFloat('MVA')"),
    mitID = cms.string("userFloat('MITID')"),
)

process.p = cms.Path(process.printElectrons)

#!/usr/bin/env cmsRun
'''

Skim on the presence of a gen. level. lepton.

Example to require at least one muon:

    ./skimByGenLepton_cfg.py inputFile=in.root outputFile=out.root \
            pdgId=13 minPt=10 maxEta=2.1 minNumber=1

'''

import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    pdgId=0, # For debugging
    minPt="5",
    maxEta="2.5",
    minNumber=1,
)
options.outputFile="selectGenLepton.root"
options.parseArguments()

process = cms.Process("SkimGenLepton")

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    )

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(
    options.maxEvents))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

process.selectGenLeptons = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        "drop  *  ", # this is the default
        'keep pdgId = %i & pt > %s & abs(eta) < %s' % (
            options.pdgId, options.minPt, options.maxEta)
    )
)

process.atLeastOneLepton = cms.EDFilter(
    "CandViewCountFilter",
    src = cms.InputTag("selectGenLeptons"),
    minNumber = cms.uint32(options.minNumber)
)

process.p = cms.Path(process.selectGenLeptons*process.atLeastOneLepton)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring()
    ),
    outputCommands = cms.untracked.vstring('keep *')
)
process.end = cms.EndPath(process.out)

process.schedule = cms.Schedule(process.p,process.end)

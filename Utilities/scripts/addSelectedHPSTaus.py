#!/usr/bin/env cmsRun
'''
Add collections of selected PFTaus to the event.  Reruns PFTau.

Useful for making a collection visible in cmsShow.

Usage: ./addSelectedPFTaus.py inputFile=input_file outputFile=output_file

'''

import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing

options = TauVarParsing.TauVarParsing()

options.parseArguments()

process = cms.Process("AddTaus")

process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration/StandardSequences/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.GlobalTag.globaltag = cms.string(options.globalTag)

process.hpsLooseTaus = cms.EDFilter(
    "PFTauSelector",
    src = cms.InputTag("hpsPFTauProducer"),
    discriminators = cms.VPSet(
        cms.PSet(
            discriminator=cms.InputTag(
                "hpsPFTauDiscriminationByDecayModeFinding"),
            selectionCut=cms.double(0.5)
        ),
        cms.PSet(
            discriminator=cms.InputTag(
                "hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr"),
            selectionCut=cms.double(0.5)
        ),
    ),
    filter = cms.bool(False),
)
process.hpsDecayModeTaus = cms.EDFilter(
    "PFTauSelector",
    src = cms.InputTag("hpsPFTauProducer"),
    discriminators = cms.VPSet(
        cms.PSet(
            discriminator=cms.InputTag(
                "hpsPFTauDiscriminationByDecayModeFinding"),
            selectionCut=cms.double(0.5)
        ),
    ),
    filter = cms.bool(False),
)
process.p = cms.Path(
    process.recoTauClassicHPSSequence*process.hpsDecayModeTaus*process.hpsLooseTaus)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
)
process.outpath = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.p,
    process.outpath
)

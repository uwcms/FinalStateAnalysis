#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    ewkSkim=1,    # Apply EWK skim conditions
    skipEvents=0, # For debugging
)

options.inputFiles = "file:output.root"
options.outputFile = 'plots.root'

options.parseArguments()

process = cms.Process("TUPLETEST")

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents),
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
)

pt = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("Pt"),
    description = cms.untracked.string("p_{T}"),
    plotquantity = cms.untracked.string("pt"),
    lazyParsing = cms.untracked.bool(True),
)

hasMuons = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("hasExtMuons"),
    description = cms.untracked.string("Has Ext Muons"),
    plotquantity = cms.untracked.string("hasOverlaps('extMuons')"),
    lazyParsing = cms.untracked.bool(True),
)

hasElectrons = hasMuons.clone(
    description = "Has Ext Electrons",
    name = "hasExtElectrons",
    plotquantity = "hasOverlaps('extElecs')"
)

hasTaus = hasMuons.clone(
    description = "Has Ext Taus",
    name = "hasExtTaus",
    plotquantity = "hasOverlaps('extTaus')",
)

extras_jetpt = pt.clone(
    description = "Ext Jet Pt",
    name = "extJetPt",
    plotquantity = " extras('extTaus', '')[0].userCand(\'patJet\').pt "
)

extras_jetbtag = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "Ext Jet Btag",
    name = "extBtag",
    plotquantity = " extras('extTaus', '')[0].userCand(\'patJet\').bDiscriminator(\'\') "
)

hltPass = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "HLT_15_or_30",
    name = "hlt",
    plotquantity = r"evt.hltResult('HLT_Mu15_v\d+,HLT_Mu30_v\d+')"
)

hltGroup = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "HLT_15_or_30",
    name = "hltGrp",
    plotquantity = r"evt.hltGroup('HLT_Mu15_v\\d+,HLT_Mu30_v\\d+')"
)

hltPrescale = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "HLT_15_or_30",
    name = "hltPrescale",
    plotquantity = r"evt.hltPrescale('HLT_Mu15_v\\d+,HLT_Mu30_v\\d+')"
)

lhe_info = pt.clone(
    min = 0,
    max = 100,
    nbins = 100,
    description = "LHE flag",
    name = "LHEFlag",
    plotquantity = "evt().lesHouches().NUP"
)

process_id = pt.clone(
    min = 0,
    max = 100,
    nbins = 100,
    description = "Process ID",
    name = "ProcessID",
    plotquantity = "evt().genEventInfo.signalProcessID()"
)

process.mt = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("finalStateMuTau"),
    histograms = cms.VPSet(
        pt,
        hasMuons,
        hasElectrons,
        hasTaus,
        extras_jetbtag,
        extras_jetpt,
        lhe_info,
        hltPass,
        hltGroup,
        hltPrescale,
        process_id,
    )
)

process.p = cms.Path(process.mt)

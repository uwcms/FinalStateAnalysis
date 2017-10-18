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

process.mt = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("finalStateElecElec"),
    histograms = cms.VPSet(
        pt,
        cms.PSet(
            min = cms.untracked.double(-1.5),
            max = cms.untracked.double(19.5),
            nbins = cms.untracked.int32(21),
            name = cms.untracked.string("MatchedObjects"),
            description = cms.untracked.string("matched objs"),
            plotquantity = cms.untracked.string('matchToHLTPath(0, "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v15")'),
            lazyParsing = cms.untracked.bool(True),
        ),
        cms.PSet(
            min = cms.untracked.double(-1.5),
            max = cms.untracked.double(19.5),
            nbins = cms.untracked.int32(21),
            name = cms.untracked.string("MatchedObjectsGrossEscaped"),
            description = cms.untracked.string("matched objs"),
            plotquantity = cms.untracked.string(r'matchToHLTPath(0, "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v\\d+,HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+")'),
            lazyParsing = cms.untracked.bool(True),
        ),
        cms.PSet(
            min = cms.untracked.double(-1.5),
            max = cms.untracked.double(19.5),
            nbins = cms.untracked.int32(21),
            name = cms.untracked.string("MatchedObjectsGross"),
            description = cms.untracked.string("matched objs"),
            plotquantity = cms.untracked.string('matchToHLTPath(0, "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v\\d+,HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+")'),
            lazyParsing = cms.untracked.bool(True),
        ),
        cms.PSet(
            min = cms.untracked.double(-1.5),
            max = cms.untracked.double(19.5),
            nbins = cms.untracked.int32(21),
            name = cms.untracked.string("MatchedObjectsGrossSecond"),
            description = cms.untracked.string("matched objs"),
            plotquantity = cms.untracked.string(r'matchToHLTPath(0, "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+")'),
            lazyParsing = cms.untracked.bool(True),
        ),
        cms.PSet(
            min = cms.untracked.double(-1.5),
            max = cms.untracked.double(19.5),
            nbins = cms.untracked.int32(21),
            name = cms.untracked.string("MatchedObjectsGrossFirst"),
            description = cms.untracked.string("matched objs"),
            plotquantity = cms.untracked.string(r'matchToHLTPath(0, "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v\\d+")'),
            lazyParsing = cms.untracked.bool(True),
        ),
        cms.PSet(
            min = cms.untracked.double(-1.5),
            max = cms.untracked.double(19.5),
            nbins = cms.untracked.int32(21),
            name = cms.untracked.string("MatchedObjectsGrossSecondStar"),
            description = cms.untracked.string("matched objs"),
            plotquantity = cms.untracked.string(r'matchToHLTPath(0, "HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v.*")'),
            lazyParsing = cms.untracked.bool(True),
        ),
    )
)

process.testTrigger = cms.EDAnalyzer(
    "PATFinalStateEventHistoAnalyzer",
    src = cms.InputTag("patFinalStateEventProducer"),
    histograms = cms.VPSet(
        cms.PSet(
            min = cms.untracked.double(-1.5),
            max = cms.untracked.double(19.5),
            nbins = cms.untracked.int32(21),
            name = cms.untracked.string("MatchedObjects"),
            description = cms.untracked.string("matched objs"),
            plotquantity = cms.untracked.string('trig().pathObjects("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v15").size()'),
            lazyParsing = cms.untracked.bool(True),
        ),
        cms.PSet(
            min = cms.untracked.double(-3.5),
            max = cms.untracked.double(3.5),
            nbins = cms.untracked.int32(100),
            name = cms.untracked.string("MatchedObjectEta"),
            description = cms.untracked.string("matched objs"),
            #plotquantity = cms.untracked.string('trig().pathObjects("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v15").size()'),
            plotquantity = cms.untracked.string('? trig().pathObjects("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v15").size() ? trig().pathObjects("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v15")[0].eta : -5'),
            lazyParsing = cms.untracked.bool(True),
        ),
        cms.PSet(
            min = cms.untracked.double(-3.5),
            max = cms.untracked.double(3.5),
            nbins = cms.untracked.int32(100),
            name = cms.untracked.string("MatchedObjectPhi"),
            description = cms.untracked.string("matched objs"),
            #plotquantity = cms.untracked.string('trig().pathObjects("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v15").size()'),
            plotquantity = cms.untracked.string('? trig().pathObjects("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v15").size() ? trig().pathObjects("HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v15")[0].phi : -5'),
            lazyParsing = cms.untracked.bool(True),
        )
    )
)


process.checkMET = cms.EDAnalyzer(
    "CandComparator",
    src1 = cms.InputTag("pfMEtMVA2"),
    src2 = cms.InputTag("pfMEtMVA"),
    comparisons = cms.PSet(
        px = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(-50),
            max = cms.double(50),
            func = cms.string('px'),
        ),
        py = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(-50),
            max = cms.double(50),
            func = cms.string('py'),
        ),
        pt = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(0),
            max = cms.double(100),
            func = cms.string('pt'),
        ),
        phi = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(0),
            max = cms.double(3.14),
            func = cms.string('phi'),
        ),
    )
)

process.p = cms.Path(
    process.mt
    *process.testTrigger
)

'''

Original author: Christian Veelken

'''

import FWCore.ParameterSet.Config as cms
import copy
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing

# Create our option set, with some extra options
options = TauVarParsing.TauVarParsing()

# Setup other defaults
for file in [
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v4/000/165/121/8C7C5983-8E81-E011-8A3B-001617E30CC8.root",
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v4/000/165/121/82E753DE-9B81-E011-B4CA-003048F1183E.root",
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v4/000/165/121/60B6804B-9181-E011-B774-001D09F23944.root",
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v4/000/165/121/4E0BDD05-9281-E011-9518-001617C3B70E.root" ]:
    options.inputFiles = "root://cmsxrootd.hep.wisc.edu//" + file

options.maxEvents = -1
options.hltProcess = 'HLT'
options.isMC = 0
options.outputFile='myFile.root'
options.globalTag = 'GR_R_42_V14::All'
options.parseArguments()

#--------------------------------------------------------------------------------
# skim event sample for tau id. efficiency measurement
#--------------------------------------------------------------------------------

process = cms.Process("skimTauIdEffSample")

process.load('Configuration/StandardSequences/Services_cff')
process.load('FWCore/MessageService/MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
#process.MessageLogger.cerr.threshold = cms.untracked.string('INFO')
process.load('Configuration/StandardSequences/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')

#--------------------------------------------------------------------------------
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles)
)

# If data, apply a luminosity mask
if not options.isMC and options.lumiMask:
    print "Applying LumiMask from", options.lumiMask
    process.source.lumisToProcess = options.buildPoolSourceLumiMask()

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

#--------------------------------------------------------------------------------
# define GlobalTag to be used for event reconstruction
process.GlobalTag.globaltag = options.globalTag

#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
process.load('FinalStateAnalysis.RecoTools.dataQuality_cfi')

process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
process.hltHighLevel.HLTPaths = cms.vstring('HLT_IsoMu17_v*')

if options.isMC:
    process.dataQualityFilters.remove(process.hltPhysicsDeclared)
    process.dataQualityFilters.remove(process.dcsstatus)
#--------------------------------------------------------------------------------

#--------------------------------------------------------------------------------
# require at least one "good quality" (global || tracker || stand-alone) muon
process.goodMuons = cms.EDFilter("MuonSelector",
    src = cms.InputTag('muons'),
    cut = cms.string("(isGlobalMuon | isStandAloneMuon | isTrackerMuon) & abs(eta) < 2.5 & pt > 15.0"),
    filter = cms.bool(True)
)
#--------------------------------------------------------------------------------

process.load('RecoTauTag.Configuration.RecoPFTauTag_cff')

process.tauJetSelector = cms.EDFilter(
    "PFTauViewRefSelector",
    src = cms.InputTag("hpsPFTauProducer"),
    cut = cms.string('jetRef.pt > 15 && abs(jetRef.eta) < 2.5'),
    filter = cms.bool(True)
)

process.cleanTauJets = cms.EDFilter(
    "CandViewOverlapSubtraction",
    src = cms.InputTag("tauJetSelector"),
    subtractSrc = cms.InputTag("goodMuons"),
    minDeltaR = cms.double(0.3),
    filter = cms.bool(True)
)

process.totalEventsProcessed = cms.EDProducer("EventCountProducer")
process.commonSkimSequence = cms.Sequence(
    process.totalEventsProcessed
    + process.hltHighLevel
    + process.dataQualityFilters
    + process.goodMuons
    + process.tauJetSelector
    + process.cleanTauJets
)


process.p = cms.Path(process.commonSkimSequence)

# add event counter for Mauro's "self baby-sitting" technology
process.dump = cms.EDAnalyzer("EventContentAnalyzer")
#------------------------------------------------------------------------------------------------------------------------

process.load("Configuration.EventContent.EventContent_cff")
process.origFEVTSIMEventContent = copy.deepcopy(process.FEVTSIMEventContent)
process.origFEVTSIMEventContent.outputCommands.extend(
    cms.untracked.vstring(
        #'drop *_*_*_%s' % process.name_(),
        'drop *_*_*_%s' % process.name_(),
        'keep edmMergeableCounter_*_*_*'
    )
)


process.skimOutputModule = cms.OutputModule("PoolOutputModule",
    process.origFEVTSIMEventContent,
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring(
            'p',
        )
    ),
    fileName = cms.untracked.string(options.outputFile)
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True)
)

process.o = cms.EndPath(process.skimOutputModule)

#--------------------------------------------------------------------------------

process.schedule = cms.Schedule(
    process.p,
    process.o
)

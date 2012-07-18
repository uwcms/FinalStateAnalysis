import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

######### EXAMPLE CFG
###  A simple test of runnning T&P on Zmumu to determine muon isolation and identification efficiencies
###  More a showcase of the tool than an actual physics example

process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:/hdfs/store/user/cepeda/DYJetsToLL_TuneZ2_M-50_7TeV-madgraph-tauola/Zjets_M50_2012-05-29-7TeV-PatTuple-67c1f94/e7c083b3facfba2612ce8e9d30894d70/output_981_1_bA2.root'

    )
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(500) )

## Tags. In a real analysis we should require that the tag muon fires the trigger,
##       that's easy with PAT muons but not RECO/AOD ones, so we won't do it here
##       (the J/Psi example shows it)
process.tagMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("cleanPatMuons"),
    cut = cms.string("isGlobalMuon && pt > 20 && abs(eta) < 2"),
)
## Probes. Now we just use Tracker Muons as probes
process.probeMuons = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("cleanPatMuons"),
    cut = cms.string("isTrackerMuon && pt > 10"),
)

## Here we show how to define passing probes with a selector
## although for this case a string cut in the TagProbeFitTreeProducer would be enough
process.probesPassingCal = cms.EDFilter("PATMuonRefSelector",
    src = cms.InputTag("cleanPatMuons"),
    cut = cms.string(process.probeMuons.cut.value() + " && caloCompatibility > 0.6"),
)


## Combine Tags and Probes into Z candidates, applying a mass cut
process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    decay = cms.string("tagMuons@+ probeMuons@-"), # charge coniugate states are implied
    cut   = cms.string("40 < mass < 200"),
)

## Match muons to MC
process.muMcMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
    pdgId = cms.vint32(13),
    src = cms.InputTag("cleanPatMuons"),
    distMin = cms.double(0.3),
    matched = cms.InputTag("genParticles")
)

## Make the tree
process.muonEffs = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # pairs
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("OneProbe"),
    # variables to use
    variables = cms.PSet(
        ## methods of reco::Candidate
        eta = cms.string("eta"),
        pt  = cms.string("pt"),
        ## a method of the reco::Muon object (thanks to the 3.4.X StringParser)
        nsegm = cms.string("numberOfMatches"),
    ),
    # choice of what defines a 'passing' probe
    flags = cms.PSet(
        ## one defined by an external collection of passing probes
        passingCal = cms.InputTag("probesPassingCal"),
        ## two defined by simple string cuts
        passingGlb = cms.string("isGlobalMuon"),
        passingPFIDTight = cms.string("userInt('tightID')"),
        hasPixHits = cms.string("? combinedMuon.isNonnull ? combinedMuon.hitPattern.numberOfValidPixelHits :-1"),
        # Need to add HLT info!
    ),
    # mc-truth info
    isMC = cms.bool(True),
    motherPdgId = cms.vint32(22,23),
    makeMCUnbiasTree = cms.bool(True),
    checkMotherInUnbiasEff = cms.bool(True),
    tagMatches = cms.InputTag("muMcMatch"),
    probeMatches  = cms.InputTag("muMcMatch"),
    allProbes     = cms.InputTag("probeMuons"),
)
##    ____       _   _
##   |  _ \ __ _| |_| |__
##   | |_) / _` | __| '_ \
##   |  __/ (_| | |_| | | |
##   |_|   \__,_|\__|_| |_|
##
process.tagAndProbe = cms.Path(
    (process.tagMuons + process.probeMuons) *   # 'A*B' means 'B needs output of A';
    (process.probesPassingCal +                 # 'A+B' means 'if you want you can re-arrange the order'
     process.tpPairs +
     process.muMcMatch) *
    process.muonEffs
)

# Specify the name of the output root file
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("testTagProbeFitTreeProducer_ZMuMu.root")
)


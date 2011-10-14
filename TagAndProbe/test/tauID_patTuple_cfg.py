import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
# Create our option set, with some extra options
options = TauVarParsing.TauVarParsing(
    pfCandidateCollection='particleFlow',
    applyZrecoilCorrection=0,
    tauType='HPS',
    tauIDForMET='byLooseIsolation',
    isEmbedded=0,
)

options.inputFiles = 'file:/hdfs/store/user/efriis//2011-07-19-TauIdEffSkim-data_SingleMu_Run2011A_PromptReco_v4-skimTauIdEffSample2_cfg/1/skimTauIdEffSample2_cfg-0CE79965-69A3-E011-AAB8-BCAEC518FF89.root'
options.isMC = 0
options.parseArguments()

process = cms.Process("PAT")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.MessageLogger.suppressWarning = cms.untracked.vstring("PATTriggerProducer",)

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
)

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output; you need a '*' to
    # unpack the list of commands 'patEventContent'
    outputCommands = cms.untracked.vstring('drop *', *patEventContent )
)

process.load('Configuration/StandardSequences/Services_cff')
process.load('Configuration/StandardSequences/GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string(options.globalTag)

process.sequence = cms.Sequence()

process.load("HLTrigger.HLTfilters.hltHighLevel_cfi")
process.hltHighLevel.HLTPaths = cms.vstring('HLT_IsoMu17_v*')

################################################################################
############## Compute some initial reco stuff #################################
################################################################################

# Run rho corrections
from RecoJets.Configuration.RecoPFJets_cff import kt6PFJets
kt6PFJets.Rho_EtaMax = cms.double(2.5)
kt6PFJets.doRhoFastjet = True
process.kt6PFJets = kt6PFJets
process.sequence += process.kt6PFJets

################################################################################
############## PU weighting   ##################################################
################################################################################

process.load("FinalStateAnalysis.RecoTools.lumiWeighting_cfi")
process.sequence += process.lumiWeights


################################################################################
############## Select PV      ##################################################
################################################################################

process.selectPrimaryVerticesQuality = cms.EDFilter(
    "VertexSelector",
    src = cms.InputTag('offlinePrimaryVerticesWithBS'),
    cut = cms.string("isValid & ndof >= 7 && abs(z) < 24 && position.Rho < 2.0"),
    filter = cms.bool(False),
)

process.selectedPrimaryVertex = cms.EDFilter(
    "PATSingleVertexSelector",
    mode = cms.string('firstVertex'),
    vertices = cms.InputTag('selectPrimaryVerticesQuality'),
    filter = cms.bool(True)
)

process.selectPrimaryVertex = cms.Sequence(
    process.selectPrimaryVerticesQuality
    *process.selectedPrimaryVertex
)

process.sequence += process.selectPrimaryVertex

# Rerun tauID
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
process.sequence += process.PFTau

################################################################################
############## PAT configuration ###############################################
################################################################################
process.load("PhysicsTools.PatAlgos.patSequences_cff")
process.sequence += process.patDefaultSequence

# Add ak5PFJets
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection
jec = [ 'L1Offset', 'L2Relative', 'L3Absolute' ]
if not options.isMC:
    jec.extend([ 'L2L3Residual' ])

switchJetCollection(process, cms.InputTag('ak5PFJets'),
                 #'AK5', 'PF',
                 doJTA            = False,
                 doBTagging       = True,
                 #jetCorrLabel     = ('AK5Calo', cms.vstring(jec)),
                 #jetCorrLabel     = ('AK5PF', cms.vstring(jec)),
                 jetCorrLabel     = None,
                 doType1MET       = False,
                 #genJetCollection = cms.InputTag("ak5GenJets"),
                 genJetCollection = (
                     cms.InputTag("ak5GenJets") if options.isMC else None),
                 doJetID          = True,
                 jetIdLabel       = "ak5",
                 outputModule     = '')

# TODO FIXME
process.patJetCorrections.remove(process.patJetCorrFactors)

# add pfMET
# set Boolean swich to true in order to apply type-1 corrections
from PhysicsTools.PatAlgos.tools.metTools import addPfMET
# NB not the same as Christians!
addPfMET(process)
process.patMETsPF.addGenMET = True if options.isMC else False

# Check if we are running on data
from PhysicsTools.PatAlgos.tools.coreTools import runOnData

if not options.isMC:
    runOnData(process)

#from PhysicsTools.PatAlgos.tools.trigTools import switchOnTrigger
# FIXME
#--------------------------------------------------------------------------------
# configure PAT trigger matching
#switchOnTrigger(process, hltProcess = options.hltProcess, outputModule = '')

#process.patTrigger.addL1Algos = cms.bool(True)
# CV: disable L1Algos for now, to prevent error messages
#
#     %MSG-e L1GlobalTriggerObjectMapRecord:  PATTriggerProducer:patTrigger
#
#       ERROR: The requested algorithm name = L1_DoubleEG1
#       does not exists in the trigger menu.
#       Returning zero pointer for getObjectMap
#
#     to be printed for every event (06/05/2011)
#process.patTrigger.addL1Algos = cms.bool(False)

################################################################################
############## Muon creation  ##################################################
################################################################################

process.muonEmbedding = cms.Sequence()

# Create muon collection with PF Iso info embedded.
# Output of embedding sequence is patMuonsLoosePFIsoEmbedded06
process.load("FinalStateAnalysis.TagAndProbe.patMuonPFIsoEmbedding_cff")


process.muonEmbedding += process.patMuonsLoosePFIsoEmbedded

# Embed VBTF ID
process.patMuonsEmbedWWId = cms.EDProducer(
    "PATMuonIdEmbedder",
    src = cms.InputTag("patMuonsLoosePFIsoEmbedded06"),
    userIntLabel = cms.string("WWID"),
    beamSpotSource = cms.InputTag("offlineBeamSpot"),
    vertexSource = cms.InputTag("selectedPrimaryVertex"),
)
process.muonEmbedding += process.patMuonsEmbedWWId

# Embed IP information
process.patMuonsEmbedIp = cms.EDProducer(
    "PATMuonIpEmbedder",
    src = cms.InputTag("patMuonsEmbedWWId"),
    userFloatLabel = cms.string("vertexDXY"),
    vtxSrc = cms.InputTag("selectedPrimaryVertex"),
)
process.muonEmbedding += process.patMuonsEmbedIp

# Load the necessary DB stuff for the muons
from FinalStateAnalysis.PatTools.muonSystematics_cff import \
        poolDBESSourceMuScleFitCentralValue, \
        poolDBESSourceMuScleFitShiftUp, \
        poolDBESSourceMuScleFitShiftDown

process.muonsMesUp = poolDBESSourceMuScleFitShiftUp
process.muonsMesDown = poolDBESSourceMuScleFitShiftDown
process.muonsMesCorr = poolDBESSourceMuScleFitCentralValue

# Embed systematics, overwriting
process.selectedPatMuons = cms.EDProducer(
    "PATMuonSystematicsEmbedder",
    src = cms.InputTag("patMuonsEmbedIp"),
    corrTag = process.muonsMesCorr.appendToDataLabel,
    corrTagUp = process.muonsMesUp.appendToDataLabel,
    corrTagDown = process.muonsMesDown.appendToDataLabel,
)

# Define our selection for PAT Muons
process.selectedPatMuons.src = cms.InputTag("patMuonsEmbedIp")

process.muonEmbedding += process.selectedPatMuons

# Redefine pat order
print process.sequence.replace(process.selectedPatMuons, process.muonEmbedding)

process.selectionDefs = cms.PSet(
    muonCuts = cms.vstring(
        'isGlobalMuon()',
        'abs(eta) < 2.1',
        'userCand("nom").pt > 15.',
        'userInt("WWID") > 0.5',
        'userFloat("pfLooseIsoPt03")/pt < 0.3',
        'innerTrack.isNonnull',
        'userFloat("vertexDXY") < 0.05',
    )
)

# Define the clean muon as those that pass the analysis cut
process.cleanPatMuons = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag("selectedPatMuons"),
    cut = cms.string(
        ' &&'.join(str(cut) for cut in process.selectionDefs.muonCuts)
    ),
    filter = cms.bool(False),
)

# Define muons for the Zmumu hypothesis
process.selectedPatMuonsForZmumuHyp = cms.EDFilter(
    "PATMuonSelector",
    src = cms.InputTag("selectedPatMuons"),
    cut = cms.string('userCand("nom").pt > 10 & (isGlobalMuon() |'
                     'isTrackerMuon() | isStandAloneMuon())'),
    filter = cms.bool(False),
)
process.sequence += process.selectedPatMuonsForZmumuHyp

process.zMuMuHypotheses = cms.EDProducer(
    "DeltaRMinCandCombiner",
    decay = cms.string("cleanPatMuons@+ selectedPatMuonsForZmumuHyp@-"),
    cut = cms.string(''),
    deltaRMin = cms.double(0.3),
)
process.sequence += process.zMuMuHypotheses

################################################################################
############## Tau creation   ##################################################
################################################################################

import PhysicsTools.PatAlgos.tools.tauTools as tauTools

if options.tauType == 'HPS':
    tauTools.switchToPFTauHPS(process)

# Setup all the JES correction nonsense
#process.jec = cms.ESSource(
    #"PoolDBESSource",
    #DBParameters = cms.PSet(
        #messageLevel = cms.untracked.int32(0)
    #),
    #timetype = cms.string('runnumber'),
    #toGet = cms.VPSet(
        #cms.PSet(
            #record = cms.string('JetCorrectionsRecord'),
            #tag    = cms.string('JetCorrectorParametersCollection_Jec11V2_AK5PF'),
            #label  = cms.untracked.string('AK5PF')
        #),
    #),
    #connect = cms.string('sqlite_fip:TauAnalysis/Configuration/data/Jec11V2.db')
#)
#process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'jec')

jetCorrectionType = "ak5PFL1L2L3Residual" if not options.isMC else "ak5PFL1L2L3"

# Embed the systematics in the taus
process.systematicsTaus = cms.EDProducer(
    "PATTauSystematicsEmbedder",
    src = cms.InputTag("patTaus"),
    unclusteredEnergyScale = cms.double(0.1),
    tauEnergyScale = cms.PSet(
        applyCorrection = cms.bool(False),
        uncLabelUp = cms.string("AK5PF"),
        uncLabelDown = cms.string("AK5PF"),
        uncTag = cms.string("Uncertainty"),
        flavorUncertainty = cms.double(0),
    ),
    jetEnergyScale = cms.PSet(
        applyCorrection = cms.bool(True),
        corrLabel = cms.string(jetCorrectionType),
        uncLabelUp = cms.string("AK5PF"),
        uncLabelDown = cms.string("AK5PF"),
        uncTag = cms.string("Uncertainty"),
        flavorUncertainty = cms.double(0),
    ),
)

process.embedGenTaus = cms.EDProducer(
    "PATTauGenInfoEmbedder",
    src = cms.InputTag("systematicsTaus")
)

# TauID preselection
process.selectedPatTaus = cms.EDFilter(
    "PATPFTauSelectorForTauIdEff2",
    src = cms.InputTag("embedGenTaus"),
    #minJetPt = cms.double(20.0),
    minJetPt = cms.double(15), # lower for systematics reasons
    maxJetEta = cms.double(2.3),
    trackQualityCuts = process.PFTauQualityCuts.signalQualityCuts,
    minLeadTrackPt = cms.double(5.0),
    maxDzLeadTrack = cms.double(0.2),
    maxLeadTrackPFElectronMVA = cms.double(0.6),
    #applyECALcrackVeto = cms.bool(True),
    applyECALcrackVeto = cms.bool(False),
    minDeltaRtoNearestMuon = cms.double(0.5),
    muonSelection = cms.string("isGlobalMuon() | isTrackerMuon() | isStandAloneMuon()"),
    srcMuon = cms.InputTag('patMuons'),
    pfIsolation = cms.PSet(
        chargedHadronIso = cms.PSet(
            ptMin = cms.double(1.0),
            dRvetoCone = cms.double(0.15),
            dRisoCone = cms.double(0.6)
        ),
        neutralHadronIso = cms.PSet(
            ptMin = cms.double(1000.),
            dRvetoCone = cms.double(0.15),
            dRisoCone = cms.double(0.)
        ),
        photonIso = cms.PSet(
            ptMin = cms.double(1.5),
            dPhiVeto = cms.double(-1.),  # asymmetric Eta x Phi veto region
            dEtaVeto = cms.double(-1.),  # to account for photon conversions in electron isolation case
            dRvetoCone = cms.double(0.15),
            dRisoCone = cms.double(0.6)
        )
    ),
    maxPFIsoPt = cms.double(2.5),
    srcPFIsoCandidates = cms.InputTag('pfNoPileUp'),
    srcBeamSpot = cms.InputTag('offlineBeamSpot'),
    srcVertex = cms.InputTag('offlinePrimaryVertices'),
    filter = cms.bool(False)
)


process.patTauSelectionSeq = cms.Sequence(
    process.systematicsTaus * process.embedGenTaus * process.selectedPatTaus)

# Put the preselection immediately after the selection so we can use it for the
# clean pat taus.
process.sequence.replace(process.selectedPatTaus, process.patTauSelectionSeq)

process.load("FinalStateAnalysis.PatTools.electrons.electronSystematics_cfi")
process.electronSystematics.src = cms.InputTag("cleanPatElectrons")

################################################################################
############## Embed systematics in MET ########################################
################################################################################
process.metTypeCategorization = cms.PSet(
    tauCut = cms.string(
        '(userInt("ps_sel_jes-") && tauID("%s"))' % options.tauIDForMET
    ),
    jetCut = cms.string(
        '!(userInt("ps_sel_jes-") && tauID("%s")) && pt > 10' % options.tauIDForMET
    ),
    unclusteredCut = cms.string(
        '!(userInt("ps_sel_jes-") && tauID("%s")) && pt < 10' % options.tauIDForMET
    ),
)
process.systematicsMET = cms.EDProducer(
    "PATMETSystematicsEmbedder",
    src = cms.InputTag("patMETsPF"),
    tauSrc = cms.InputTag("selectedPatTaus"),
    muonSrc = cms.InputTag("cleanPatMuons"),
    electronSrc = cms.InputTag("electronSystematics"),
    tauCut = process.metTypeCategorization.tauCut,
    jetCut = process.metTypeCategorization.jetCut,
    unclusteredCut = process.metTypeCategorization.unclusteredCut,
)
process.sequence += process.electronSystematics
process.sequence += process.systematicsMET

################################################################################
############## Build mu tau pairs       ########################################
################################################################################
process.rawMuTauPairs = cms.EDProducer(
    "PATMuTauSystematicsProducer",
    srcLeg1 = cms.InputTag("selectedPatMuons"),
    srcLeg2 = cms.InputTag("selectedPatTaus"),
    srcMET = cms.InputTag("systematicsMET"),
    srcVtx = cms.InputTag("offlinePrimaryVertices"),
)

process.sequence += process.rawMuTauPairs

process.muTauPairs = cms.EDProducer(
    "PATMuTauIPInfoEmbedder",
    src = cms.InputTag('rawMuTauPairs'),
    d1DirTag = cms.string('nom'),
    d2DirTag = cms.string('jet_nom'),
)
process.sequence += process.muTauPairs
process.p = cms.Path(process.sequence)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output; you need a '*' to
    # unpack the list of commands 'patEventContent'
    outputCommands = cms.untracked.vstring(
        'drop *',
        'keep recoGenParticles_genParticles*_*_*',
        'keep *_offlinePrimaryVertices*_*_*',
        'keep edmTriggerResults_TriggerResults*_*_*',
        'keep *_hltTriggerSummaryAOD_*_*',
        'keep *_muTauPairs_*_*',
        'keep *_systematicsMET_*_*',
        'keep recoLeafCandidates_*systematics*_*_*',
        'keep *_selectedPatTaus_*_*',
        'keep *_selectedPatMuons_*_*',
        'keep *_zMuMuHypotheses_*_*',
        'keep edmMergeableCounter_*_*_*',
        'keep PileupSummaryInfos_*_*_*',
        'keep PileupSummaryInfo_*_*_*',
        'keep *_lumiWeights_*_*',
    )
)

process.outpath = cms.EndPath(process.out)

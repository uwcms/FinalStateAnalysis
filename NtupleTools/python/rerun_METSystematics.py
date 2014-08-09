import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.met.pfMETSignficiance_cfi import \
    metSignficanceSequence, \
    metSigDecentMuons, \
    metSigDecentElectrons, \
    metSigDecentTausUnclean, \
    metSigDecentTaus, \
    metSigJetsDirty, \
    metSigJetsNoMuons, \
    metSigJetsNoElectrons, \
    metSigJetsClean, \
    metSigGetPFJets, \
    pfCandsNotInSelectedJets, \
    pfMEtSignCovMatrix

def rerun_metsys(process):
    process.metTypeCategorization = cms.PSet(
    tauCut = cms.string(
    	'pt > 10 && (tauID("decayModeFinding") && tauID("byLooseIsolation"))'
    ),
    jetCut = cms.string(
        '!(tauID("decayModeFinding") && tauID("byLooseIsolation")) && userCand("patJet").pt > 10'
    ),
    # The part about passing the tauID is to catch the low pt taus
    unclusteredCut = cms.string(
        'userCand("patJet").pt < 10 | (pt < 10 && tauID("decayModeFinding") && tauID("byLooseIsolation"))'
    	#'userCand("patJet").pt < 10 | (pt < 10 && !tauID("decayModeFinding") && tauID("byLooseIsolation"))'
        #'userCand("patJet").pt < 10 | (pt < 10 && tauID("decayModeFinding"))'
        #'userCand("cleanPatJets").pt < 10 | userCand("cleanPatTaus").pt < 10'
    ),
    )

    process.newsystematicsMET = cms.EDProducer(
        "PATMETSystematicsEmbedder",
        src = cms.InputTag("systematicsMET"),
        tauSrc = cms.InputTag("cleanPatTaus"),
        muonSrc = cms.InputTag("cleanPatMuons"),
        electronSrc = cms.InputTag("cleanPatElectrons"),
        tauCut = process.metTypeCategorization.tauCut,
        jetCut = process.metTypeCategorization.jetCut,
        unclusteredCut = process.metTypeCategorization.unclusteredCut,
        applyType1ForTaus = cms.bool(False),
        applyType1ForMuons = cms.bool(False),
        applyType1ForElectrons = cms.bool(False),
        applyType1ForJets = cms.bool(True),
        applyType2ForJets = cms.bool(False),
    )

    #customizeMETSequence = cms.Sequence(newsystematicsMET)

    process.rerun_metsys = cms.Path(process.newsystematicsMET)

    return process.rerun_metsys

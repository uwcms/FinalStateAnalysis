import FWCore.ParameterSet.Config as cms

def rerun_matchers(process):
    process.photonMatch = cms.EDProducer(
        "MCMatcherByPt",
        src = cms.InputTag("cleanPatPhotons"),
        maxDPtRel = cms.double(999.0),
        mcPdgId = cms.vint32(),
        mcStatus = cms.vint32(1),
        resolveByMatchQuality = cms.bool(False),
        maxDeltaR = cms.double(0.3),
        checkCharge = cms.bool(False),
        resolveAmbiguities = cms.bool(True),
        matched = cms.InputTag("genParticles")
        )
    

    process.electronMatch = cms.EDProducer(
        "MCMatcher",
        src = cms.InputTag("cleanPatElectrons"),
        maxDPtRel = cms.double(0.5),
        mcPdgId = cms.vint32(11),
        mcStatus = cms.vint32(1),
        resolveByMatchQuality = cms.bool(False),
        maxDeltaR = cms.double(0.5),
        checkCharge = cms.bool(False),
        resolveAmbiguities = cms.bool(True),
        matched = cms.InputTag("genParticles")
        )

    process.muonMatch = cms.EDProducer(
        "MCMatcher",
        src = cms.InputTag("cleanPatMuons"),
        maxDPtRel = cms.double(0.5),
        mcPdgId = cms.vint32(13),
        mcStatus = cms.vint32(1),
        resolveByMatchQuality = cms.bool(False),
        maxDeltaR = cms.double(0.5),
        checkCharge = cms.bool(True),
        resolveAmbiguities = cms.bool(True),
        matched = cms.InputTag("genParticles")
        )

    process.tauMatch = cms.EDProducer(
        "MCMatcher",
        src = cms.InputTag("cleanPatTaus"),
        maxDPtRel = cms.double(999.9),
        mcPdgId = cms.vint32(15),
        mcStatus = cms.vint32(2),
        resolveByMatchQuality = cms.bool(False),
        maxDeltaR = cms.double(999.9),
        checkCharge = cms.bool(True),
        resolveAmbiguities = cms.bool(True),
        matched = cms.InputTag("genParticles")
        )

    process.patJetGenJetMatch = cms.EDProducer(
        "GenJetMatcher",
        src = cms.InputTag("selectedPatJets"),
        maxDPtRel = cms.double(3.0),
        mcPdgId = cms.vint32(),
        mcStatus = cms.vint32(),
        resolveByMatchQuality = cms.bool(False),
        maxDeltaR = cms.double(0.4),
        checkCharge = cms.bool(False),
        resolveAmbiguities = cms.bool(True),
        matched = cms.InputTag("ak5GenJets")
        )

    process.patJetPartonMatch = cms.EDProducer(
        "MCMatcher",
        src = cms.InputTag("selectedPatJets"),
        maxDPtRel = cms.double(3.0),
        mcPdgId = cms.vint32(1, 2, 3, 4, 5, 
                             21),
        mcStatus = cms.vint32(3),
        resolveByMatchQuality = cms.bool(False),
        maxDeltaR = cms.double(0.4),
        checkCharge = cms.bool(False),
        resolveAmbiguities = cms.bool(True),
        matched = cms.InputTag("genParticles")
        )

    process.cleanPatElectronsRematched = cms.EDProducer(
        "PATElectronGenRematchEmbedder",
        src = cms.InputTag('cleanPatElectrons'),
        matchSrc = cms.InputTag('electronMatch')
        )

    process.cleanPatMuonsRematched = cms.EDProducer(
        "PATMuonGenRematchEmbedder",
        src = cms.InputTag('cleanPatMuons'),
        matchSrc = cms.InputTag('muonMatch')
        )

    process.cleanPatTausRematched = cms.EDProducer(
        "PATTauGenRematchEmbedder",
        src = cms.InputTag('cleanPatTaus'),
        matchSrc = cms.InputTag('tauMatch')
        )

    process.cleanPatPhotonsRematched = cms.EDProducer(
        "PATPhotonGenRematchEmbedder",
        src = cms.InputTag('cleanPatPhotons'),
        matchSrc = cms.InputTag('photonMatch')
        )
    process.photonParentage = cms.EDProducer(
        "PATPhotonParentageEmbedder",
        src = cms.InputTag("cleanPatPhotonsRematched")
        )

    process.selectedPatJetsRematched = cms.EDProducer(
        "PATJetGenRematchEmbedder",
        src = cms.InputTag('selectedPatJets'),
        matchSrc = cms.InputTag('patJetPartonMatch'),
        genJetMatchSrc = cms.InputTag('patJetGenJetMatch'),
        )

    process.rerunMCMatch = cms.Sequence( process.electronMatch+
                                         process.cleanPatElectronsRematched+
                                         process.muonMatch+
                                         process.cleanPatMuonsRematched+
                                         process.tauMatch+
                                         process.cleanPatTausRematched+
                                         process.photonMatch+
                                         process.cleanPatPhotonsRematched+
                                         process.photonParentage+
                                         process.patJetGenJetMatch+
                                         process.patJetPartonMatch+
                                         process.selectedPatJetsRematched )    
    
    process.rerunMCMatchPath = cms.Path(process.rerunMCMatch)

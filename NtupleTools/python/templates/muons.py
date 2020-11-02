'''

Ntuple branch template sets for muon objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# ID and isolation
id = PSet(
    objectCutBasedIdLoose = '{object}.userInt("CutBasedIdLoose")',
    objectCutBasedIdMedium = '{object}.userInt("CutBasedIdMedium")',
    objectCutBasedIdMediumPrompt = '{object}.userInt("CutBasedIdMediumPrompt")',
    objectCutBasedIdTight = '{object}.userInt("CutBasedIdTight")',
    objectCutBasedIdGlobalHighPt = '{object}.userInt("CutBasedIdGlobalHighPt")',
    objectCutBasedIdTrkHighPt = '{object}.userInt("CutBasedIdTrkHighPt")',
    objectPFIsoVeryLoose = '{object}.userInt("PFIsoVeryLoose")',
    objectPFIsoLoose = '{object}.userInt("PFIsoLoose")',
    objectPFIsoMedium = '{object}.userInt("PFIsoMedium")',
    objectPFIsoTight = '{object}.userInt("PFIsoTight")',
    objectPFIsoVeryTight = '{object}.userInt("PFIsoVeryTight")',
    #objectPFIsoVeryVeryTight = '{object}.userInt("PFIsoVeryVeryTight")', # for CMSSW_10_1_X
    objectTkIsoLoose = '{object}.userInt("TkIsoLoose")',
    objectTkIsoTight = '{object}.userInt("TkIsoTight")',
    objectSoftCutBasedId = '{object}.userInt("SoftCutBasedId")',
    #objectSoftMvaId = '{object}.userInt("SoftMvaId")', # for CMSSW_10_1_X
    objectMvaLoose = '{object}.userInt("MvaLoose")',
    objectMvaMedium = '{object}.userInt("MvaMedium")',
    objectMvaTight = '{object}.userInt("MvaTight")',
    objectMiniIsoLoose = '{object}.userInt("MiniIsoLoose")',
    objectMiniIsoMedium = '{object}.userInt("MiniIsoMedium")',
    objectMiniIsoTight = '{object}.userInt("MiniIsoTight")',
    objectMiniIsoVeryTight = '{object}.userInt("MiniIsoVeryTight")',
    #objectTriggerIdLoose = '{object}.userInt("TriggerIdLoose")', # for CMSSW_10_1_X 
    #objectInTimeMuon = '{object}.userInt("InTimeMuon")', # for CMSSW_10_1_X
    #objectMultiIsoLoose = '{object}.userInt("MultiIsoLoose")', # for CMSSW_10_1_X
    #objectMultiIsoMedium = '{object}.userInt("MultiIsoMedium")', # for CMSSW_10_1_X

    objectMvaTopId = cms.string('{object}.userFloat("muonMVATopID")'),
    objectPFIDTight = 'isTightMuon({object_idx})',
    objectPFIDMedium = '{object}.isMediumMuon()',
    objectPFIDLoose = '{object}.isLooseMuon()',
    objectSegmentCompatibility = '{object}.segmentCompatibility()',
    # For charged, we use ALL charged particles
    objectPFChargedIso = cms.string('{object}.userIsolation("PfChargedHadronIso")'),
    objectPFNeutralIso = cms.string('{object}.userIsolation("PfNeutralHadronIso")'),
    objectPFPhotonIso  = cms.string('{object}.userIsolation("PfGammaIso")'),
    objectPFPUChargedIso = cms.string('{object}.userIsolation("PfPUChargedHadronIso")'),
    objectTrkIsoDR03 = cms.string('{object}.trackIso()'),
    objectEcalIsoDR03 = cms.string('{object}.ecalIso()'),
    objectHcalIsoDR03 = cms.string('{object}.hcalIso()'),
    objectRelPFIsoDBDefault = cms.string(
        "({object}.chargedHadronIso()"
        "+max({object}.photonIso()"
        "+{object}.neutralHadronIso()"
        "-0.5*{object}.puChargedHadronIso,0.0))"
        "/{object}.pt()"
    ),
    objectPFChargedHadronIsoR04 = cms.string('{object}.pfIsolationR04().sumChargedHadronPt'),
    objectPFNeutralHadronIsoR04 = cms.string('{object}.pfIsolationR04().sumNeutralHadronEt'),
    objectPFPhotonIsoR04 = cms.string('{object}.pfIsolationR04().sumPhotonEt'),
    objectPFPileupIsoR04 = cms.string('{object}.pfIsolationR04().sumPUPt'),
    objectRelPFIsoDBDefaultR04 = cms.string(
        '({object}.pfIsolationR04().sumChargedHadronPt'
        '+ max(0., {object}.pfIsolationR04().sumNeutralHadronEt'
        '+ {object}.pfIsolationR04().sumPhotonEt'
        '- 0.5*{object}.pfIsolationR04().sumPUPt))'
        '/{object}.pt()'
    ),

    objectIsPFMuon = '{object}.isPFMuon',
    objectIsGlobal = '{object}.isGlobalMuon',
    objectIsTracker = '{object}.isTrackerMuon',
    objectTypeCode = cms.vstring('{object}.type','I'),
    objectBestTrackType = '{object}.muonBestTrackType',
    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}, 13, 1).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 13, 1).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 13, 1).pdgId() : -999',
    #objectComesFromHiggs = 'comesFromHiggs({object_idx}, 13, 1)',
        

    objectGenPromptTauDecay       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPromptTauDecayProduct() : -999',
    objectGenTauDecay       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isTauDecayProduct() : -999',
    objectGenPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',

    objectGenParticle    = '? ({object}.genParticleRef.isNonnull() ) ? {object}.genParticleRef().pdgId() : -999',
    objectGenPdgId       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).pdgId() : -999',
    objectGenCharge      = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).charge() : -999',
    objectGenEnergy      = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).energy() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).eta()   : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).phi()   : -999',
    objectGenPt          = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).pt()   : -999',
    objectGenVZ          = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).vz()   : -999',
    #objectGenVtxPVMatch  = 'genVtxPVMatch({object_idx})', # is PV closest vtx to gen vtx?
    ## closest Z mass
    #objectNearestZMass = 'closestZMuon({object_idx},"")',
    ## lowest invariant mass
    #objectLowestMll = 'smallestMmm({object_idx},"")',
)

energyCorrections = PSet(
    #objectPt_MuonEnUp = '? daughterHasUserCand({object_idx}, "mesUpMuons") ? daughterAsMuon({object_idx}).userCand("mesUpMuons").pt : -999.',
    #objectEta_MuonEnUp = '? daughterHasUserCand({object_idx}, "mesUpMuons") ? daughterAsMuon({object_idx}).userCand("mesUpMuons").eta : -999.',
    #objectPhi_MuonEnUp = '? daughterHasUserCand({object_idx}, "mesUpMuons") ? daughterAsMuon({object_idx}).userCand("mesUpMuons").phi : -999.',

    #objectPt_MuonEnDown = '? daughterHasUserCand({object_idx}, "mesDownMuons") ? daughterAsMuon({object_idx}).userCand("mesDownMuons").pt : -999.',
    #objectEta_MuonEnDown = '? daughterHasUserCand({object_idx}, "mesDownMuons") ? daughterAsMuon({object_idx}).userCand("mesDownMuons").eta : -999.',
    #objectPhi_MuonEnDown = '? daughterHasUserCand({object_idx}, "mesDownMuons") ? daughterAsMuon({object_idx}).userCand("mesDownMuons").phi : -999.',

)

# Information about the associated track
tracking = PSet(
    objectPixHits = '? {object}.innerTrack.isNonnull ? '
        '{object}.innerTrack.hitPattern.numberOfValidPixelHits :-1',
    objectNormalizedChi2 = '? {object}.globalTrack.isNonnull ? '
        '{object}.globalTrack().normalizedChi2() : -1',
    objectValidFraction = '? {object}.innerTrack.isNonnull ? '
        '{object}.innerTrack().validFraction() : -1',
    objectChi2LocalPosition = '{object}.combinedQuality().chi2LocalPosition()',
    objectTrkKink = '{object}.combinedQuality().trkKink()',
    objectNormTrkChi2 = "? {object}.combinedMuon.isNonnull ? "
        "{object}.combinedMuon.normalizedChi2 : 1e99",
    objectTkLayersWithMeasurement = '? {object}.innerTrack.isNonnull ? '
        '{object}.innerTrack().hitPattern().trackerLayersWithMeasurement : -1',
    objectMuonHits = '? {object}.globalTrack.isNonnull ? '
        '{object}.globalTrack().hitPattern().numberOfValidMuonHits() : -1',
    objectMatchedStations = '{object}.numberOfMatchedStations',
)

# Trigger matching
trigger_50ns = PSet(
)

trigger_25ns = PSet(
)

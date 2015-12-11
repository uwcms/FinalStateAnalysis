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
    objectPFIDTight = 'isTightMuon({object_idx})',
    objectPFIDMedium = '{object}.isMediumMuon()',
    objectPFIDLoose = '{object}.isLooseMuon()',
    # For charged, we use ALL charged particles
    objectEffectiveArea2012 = '{object}.userFloat("ea_comb_iso04_kt6PFJCNth05")',
    objectEffectiveArea2011 = '{object}.userFloat("ea_comb_iso04_kt6PFJCth05")',
    objectRho = cms.string('{object}.userFloat("rho_fastjet")'),
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
    objectRelPFIsoRho = cms.string(
        '({object}.chargedHadronIso()'
        '+max(0.0,{object}.neutralHadronIso()'
        '+{object}.photonIso()'
        '-{object}.userFloat("rho_fastjet")*{object}.userFloat("ea_comb_iso04_kt6PFJCNth05")))'
        '/{object}.pt()'
    ),
    objectRelPFIsoRhoFSR = cms.string(
        '({object}.chargedHadronIso()'
        '+max(0.0,{object}.neutralHadronIso()'
        '+{object}.photonIso() - userFloat("leg{object_idx}fsrIsoCorr")'
        '-{object}.userFloat("rho_fastjet")*{object}.userFloat("ea_comb_iso04_kt6PFJCNth05")))'
        '/{object}.pt()'
    ),

    objectIsPFMuon = '{object}.isPFMuon',
    objectIsGlobal = '{object}.isGlobalMuon',
    objectIsTracker = '{object}.isTrackerMuon',
    objectTypeCode = cms.vstring('{object}.type','I'),
    objectBestTrackType = '{object}.muonBestTrackType',
    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}, 13, 1).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 13, 1).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 13, 1).pdgId() : -999',
    objectComesFromHiggs = 'comesFromHiggs({object_idx}, 13, 1)',
        

    objectGenPromptTauDecay       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPromptTauDecayProduct() : -999',
    objectGenTauDecay       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isTauDecayProduct() : -999',
    objectGenPrompt       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).statusFlags().isPrompt() : -999',

    objectGenPdgId       = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).pdgId() : -999',
    objectGenCharge      = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).charge() : -999',
    objectGenEnergy      = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).energy() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).eta()   : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).phi()   : -999',
    objectGenPt          = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).pt()   : -999',
    objectGenVZ          = '? (getDaughterGenParticle({object_idx}, 13, 0).isAvailable && getDaughterGenParticle({object_idx}, 13, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 13, 0).vz()   : -999',
    objectGenVtxPVMatch  = 'genVtxPVMatch({object_idx})', # is PV closest vtx to gen vtx?
    # closest Z mass
    objectNearestZMass = 'closestZMuon({object_idx},"")',
    # lowest invariant mass
    objectLowestMll = 'smallestMmm({object_idx},"")',
)

energyCorrections = PSet(
    # left as template
    #objectERochCor2012 = 'getUserLorentzVector({object_idx},"p4_RochCor2012").t',
    #objectPtRochCor2012 = 'getUserLorentzVector({object_idx},"p4_RochCor2012").Pt',
    #objectEtaRochCor2012 = 'getUserLorentzVector({object_idx},"p4_RochCor2012").Eta',
    #objectPhiRochCor2012 = 'getUserLorentzVector({object_idx},"p4_RochCor2012").Phi',
    #objectEErrRochCor2012 = '{object}.userFloat("p4_RochCor2012_tkFitErr")'
)

# Information about the associated track
tracking = PSet(
    objectPixHits = '? {object}.innerTrack.isNonnull ? '
        '{object}.innerTrack.hitPattern.numberOfValidPixelHits :-1',
    objectNormTrkChi2 = "? {object}.combinedMuon.isNonnull ? "
        "{object}.combinedMuon.normalizedChi2 : 1e99",
    objectTkLayersWithMeasurement = '? {object}.innerTrack.isNonnull ? '
        '{object}.innerTrack().hitPattern().trackerLayersWithMeasurement : -1',
    objectMuonHits = '? {object}.globalTrack.isNonnull ? '
        '{object}.globalTrack().hitPattern().numberOfValidMuonHits() : -1',
    objectMatchedStations = '{object}.numberOfMatchedStations',
    #objectD0 = '{object}.dB("PV3D")',
)

# Trigger matching
trigger_50ns = PSet(
    objectMatchesSingleMu = r'matchToHLTPath({object_idx},"HLT_Mu40_v\\d+",0.5)',
    objectMatchesSingleMu_leg1 = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_v\\d+",0.5)',
    objectMatchesSingleMu_leg2 = r'matchToHLTPath({object_idx},"HLT_Mu8_TrkIsoVVL_v\\d+",0.5)',
    objectMatchesSingleMu_leg1_noiso = r'matchToHLTPath({object_idx},"HLT_Mu17_v\\d+",0.5)',
    objectMatchesSingleMu_leg2_noiso = r'matchToHLTPath({object_idx},"HLT_Mu8_v\\d+",0.5)',
    objectMatchesDoubleMu = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\d+|HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+",0.5)',
    objectMatchesSingleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleMuSingleE = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesTripleMu = r'matchToHLTPath({object_idx},"HLT_TripleMu_12_10_5_v\\d+",0.5)',
    objectMatchesDoubleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleMuSingleE = r'matchToHLTPath({object_idx},"HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\d+",0.5)',
)

trigger_25ns = PSet(
    objectMatchesSingleMuIso20 = r'matchToHLTPath({object_idx},"HLT_IsoMu20_v\\d+",0.5)',
    objectMatchesSingleMu = r'matchToHLTPath({object_idx},"HLT_Mu50_v\\d+",0.5)',
    objectMatchesSingleMu_leg1 = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_v\\d+",0.5)',
    objectMatchesSingleMu_leg2 = r'matchToHLTPath({object_idx},"HLT_Mu8_TrkIsoVVL_v\\d+",0.5)',
    objectMatchesSingleMu_leg1_noiso = r'matchToHLTPath({object_idx},"HLT_Mu17_v\\d+",0.5)',
    objectMatchesSingleMu_leg2_noiso = r'matchToHLTPath({object_idx},"HLT_Mu8_v\\d+",0.5)',
    objectMatchesDoubleMu = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\d+|HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+",0.5)',
    objectMatchesSingleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleMuSingleE = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesTripleMu = r'matchToHLTPath({object_idx},"HLT_TripleMu_12_10_5_v\\d+",0.5)',
    objectMatchesDoubleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleMuSingleE = r'matchToHLTPath({object_idx},"HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\d+",0.5)',
)


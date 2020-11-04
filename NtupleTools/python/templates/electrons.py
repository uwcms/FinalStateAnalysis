'''

Ntuple branch template sets for electron objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Electron
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# ID and isolation
id = PSet(
    objectCBIDVeto = '{object}.electronID("cutBasedElectronID-Fall17-94X-V2-veto")',
    objectCBIDLoose = '{object}.electronID("cutBasedElectronID-Fall17-94X-V2-loose")',
    objectCBIDMedium = '{object}.electronID("cutBasedElectronID-Fall17-94X-V2-medium")',
    objectCBIDTight = '{object}.electronID("cutBasedElectronID-Fall17-94X-V2-tight")',
    objectMVAIsoWP80 = '{object}.electronID("mvaEleID-Fall17-iso-V2-wp80")',
    objectMVAIsoWP90 = '{object}.electronID("mvaEleID-Fall17-iso-V2-wp90")',
    objectMVAIsoWPHZZ = '{object}.electronID("mvaEleID-Fall17-iso-V2-wpHZZ")',
    objectMVAIsoWPLoose = '{object}.electronID("mvaEleID-Fall17-iso-V2-wpLoose")',
    objectMVANoisoWP80 = '{object}.electronID("mvaEleID-Fall17-noIso-V2-wp80")',
    objectMVANoisoWP90 = '{object}.electronID("mvaEleID-Fall17-noIso-V2-wp90")',
    objectMVANoisoWPLoose = '{object}.electronID("mvaEleID-Fall17-noIso-V2-wpLoose")',
    objectElectronMvaSummer16GP = '{object}.userFloat("ElectronMVAEstimatorRun2Spring16GeneralPurposeV1Values")',
    objectElectronMvaFall17v1NoIso = '{object}.userFloat("ElectronMVAEstimatorRun2Fall17NoIsoV1Values")',
    objectElectronMvaFall17NoIso = '{object}.userFloat("ElectronMVAEstimatorRun2Fall17NoIsoV2Values")',

    objectCorrectedEt = '{object}.userFloat("ecalTrkEnergyPostCorr")',
    objectEnergyScaleDown = '{object}.userFloat("energyScaleDown")',
    objectEnergyScaleUp = '{object}.userFloat("energyScaleUp")',
    objectEnergyScaleStatDown = '{object}.userFloat("energyScaleStatDown")',
    objectEnergyScaleStatUp = '{object}.userFloat("energyScaleStatUp")',
    objectEnergyScaleSystDown = '{object}.userFloat("energyScaleSystDown")',
    objectEnergyScaleSystUp = '{object}.userFloat("energyScaleSystUp")',
    objectEnergyScaleGainDown = '{object}.userFloat("energyScaleGainDown")',
    objectEnergyScaleGainUp = '{object}.userFloat("energyScaleGainUp")',
    objectEnergySigmaDown = '{object}.userFloat("energySigmaDown")',
    objectEnergySigmaUp = '{object}.userFloat("energySigmaUp")',
    objectEnergySigmaPhiDown = '{object}.userFloat("energySigmaPhiDown")',
    objectEnergySigmaPhiUp = '{object}.userFloat("energySigmaPhiUp")',
    objectEnergySigmaRhoDown = '{object}.userFloat("energySigmaRhoDown")',
    objectEnergySigmaRhoUp = '{object}.userFloat("energySigmaRhoUp")',

    objectRelPFIsoDB = cms.string(
        "({object}.userIsolation('PfChargedHadronIso')"
        "+max({object}.userIsolation('PfNeutralHadronIso')"
        "+{object}.userIsolation('PfGammaIso')"
        "-0.5*{object}.userIsolation('PfPUChargedHadronIso'),0.0))"
        "/{object}.pt()"
    ),
    objectRelPFIsoRho = cms.string(
        '({object}.pfIsolationVariables().sumChargedHadronPt'
        '+max(0.0,{object}.pfIsolationVariables().sumNeutralHadronEt'
        '+{object}.pfIsolationVariables().sumPhotonEt'
        '-{object}.userFloat("rho_fastjet")*{object}.userFloat("EffectiveArea")))'
        '/{object}.pt()'
    ),
    objectMiniIso = cms.string('{object}.userFloat("miniIso")'),
    objectIP3D = cms.string('{object}.userFloat("ip3D")'),
    objectIP3DS = cms.string('{object}.userFloat("ip3DS")'),
    objectIPDXY = cms.string('{object}.userFloat("ipDXY")'),

    # Number of matched conversions
    objectPassesConversionVeto = '{object}.passConversionVeto()',

    objectPFChargedIso = cms.string('{object}.userIsolation("PfChargedHadronIso")'),
    objectPFNeutralIso = cms.string('{object}.userIsolation("PfNeutralHadronIso")'),
    objectPFPhotonIso  = cms.string('{object}.userIsolation("PfGammaIso")'),
    objectPFPUChargedIso = cms.string('{object}.userIsolation("PfPUChargedHadronIso")'),

    #objectEffectiveArea2012Data = cms.string('{object}.userFloat("ea_comb_Data2012_iso04_kt6PFJ")'),
    #objectEffectiveAreaSpring15 = cms.string('{object}.userFloat("EffectiveArea")'),

    objectMvaTopId = cms.string('{object}.userFloat("electronMVATopID")'),
    objectPtRatio = cms.string('{object}.userFloat("ptRatio")'),
    objectClosestJetDeepFlavor = cms.string('{object}.userFloat("closestJetDeepFlavor")'),
    objectRho = cms.string('{object}.userFloat("rho_fastjet")'),
    objectRelIso = cms.string("({object}.dr03TkSumPt()"
               "+max({object}.dr03EcalRecHitSumEt()-1.0,0.0)"
               "+{object}.dr03HcalTowerSumEt())/{object}.pt()"),
    objectTrkIsoDR03 = cms.string("{object}.dr03TkSumPt()"),
    objectEcalIsoDR03 = cms.string("{object}.dr03EcalRecHitSumEt()"),
    objectHcalIsoDR03 = cms.string("{object}.dr03HcalTowerSumEt()"),
    objectChargeIdTight = '{object}.isGsfCtfScPixChargeConsistent',
    objectChargeIdMed = '{object}.isGsfScPixChargeConsistent',
    objectChargeIdLoose = '{object}.isGsfCtfChargeConsistent',
    ## raw energy error
    #objectEnergyError = '{object}.corrections().combinedP4Error',
    ## shower shape / ID variables
    objectHadronicOverEM = '{object}.hcalOverEcal',
    objectElectronEInvMinusPInv = cms.string("(1.0 - {object}.eSuperClusterOverP())/{object}.correctedEcalEnergy()"),
    #objectHadronicDepth1OverEm = '{object}.hcalDepth1OverEcal',
    #objectHadronicDepth2OverEm = '{object}.hcalDepth2OverEcal',
    objectSigmaIEtaIEta = '{object}.sigmaIetaIeta',
    #objectdeltaEtaSuperClusterTrackAtVtx = '{object}.deltaEtaSuperClusterTrackAtVtx',
    #objectdeltaPhiSuperClusterTrackAtVtx = '{object}.deltaPhiSuperClusterTrackAtVtx',
    #objectfBrem = '{object}.fbrem',
    #objecteSuperClusterOverP = '{object}.eSuperClusterOverP',
    #objectecalEnergy = '{object}.ecalEnergy',
    #objecttrackMomentumAtVtxP = '{object}.trackMomentumAtVtx.r',
    #objectE1x5 = '{object}.scE1x5',
    #objectE2x5Max = '{object}.scE2x5Max',
    #objectE5x5 = '{object}.scE5x5',
    #objectNearMuonVeto = 'overlapMuons({object_idx},0.05,"isGlobalMuon() & abs(eta()) < 2.4").size()',
    #objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}, 11, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 11, 0).pdgId() : -999',
    #objectComesFromHiggs = 'comesFromHiggs({object_idx}, 11, 1)',
    objectGenParticle    = '? ({object}.genParticleRef.isNonnull() ) ? {object}.genParticleRef().pdgId() : -999',
    objectGenPdgId       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).pdgId() : -999',
    objectGenCharge      = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).charge() : -999',
    objectGenEnergy      = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).energy() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).eta()   : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).phi()   : -999',
    objectGenPt          = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).pt()   : -999',
    objectGenVZ          = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).vz()   : -999',
    objectGenVtxPVMatch  = 'genVtxPVMatch({object_idx})', # is PV closest vtx to gen vtx?
    objectGenPromptTauDecay       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isPromptTauDecayProduct() : -999',
    objectGenTauDecay       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isTauDecayProduct() : -999',
    objectGenPrompt       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).statusFlags().isPrompt() : -999',

    ## How close is the nearest muon passing some basic quality cuts?
    #objectNearestMuonDR = "electronClosestMuonDR({object_idx})",
    ## closest Z mass
    #objectNearestZMass = 'closestZElectron({object_idx},"")',
    ## lowest invariant mass
    #objectLowestMll = 'smallestMee({object_idx},"")',
)

energyCorrections = PSet(

)

tracking = PSet(
    #objectHasConversion = '{object}.userFloat("hasConversion")',
    objectMissingHits = 'getElectronMissingHits({object_idx})',
)

# Information about the matched supercluster
supercluster = PSet(
    objectSCEta = '{object}.superCluster().eta',
    objectSCPhi = '{object}.superCluster().phi',
    objectSCEnergy = '{object}.superCluster().energy',
    objectSCRawEnergy = '{object}.superCluster().rawEnergy',
    objectSCPreshowerEnergy = '{object}.superCluster().preshowerEnergy',
    objectSCPhiWidth = '{object}.superCluster().phiWidth',
    objectSCEtaWidth = '{object}.superCluster().etaWidth'   
)

trigger_50ns = PSet(
)

trigger_25ns_MC = PSet(
)

trigger_25ns = PSet(
)

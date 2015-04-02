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
    # PHYS14 IDs (some of which are still CSA14 IDs...)
    objectCBIDVeto = '{object}.userFloat("CBIDVeto")',
    objectCBIDLoose = '{object}.userFloat("CBIDLoose")',
    objectCBIDMedium = '{object}.userFloat("CBIDMedium")',
    objectCBIDTight = '{object}.userFloat("CBIDTight")',
    objectMVATrigID = '{object}.userFloat("BDTIDTrig")',
    objectMVANonTrigID = '{object}.userFloat("BDTIDNonTrig")',
    
    # Use cms.string so we get the parentheses formatting bonus
    objectRelPFIsoDB = cms.string(
        "({object}.userIso(0)"
        "+max({object}.userIso(1)"
        "+{object}.neutralHadronIso()"
        "-0.5*{object}.userIso(2),0.0))"
        "/{object}.pt()"
    ),
    objectRelPFIsoRho = cms.string(
        '({object}.chargedHadronIso()'
        '+max(0.0,{object}.neutralHadronIso()'
        '+{object}.photonIso()'
        '-{object}.userFloat("rhoCSA14")*{object}.userFloat("EffectiveArea_HZZ4l2015")))'
        '/{object}.pt()'
    ),

    objectPFChargedIso = cms.string('{object}.userIsolation("PfChargedHadronIso")'),
    objectPFNeutralIso = cms.string('{object}.userIsolation("PfNeutralHadronIso")'),
    objectPFPhotonIso  = cms.string('{object}.userIsolation("PfGammaIso")'),
    
    objectEffectiveArea2012Data = cms.string('{object}.userFloat("ea_comb_Data2012_iso04_kt6PFJ")'),
    objectEffectiveAreaPHYS14 = cms.string('{object}.userFloat("EffectiveArea_HZZ4l2015")'),

    objectRho = cms.string('{object}.userFloat("rhoCSA14")'),
    objectRelIso = cms.string("({object}.dr03TkSumPt()"
               "+max({object}.dr03EcalRecHitSumEt()-1.0,0.0)"
               "+{object}.dr03HcalTowerSumEt())/{object}.pt()"),
    objectTrkIsoDR03 = cms.string("{object}.dr03TkSumPt()"),
    objectEcalIsoDR03 = cms.string("{object}.dr03EcalRecHitSumEt()"),
    objectHcalIsoDR03 = cms.string("{object}.dr03HcalTowerSumEt()"),
    #objectChargeIdTight = '{object}.isGsfCtfScPixChargeConsistent',
    #objectChargeIdMed = '{object}.isGsfScPixChargeConsistent',
    #objectChargeIdLoose = '{object}.isGsfCtfChargeConsistent',
    # raw energy error
    objectEnergyError = '{object}.corrections().combinedP4Error',
    # shower shape / ID variables
    objectHadronicOverEM = '{object}.hcalOverEcal',
    objectHadronicDepth1OverEm = '{object}.hcalDepth1OverEcal',
    objectHadronicDepth2OverEm = '{object}.hcalDepth2OverEcal',
    objectSigmaIEtaIEta = '{object}.sigmaIetaIeta',
    objectdeltaEtaSuperClusterTrackAtVtx = '{object}.deltaEtaSuperClusterTrackAtVtx',
    objectdeltaPhiSuperClusterTrackAtVtx = '{object}.deltaPhiSuperClusterTrackAtVtx',
    objectfBrem = '{object}.fbrem',
    objecteSuperClusterOverP = '{object}.eSuperClusterOverP',
    objectecalEnergy = '{object}.ecalEnergy',
    objecttrackMomentumAtVtxP = '{object}.trackMomentumAtVtx.r',
    objectHasMatchedConversion = cms.vstring('{object}.userInt("HasMatchedConversion")','I'),    
    objectE1x5 = '{object}.scE1x5',
    objectE2x5Max = '{object}.scE2x5Max',
    objectE5x5 = '{object}.scE5x5',
    objectNearMuonVeto = 'overlapMuons({object_idx},0.05,"isGlobalMuon() & abs(eta()) < 2.4").size()',
    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}, 11, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 11, 0).pdgId() : -999',
    objectComesFromHiggs = 'comesFromHiggs({object_idx}, 11, 1)',
    objectGenPdgId       = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).pdgId() : -999',
    objectGenCharge      = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).charge() : -999',
    objectGenEnergy      = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).energy() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).eta()   : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).phi()   : -999',
    objectGenVZ          = '? (getDaughterGenParticle({object_idx}, 11, 0).isAvailable && getDaughterGenParticle({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 11, 0).vz()   : -999',
    objectGenVtxPVMatch  = 'genVtxPVMatch({object_idx})', # is PV closest vtx to gen vtx?
    
    # How close is the nearest muon passing some basic quality cuts?
    objectNearestMuonDR = "electronClosestMuonDR({object_idx})",
)

energyCorrections = PSet(
    # left as template
    #objectECorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").t',
    #objectPtCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Pt',
    #objectEtaCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Eta',
    #objectPhiCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Phi',
    #objectdECorrSmearedNoReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoSmearedNoRegression_error")',
    #
    #objectECorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").t',
    #objectPtCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Pt',
    #objectEtaCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Eta',
    #objectPhiCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Phi',
    #objectdECorrSmearedReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoSmearedRegression_error")',
    #
    #objectECorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").t',
    #objectPtCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Pt',
    #objectEtaCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Eta',
    #objectPhiCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Phi',
    #objectdECorrReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoRegressionOnly_error")',
)

tracking = PSet(
    objectHasConversion = '{object}.userFloat("hasConversion")',
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

trigger = PSet(
    objectMu17Ele8dZFilter  = 'matchToHLTFilter({object_idx}, "hltMu17Ele8dZFilter")', # HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v4-v6
    objectMu17Ele8CaloIdTPixelMatchFilter  = 'matchToHLTFilter({object_idx}, "hltMu17Ele8CaloIdTPixelMatchFilter")',
    objectL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter  = 'matchToHLTFilter({object_idx}, "hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter")',
    objectMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter  = 'matchToHLTFilter({object_idx}, "hltMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter")',
    objectEle27WP80TrackIsoMatchFilter = 'matchToHLTFilter({object_idx}, "hltEle27WP80TrackIsoFilter")',
    objectEle32WP70PFMT50PFMTFilter = 'matchToHLTFilter({object_idx},"hltEle32WP70PFMT50PFMTFilter")',
    objectEle27WP80PFMT50PFMTFilter = 'matchToHLTFilter({object_idx},"hltEle27WP80PFMT50PFMTFilter")',
    objectMatchesDoubleEPath       = r'matchToHLTPath({object_idx}, "HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v\\d+,HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+")',
    objectMatchesMu17Ele8Path      = r'matchToHLTPath({object_idx}, "HLT_Mu17_Ele8_CaloIdL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+")',
    objectMatchesMu8Ele17Path      = r'matchToHLTPath({object_idx}, "HLT_Mu8_Ele17_CaloIdL_v\\d+,HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v\\d+")',
    objectMatchesMu17Ele8IsoPath      = r'matchToHLTPath({object_idx}, "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+")',
    objectMatchesMu8Ele17IsoPath      = r'matchToHLTPath({object_idx}, "HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+")',
    objectMatchesSingleE    = r'matchToHLTPath({object_idx}, "HLT_Ele27_WP80_v\\d+,HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v\\d+,HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v\\d+")',
    objectMatchesSingleEPlusMET = r'matchToHLTPath({object_idx},"HLT_Ele27_WP80_PFMET_MT50_v\\d+,HLT_Ele32_WP70_PFMT50_v\\d+")',
)

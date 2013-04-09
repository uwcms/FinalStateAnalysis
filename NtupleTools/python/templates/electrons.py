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
    objectWWID = '{object}.userFloat("WWID")',
    objectMITID = '{object}.userFloat("MITID")',
    objectMVANonTrig = '{object}.electronID("mvaNonTrigV0")',
    objectMVATrig = '{object}.electronID("mvaTrigV0")',
    objectMVATrigIDISO = '? {object}.isElectronIDAvailable("mvaTrigIDISOV0") ?{object}.electronID("mvaTrigIDISOV0") : -1',
    objectMVATrigIDISOPUSUB = '? {object}.isElectronIDAvailable("mvaTrigIDISOPUSUBV0") ?{object}.electronID("mvaTrigIDISOPUSUBV0") : -1',
    objectMVAIDH2TauWP = '{object}.userInt("mvaidwp")',
    objectCiCTight = '{object}.electronID("cicTight")',
    objectCBID_VETO = '{object}.userInt("CBID_VETO")',
    objectCBID_LOOSE = '{object}.userInt("CBID_LOOSE")',
    objectCBID_MEDIUM = '{object}.userInt("CBID_MEDIUM")',
    objectCBID_TIGHT = '{object}.userInt("CBID_TIGHT")',
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
        '-{object}.userFloat("zzRho2012")*{object}.userFloat("ea_comb_Data2012_iso04_kt6PFJ")))'
        '/{object}.pt()'
    ),
    objectRelPFIsoRhoFSR = cms.string(
        '({object}.chargedHadronIso()'
        '+max(0.0,{object}.neutralHadronIso()'
        '+{object}.photonIso() - userFloat("leg{object_idx}fsrIsoCorr")'
        '-{object}.userFloat("zzRho2012")*{object}.userFloat("ea_comb_Data2012_iso04_kt6PFJ")))'
        '/{object}.pt()'
    ),
    objectPFChargedIso = cms.string('{object}.userIsolation("PfChargedHadronIso")'),
    objectPFNeutralIso = cms.string('{object}.userIsolation("PfNeutralHadronIso")'),
    objectPFPhotonIso  = cms.string('{object}.userIsolation("PfGammaIso")'),
    #ZH Synch iso variables
    ## objectRelPFIsoDBZhLike = cms.string(
    ##     "({object}.chargedHadronIso()"
    ##     "+max({object}.photonIso()"
    ##     "+{object}.neutralHadronIso()"
    ##     "-0.5*{object}.userIso(2),0.0))"
    ##     "/{object}.pt()"
    ## ),
    
    objectEffectiveArea2012Data = cms.string('{object}.userFloat("ea_comb_Data2012_iso04_kt6PFJ")'),
    objectEffectiveArea2011Data = cms.string('{object}.userFloat("ea_comb_Data2011_iso04_kt6PFJ")'),
    objectEffectiveAreaFall11MC = cms.string('{object}.userFloat("ea_comb_Fall11MC_iso04_kt6PFJ")'),
    objectRhoHZG2011 = cms.string('{object}.userFloat("hzgRho2011")'),
    objectRhoHZG2012 = cms.string('{object}.userFloat("hzgRho2012")'),
    objectRelIso = cms.string("({object}.dr03TkSumPt()"
               "+max({object}.dr03EcalRecHitSumEt()-1.0,0.0)"
               "+{object}.dr03HcalTowerSumEt())/{object}.pt()"),
    objectTrkIsoDR03 = cms.string("{object}.dr03TkSumPt()"),
    objectEcalIsoDR03 = cms.string("{object}.dr03EcalRecHitSumEt()"),
    objectHcalIsoDR03 = cms.string("{object}.dr03HcalTowerSumEt()"),
    objectChargeIdTight = '{object}.isGsfCtfScPixChargeConsistent',
    objectChargeIdMed = '{object}.isGsfScPixChargeConsistent',
    objectChargeIdLoose = '{object}.isGsfCtfChargeConsistent',
    #Experimental charge id from Silvia
    ## objectGsfCharge = '{object}.gsfTrack().charge()',
    ## objectTrkCharge = '{object}.track().charge()',
    ## objectScPixCharge =  '{object}.scPixCharge()',
    
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
)

energyCorrections = PSet(
    objectECorrSmearedNoReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoSmearedNoRegression").t',
    objectPtCorrSmearedNoReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoSmearedNoRegression").Pt',
    objectEtaCorrSmearedNoReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoSmearedNoRegression").Eta',
    objectPhiCorrSmearedNoReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoSmearedNoRegression").Phi',
    objectdECorrSmearedNoReg_2012Jul13ReReco = '{object}.userFloat("EGCorr_2012Jul13ReRecoSmearedNoRegression_error")',
    
    objectECorrSmearedReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoSmearedRegression").t',
    objectPtCorrSmearedReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoSmearedRegression").Pt',
    objectEtaCorrSmearedReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoSmearedRegression").Eta',
    objectPhiCorrSmearedReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoSmearedRegression").Phi',
    objectdECorrSmearedReg_2012Jul13ReReco = '{object}.userFloat("EGCorr_2012Jul13ReRecoSmearedRegression_error")',
    
    objectECorrReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoRegressionOnly").t',
    objectPtCorrReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoRegressionOnly").Pt',
    objectEtaCorrReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoRegressionOnly").Eta',
    objectPhiCorrReg_2012Jul13ReReco = 'getUserLorentzVector({object_idx},"EGCorr_2012Jul13ReRecoRegressionOnly").Phi',
    objectdECorrReg_2012Jul13ReReco = '{object}.userFloat("EGCorr_2012Jul13ReRecoRegressionOnly_error")',

    objectECorrSmearedNoReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012SmearedNoRegression").t',
    objectPtCorrSmearedNoReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012SmearedNoRegression").Pt',
    objectEtaCorrSmearedNoReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012SmearedNoRegression").Eta',
    objectPhiCorrSmearedNoReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012SmearedNoRegression").Phi',
    objectdECorrSmearedNoReg_Summer12_DR53X_HCP2012 = '{object}.userFloat("EGCorr_Summer12_DR53X_HCP2012SmearedNoRegression_error")',
    
    objectECorrSmearedReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012SmearedRegression").t',
    objectPtCorrSmearedReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012SmearedRegression").Pt',
    objectEtaCorrSmearedReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012SmearedRegression").Eta',
    objectPhiCorrSmearedReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012SmearedRegression").Phi',
    objectdECorrSmearedReg_Summer12_DR53X_HCP2012 = '{object}.userFloat("EGCorr_Summer12_DR53X_HCP2012SmearedRegression_error")',
    
    objectECorrReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012RegressionOnly").t',
    objectPtCorrReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012RegressionOnly").Pt',
    objectEtaCorrReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012RegressionOnly").Eta',
    objectPhiCorrReg_Summer12_DR53X_HCP2012 = 'getUserLorentzVector({object_idx},"EGCorr_Summer12_DR53X_HCP2012RegressionOnly").Phi',
    objectdECorrReg_Summer12_DR53X_HCP2012 = '{object}.userFloat("EGCorr_Summer12_DR53X_HCP2012RegressionOnly_error")',

    objectECorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").t',
    objectPtCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Pt',
    objectEtaCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Eta',
    objectPhiCorrSmearedNoReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedNoRegression").Phi',
    objectdECorrSmearedNoReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoSmearedNoRegression_error")',
    
    objectECorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").t',
    objectPtCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Pt',
    objectEtaCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Eta',
    objectPhiCorrSmearedReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoSmearedRegression").Phi',
    objectdECorrSmearedReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoSmearedRegression_error")',
    
    objectECorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").t',
    objectPtCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Pt',
    objectEtaCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Eta',
    objectPhiCorrReg_Jan16ReReco = 'getUserLorentzVector({object_idx},"EGCorr_Jan16ReRecoRegressionOnly").Phi',
    objectdECorrReg_Jan16ReReco = '{object}.userFloat("EGCorr_Jan16ReRecoRegressionOnly_error")',

    objectECorrSmearedNoReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11SmearedNoRegression").t',
    objectPtCorrSmearedNoReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11SmearedNoRegression").Pt',
    objectEtaCorrSmearedNoReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11SmearedNoRegression").Eta',
    objectPhiCorrSmearedNoReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11SmearedNoRegression").Phi',
    objectdECorrSmearedNoReg_Fall11 = '{object}.userFloat("EGCorr_Fall11SmearedNoRegression_error")',
    
    objectECorrSmearedReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11SmearedRegression").t',
    objectPtCorrSmearedReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11SmearedRegression").Pt',
    objectEtaCorrSmearedReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11SmearedRegression").Eta',
    objectPhiCorrSmearedReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11SmearedRegression").Phi',
    objectdECorrSmearedReg_Fall11 = '{object}.userFloat("EGCorr_Fall11SmearedRegression_error")',
    
    objectECorrReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11RegressionOnly").t',
    objectPtCorrReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11RegressionOnly").Pt',
    objectEtaCorrReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11RegressionOnly").Eta',
    objectPhiCorrReg_Fall11 = 'getUserLorentzVector({object_idx},"EGCorr_Fall11RegressionOnly").Phi',
    objectdECorrReg_Fall11 = '{object}.userFloat("EGCorr_Fall11RegressionOnly_error")'
)

tracking = PSet(
    objectHasConversion = '{object}.userFloat("hasConversion")',
    objectMissingHits = cms.string(
        '? {object}.gsfTrack.isNonnull? '
        '{object}.gsfTrack.trackerExpectedHitsInner.numberOfHits() : 10'),
    objectPVDXY = '{object}.userFloat("ipDXY")',
    objectPVDZ = '{object}.userFloat("dz")'    
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
    objectMatchesSingleE    = r'matchToHLTPath({object_idx}, "HLT_Ele27_WP80_v\\d+,HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v\\d+,HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v\\d+")',
    objectMatchesSingleEPlusMET = r'matchToHLTPath({object_idx},"HLT_Ele27_WP80_PFMET_MT50_v\\d+,HLT_Ele32_WP70_PFMT50_v\\d+")',
)

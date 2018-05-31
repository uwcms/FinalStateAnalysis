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
    objectMVAIsoWP80 = '{object}.userFloat("MVA_iso_WP80")',
    objectMVAIsoWP90 = '{object}.userFloat("MVA_iso_WP90")',
    objectMVAIsoLoose = '{object}.userFloat("MVA_iso_WPLoose")',
    objectMVANoisoWP80 = '{object}.userFloat("MVA_noiso_WP80")',
    objectMVANoisoWP90 = '{object}.userFloat("MVA_noiso_WP90")',
    objectMVANoisoLoose = '{object}.userFloat("MVA_noiso_WPLoose")',    

    objectRelPFIsoDB = cms.string(
        "({object}.userIsolation('PfChargedHadronIso')"
        "+max({object}.userIsolation('PfNeutralHadronIso')"
        "+{object}.userIsolation('PfGammaIso')"
        "-0.5*{object}.userIsolation('PfPUChargedHadronIso'),0.0))"
        "/{object}.pt()"
    ),
    objectRelPFIsoRho = cms.string(
        '({object}.chargedHadronIso()'
        '+max(0.0,{object}.neutralHadronIso()'
        '+{object}.photonIso()'
        '-{object}.userFloat("rho_fastjet")*{object}.userFloat("EffectiveArea")))'
        '/{object}.pt()'
    ),

    # Number of matched conversions
    objectPassesConversionVeto = '{object}.passConversionVeto()',

    objectPFChargedIso = cms.string('{object}.userIsolation("PfChargedHadronIso")'),
    objectPFNeutralIso = cms.string('{object}.userIsolation("PfNeutralHadronIso")'),
    objectPFPhotonIso  = cms.string('{object}.userIsolation("PfGammaIso")'),
    objectPFPUChargedIso = cms.string('{object}.userIsolation("PfPUChargedHadronIso")'),

    objectEffectiveArea2012Data = cms.string('{object}.userFloat("ea_comb_Data2012_iso04_kt6PFJ")'),
    objectEffectiveAreaSpring15 = cms.string('{object}.userFloat("EffectiveArea")'),

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
    #objectHasMatchedConversion = cms.vstring('{object}.userInt("HasMatchedConversion")','I'),    
    objectE1x5 = '{object}.scE1x5',
    objectE2x5Max = '{object}.scE2x5Max',
    objectE5x5 = '{object}.scE5x5',
    objectNearMuonVeto = 'overlapMuons({object_idx},0.05,"isGlobalMuon() & abs(eta()) < 2.4").size()',
    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}, 11, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 11, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 11, 0).pdgId() : -999',
    objectComesFromHiggs = 'comesFromHiggs({object_idx}, 11, 1)',
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

    # How close is the nearest muon passing some basic quality cuts?
    objectNearestMuonDR = "electronClosestMuonDR({object_idx})",
    # closest Z mass
    objectNearestZMass = 'closestZElectron({object_idx},"")',
    # lowest invariant mass
    objectLowestMll = 'smallestMee({object_idx},"")',
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

    objectPt_ElectronScaleUp = '? daughterHasUserCand({object_idx}, "eScaleUp") ? daughterAsElectron({object_idx}).userCand("eScaleUp").pt : -999.',
    objectPt_ElectronScaleDown = '? daughterHasUserCand({object_idx}, "eScaleDown") ? daughterAsElectron({object_idx}).userCand("eScaleDown").pt : -999.',
    objectPt_ElectronUncorr = '? daughterHasUserCand({object_idx}, "uncorr") ? daughterAsElectron({object_idx}).userCand("uncorr").pt : -999.',
    objectPt_ElectronResRhoUp = '? daughterHasUserCand({object_idx}, "eResUp") ? daughterAsElectron({object_idx}).userCand("eResUp").pt : -999.',
    objectPt_ElectronResRhoDown = '? daughterHasUserCand({object_idx}, "eResDown") ? daughterAsElectron({object_idx}).userCand("eResDown").pt : -999.',
    objectPt_ElectronResPhiDown = '? daughterHasUserCand({object_idx}, "eResPhiDown") ? daughterAsElectron({object_idx}).userCand("eResPhiDown").pt : -999.',
#    objectPt_ElectronEnUp = '? daughterHasUserCand({object_idx}, "eesUpElectrons") ? daughterAsElectron({object_idx}).userCand("eesUpElectrons").pt : -999.',
 #   objectEta_ElectronEnUp = '? daughterHasUserCand({object_idx}, "eesUpElectrons") ? daughterAsElectron({object_idx}).userCand("eesUpElectrons").eta : -999.',
  #  objectPhi_ElectronEnUp = '? daughterHasUserCand({object_idx}, "eesUpElectrons") ? daughterAsElectron({object_idx}).userCand("eesUpElectrons").phi : -999.',

   # objectPt_ElectronEnDown = '? daughterHasUserCand({object_idx}, "eesDownElectrons") ? daughterAsElectron({object_idx}).userCand("eesDownElectrons").pt : -999.',
   # objectEta_ElectronEnDown = '? daughterHasUserCand({object_idx}, "eesDownElectrons") ? daughterAsElectron({object_idx}).userCand("eesDownElectrons").eta : -999.',
   # objectPhi_ElectronEnDown = '? daughterHasUserCand({object_idx}, "eesDownElectrons") ? daughterAsElectron({object_idx}).userCand("eesDownElectrons").phi : -999.',

#    objectPt_ElectronScaleUp = '? daughterHasUserCand({object_idx}, "ees+") ? daughterAsElectron({object_idx}).userCand(n"ees+").pt : -999.',

 #   objectPt_ElectronScaleDown = '? daughterHasUserCand({object_idx}, "ees-") ? daughterAsElectron({object_idx}).userCand("ees-").pt : -999.',

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
    objectMatchesSingleE = r'matchToHLTPath({object_idx},"HLT_Ele27_eta2p1_WPLoose_Gsf_v\\d+|HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleE_leg1 = r'matchToHLTPath({object_idx},"HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleE_leg2 = r'matchToHLTPath({object_idx},"HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesDoubleE = r'matchToHLTPath({object_idx},"HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+",0.5)',
    objectMatchesSingleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleMuSingleE = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesTripleE = r'matchToHLTPath({object_idx},"HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleMuSingleE = r'matchToHLTPath({object_idx},"HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\d+",0.5)',
)

trigger_25ns_MC = PSet(
    objectMatchesSingleE = r'matchToHLTPath({object_idx},"HLT_Ele27_WP85_Gsf_v\\d+",0.5)',
    objectMatchesSingleE_leg1 = r'matchToHLTPath({object_idx},"HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleE_leg2 = r'matchToHLTPath({object_idx},"HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesDoubleE = r'matchToHLTPath({object_idx},"HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+",0.5)',
    objectMatchesSingleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleMuSingleE = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesTripleE = r'matchToHLTPath({object_idx},"HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleMuSingleE = r'matchToHLTPath({object_idx},"HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\d+",0.5)',
)

trigger_25ns = PSet(
    objectMatchesSingleE22Tight = r'matchToHLTPath({object_idx},"HLT_Ele22_eta2p1_WPTight_Gsf_v\\d+",0.5)',
    objectMatchesSingleE22Loose = r'matchToHLTPath({object_idx},"HLT_Ele22_eta2p1_WPLoose_Gsf_v\\d+|HLT_Ele22_eta2p1_WP75_Gsf_v\\d+",0.5)',
    objectMatchesSingleE23Tight = r'matchToHLTPath({object_idx},"HLT_Ele23_WPTight_Gsf_v\\d+",0.5)',
    objectMatchesSingleE23Loose = r'matchToHLTPath({object_idx},"HLT_Ele23_WPLoose_Gsf_v\\d+|HLT_Ele23_WP75_Gsf_v\\d+",0.5)',
    objectMatchesSingleE27Tight = r'matchToHLTPath({object_idx},"HLT_Ele27_WPTight_Gsf_v\\d+",0.5)',
    objectMatchesSingleE27LooseEr = r'matchToHLTPath({object_idx},"HLT_Ele27_eta2p1_WPLoose_Gsf_v\\d+",0.5)',
    objectMatchesSingleE25Tight = r'matchToHLTPath({object_idx},"HLT_Ele25_eta2p1_WPTight_Gsf_v\\d+",0.5)',
    objectMatchesSingleE25Loose = r'matchToHLTPath({object_idx},"HLT_Ele25_eta2p1_WPLoose_Gsf_v\\d+",0.5)',
    objectMatchesSingleE_leg1 = r'matchToHLTPath({object_idx},"HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleE_leg2 = r'matchToHLTPath({object_idx},"HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesDoubleE = r'matchToHLTPath({object_idx},"HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+",0.5)',
    objectMatchesSingleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleMuSingleE = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesTripleE = r'matchToHLTPath({object_idx},"HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleMuSingleE = r'matchToHLTPath({object_idx},"HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesSingleE20SingleTau28 = r'matchToHLTPath({object_idx},"HLT_Ele20_eta2p1_WPLoose_Gsf_LooseIsoPFTau28_v\\d+",0.5)',
    objectMatchesSingleE22SingleTau29 = r'matchToHLTPath({object_idx},"HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau29_v\\d+",0.5)',
    objectMatchesSingleE24SingleTau30 = r'matchToHLTPath({object_idx},"HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v\\d+",0.5)',  
    objectMatchesSingleE36SingleTau30 = r'matchToHLTPath({object_idx},"HLT_Ele36_eta2p1_WPLoose_Gsf_LooseIsoPFTau30_v\\d+",0.5)',  
    objectMatchesSingleE22SingleTau20L1 = r'matchToHLTPath({object_idx},"HLT_Ele22_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v\\d+",0.5)',
    objectMatchesSingleE24SingleTau20 = r'matchToHLTPath({object_idx},"HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_v\\d+",0.5)',
    objectMatchesSingleE24SingleTau20L1 = r'matchToHLTPath({object_idx},"HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v\\d+",0.5)',  
    objectMatchesSingleE27SingleTau20L1 = r'matchToHLTPath({object_idx},"HLT_Ele27_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v\\d+",0.5)',
    objectMatchesSingleE32SingleTau20L1 = r'matchToHLTPath({object_idx},"HLT_Ele32_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1_v\\d+",0.5)',
)

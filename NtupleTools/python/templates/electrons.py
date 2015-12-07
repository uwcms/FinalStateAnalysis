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
    objectCBIDVetoNoIso = '{object}.userFloat("CBIDVetoNoIso")',
    objectCBIDLooseNoIso = '{object}.userFloat("CBIDLooseNoIso")',
    objectCBIDMediumNoIso = '{object}.userFloat("CBIDMediumNoIso")',
    objectCBIDTightNoIso = '{object}.userFloat("CBIDTightNoIso")',
    objectMVANonTrigID = '{object}.userFloat("BDTIDNonTrig")',
    objectMVANonTrigCategory = '{object}.userFloat("BDTIDNonTrigCategory")',
    objectMVANonTrigWP80 = '{object}.userFloat("MVANonTrigWP80")',
    objectMVANonTrigWP90 = '{object}.userFloat("MVANonTrigWP90")',
    objectMVATrigID = '{object}.userFloat("BDTIDTrig")',
    objectMVATrigCategory = '{object}.userFloat("BDTIDTrigCategory")',
    objectMVATrigWP80 = '{object}.userFloat("MVATrigWP80")',
    objectMVATrigWP90 = '{object}.userFloat("MVATrigWP90")',
    
    # Use cms.string so we get the parentheses formatting bonus
#    objectRelPFIsoDB = cms.string(
#        "({object}.userIso(0)"
#        "+max({object}.userIso(1)"
#        "+{object}.neutralHadronIso()"
#        "-0.5*{object}.userIso(2),0.0))"
#        "/{object}.pt()"
#    ),
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

trigger_50ns = PSet(
    objectMatchesSingleE = r'matchToHLTPath({object_idx},"HLT_Ele27_eta2p1_WPLoose_Gsf_v\\d+|HLT_Ele23_CaloIdL_TrackIdL_IsoVL_V\\d+",0.5)',
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
    objectMatchesSingleE = r'matchToHLTPath({object_idx},"HLT_Ele27_WPLoose_Gsf_v\\d+",0.5)',
    objectMatchesSingleE_leg1 = r'matchToHLTPath({object_idx},"HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleE_leg2 = r'matchToHLTPath({object_idx},"HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesDoubleE = r'matchToHLTPath({object_idx},"HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+",0.5)',
    objectMatchesSingleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesSingleMuSingleE = r'matchToHLTPath({object_idx},"HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+",0.5)',
    objectMatchesTripleE = r'matchToHLTPath({object_idx},"HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleESingleMu = r'matchToHLTPath({object_idx},"HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\d+",0.5)',
    objectMatchesDoubleMuSingleE = r'matchToHLTPath({object_idx},"HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\d+",0.5)',
)

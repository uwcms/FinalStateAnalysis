'''

Ntuple branch template sets for electron objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Photon
i.e. daughter(1) or somesuch.

Author: L. Gray (copied mostly from electrons.py)

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# ID and isolation
id = PSet(
    objectCBIDLOOSE = '{object}.userInt("CBID_LOOSE")',
    objectCBIDMEDIUM = '{object}.userInt("CBID_MEDIUM")',
    objectCBIDTIGHT = '{object}.userInt("CBID_TIGHT")',
    # isolations
    objectPFChargedIso  = '{object}.userIsolation(4)',
    objectPFNeutralIso  = '{object}.userIsolation(5)',
    objectPFPhotonIso   = '{object}.userIsolation(6)',
    objectEffectiveAreaCHad = '{object}.userFloat("PhotonEA_pfchg")',
    objectEffectiveAreaNHad = '{object}.userFloat("PhotonEA_pfneut")',
    objectEffectiveAreaPho  = '{object}.userFloat("PhotonEA_pfpho")',    
    # photon id variables
    objectConvSafeElectronVeto = '{object}.userInt("ConvSaveElectronVeto")',
    objectHadronicOverEM = '{object}.hadronicOverEm',
    objectHadronicDepth1OverEm = '{object}.hadronicDepth1OverEm',
    objectHadronicDepth2OverEm = '{object}.hadronicDepth2OverEm',
    objectSingleTowerHadronicOverEm = '{object}.userFloat("SingleTowerHoE")',
    objectSingleTowerHadronicDepth1OverEm = '{object}.userFloat("SingleTowerHoEDepth1")',
    objectSingleTowerHadronicDepth2OverEm = '{object}.userFloat("SingleTowerHoEDepth2")',
    objectSigmaIEtaIEta = '{object}.sigmaIetaIeta',
    objectE1x5 = '{object}.e1x5',
    objectE2x5 = '{object}.e2x5',
    objectE3x3 = '{object}.e3x3',
    objectE5x5 = '{object}.e5x5',
    objectMaxEnergyXtal = '{object}.maxEnergyXtal',
    objectR1x5 = '{object}.r1x5',
    objectR2x5 = '{object}.r2x5',
    objectR9   = '{object}.r9',
    # locations and gaps
    objectIsEB = '{object}.isEB',
    objectIsEE = '{object}.isEE',
    objectIsEBGap = '{object}.isEBGap',
    objectIsEBEtaGap = '{object}.isEBEtaGap',
    objectIsEBPhiGap = '{object}.isEBPhiGap',
    objectIsEEGap = '{object}.isEEGap',
    objectIsEERingGap = '{object}.isEERingGap',
    objectIsEEDeeGap = '{object}.isEEDeeGap',
    objectIsEBEEGap = '{object}.isEBEEGap',
    # reco provenance
    objectIsPFlowPhoton = '{object}.isPFlowPhoton',
    objectIsStandardPhoton = '{object}.isStandardPhoton',   
    objectHasPixelSeed = '{object}.hasPixelSeed',
    # gen matching
    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}).isAvailable && getDaughterGenParticleMotherSmart({object_idx}).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}).pdgId() : -999',
    objectComesFromHiggs = 'comesFromHiggs({object_idx})',        
)

tracking = PSet(
    objectPositionX = '{object}.caloPosition().x',
    objectPositionY = '{object}.caloPosition().y',
    objectPositionZ = '{object}.caloPosition().z',
    objectSCPositionX = '{object}.superCluster().position().x',
    objectSCPositionY = '{object}.superCluster().position().y',
    objectSCPositionZ = '{object}.superCluster().position().z',   
    objectHasConversionTracks = '{object}.hasConversionTracks',    
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
    objectPhoton26RPhoton18_caloORr9_MatchLastFilter  = 'matchToHLTFilter({object_idx}, "hltPhoton26R9Id85ORCaloId10Iso50Photon18R9Id85ORCaloId10Iso50Mass70EgammaAllCombMassLastFilter")', # HLT_Photon26_R9Id85_OR_CaloId10_Iso50_Photon18_R9Id85_OR_CaloId10_Iso50_Mass70_v* (2012),
    objectPhoton36Photon10_caloORr9_MassLastFilter  = 'matchToHLTFilter({object_idx}, " hltPhoton36R9Id85ORCaloId10Iso50Photon10R9Id85ORCaloId10Iso50Mass80EgammaAllCombMassLastFilter")', #	HLT_Photon36_R9Id85_OR_CaloId10_Iso50_Photon10_R9Id85_OR_CaloId10_Iso50_Mass80_v* (2012)
    objectEG26HE10LastFilter = 'matchToHLTFilter({object_idx}, "hltEG26HE10LastFilter")', #for HLT_photon26_photon18
    objectEG18EtDoubleFilterUnseeded = 'matchToHLTFilter({object_idx}, "hltEG18EtDoubleFilterUnseeded")', #for HLT_photon26_photon18    
)

import FWCore.ParameterSet.Config as cms

cbid_LOOSE = cms.PSet(
    #Electron Veto configuration
    ElectronVeto = cms.bool(True),
    Mask_ElectronVeto = cms.bool(False),
    Veto_ElectronVeto = cms.bool(False),
    #SingleTower H/E configuration
    #                       (EB_min, EB_max, EE_min, EE_max)
    SingleTowerHoverE = cms.vdouble(0.0,0.05,0.0,0.05),
    Mask_SingleTowerHoverE = cms.bool(False),
    Veto_SingleTowerHoverE = cms.bool(False),
    #sigmaIetaIeta configuration
    # again (EB_min,EB_max,EE_min,EE_max)
    SigmaIEtaIEta = cms.vdouble(0.0,0.012,0.0,0.034),
    Mask_SigmaIEtaIEta = cms.bool(False),
    Veto_SigmaIEtaIEta = cms.bool(False),
    #PFChargedIso configuration
    #                                ( EB, EE)
    PFChargedIsoPtSlope = cms.vdouble(0.0,0.0),
    PFChargedIso = cms.vdouble(0.0,2.6,0.0,2.3),
    Mask_PFChargedIso = cms.bool(False),
    Veto_PFChargedIso = cms.bool(False),
    #PFNeutralIso configuration
    PFNeutralIsoPtSlope = cms.vdouble(0.04,0.04),
    PFNeutralIso = cms.vdouble(0.0,3.5,0.0,2.9),
    Mask_PFNeutralIso = cms.bool(False),
    Veto_PFNeutralIso = cms.bool(False),
    #PFPhotonIso configuration
    PFPhotonIsoPtSlope = cms.vdouble(0.005,0.005),
    PFPhotonIso = cms.vdouble(0.0,1.3,0.0,1e6),
    Mask_PFPhotonIso = cms.bool(False),
    Veto_PFPhotonIso = cms.bool(False),
    )

cbid_MEDIUM = cbid_LOOSE.clone(
    SigmaIEtaIEta = cms.vdouble(0.0,0.011,0.0,0.033),
    PFChargedIso  = cms.vdouble(0.0,1.5,0.0,1.2),
    PFNeutralIso  = cms.vdouble(0.0,1.0,0.0,1.5),
    PFPhotonIso   = cms.vdouble(0.0,0.7,0.0,1.0)
    )

cbid_TIGHT = cbid_LOOSE.clone(
    SigmaIEtaIEta = cms.vdouble(0.0,0.011,0.0,0.031),
    PFChargedIso  = cms.vdouble(0.0,0.7,0.0,0.5),
    PFNeutralIso  = cms.vdouble(0.0,0.4,0.0,1.5),
    PFPhotonIso   = cms.vdouble(0.0,0.5,0.0,1.0)
    )

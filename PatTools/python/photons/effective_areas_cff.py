import FWCore.ParameterSet.Config as cms


# these values are taken from:
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedPhotonID2012
# uses the rho mentioned on that twiki

PhotonEA_pfchg = cms.PSet(
    name = cms.string('PhotonEA_pfchg'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(False),
    needs_pfphoton  = cms.bool(False),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.479,2.0,2.2,2.3,2.4,3.0),
    effective_areas = cms.vdouble(0.012,0.010,0.014,0.012,0.016,0.020,0.012)
    )

PhotonEA_pfneut = cms.PSet(
    name = cms.string('PhotonEA_pfneut'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(False),
    needs_pfphoton  = cms.bool(False),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.479,2.0,2.2,2.3,2.4,3.0),
    effective_areas = cms.vdouble(0.030,0.057,0.039,0.015,0.024,0.039,0.072)
    )

PhotonEA_pfpho = cms.PSet(
    name = cms.string('PhotonEA_pfpho'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(False),
    needs_pfphoton  = cms.bool(False),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.479,2.0,2.2,2.3,2.4,3.0),
    effective_areas = cms.vdouble(0.148,0.130,0.112,0.216,0.262,0.260,0.266)
    )

photon_eas = cms.VPSet(PhotonEA_pfchg,PhotonEA_pfneut,PhotonEA_pfpho)

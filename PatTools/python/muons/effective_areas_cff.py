import FWCore.ParameterSet.Config as cms


# these values are taken from the slides at:
# https://indico.cern.ch/getFile.py/access?contribId=1&resId=0&materialId=slides&confId=188494

# eas_<type><conesize>_<fastjettype>_th<neutral threshold>

eas_comb04_kt6PFJetsCentralNeutral_th05 = cms.PSet(
    name = cms.string('ea_comb_iso04_kt6PFJCNth05'),
    cone_size = cms.double(0.4),
    needs_pfneutral = cms.bool(True),
    needs_pfphoton  = cms.bool(True),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.674,0.565,0.442,0.515,0.821,0.660)
    )

eas_comb03_kt6PFJetsCentralNeutral_th05 = cms.PSet(
    name = cms.string('ea_comb_iso03_kt6PFJCNth05'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(True),
    needs_pfphoton  = cms.bool(True),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.382,0.317,0.242,0.326,0.462,0.372)
    )

eas_pho04_kt6PFJetsCentralNeutral_th05 = cms.PSet(
    name = cms.string('ea_pho_iso04_kt6PFJCNth05'),
    cone_size = cms.double(0.4),
    needs_pfneutral = cms.bool(False),
    needs_pfphoton  = cms.bool(True),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.504,0.306,0.198,0.287,0.525,0.488)
    )

eas_pho03_kt6PFJetsCentralNeutral_th05 = cms.PSet(
    name = cms.string('ea_pho_iso03_kt6PFJCNth05'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(False),
    needs_pfphoton  = cms.bool(True),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.274,0.161,0.079,0.168,0.369,0.294)
    )

eas_neut04_kt6PFJetsCentralNeutral_th05 = cms.PSet(
    name = cms.string('ea_neut_iso04_kt6PFJCNth05'),
    cone_size = cms.double(0.4),
    needs_pfneutral = cms.bool(True),
    needs_pfphoton  = cms.bool(False),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.166,0.259,0.247,0.220,0.340,0.216)
    )

eas_neut03_kt6PFJetsCentralNeutral_th05 = cms.PSet(
    name = cms.string('ea_neut_iso03_kt6PFJCNth05'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(True),
    needs_pfphoton  = cms.bool(False),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.107,0.141,0.159,0.102,0.096,0.104)
    )

# list of all effective areas for 2012 data using a 0.5 GeV neutral
# threshold veto.
# rho calculation needs to be from kt6PFJetsCentralNeutral a'la slides
eas_kt6PFJetsCentralNeutral_th05 = cms.VPSet(
    eas_comb04_kt6PFJetsCentralNeutral_th05,
    eas_comb03_kt6PFJetsCentralNeutral_th05,
    eas_pho04_kt6PFJetsCentralNeutral_th05,
    eas_pho03_kt6PFJetsCentralNeutral_th05,
    eas_neut04_kt6PFJetsCentralNeutral_th05,
    eas_neut03_kt6PFJetsCentralNeutral_th05
    )
    

eas_comb04_kt6PFJetsCentral_th05 = cms.PSet(
    name = cms.string('ea_comb_iso04_kt6PFJCth05'),
    cone_size = cms.double(0.4),
    needs_pfneutral = cms.bool(True),
    needs_pfphoton  = cms.bool(True),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.132,0.120,0.114,0.139,0.168,0.189)
    )

eas_comb03_kt6PFJetsCentral_th05 = cms.PSet(
    name = cms.string('ea_comb_iso03_kt6PFJCth05'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(True),
    needs_pfphoton  = cms.bool(True),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.076,0.070,0.067,0.082,0.097,0.115)
    )

eas_pho04_kt6PFJetsCentral_th05 = cms.PSet(
    name = cms.string('ea_pho_iso04_kt6PFJCth05'),
    cone_size = cms.double(0.4),
    needs_pfneutral = cms.bool(False),
    needs_pfphoton  = cms.bool(True),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.085,0.052,0.038,0.055,0.070,0.081)
    )

eas_pho03_kt6PFJetsCentral_th05 = cms.PSet(
    name = cms.string('ea_pho_iso03_kt6PFJCth05'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(False),
    needs_pfphoton  = cms.bool(True),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.049,0.030,0.022,0.034,0.041,0.048)
    )

eas_neut04_kt6PFJetsCentral_th05 = cms.PSet(
    name = cms.string('ea_neut_iso04_kt6PFJCth05'),
    cone_size = cms.double(0.4),
    needs_pfneutral = cms.bool(True),
    needs_pfphoton  = cms.bool(False),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.046,0.067,0.074,0.083,0.095,0.105)
    )

eas_neut03_kt6PFJetsCentral_th05 = cms.PSet(
    name = cms.string('ea_neut_iso03_kt6PFJCth05'),
    cone_size = cms.double(0.3),
    needs_pfneutral = cms.bool(True),
    needs_pfphoton  = cms.bool(False),
    eta_boundaries  = cms.vdouble(0.0,1.0,1.5,2.0,2.2,2.3,2.4),
    effective_areas = cms.vdouble(0.027,0.039,0.044,0.047,0.055,0.065)
    )

# list of all effective areas for 2011 data using a 0.5 GeV neutral
# threshold veto.
# rho calculation needs to be from kt6PFJetsCentral a'la slides
eas_kt6PFJetsCentral_th05 = cms.VPSet(
    eas_comb04_kt6PFJetsCentral_th05,
    eas_comb03_kt6PFJetsCentral_th05,
    eas_pho04_kt6PFJetsCentral_th05,
    eas_pho03_kt6PFJetsCentral_th05,
    eas_neut04_kt6PFJetsCentral_th05,
    eas_neut03_kt6PFJetsCentral_th05
    )

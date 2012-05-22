import FWCore.ParameterSet.Config as cms
'''

Embed VTBF ID info into pat::Electrons.  Code by Mike Bachtis - originally in
UWAnalysis/Configuration/python/tools/analysisTools.py

'''

electronsWP80 = cms.EDProducer(
    'PATElectronVBTFEmbedder',
    src             = cms.InputTag('replace'),
    sigmaEtaEta     = cms.vdouble(0.01,0.03),
    deltaEta        = cms.vdouble(0.004,0.007),
    deltaPhi        = cms.vdouble(0.06,0.03),
    hoE             = cms.vdouble(0.04,0.025),
    id              = cms.string("wp80")

)

electronsWP90 = cms.EDProducer(
    'PATElectronVBTFEmbedder',
    src             = cms.InputTag("electronsWP80"),
    sigmaEtaEta     = cms.vdouble(0.01,0.03),
    deltaEta        = cms.vdouble(0.007,0.009),
    deltaPhi        = cms.vdouble(0.8,0.7),
    hoE             = cms.vdouble(0.12,0.05),
    id              = cms.string("wp90")
)

electronsWP95 = cms.EDProducer(
    'PATElectronVBTFEmbedder',
    src             = cms.InputTag("electronsWP90"),
    sigmaEtaEta     = cms.vdouble(0.01,0.03),
    deltaEta        = cms.vdouble(0.007,0.01),
    deltaPhi        = cms.vdouble(0.8,0.7),
    hoE             = cms.vdouble(0.15,0.07),
    id              = cms.string("wp95")
)

# An extra loose WP95 with no H/E cut in the endcap
electronsWP95V = cms.EDProducer(
    'PATElectronVBTFEmbedder',
    src             = cms.InputTag("electronsWP90"),
    sigmaEtaEta     = cms.vdouble(0.01,0.03),
    deltaEta        = cms.vdouble(0.007,0.01),
    deltaPhi        = cms.vdouble(0.8,0.7),
    hoE             = cms.vdouble(0.15,999),
    id              = cms.string("wp95V")
)

electronsVBTFId = cms.Sequence(
    electronsWP80
    + electronsWP90
    + electronsWP95
    + electronsWP95V
)

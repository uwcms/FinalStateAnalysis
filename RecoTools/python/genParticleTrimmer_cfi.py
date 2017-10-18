import FWCore.ParameterSet.Config as cms

'''
Keep only high (> 0.5) and EWK signals
'''

from SimGeneral.HepPDTESSource.pythiapdt_cfi import HepPDTESSource

# This will

prunedGenParticles = cms.EDProducer(
    "GenParticlePruner",
    src = cms.InputTag("genParticles"),
    select = cms.vstring(
        "drop  *  ", # this is the default
        'keep pt > 0.5 & abs(eta) < 5',
        "keep++ pdgId = {Z0}",
        "keep++ pdgId = 24", # W+
        "keep++ pdgId = -24", # W+
        'keep++ pdgId = 6', # top quark
        'keep++ pdgId = 15', # Any tau daughter
        'keep++ pdgId = -15', # Any tau daughter
        'keep++ pdgId = 25', # Higgs
        'keep++ pdgId = 35', # MSSM H
        'keep++ pdgId = 36', # MSSM A
        'keep++ pdgId = 37', # Charged Higgs
        #"drop pdgId = 6 & status = 2",
        #"drop pdgId = {Z0} & status = 2",
        #"drop pdgId = 24 & status = 2",
        #'drop pdgId = 25 & status = 2',
        #'drop pdgId = 35 & status = 2',
        #'drop pdgId = 36 & status = 2',
        #'drop pdgId = 37 & status = 2',
    )
)

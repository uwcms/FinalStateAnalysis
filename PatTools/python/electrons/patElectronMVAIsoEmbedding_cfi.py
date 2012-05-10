'''

Embed the MVA ISO variable into the PAT muons

See: https://twiki.cern.ch/twiki/bin/view/CMS/EgammaMultivariateIsoElectrons

Author: Evan K. Friis, UW Madison

'''

import FWCore.ParameterSet.Config as cms

patElectronMVAIsoEmbedding = cms.EDProducer(
    "PATElectronMVAIsoEmbedding",
    src = cms.InputTag("fixme"),
    target = cms.string('fixme'),
    ebRecHits = cms.InputTag("reducedEcalRecHitsEB"),
    eeRecHits = cms.InputTag("reducedEcalRecHitsEE"),
    vertexSrc = cms.InputTag("selectedPrimaryVertex"),
    pfSrc = cms.InputTag("particleFlow"),
    rhoSrc = cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho"),
)

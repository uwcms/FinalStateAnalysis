'''

Embed the MVA ID and ISO variables into the PAT muons

See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MultivariateMuonSelection

Author: Evan K. Friis, UW Madison

'''

import FWCore.ParameterSet.Config as cms

patMuonMVAIdIsoEmbedding = cms.EDProducer(
    "PATMuonMVAEmbedder",
    src = cms.InputTag("fixme"),
    vertexSrc = cms.InputTag("selectedPrimaryVertex"),
    pfSrc = cms.InputTag("particleFlow"),
    rhoSrc = cms.InputTag("kt6PFJetsForRhoComputationVoronoi", "rho"),
)

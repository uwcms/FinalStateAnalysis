import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.version import cmssw_major_version

#prescription for calculating the photon PF isolation
#embeds per-vertex isolation information
from FinalStateAnalysis.PatTools.photons.patPhotonPFIsolationEmbedding_cfi import \
        patPhotonPFIsolation

customizePhotonSequence = cms.Sequence()
customizePhotonSequence += patPhotonPFIsolation

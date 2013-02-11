import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.version import cmssw_major_version

customizePhotonSequence = cms.Sequence()

# rhos for the photon ID
from FinalStateAnalysis.PatTools.photons.patPhotonRhoEmbedding_cfi import \
     patPhotonRhoEmbedder

customizePhotonSequence += patPhotonRhoEmbedder

#prescription for calculating the photon PF isolation
#embeds per-vertex isolation information
from FinalStateAnalysis.PatTools.photons.patPhotonPFIsolationEmbedding_cfi import \
        patPhotonPFIsolation

customizePhotonSequence += patPhotonPFIsolation

from FinalStateAnalysis.PatTools.photons.patPhotonEAEmbedder_cfi import \
     patPhotonEAEmbedder

customizePhotonSequence += patPhotonEAEmbedder

# calculated photon ID
from FinalStateAnalysis.PatTools.photons.patPhotonCutBasedIdEmbedding_cfi import \
     patPhotonCutBasedIdEmbedder

customizePhotonSequence += patPhotonCutBasedIdEmbedder

#phosphor corrections from CalTech
from FinalStateAnalysis.PatTools.photons.patPhotonPHOSPHOREmbedder_cff import \
     patPhotonPHOSPHOREmbedder

customizePhotonSequence += patPhotonPHOSPHOREmbedder

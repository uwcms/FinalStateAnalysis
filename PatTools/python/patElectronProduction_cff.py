import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.version import cmssw_major_version

from FinalStateAnalysis.PatTools.electrons.patConversionRejection_cfi import \
        electronsWWID
from FinalStateAnalysis.PatTools.electrons.patElectronVBTFEmbedding_cff import \
        electronsWP80, electronsWP90, electronsWP95, electronsWP95V, electronsVBTFId

from FinalStateAnalysis.PatTools.electrons.patElectronRhoEmbedding_cfi import \
        patElectronRhoEmbedding, patElectronZZRhoEmbedding, patElectronZZ2012RhoEmbedding

from FinalStateAnalysis.PatTools.electrons.electronSystematics_cfi import \
        electronSystematics

from FinalStateAnalysis.PatTools.electrons.triggerMatch_cfi import \
        triggeredPatElectrons, triggeredPatElectronsL

# This is the 2011 MIT MVA ID.  The 2012 one is handled in electronId_cff
from FinalStateAnalysis.PatTools.electrons.patElectronMVAIDEmbedding_cfi import\
        patElectronMVAIDEmbedder

from FinalStateAnalysis.PatTools.electrons.patElectronMVAIsoEmbedding_cfi import\
        patElectronMVAIsoEmbedding

from FinalStateAnalysis.PatTools.electrons.patElectronMVAWPEmbedding_cfi import\
        patElectronMVAIDWPEmbedding, patElectronMVAIsoWPEmbedding

from FinalStateAnalysis.PatTools.electrons.patElectronEmbedJetInfo_cfi import \
        patElectronsEmbedJetInfo

from FinalStateAnalysis.PatTools.electrons.patElectronsIpEmbedding_cfi import \
        patElectronsEmbedIp

from FinalStateAnalysis.PatTools.electrons.eTrackCandidates_cfi import \
        gsfTrackCandidates

from FinalStateAnalysis.PatTools.electrons.patElectronEmbedCalibratedGsf_cfi import \
        patElectronEmbedCalibratedGsf

from FinalStateAnalysis.PatTools.electrons.patElectronEffectiveAreaEmbedder_cfi import \
        patElectronEffectiveAreaEmbedder

customizeElectronSequence = cms.Sequence()
customizeElectronSequence += gsfTrackCandidates
customizeElectronSequence += patElectronRhoEmbedding
customizeElectronSequence += patElectronZZRhoEmbedding
if cmssw_major_version() == 5:
	customizeElectronSequence += patElectronZZ2012RhoEmbedding
customizeElectronSequence += electronsWWID
customizeElectronSequence += electronsVBTFId
customizeElectronSequence += patElectronsEmbedJetInfo
customizeElectronSequence += electronSystematics
#customizeElectronSequence += triggeredPatElectrons
#customizeElectronSequence += triggeredPatElectronsL
customizeElectronSequence += patElectronMVAIDEmbedder
customizeElectronSequence += patElectronMVAIsoEmbedding
customizeElectronSequence += patElectronMVAIDWPEmbedding
customizeElectronSequence += patElectronMVAIsoWPEmbedding
customizeElectronSequence += patElectronsEmbedIp
customizeElectronSequence += patElectronEmbedCalibratedGsf
customizeElectronSequence += patElectronEffectiveAreaEmbedder

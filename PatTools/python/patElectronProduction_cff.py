import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.electrons.patConversionRejection_cfi import \
        electronsWWID
from FinalStateAnalysis.PatTools.electrons.patElectronVBTFEmbedding_cff import \
        electronsWP80, electronsWP90, electronsWP95, electronsVBTFId

from FinalStateAnalysis.PatTools.electrons.electronSystematics_cfi import \
        electronSystematics

from FinalStateAnalysis.PatTools.electrons.triggerMatch_cfi import triggeredPatElectrons

from FinalStateAnalysis.PatTools.electrons.patElectronMVAIDEmbedding_cfi import\
        patElectronMVAIDEmbedder

from FinalStateAnalysis.PatTools.electrons.patElectronEmbedJetInfo_cfi import \
        patElectronsEmbedJetInfo

from FinalStateAnalysis.PatTools.electrons.patElectronsIpEmbedding_cfi import \
        patElectronsEmbedIp

from FinalStateAnalysis.PatTools.electrons.eTrackCandidates_cfi import \
        gsfTrackCandidates

customizeElectronSequence = cms.Sequence()
customizeElectronSequence += gsfTrackCandidates
customizeElectronSequence += electronsWWID
customizeElectronSequence += electronsVBTFId
customizeElectronSequence += patElectronsEmbedJetInfo
customizeElectronSequence += electronSystematics
customizeElectronSequence += triggeredPatElectrons
customizeElectronSequence += patElectronMVAIDEmbedder
customizeElectronSequence += patElectronsEmbedIp

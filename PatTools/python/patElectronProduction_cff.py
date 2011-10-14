import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.electrons.patConversionRejection_cfi import \
        electronsWWID
from FinalStateAnalysis.PatTools.electrons.patElectronVBTFEmbedding_cff import \
        electronsWP80, electronsWP90, electronsWP95, electronsVBTFId

from FinalStateAnalysis.PatTools.electrons.electronSystematics_cfi import \
        electronSystematics

from FinalStateAnalysis.PatTools.electrons.triggerMatch_cfi import triggeredPatElectrons

customizeElectronSequence = cms.Sequence()
customizeElectronSequence += electronsWWID
customizeElectronSequence += electronsVBTFId
customizeElectronSequence += electronSystematics
customizeElectronSequence += triggeredPatElectrons

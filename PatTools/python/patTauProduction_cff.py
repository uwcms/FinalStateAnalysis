import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.taus.patTauSystematics_cfi import systematicsTaus
from FinalStateAnalysis.PatTools.taus.patTauEmbedJetInfo_cfi import patTausEmbedJetInfo
from FinalStateAnalysis.PatTools.taus.patTauEmbedPresel_cfi import patTauEmbedPresel
from FinalStateAnalysis.PatTools.taus.triggerMatch_cfi import triggeredPatTaus, preTriggeredPatTaus
from FinalStateAnalysis.PatTools.taus.patTausIpEmbedding_cfi import patTausEmbedIp

customizeTauSequence = cms.Sequence()

embedGenTaus = cms.EDProducer(
    "PATTauGenInfoEmbedder",
    src = cms.InputTag("systematicsTaus")
)

customizeTauSequence += embedGenTaus
customizeTauSequence += patTausEmbedJetInfo
customizeTauSequence += preTriggeredPatTaus
customizeTauSequence += triggeredPatTaus
customizeTauSequence += systematicsTaus
customizeTauSequence += patTauEmbedPresel # this has to come after the systematics
customizeTauSequence += patTausEmbedIp

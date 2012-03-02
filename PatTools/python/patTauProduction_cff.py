import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.taus.patTauSystematics_cfi import systematicsTaus
from FinalStateAnalysis.PatTools.taus.patTauEmbedJetInfo_cfi import patTausEmbedJetInfo
from FinalStateAnalysis.PatTools.taus.patTauEmbedPresel_cfi import patTauEmbedPresel
from FinalStateAnalysis.PatTools.taus.triggerMatch_cfi import triggeredPatTaus
from FinalStateAnalysis.PatTools.taus.patTausIpEmbedding_cfi import patTausEmbedIp

customizeTauSequence = cms.Sequence()

embedGenTaus = cms.EDProducer(
    "PATTauGenInfoEmbedder",
    src = cms.InputTag("systematicsTaus")
)

# We reduce the size of the tau collection by reducing the size of the seed jet
# collection.  The taus without jets need to be removed here, because some of
# the later modules assume every tau has a jet.
patTausThatHaveJets = cms.EDFilter(
    "PATTauSelector",
    src = cms.InputTag("fixme"),
    cut = cms.string('userCand("patJet").isNonnull'),
    filter = cms.bool(False),
)

customizeTauSequence += embedGenTaus
customizeTauSequence += patTausEmbedJetInfo
customizeTauSequence += patTausThatHaveJets
customizeTauSequence += triggeredPatTaus
customizeTauSequence += systematicsTaus
customizeTauSequence += patTauEmbedPresel # this has to come after the systematics
customizeTauSequence += patTausEmbedIp

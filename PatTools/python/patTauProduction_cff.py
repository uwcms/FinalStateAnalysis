import FWCore.ParameterSet.Config as cms

from FinalStateAnalysis.PatTools.taus.patTauSystematics_cfi \
    import systematicsTaus
from FinalStateAnalysis.PatTools.taus.patTauEmbedJetInfo_cfi \
    import patTausEmbedJetInfo
from FinalStateAnalysis.PatTools.taus.patTausIpEmbedding_cfi \
    import patTausEmbedIp

customizeTauSequence = cms.Sequence()

# Remove garbage low pt taus.  This cut is important, so we define
# it in the main sequence.
patTauGarbageRemoval = cms.EDFilter(
    "PATTauSelector",
    src=cms.InputTag("fixme"),
    cut=cms.string("fixme"),
    filter=cms.bool(False),
)

embedGenTaus = cms.EDProducer(
    "PATTauGenInfoEmbedder",
    src=cms.InputTag("systematicsTaus")
)

customizeTauSequence += patTauGarbageRemoval
customizeTauSequence += embedGenTaus
customizeTauSequence += patTausEmbedJetInfo
customizeTauSequence += systematicsTaus
customizeTauSequence += patTausEmbedIp

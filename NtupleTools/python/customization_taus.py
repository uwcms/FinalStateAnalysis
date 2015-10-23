# Embed IDs for taus
import FWCore.ParameterSet.Config as cms

def preTaus(process, use25ns, tSrc, vSrc,**kwargs):
    process.genembeddedTaus=cms.EDProducer("PATTauGenInfoEmbedder",
          src=cms.InputTag(tSrc)
    )
    
    process.embeddedTaus=cms.Path(process.genembeddedTaus)
    
    process.schedule.append(process.embeddedTaus)
    tSrc = 'genembeddedTaus'

    return tSrc

def postTaus(process, use25ns, tSrc, jSrc,**kwargs):
    process.miniAODTauJetInfoEmbedding = cms.EDProducer(
        "MiniAODTauJetInfoEmbedder",
        src = cms.InputTag(tSrc),
        embedBtags = cms.bool(False),
        suffix = cms.string(''),
        jetSrc = cms.InputTag(jSrc),
        maxDeltaR = cms.double(0.1),
    )
    tSrc = 'miniAODTauJetInfoEmbedding'
    process.TauJetInfoEmbedding = cms.Path(
        process.miniAODTauJetInfoEmbedding
    )
    process.schedule.append(process.TauJetInfoEmbedding)

    return tSrc


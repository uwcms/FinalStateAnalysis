# Embed IDs for jets
import FWCore.ParameterSet.Config as cms

def preJets(process, use25ns, jSrc, vSrc,**kwargs):

    process.miniPatJets = cms.EDProducer(
        "MiniAODJetIdEmbedder",
        src=cms.InputTag(jSrc)
    )
    jSrc = 'miniPatJets'
    
    process.runMiniAODJetEmbedding = cms.Path(
        process.miniPatJets
    )
    process.schedule.append(process.runMiniAODJetEmbedding)

    return jSrc

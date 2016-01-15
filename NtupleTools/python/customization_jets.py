# Embed IDs for jets
import FWCore.ParameterSet.Config as cms

def preJets(process, use25ns, jSrc, vSrc, mSrc, eSrc, eCut,eDeltaR,mCut,mDeltaR,jCut,**kwargs):

    process.miniPatJets = cms.EDProducer(
        "MiniAODJetIdEmbedder",
        src=cms.InputTag(jSrc)
    )
    jSrc = 'miniPatJets'
    
    process.runMiniAODJetEmbedding = cms.Path(
        process.miniPatJets
    )
    process.schedule.append(process.runMiniAODJetEmbedding)

    process.miniAODJetCleaningEmbedding = cms.EDProducer(
        "MiniAODJetCleaningEmbedder",
        jetSrc = cms.InputTag(jSrc),
        muSrc = cms.InputTag(mSrc),
        eSrc = cms.InputTag(eSrc),
        eID = cms.string(eCut),
        eDR = cms.double(eDeltaR),
        mID = cms.string(mCut),
        mDR = cms.double(mDeltaR),
        jID = cms.string(jCut),
    )
    jSrc = 'miniAODJetCleaningEmbedding'
    process.jetCleaningEmbedding = cms.Path(
        process.miniAODJetCleaningEmbedding
    )
    process.schedule.append(process.jetCleaningEmbedding)

    return jSrc

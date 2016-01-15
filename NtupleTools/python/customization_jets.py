# Embed IDs for jets
import FWCore.ParameterSet.Config as cms

def preJets(process, use25ns, jSrc, vSrc, mSrc, eSrc, eCut,eDeltaR,mCut,mDeltaR,jCut,**kwargs):
    postfix = kwargs.pop('postfix','')

    mod = cms.EDProducer(
        "MiniAODJetIdEmbedder",
        src=cms.InputTag(jSrc)
    )
    modName = 'miniPatJets{0}'.format(postfix)
    setattr(process,modName,mod)
    jSrc = modName
    
    pathName = 'runMiniAODJetEmbedding{0}'.format(postfix)
    setattr(process,pathName,cms.Path(getattr(process,modName)))
    process.schedule.append(getattr(process,pathName))

    # embed IP stuff
    modName = 'miniJetsEmbedIp{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODJetIpEmbedder",
        src = cms.InputTag(jSrc),
        vtxSrc = cms.InputTag(vSrc),
    )
    jSrc = modName
    setattr(process,modName,mod)

    pathName = 'runMiniAODJetIpEmbedding{0}'.format(postfix)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))

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

# Embed IDs for jets
import FWCore.ParameterSet.Config as cms

def preJets(process, use25ns, jSrc, vSrc, mSrc, eSrc, **kwargs):
    postfix = kwargs.pop('postfix','')
    eCut = kwargs.pop('eCut','')
    mCut = kwargs.pop('mCut','')
    jCut = kwargs.pop('jCut','')
    eDeltaR = kwargs.pop('eDeltaR',0.3)
    mDeltaR = kwargs.pop('mDeltaR',0.3)
    jType = kwargs.pop('jType','AK4PFchs')

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

    ## embed IP stuff
    #modName = 'miniJetsEmbedIp{0}'.format(postfix)
    #mod = cms.EDProducer(
    #    "MiniAODJetIpEmbedder",
    #    src = cms.InputTag(jSrc),
    #    vtxSrc = cms.InputTag(vSrc),
    #)
    #jSrc = modName
    #setattr(process,modName,mod)

    #pathName = 'runMiniAODJetIpEmbedding{0}'.format(postfix)
    #path = cms.Path(getattr(process,modName))
    #setattr(process,pathName,path)
    #process.schedule.append(getattr(process,pathName))

    modName = 'miniAODJetCleaningEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODJetCleaningEmbedder",
        jetSrc = cms.InputTag(jSrc),
        muSrc = cms.InputTag(mSrc),
        eSrc = cms.InputTag(eSrc),
        eID = cms.string(eCut),
        eDR = cms.double(eDeltaR),
        mID = cms.string(mCut),
        mDR = cms.double(mDeltaR),
        jID = cms.string(jCut)
    )
    jSrc = modName
    setattr(process,modName,mod)

    pathName = 'jetCleaningEmbedding{0}'.format(postfix)
    path = cms.Path(
        getattr(process,modName)
    )
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))

    modName = 'miniAODJetSystematicsEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
	"MiniAODJetSystematicsEmbedder",
        src = cms.InputTag(jSrc),
        corrLabel = cms.string(jType)
    )
    jSrc = modName
    setattr(process,modName,mod)

    pathName = 'jetSystematicsEmbedding{0}'.format(postfix)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)
  
    process.schedule.append(getattr(process,pathName))

    return jSrc


# Embed IDs for jets
import FWCore.ParameterSet.Config as cms

def preJets(process, jSrc, vSrc, mSrc, eSrc, **kwargs):
    postfix = kwargs.pop('postfix','')
    jType = kwargs.pop('jType','AK4PFchs')
    doBTag = kwargs.pop('doBTag',False)

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

    # embed BTag SFs
    if doBTag :
        modName = 'miniJetsEmbedBTagSFLoose{0}'.format(postfix)
        mod = cms.EDProducer(
            "MiniAODJetBTagSFLooseEmbedder",
            src=cms.InputTag(jSrc)
        )
        jSrc = modName
        setattr(process,modName,mod)

        pathName = 'runMiniAODJetBTagSFLooseEmbedding{0}'.format(postfix)
        path = cms.Path(getattr(process,modName))
        setattr(process,pathName,path)
        process.schedule.append(getattr(process,pathName))

    # embed BTag SFs
    if doBTag :
        modName = 'miniJetsEmbedBTagSFMedium{0}'.format(postfix)
        mod = cms.EDProducer(
            "MiniAODJetBTagSFMediumEmbedder",
            src=cms.InputTag(jSrc)
        )
        jSrc = modName
        setattr(process,modName,mod)

        pathName = 'runMiniAODJetBTagSFMediumEmbedding{0}'.format(postfix)
        path = cms.Path(getattr(process,modName))
        setattr(process,pathName,path)
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


# Embed IDs for jets
import FWCore.ParameterSet.Config as cms

def preJets(process, use25ns, jSrc, vSrc,**kwargs):
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

    return jSrc

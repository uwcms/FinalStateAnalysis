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

    return jSrc

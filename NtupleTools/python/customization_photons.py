# Embed IDs for jets
import FWCore.ParameterSet.Config as cms

def prePhotons(process, use25ns, pSrc, vSrc, **kwargs):
    postfix = kwargs.pop('postfix','')


    return pSrc

def postPhotons(process, use25ns, pSrc, jSrc,**kwargs):
    postfix = kwargs.pop('postfix','')
    modName = 'miniAODPhotonJetInfoEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODPhotonJetInfoEmbedder",
        src = cms.InputTag(pSrc),
        embedBtags = cms.bool(False),
        suffix = cms.string(''),
        jetSrc = cms.InputTag(jSrc),
        maxDeltaR = cms.double(0.1),
    )
    setattr(process,modName,mod)
    pSrc = modName
    modPath = 'PhotonJetInfoEmbedding{0}'.format(postfix)
    setattr(process,modPath,cms.Path(getattr(process,modName)))
    process.schedule.append(getattr(process,modPath))

    return pSrc



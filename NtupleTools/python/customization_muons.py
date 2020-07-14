# Embed IDs for muons
import FWCore.ParameterSet.Config as cms

def preMuons(process, year, isEmbedded, mSrc, vSrc, **kwargs):
    postfix = kwargs.pop('postfix','')

    # embed ids
    modName = 'miniPatMuons{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODMuonIDEmbedder",
        src=cms.InputTag(mSrc),
        vertices=cms.InputTag(vSrc),
    )
    mSrc = modName
    setattr(process,modName,mod)

    pathName = 'runMiniAODMuonEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))

    # embed trigger filters
    modName = 'minitriggerfilterMuons{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODMuonTriggerFilterEmbedder",
        src=cms.InputTag(mSrc),
        bits = cms.InputTag("TriggerResults","","HLT"),
        objects = cms.InputTag("slimmedPatTrigger"),
        #bits = cms.InputTag("TriggerResults","","SIMembedding"),
        #objects = cms.InputTag("slimmedPatTrigger","","MERGE"),
    )
    if isEmbedded:
        mod.bits=cms.InputTag("TriggerResults","","SIMembedding")
        mod.objects=cms.InputTag("slimmedPatTrigger","","MERGE")
	if year=="2016":
	   mod.objects=cms.InputTag("slimmedPatTrigger","","PAT")

    mSrc = modName
    setattr(process,modName,mod)
    
    pathName = 'runTriggerFilterMuonEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))
    
    return mSrc

def postMuons(process, mSrc, jSrc,**kwargs):

    return mSrc


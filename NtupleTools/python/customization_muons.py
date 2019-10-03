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
    
    # embed IP
    modName = 'miniMuonsEmbedIp{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODMuonIpEmbedder",
        src = cms.InputTag(mSrc),
        vtxSrc = cms.InputTag(vSrc),
    )
    mSrc = modName
    setattr(process,modName,mod)
    
    pathName = 'runMiniAODMuonIpEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))

    # embed IP2 (needed for bestMuonTrack version of dZ)
    modName = 'miniMuonsEmbedIp2{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODMuonIpEmbedder2",
        muonSrc = cms.InputTag(mSrc),
        vtxSrc = cms.InputTag(vSrc),
    )
    mSrc = modName
    setattr(process,modName,mod)
    
    pathName = 'runMiniAODMuonIpEmbedding2{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))

    # Embed effective areas in muons
    if not hasattr(process,'patMuonEAEmbedder'):
        process.load("FinalStateAnalysis.PatTools.muons.patMuonEAEmbedding_cfi")
    eaModName = 'patMuonEAEmbedder{0}'.format(postfix)
    if postfix:
         setattr(process,eaModName,process.patMuonEAEmbedder.clone())
    getattr(process,eaModName).src = cms.InputTag(mSrc)
    mSrc = eaModName
    eaPathName = 'MuonEAEmbedding{0}'.format(postfix)
    eaPath = cms.Path(getattr(process,eaModName))
    setattr(process,eaPathName,eaPath)
    process.schedule.append(getattr(process,eaPathName))
    
    # rho embedding
    rhoModName = 'miniAODMuonRhoEmbedding{0}'.format(postfix)
    rhoMod = cms.EDProducer(
        "MuonRhoOverloader",
        src = cms.InputTag(mSrc),
        srcRho = cms.InputTag("fixedGridRhoFastjetCentralNeutral"), # not sure this is right
        userLabel = cms.string("rho_fastjet")
        )
    mSrc = rhoModName
    setattr(process,rhoModName,rhoMod)
    rhoPathName = 'muonRhoEmbedding{0}'.format(postfix)
    rhoPath = cms.Path(getattr(process,rhoModName))
    setattr(process,rhoPathName,rhoPath)
    process.schedule.append(getattr(process,rhoPathName))

    return mSrc

def postMuons(process, mSrc, jSrc,**kwargs):
    postfix = kwargs.pop('postfix','')
    modName = 'miniAODMuonJetInfoEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODMuonJetInfoEmbedder",
        src = cms.InputTag(mSrc),
        embedBtags = cms.bool(False),
        suffix = cms.string(''),
        jetSrc = cms.InputTag(jSrc),
        maxDeltaR = cms.double(0.5),
    )
    mSrc = modName
    setattr(process,modName,mod)

    pathName = 'MuonJetInfoEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))

    return mSrc


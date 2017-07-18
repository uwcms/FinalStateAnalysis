# Embed IDs for muons
import FWCore.ParameterSet.Config as cms

def preMuons(process, mSrc, vSrc, **kwargs):
    postfix = kwargs.pop('postfix','')
    skipGhost = kwargs.pop('skipGhost', False)

    if not skipGhost:
        # Clean out muon "ghosts" caused by track ambiguities
        modName = 'ghostCleanedMuons{0}'.format(postfix)
        mod = cms.EDProducer("PATMuonCleanerBySegments",
                             src = cms.InputTag(mSrc),
                             preselection = cms.string("track.isNonnull"),
                             passthrough = cms.string("isGlobalMuon && numberOfMatches >= 2"),
                             fractionOfSharedSegments = cms.double(0.499))
        mSrc = modName
        setattr(process,modName,mod)
    
        pathName = 'miniCleanedMuons{0}'.format(postfix)
        modPath = cms.Path(getattr(process,modName))
        setattr(process,pathName,modPath)
        process.schedule.append(getattr(process,pathName))

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


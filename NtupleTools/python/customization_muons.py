# Embed IDs for muons
import FWCore.ParameterSet.Config as cms

def preMuons(process, use25ns, mSrc, vSrc, **kwargs):
    isoCheatLabel = kwargs.pop('isoCheatLabel','HZZ4lISoPass')
    idCheatLabel = kwargs.pop('idCheatLabel','HZZ4lIDPass')
    skipGhost = kwargs.pop('skipGhost', False)

    if not skipGhost:
        # Clean out muon "ghosts" caused by track ambiguities
        process.ghostCleanedMuons = cms.EDProducer("PATMuonCleanerBySegments",
                                                   src = cms.InputTag(mSrc),
                                                   preselection = cms.string("track.isNonnull"),
                                                   passthrough = cms.string("isGlobalMuon && numberOfMatches >= 2"),
                                                   fractionOfSharedSegments = cms.double(0.499))
        mSrc = "ghostCleanedMuons"
    
        process.miniCleanedMuons = cms.Path(process.ghostCleanedMuons)
        process.schedule.append(process.miniCleanedMuons)

    process.miniPatMuons = cms.EDProducer(
        "MiniAODMuonIDEmbedder",
        src=cms.InputTag(mSrc),
        vertices=cms.InputTag(vSrc),
    )
    mSrc = "miniPatMuons"
    
    process.runMiniAODMuonEmbedding = cms.Path(
        process.miniPatMuons
    )
    process.schedule.append(process.runMiniAODMuonEmbedding)
    
    process.miniMuonsEmbedIp = cms.EDProducer(
        "MiniAODMuonIpEmbedder",
        src = cms.InputTag(mSrc),
        vtxSrc = cms.InputTag(vSrc),
    )
    mSrc = 'miniMuonsEmbedIp'
    
    process.runMiniAODMuonIpEmbedding = cms.Path(
        process.miniMuonsEmbedIp
    )
    process.schedule.append(process.runMiniAODMuonIpEmbedding)

    # Embed effective areas in muons and electrons
    process.load("FinalStateAnalysis.PatTools.muons.patMuonEAEmbedding_cfi")
    process.patMuonEAEmbedder.src = cms.InputTag(mSrc)
    mSrc = 'patMuonEAEmbedder'
    process.MuonEAEmbedding = cms.Path(
        process.patMuonEAEmbedder
        )
    process.schedule.append(process.MuonEAEmbedding)
    
    # ... and muons
    process.miniAODMuonRhoEmbedding = cms.EDProducer(
        "MuonRhoOverloader",
        src = cms.InputTag(mSrc),
        srcRho = cms.InputTag("fixedGridRhoFastjetCentralNeutral"), # not sure this is right
        userLabel = cms.string("rho_fastjet")
        )
    mSrc = 'miniAODMuonRhoEmbedding'
    process.muonRhoEmbedding = cms.Path(
        process.miniAODMuonRhoEmbedding
        )
    process.schedule.append(process.muonRhoEmbedding)


    return mSrc

def postMuons(process, use25ns, mSrc, jSrc,**kwargs):
    process.miniAODMuonJetInfoEmbedding = cms.EDProducer(
        "MiniAODMuonJetInfoEmbedder",
        src = cms.InputTag(mSrc),
        embedBtags = cms.bool(False),
        suffix = cms.string(''),
        jetSrc = cms.InputTag(jSrc),
        maxDeltaR = cms.double(0.1),
    )

    process.MuonJetInfoEmbedding = cms.Path(
        process.miniAODMuonJetInfoEmbedding
    )
    process.schedule.append(process.MuonJetInfoEmbedding)

    return mSrc


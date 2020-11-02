# Embed IDs for muons
import FWCore.ParameterSet.Config as cms
import os

def preMuons(process, year, isEmbedded, mSrc, vSrc, **kwargs):
    postfix = kwargs.pop('postfix','')
    runningLocal = kwargs.pop('runningLocal',False)

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

    # embed MVA top ID
    training_file = "FinalStateAnalysis/NtupleTools/data/el_TOP18_BDTG.weights.xml"
    training_file_mu="FinalStateAnalysis/NtupleTools/data/mu_TOP18_BDTG.weights.xml"
    if runningLocal :
        training_file = "FinalStateAnalysis/NtupleTools/data/el_TOP18_BDTG.weights.xml"
        if year=="2016":
           training_file="FinalStateAnalysis/NtupleTools/data/el_TOP16_BDTG.weights.xml"
        if year=="2017":
           training_file="FinalStateAnalysis/NtupleTools/data/el_TOP17_BDTG.weights.xml"

        training_file_mu="FinalStateAnalysis/NtupleTools/data/mu_TOP18_BDTG.weights.xml"
        if year=="2016":
           training_file_mu="FinalStateAnalysis/NtupleTools/data/mu_TOP16_BDTG.weights.xml"
        if year=="2017":
           training_file_mu="FinalStateAnalysis/NtupleTools/data/mu_TOP17_BDTG.weights.xml"
    else:
        cmsswversion=os.environ['CMSSW_VERSION']
        training_file = "{0}/src/FinalStateAnalysis/NtupleTools/data/el_TOP18_BDTG.weights.xml".format(cmsswversion)
        if year=="2016":
           training_file="{0}/src/FinalStateAnalysis/NtupleTools/data/el_TOP16_BDTG.weights.xml".format(cmsswversion)
        if year=="2017":
           training_file="{0}/src/FinalStateAnalysis/NtupleTools/data/el_TOP17_BDTG.weights.xml".format(cmsswversion)

        training_file_mu="{0}/src/FinalStateAnalysis/NtupleTools/data/mu_TOP18_BDTG.weights.xml".format(cmsswversion)
        if year=="2016":
           training_file_mu="{0}/src/FinalStateAnalysis/NtupleTools/data/mu_TOP16_BDTG.weights.xml".format(cmsswversion)
        if year=="2017":
           training_file_mu="{0}/src/FinalStateAnalysis/NtupleTools/data/mu_TOP17_BDTG.weights.xml".format(cmsswversion)

    modName = 'minitopmvaidMuons{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODMuonTopIdEmbedder",
        src=cms.InputTag(mSrc),
        jetSrc=cms.InputTag("slimmedJets"),
        vtxSrc = cms.InputTag(vSrc),
        srcRho = cms.InputTag("fixedGridRhoFastjetAll"),
        is2016 = cms.bool(False),
        muonsEffAreas                 = cms.FileInPath('FinalStateAnalysis/NtupleTools/data/effAreaMuons_cone03_pfNeuHadronsAndPhotons_94X.txt'),
        muonsEffAreas_80X             = cms.FileInPath('FinalStateAnalysis/NtupleTools/data/effAreaMuons_cone03_pfNeuHadronsAndPhotons_80X.txt'),
        leptonMvaWeightsEleTOP        = cms.FileInPath(training_file),
        leptonMvaWeightsMuTOP        = cms.FileInPath(training_file_mu)

    )
    if year=="2016":
        mod.is2016 = cms.bool(True)
    mSrc = modName
    setattr(process,modName,mod)

    pathName = 'runMuonTopIdEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))
    
    return mSrc

def postMuons(process, mSrc, jSrc,**kwargs):

    return mSrc


# Embed IDs for electrons
import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat, setupVIDSelection
#from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights


def preElectrons(process, eSrc, vSrc, year, **kwargs):
    postfix = kwargs.pop('postfix','')

    from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
    myera='2018-Prompt'
    if year=="2016":
       myera='2016-Legacy'
    if year=="2017":
       myera='2017-Nov17ReReco'

    setupEgammaPostRecoSeq(process,
                       era=myera) 

    pathName = 'miniAODElectrons{0}'.format(postfix)
    path=cms.Path(process.egammaPostRecoSeq)
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))

    # embed IP stuff
    modName = 'miniElectronsEmbedIp{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODElectronIpEmbedder",
        src = cms.InputTag(eSrc),
        vtxSrc = cms.InputTag(vSrc),
    )
    eSrc = modName
    setattr(process,modName,mod)
    
    pathName = 'runMiniAODElectronIpEmbedding{0}'.format(postfix)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))
    # Embed effective areas in muons and electrons
    if not hasattr(process,'patElectronEAEmbedder'):
        process.load("FinalStateAnalysis.PatTools.electrons.patElectronEAEmbedding_cfi")
    eaModName = 'patElectronEAEmbedder{0}'.format(postfix)
    if postfix:
        setattr(process,eaModName,process.patElectronEAEmbedder.clone())
    getattr(process,eaModName).src = cms.InputTag(eSrc)
    eSrc = eaModName
    eaFile = 'RecoEgamma/EgammaTools/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt'
    newEaModName = 'miniAODElectronEAEmbedding{0}'.format(postfix)
    newEaMod = cms.EDProducer(
        "MiniAODElectronEffectiveAreaEmbedder",
        src = cms.InputTag(eSrc),
        label = cms.string("EffectiveArea"), # embeds a user float with this name
        configFile = cms.FileInPath(eaFile), # the effective areas file
        )
    eSrc = newEaModName
    setattr(process,newEaModName,newEaMod)
    pathName = 'ElectronEAEmbedding{0}'.format(postfix)
    path = cms.Path(getattr(process,eaModName) + getattr(process,newEaModName))
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))
    
    # Embed rhos in electrons
    modName = 'miniAODElectronRhoEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
        "ElectronRhoOverloader",
        src = cms.InputTag(eSrc),
        srcRho = cms.InputTag("fixedGridRhoFastjetAll"), # not sure this is right
        userLabel = cms.string("rho_fastjet")
        )
    eSrc = modName
    setattr(process,modName,mod)
    
    pathName = 'electronRhoEmbedding{0}'.format(postfix)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))

    # embed WW ID
    modName = 'miniAODElectronWWIdEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODElectronWWIdEmbedder",
        src = cms.InputTag(eSrc),
        vertices = cms.InputTag(vSrc),
    )
    eSrc = modName
    setattr(process,modName,mod)
    pathName = 'miniAODElectronWWEmbeddingPath{0}'.format(postfix)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))

    
    return eSrc

def postElectrons(process, eSrc, jSrc,**kwargs):
    postfix = kwargs.pop('postfix','')
    modName = 'miniAODElectronJetInfoEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODElectronJetInfoEmbedder",
        src = cms.InputTag(eSrc),
        embedBtags = cms.bool(False),
        suffix = cms.string(''),
        jetSrc = cms.InputTag(jSrc),
        maxDeltaR = cms.double(0.5),
    )
    eSrc = modName
    setattr(process,modName,mod)

    pathName = 'ElectronJetInfoEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))

    return eSrc


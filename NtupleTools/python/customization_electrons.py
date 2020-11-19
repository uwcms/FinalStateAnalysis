# Embed IDs for electrons
import FWCore.ParameterSet.Config as cms
import os
from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat, setupVIDSelection
#from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights


def preElectrons(process, eSrc, vSrc, year, isEmbedded, **kwargs):
    postfix = kwargs.pop('postfix','')
    runningLocal = kwargs.pop('runningLocal',False)

    from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
    myera='2018-Prompt'
    if year=="2016":
       myera='2016-Legacy'
    if year=="2017":
       myera='2017-Nov17ReReco'

    setupEgammaPostRecoSeq(process,
		       eleIDModules=[
                        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V2_cff',
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
                        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff'
                        ],
                       phoIDModules=[],
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
    eaFile = 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt'
    newEaModName = 'miniAODElectronEAEmbedding{0}'.format(postfix)
    newEaMod = cms.EDProducer(
        "MiniAODElectronEffectiveAreaEmbedder",
        src = cms.InputTag(eSrc),
        label = cms.string("EffectiveArea"), # embeds a user float with this name
	year = cms.string("year"),
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

    # embed trigger filters
    modName = 'minitriggerfilterElectrons{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODElectronTriggerFilterEmbedder",
        src=cms.InputTag(eSrc),
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
    eSrc = modName
    setattr(process,modName,mod)

    pathName = 'runTriggerFilterElectronEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))

    # embed top mva id
    training_file = "FinalStateAnalysis/NtupleTools/data/el_TOP18_BDTG.weights.xml"
    training_file_mu="FinalStateAnalysis/NtupleTools/data/mu_TOP18_BDTG.weights.xml"
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

    modName = 'minitopmvaidElectrons{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODElectronTopIdEmbedder",
        src=cms.InputTag(eSrc),
        jetSrc=cms.InputTag("updatedPatJetsTransientCorrectedUpdatedJJEC"),
        #jetSrc= cms.InputTag("updatedPatJetsTransientCorrectedNewDFTraining"),
        vtxSrc = cms.InputTag(vSrc),
        srcRho = cms.InputTag("fixedGridRhoFastjetAll"),
        is2016 = cms.bool(False),
        electronsEffAreas             = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_94X.txt'),    # Recommended, used by standard IDs (the difference with the outdated effective areas is typically small)
        electronsEffAreas_Summer16    = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt'),  # old effective aras are used in 2016 computation of ttH MVA
        electronsEffAreas_Spring15    = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt'), # prehistoric effective aras are used in 2016 computation of ttH MVA
        leptonMvaWeightsEleTOP        = cms.FileInPath(training_file),
        leptonMvaWeightsMuTOP        = cms.FileInPath(training_file_mu)

    )
    if year=="2016":
        mod.is2016 = cms.bool(True)
    eSrc = modName
    setattr(process,modName,mod)

    pathName = 'runElectronTopIdEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))

    return eSrc

def postElectrons(process, eSrc, jSrc,**kwargs):

    return eSrc


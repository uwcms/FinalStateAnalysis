# Embed IDs for electrons
import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat, setupVIDSelection
#from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights


def preElectrons(process, eSrc, vSrc,**kwargs):
    postfix = kwargs.pop('postfix','')
    electronMVAIsoGeneralIDLabel = kwargs.pop('electronMVAIsoGeneralIDLabel',"BDTIsoIDGeneral")
    electronMVANoisoGeneralIDLabel = kwargs.pop('electronMVANoisoGeneralIDLabel',"BDTNoisoIDGeneral")
    applyEnergyCorrections = kwargs.pop("applyEnergyCorrections", False)
    isMCflag= kwargs.pop("isMC",False)
    isLFV=kwargs.pop("isLFV",False)

    #XXXif isLFV:
    #XXX    process = regressionWeights(process)
    #XXX    
    #XXX    process.load('EgammaAnalysis.ElectronTools.regressionApplication_cff')
    #XXX    
    #XXX    process.EGMRegression = cms.Path(process.regressionApplication)

    #XXX    process.schedule.append(process.EGMRegression)
    #XXX
    #XXX    process.selectedSlimmedElectrons = cms.EDFilter("PATElectronSelector",
    #XXX                                                    ##energy recalibration may take the corrected object outside the acceptable range for the calculation of the MVA score.
    #XXX                                                    ## this protects against a crash in electron calibration
    #XXX                                                    ## due to electrons with eta > 2.5
    #XXX                                                    src = cms.InputTag("slimmedElectrons"),
    #XXX                                                    cut = cms.string("pt>5 && abs(eta)<2.5 && abs(-log(tan(superClusterPosition.theta/2.)))<2.5")
    #XXX                                                    )

    #XXX    process.selectInBoundElectrons=cms.Path(process.selectedSlimmedElectrons)
    #XXX    process.schedule.append(process.selectInBoundElectrons)

    #XXX    eSrc='selectedSlimmedElectrons'


    if not hasattr(process,'egmGsfElectronIDs'):
        switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    egmMod = 'egmGsfElectronIDs{0}'.format(postfix)
    mvaMod = 'electronMVAValueMapProducer{0}'.format(postfix)
    regMod = 'electronRegressionValueMapProducer{0}'.format(postfix)
    egmSeq = 'egmGsfElectronIDSequence{0}'.format(postfix)

    if postfix:
        setattr(process,egmMod,process.egmGsfElectronIDs.clone())
        setattr(process,mvaMod,process.electronMVAValueMapProducer.clone())
        setattr(process,regMod,process.electronRegressionValueMapProducer.clone())
        setattr(process,egmSeq,cms.Sequence(getattr(process,mvaMod)*getattr(process,egmMod)*getattr(process,regMod)))

    getattr(process,egmMod).physicsObjectSrc = cms.InputTag(eSrc)
    getattr(process,mvaMod).srcMiniAOD = cms.InputTag(eSrc)
    getattr(process,regMod).srcMiniAOD = cms.InputTag(eSrc)

    id_modules = [
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V1_cff',
	'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff', 
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V2_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V2_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V2_cff',
        ]

    # redefine the setupVIDElectronSelection function
    def modSetupVIDElectronSelection(process,cutflow,patProducer=None,addUserData=True, task=None):
        eids = 'egmGsfElectronIDs{0}'.format(postfix)
        if not hasattr(process,eids):
            raise Exception('VIDProducerNotAvailable','{0} producer not available in process!'.format(eids))
        setupVIDSelection(getattr(process,eids),cutflow)
        print 'vidproducer', getattr(process,eids)
        #add to PAT electron producer if available or specified
        if hasattr(process,'patElectrons') or patProducer is not None:
            if patProducer is None:
                patProducer = process.patElectrons
            idName = cutflow.idName.value()
            addVIDSelectionToPATProducer(patProducer,eids,idName,addUserData)
    for idmod in id_modules:
        print 'idmod', idmod
        setupAllVIDIdsInModule(process,idmod,modSetupVIDElectronSelection)

    
    CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight", "MVA_iso_WP90", "MVA_iso_WP80", "MVA_iso_WPLoose", "MVA_noiso_WP90", "MVA_noiso_WP80", "MVA_noiso_WPLoose"]
    
    CBIDTags = [
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V2-veto'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V2-loose'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V2-medium'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V2-tight'.format(postfix)),
        cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-iso-V2-wp90".format(postfix)),
	cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-iso-V2-wp80".format(postfix)),
	cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-iso-V2-wpLoose".format(postfix)),
        cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-noIso-V2-wp90".format(postfix)),
        cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-noIso-V2-wp80".format(postfix)),
        cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-noIso-V2-wpLoose".format(postfix)),
        ]

    mvaValueLabels = [electronMVAIsoGeneralIDLabel,electronMVANoisoGeneralIDLabel]
    mvaValues = [
	cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Fall17IsoV2Values".format(postfix)),
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Fall17NoIsoV2Values".format(postfix)),
        ]
    mvaCategoryLabels = ["BDTIsoIDGeneral","BDTNoisoIDGeneral"]
    mvaCategories = [
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Fall17IsoV2Categories".format(postfix)),
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Fall17NoIsoV2Categories".format(postfix)),
        ]

    # N-1 results
    nMinusOneNames = ['GsfEleEffAreaPFIsoCut_0']
    nMinusOneLabels = ['NoIso']
    FullIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight"] # keys of cut based id user floats
    FullIDTags = [
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V2-veto'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V2-loose'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V2-medium'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V2-tight'.format(postfix)),
        ]

    # Embed cut-based VIDs
    modName = 'miniAODElectronID{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODElectronIDEmbedder",
        src=cms.InputTag(eSrc),
        idLabels = cms.vstring(*CBIDLabels),
        ids = cms.VInputTag(*CBIDTags),
        valueLabels = cms.vstring(*mvaValueLabels),       # labels for MVA values
        values = cms.VInputTag(*mvaValues),               # mva values
        categoryLabels = cms.vstring(*mvaCategoryLabels),
        categories = cms.VInputTag(*mvaCategories),
        fullIdLabels = cms.vstring(*FullIDLabels),
        #nMinusOneNames = cms.vstring(*nMinusOneNames),
        #nMinusOneLabels = cms.vstring(*nMinusOneLabels),
        fullIds = cms.VInputTag(*FullIDTags),
    )
    eSrc = modName
    setattr(process,modName,mod)

    pathName = 'miniAODElectrons{0}'.format(postfix)
    path = cms.Path(getattr(process,egmSeq)+getattr(process,modName))
    
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


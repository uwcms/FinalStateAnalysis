# Embed IDs for electrons
import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat, setupVIDSelection
#from EgammaAnalysis.ElectronTools.regressionWeights_cfi import regressionWeights


def preElectrons(process, eSrc, vSrc,**kwargs):
    postfix = kwargs.pop('postfix','')
    electronMVAGeneralIDLabel = kwargs.pop('electronMVAGeneralIDLabel',"BDTIDGeneral")
    electronMVAHzzIDLabel = kwargs.pop('electronMVAHzzIDLabel',"BDTIDHzz")
    #electronMVANonTrigIDLabel = kwargs.pop('electronMVANonTrigIDLabel',"BDTIDNonTrig")
    #electronMVATrigIDLabel = kwargs.pop('electronMVATrigIDLabel',"BDTIDTrig")
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
        
        #'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
        #'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
        #'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
        #'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV51_cff',                 # recommended for both 50 and 25 ns
        #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
        #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
        #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
        #'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronHLTPreselecition_Summer16_V1_cff',
        #XXX'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Fall17_94X_V1_cff',
        #XXX'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_noIso_V1_cff',
        #XXX'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Fall17_iso_V1_cff',
        ]
    # something here breaks the postfix stuff... no idea
    # ----- Begin Fatal Exception 12-Nov-2015 08:36:25 CST-----------------------
    # An exception of category 'Configuration' occurred while
    #    [0] Constructing the EventProcessor
    #    [1] Constructing module: class=VersionedGsfElectronIdProducer label='egmGsfElectronIDsmesUp'
    # Exception Message:
    # Duplicate Process The process name Ntuples was previously used on these products.
    # Please modify the configuration file to use a distinct process name.
    # ----- End Fatal Exception -------------------------------------------------

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

    
    CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight", "MVA_WP90", "MVA_WP80", "MVA_WPLoose"]#, "HEEPV60", "MVANonTrigWP80", "MVANonTrigWP90", "MVATrigWP90", "MVATrigWP80"] # keys of cut based id user floats
    
    CBIDTags = [
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V1-veto'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V1-loose'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V1-medium'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V1-tight'.format(postfix)),
        #cms.InputTag('egmGsfElectronIDs{0}:heepElectronID-HEEPV60'.format(postfix)),
        #cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring16-GeneralPurpose-V1-wp80'.format(postfix)),
        #cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring16-GeneralPurpose-V1-wp90'.format(postfix)),
        #cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-25ns-Trig-V1-wp90'.format(postfix)),
        #cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-25ns-Trig-V1-wp80'.format(postfix)),
        cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-iso-V1-wp90".format(postfix)),
        cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-iso-V1-wp80".format(postfix)),
        cms.InputTag("egmGsfElectronIDs{0}:mvaEleID-Fall17-iso-V1-wpLoose".format(postfix)),
        ]

    mvaValueLabels = [electronMVAGeneralIDLabel,electronMVAHzzIDLabel]
    mvaValues = [
        #cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values".format(postfix)),
        #cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values".format(postfix)),
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Fall17IsoV1Values".format(postfix)),
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Fall17NoIsoV1Values".format(postfix)),
        ]
    mvaCategoryLabels = ["BDTIDGeneral","BDTIDHzz"]
    mvaCategories = [
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Fall17IsoV1Categories".format(postfix)),
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Fall17NoIsoV1Categories".format(postfix)),
        ]

    # N-1 results
    nMinusOneNames = ['GsfEleEffAreaPFIsoCut_0']
    nMinusOneLabels = ['NoIso']
    FullIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight"] # keys of cut based id user floats
    FullIDTags = [
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V1-veto'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V1-loose'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V1-medium'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Fall17-94X-V1-tight'.format(postfix)),
        ]

    

    #XXX # Embed cut-based VIDs
    #XXX modName = 'miniAODElectronID{0}'.format(postfix)
    #XXX mod = cms.EDProducer(
    #XXX     "MiniAODElectronIDEmbedder",
    #XXX     src=cms.InputTag(eSrc),
    #XXX     idLabels = cms.vstring(*CBIDLabels),
    #XXX     ids = cms.VInputTag(*CBIDTags),
    #XXX     valueLabels = cms.vstring(*mvaValueLabels),       # labels for MVA values
    #XXX     values = cms.VInputTag(*mvaValues),               # mva values
    #XXX     categoryLabels = cms.vstring(*mvaCategoryLabels),
    #XXX     categories = cms.VInputTag(*mvaCategories),
    #XXX     fullIdLabels = cms.vstring(*FullIDLabels),
    #XXX     nMinusOneNames = cms.vstring(*nMinusOneNames),
    #XXX     nMinusOneLabels = cms.vstring(*nMinusOneLabels),
    #XXX     fullIds = cms.VInputTag(*FullIDTags),
    #XXX )
    #XXX eSrc = modName
    #XXX setattr(process,modName,mod)

    #XXX pathName = 'miniAODElectrons{0}'.format(postfix)
    #XXX path = cms.Path(getattr(process,egmSeq)+getattr(process,modName))
    #XXX 
    #XXX setattr(process,pathName,path)
    #XXX process.schedule.append(getattr(process,pathName))

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


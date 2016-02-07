# Embed IDs for electrons
import FWCore.ParameterSet.Config as cms
from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat, setupVIDSelection

def preElectrons(process, use25ns, eSrc, vSrc,**kwargs):
    postfix = kwargs.pop('postfix','')
    electronMVANonTrigIDLabel = kwargs.pop('electronMVANonTrigIDLabel',"BDTIDNonTrig")
    electronMVATrigIDLabel = kwargs.pop('electronMVATrigIDLabel',"BDTIDTrig")
    applyEnergyCorrections = kwargs.pop("applyEnergyCorrections", False)

    # Removed for now; calibrations only currently exist for 74X
    # if applyEnergyCorrections:
    #     isMC = kwargs.pop("isMC", False)
    #     isSync = kwargs.pop("isSync", False) and isMC
    #     grbForestName = "gedelectron_p4combination_%sns"%("25" if use25ns else "50")
    #     modName = 'calibratedElectrons{0}'.format(postfix)
    #     mod = cms.EDProducer(
    #         "CalibratedPatElectronProducerRun2",
    #         electrons = cms.InputTag(eSrc),
    #         grbForestName = cms.string(grbForestName),
    #         isMC = cms.bool(isMC),
    #         isSynchronization = cms.bool(isSync),
    #     )
    #     setattr(process,modName,mod)
    #     eSrc = modName
    #     pathName = 'applyElectronCalibrations{0}'.format(postfix)
    #     path = cms.Path(process.calibratedElectrons)
    #     setattr(process,pathName,path)
    #     process.schedule.append(getattr(process,pathName))
    # 
    #     # Get a random number generator and give it a seed if needed
    #     if isMC and not isSync:
    #         if not hasattr(process, "RandomNumberGeneratorService"):
    #             process.load('Configuration.StandardSequences.Services_cff')
    #         process.RandomNumberGeneratorService.calibratedElectrons = cms.PSet(
    #             initialSeed = cms.untracked.uint32(1029384756),
    #             engineName = cms.untracked.string('TRandom3'),
    #         )

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
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
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
    def modSetupVIDElectronSelection(process,cutflow,patProducer=None,addUserData=True):
        eids = 'egmGsfElectronIDs{0}'.format(postfix)
        if not hasattr(process,eids):
            raise Exception('VIDProducerNotAvailable','{0} producer not available in process!'.format(eids))
        setupVIDSelection(getattr(process,eids),cutflow)
        #add to PAT electron producer if available or specified
        if hasattr(process,'patElectrons') or patProducer is not None:
            if patProducer is None:
                patProducer = process.patElectrons
            idName = cutflow.idName.value()
            addVIDSelectionToPATProducer(patProducer,eids,idName,addUserData)
    for idmod in id_modules:
        setupAllVIDIdsInModule(process,idmod,modSetupVIDElectronSelection)
    
    CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight", "HEEPV60", "MVANonTrigWP80", "MVANonTrigWP90", "MVATrigWP90", "MVATrigWP80"] # keys of cut based id user floats
    
    CBIDTags = [
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-50ns-V1-standalone-veto'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-50ns-V1-standalone-loose'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-50ns-V1-standalone-medium'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-50ns-V1-standalone-tight'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:heepElectronID-HEEPV60'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-50ns-Trig-V1-wp90'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-50ns-Trig-V1-wp80'.format(postfix)),
        ]
    if use25ns:
        CBIDTags = [
            cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-25ns-V1-standalone-veto'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-25ns-V1-standalone-tight'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:heepElectronID-HEEPV60'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-25ns-Trig-V1-wp90'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:mvaEleID-Spring15-25ns-Trig-V1-wp80'.format(postfix)),
            ]

    mvaValueLabels = [electronMVANonTrigIDLabel,electronMVATrigIDLabel]
    mvaValues = [
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values".format(postfix)),
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15Trig50nsV1Values".format(postfix)),
        ]
    if use25ns:
        mvaValues = [
            cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values".format(postfix)),
            cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values".format(postfix)),
            ]
    mvaCategoryLabels = ["BDTIDNonTrigCategory","BDTIDTrigCategory"]
    mvaCategories = [
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories".format(postfix)),
        cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15Trig50nsV1Categories".format(postfix)),
        ]
    if use25ns:
        mvaCategories = [
            cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories".format(postfix)),
            cms.InputTag("electronMVAValueMapProducer{0}:ElectronMVAEstimatorRun2Spring15Trig25nsV1Categories".format(postfix)),
            ]

    # N-1 results
    nMinusOneNames = ['GsfEleEffAreaPFIsoCut_0']
    nMinusOneLabels = ['NoIso']
    FullIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight"] # keys of cut based id user floats
    FullIDTags = [
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-50ns-V1-standalone-veto'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-50ns-V1-standalone-loose'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-50ns-V1-standalone-medium'.format(postfix)),
        cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-50ns-V1-standalone-tight'.format(postfix)),
        ]
    if use25ns:
        FullIDTags = [
            cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-25ns-V1-standalone-veto'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'.format(postfix)),
            cms.InputTag('egmGsfElectronIDs{0}:cutBasedElectronID-Spring15-25ns-V1-standalone-tight'.format(postfix)),
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
        nMinusOneNames = cms.vstring(*nMinusOneNames),
        nMinusOneLabels = cms.vstring(*nMinusOneLabels),
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
    eaFile = 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_{0}ns.txt'.format('25' if use25ns else '50')
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

def postElectrons(process, use25ns, eSrc, jSrc,**kwargs):
    postfix = kwargs.pop('postfix','')
    modName = 'miniAODElectronJetInfoEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODElectronJetInfoEmbedder",
        src = cms.InputTag(eSrc),
        embedBtags = cms.bool(False),
        suffix = cms.string(''),
        jetSrc = cms.InputTag(jSrc),
        maxDeltaR = cms.double(0.1),
    )
    eSrc = modName
    setattr(process,modName,mod)

    pathName = 'ElectronJetInfoEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
    process.schedule.append(getattr(process,pathName))

    return eSrc


# Embed IDs for electrons
import FWCore.ParameterSet.Config as cms

def preElectrons(process, use25ns, eSrc, vSrc,**kwargs):
    isoCheatLabel = kwargs.pop('isoCheatLabel','HZZ4lISoPass')
    idCheatLabel = kwargs.pop('idCheatLabel','HZZ4lIDPass')
    electronMVANonTrigIDLabel = kwargs.pop('electronMVANonTrigIDLabel',"BDTIDNonTrig")
    electronMVATrigIDLabel = kwargs.pop('electronMVATrigIDLabel',"BDTIDTrig")


    from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(eSrc)
    id_modules = [
        #'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V2_cff',
        #'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_PHYS14_PU20bx25_nonTrig_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_Trig_V1_cff',    # 25 ns trig
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_50ns_Trig_V1_cff',    # 50 ns trig
        ]
    for idmod in id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    
    CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight", "HEEPV60", "MVANonTrigWP80", "MVANonTrigWP90", "MVATrigWP90", "MVATrigWP80"] # keys of cut based id user floats
    
    CBIDTags = [
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-veto'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-loose'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-medium'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-tight'),
        cms.InputTag('egmGsfElectronIDs:heepElectronID-HEEPV60'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-50ns-Trig-V1-wp90'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-50ns-Trig-V1-wp80'),
        ]
    if use25ns:
        CBIDTags = [
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight'),
            cms.InputTag('egmGsfElectronIDs:heepElectronID-HEEPV60'),
            cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'),
            cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'),
            cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-Trig-V1-wp90'),
            cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-Trig-V1-wp80'),
            ]

    mvaValueLabels = [electronMVANonTrigIDLabel,electronMVATrigIDLabel]
    mvaValues = [
        cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
        cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig50nsV1Values"),
        ]
    if use25ns:
        mvaValues = [
            cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
            cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Values"),
            ]
    mvaCategoryLabels = ["BDTIDNonTrigCategory","BDTIDTrigCategory"]
    mvaCategories = [
        cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories"),
        cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig50nsV1Categories"),
        ]
    if use25ns:
        mvaCategories = [
            cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories"),
            cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15Trig25nsV1Categories"),
            ]

    # N-1 results
    nMinusOneNames = ['GsfEleEffAreaPFIsoCut_0']
    nMinusOneLabels = ['NoIso']
    FullIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight"] # keys of cut based id user floats
    FullIDTags = [
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-veto'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-loose'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-medium'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-tight'),
        ]
    if use25ns:
        FullIDTags = [
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight'),
            ]

    

    # Embed cut-based VIDs
    process.miniAODElectronID = cms.EDProducer(
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
    eSrc = "miniAODElectronID"
    
    process.miniAODElectrons = cms.Path(
        process.egmGsfElectronIDSequence+
        process.miniAODElectronID
        )
    process.schedule.append(process.miniAODElectrons)

    process.miniElectronsEmbedIp = cms.EDProducer(
        "MiniAODElectronIpEmbedder",
        src = cms.InputTag(eSrc),
        vtxSrc = cms.InputTag(vSrc),
    )
    eSrc = 'miniElectronsEmbedIp'
    
    process.runMiniAODElectronIpEmbedding = cms.Path(
        process.miniElectronsEmbedIp
    )
    process.schedule.append(process.runMiniAODElectronIpEmbedding)

    # Embed effective areas in muons and electrons
    process.load("FinalStateAnalysis.PatTools.electrons.patElectronEAEmbedding_cfi")
    process.patElectronEAEmbedder.src = cms.InputTag(eSrc)
    eSrc = 'patElectronEAEmbedder'
    # And for electrons, the new HZZ4l EAs as well
    process.miniAODElectronEAHZZEmbedding = cms.EDProducer(
        "MiniAODElectronEffectiveArea2015Embedder",
        src = cms.InputTag(eSrc),
        label = cms.string("EffectiveArea_HZZ4l2015"), # embeds a user float with this name
        use25ns = cms.bool(bool(use25ns)),
        )
    eSrc = 'miniAODElectronEAHZZEmbedding'
    eaFile = 'RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_{0}ns.txt'.format('25' if use25ns else '50')
    process.miniAODElectronEAEmbedding = cms.EDProducer(
        "MiniAODElectronEffectiveAreaEmbedder",
        src = cms.InputTag(eSrc),
        label = cms.string("EffectiveArea"), # embeds a user float with this name
        configFile = cms.FileInPath(eaFile), # the effective areas file
        )
    eSrc = 'miniAODElectronEAEmbedding'
    process.ElectronEAEmbedding = cms.Path(
        process.patElectronEAEmbedder +
        process.miniAODElectronEAHZZEmbedding +
        process.miniAODElectronEAEmbedding
        )
    process.schedule.append(process.ElectronEAEmbedding)
    
    # Embed rhos in electrons
    process.miniAODElectronRhoEmbedding = cms.EDProducer(
        "ElectronRhoOverloader",
        src = cms.InputTag(eSrc),
        srcRho = cms.InputTag("fixedGridRhoFastjetAll"), # not sure this is right
        userLabel = cms.string("rho_fastjet")
        )
    eSrc = 'miniAODElectronRhoEmbedding'
    
    process.electronRhoEmbedding = cms.Path(
        process.miniAODElectronRhoEmbedding
        )
    process.schedule.append(process.electronRhoEmbedding)

    # Embed HZZ ID and isolation decisions because we need to know them for FSR recovery
    process.electronIDIsoCheatEmbedding = cms.EDProducer(
        "MiniAODElectronHZZIDDecider",
        src = cms.InputTag(eSrc),
        idLabel = cms.string(idCheatLabel), # boolean stored as userFloat with this name
        isoLabel = cms.string(isoCheatLabel), # boolean stored as userFloat with this name
        rhoLabel = cms.string("rho_fastjet"), # use rho and EA userFloats with these names
        eaLabel = cms.string("EffectiveArea_HZZ4l2015"),
        vtxSrc = cms.InputTag(vSrc),
        bdtLabel = cms.string(electronMVANonTrigIDLabel),
        idCutLowPtLowEta = cms.double(-.265),
        idCutLowPtMedEta = cms.double(-.556),
        idCutLowPtHighEta = cms.double(-.551),
        idCutHighPtLowEta = cms.double(-.072),
        idCutHighPtMedEta = cms.double(-.286),
        idCutHighPtHighEta = cms.double(-.267),
        missingHitsCut = cms.int32(999),
        )
    eSrc = 'electronIDIsoCheatEmbedding'

    if not use25ns:
        process.electronIDIsoCheatEmbedding.bdtLabel = cms.string('')
        process.electronIDIsoCheatEmbedding.selection = cms.string('userFloat("CBIDMedium") > 0.5')
        process.electronIDIsoCheatEmbedding.ptCut = cms.double(10.)
        process.electronIDIsoCheatEmbedding.sipCut = cms.double(9999.)

    process.embedHZZ4lIDDecisionsElectron = cms.Path(
        process.electronIDIsoCheatEmbedding
        )
    process.schedule.append(process.embedHZZ4lIDDecisionsElectron)


    return eSrc

def postElectrons(process, use25ns, eSrc, jSrc,**kwargs):
    process.miniAODElectronJetInfoEmbedding = cms.EDProducer(
        "MiniAODElectronJetInfoEmbedder",
        src = cms.InputTag(eSrc),
        embedBtags = cms.bool(False),
        suffix = cms.string(''),
        jetSrc = cms.InputTag(jSrc),
        maxDeltaR = cms.double(0.1),
    )
    eSrc = 'miniAODElectronJetInfoEmbedding'

    process.ElectronJetInfoEmbedding = cms.Path(
        process.miniAODElectronJetInfoEmbedding
    )
    process.schedule.append(process.ElectronJetInfoEmbedding)


    return eSrc


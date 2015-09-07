# Embed IDs for electrons
import FWCore.ParameterSet.Config as cms

def embedElectronIDs(process, use25ns, eSrc):
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(eSrc)
    id_modules = [
        'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V2_cff',
        'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_PHYS14_PU20bx25_nonTrig_V1_cff',
        # 'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_25ns_V1_cff',    # both 25 and 50 ns cutbased ids produced
        # 'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_Spring15_50ns_V1_cff',
        'RecoEgamma.ElectronIdentification.Identification.heepElectronID_HEEPV60_cff',                 # recommended for both 50 and 25 ns
        # 'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_Spring15_25ns_nonTrig_V1_cff', # will not be produced for 50 ns, triggering still to come
        ]
    for idmod in id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    
    CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight", "HEEPV60", "MVANonTrigWP80", "MVANonTrigWP90"] # keys of cut based id user floats
    
    CBIDTags = [
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-veto'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-loose'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-medium'),
        cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tight'),
        cms.InputTag('egmGsfElectronIDs:heepElectronID-HEEPV60'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80'),
        cms.InputTag('egmGsfElectronIDs:mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90'),
        # cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-veto'),
        # cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-loose'),
        # cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-medium'),
        # cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-50ns-V1-standalone-tight'),
        # cms.InputTag('egmGsfElectronIDs:heepElectronID-HEEPV60'),
        # cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'),
        # cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'),
        ]
    # if use25ns:
    #     CBIDTags = [
    #         cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-veto'),
    #         cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-loose'),
    #         cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-medium'),
    #         cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-Spring15-25ns-V1-standalone-tight'),
    #         cms.InputTag('egmGsfElectronIDs:heepElectronID-HEEPV60'),
    #         cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp80'),
    #         cms.InputTag('egmGsfElectronIDs:mvaEleID-Spring15-25ns-nonTrig-V1-wp90'),
    #         ]

    mvaValueLabels = ["BDTIDNonTrig"]
    mvaValues = [
        cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Phys14NonTrigValues"),
        # cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Values"),
        ]
    mvaCategoryLabels = ["BDTIDNonTrigCategory"]
    mvaCategories = [
        cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Phys14NonTrigCategories"),
        # cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Spring15NonTrig25nsV1Categories"),
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
    )
    eSrc = "miniAODElectronID"
    
    process.miniAODElectrons = cms.Path(
        process.egmGsfElectronIDSequence+
        process.miniAODElectronID
        )
    process.schedule.append(process.miniAODElectrons)

    return eSrc

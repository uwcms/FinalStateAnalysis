# Embed IDs for electrons
import FWCore.ParameterSet.Config as cms

def embedElectronIDs(process, use25ns, eSrc):
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import setupAllVIDIdsInModule, setupVIDElectronSelection, switchOnVIDElectronIdProducer, DataFormat
    switchOnVIDElectronIdProducer(process, DataFormat.MiniAOD)
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(eSrc)
    if use25ns:
        id_modules = [
            'RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V2_cff',
            'RecoEgamma.ElectronIdentification.Identification.mvaElectronID_PHYS14_PU20bx25_nonTrig_V1_cff',
            ]
    else:
        print "50 ns cut based electron IDs don't exist yet for PHYS14. Using CSA14 cuts."
        id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_CSA14_50ns_V1_cff']
    for idmod in id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    
    CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight", "MVANonTrigWP80", "MVANonTrigWP90"] # keys of cut based id user floats
    if use25ns:
        CBIDTags = [
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-veto'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-loose'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-medium'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V2-standalone-tight'),
            cms.InputTag("egmGsfElectronIDs:mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp80"),
            cms.InputTag("egmGsfElectronIDs:mvaEleID-PHYS14-PU20bx25-nonTrig-V1-wp90"),
            ]
    else:
        CBIDTags = [ # almost certainly wrong. Just don't use 50ns miniAOD any more
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-veto'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-loose'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-medium'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-tight'),
            ]
    if use25ns:
        mvaValueLabels = ["BDTIDNonTrig"]
        mvaValues = [
            cms.InputTag("electronMVAValueMapProducer:ElectronMVAEstimatorRun2Phys14NonTrigValues"),
            ]
    else:
        mvaValueLabels = []
        mvaValues = []

    # Embed cut-based VIDs
    process.miniAODElectronID = cms.EDProducer(
        "MiniAODElectronIDEmbedder",
        src=cms.InputTag(eSrc),
        idLabels = cms.vstring(*CBIDLabels),
        ids = cms.VInputTag(*CBIDTags),
        valueLabels = cms.vstring(*mvaValueLabels),       # labels for MVA values
        values = cms.VInputTag(*mvaValues),               # mva values
    )
    eSrc = "miniAODElectronID"
    
    process.miniAODElectrons = cms.Path(
        process.egmGsfElectronIDSequence+
        process.miniAODElectronID
        )
    process.schedule.append(process.miniAODElectrons)

    return eSrc

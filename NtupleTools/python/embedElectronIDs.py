# Embed IDs for electrons

def embedElectronIDs(process,use25ns,eSrc):
    # Turn on versioned cut-based ID
    from PhysicsTools.SelectorUtils.tools.vid_id_tools import *
    process.load("RecoEgamma.ElectronIdentification.egmGsfElectronIDs_cfi")
    process.egmGsfElectronIDs.physicsObjectSrc = cms.InputTag(eSrc)
    from PhysicsTools.SelectorUtils.centralIDRegistry import central_id_registry
    process.egmGsfElectronIDSequence = cms.Sequence(process.egmGsfElectronIDs)
    if use25ns:
        cb_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_PHYS14_PU20bx25_V1_miniAOD_cff']
    else:
        print "50 ns cut based electron IDs don't exist yet for PHYS14. Using CSA14 cuts."
        cb_id_modules = ['RecoEgamma.ElectronIdentification.Identification.cutBasedElectronID_CSA14_50ns_V1_cff']
    for idmod in cb_id_modules:
        setupAllVIDIdsInModule(process,idmod,setupVIDElectronSelection)
    
    CBIDLabels = ["CBIDVeto", "CBIDLoose", "CBIDMedium", "CBIDTight"] # keys of cut based id user floats
    if use25ns:
        CBIDTags = [
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-veto'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-loose'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-medium'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-PHYS14-PU20bx25-V1-miniAOD-standalone-tight'),
            ]
    else:
        CBIDTags = [ # almost certainly wrong. Just don't use 50ns miniAOD any more
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-veto'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-loose'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-medium'),
            cms.InputTag('egmGsfElectronIDs:cutBasedElectronID-CSA14-50ns-V1-standalone-tight'),
            ]
    
    # Embed cut-based VIDs
    process.miniAODElectronCutBasedID = cms.EDProducer(
        "MiniAODElectronCutBasedIDEmbedder",
        src=cms.InputTag(eSrc),
        idLabels = cms.vstring(*CBIDLabels),
        ids = cms.VInputTag(*CBIDTags)
    )
    eSrc = "miniAODElectronCutBasedID"
    
    # Embed MVA VIDs (weights will change soon for PHYS14!)
    trigMVAWeights = [
        'EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_25ns_EB_BDT.weights.xml',
        'EgammaAnalysis/ElectronTools/data/CSA14/TrigIDMVA_25ns_EE_BDT.weights.xml',
        ]
    nonTrigMVAWeights = [
        'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EB1_5_oldscenario2phys14_BDT.weights.xml',
        'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EB2_5_oldscenario2phys14_BDT.weights.xml',
        'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EE_5_oldscenario2phys14_BDT.weights.xml',
        'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EB1_10_oldscenario2phys14_BDT.weights.xml',
        'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EB2_10_oldscenario2phys14_BDT.weights.xml',
        'EgammaAnalysis/ElectronTools/data/PHYS14/EIDmva_EE_10_oldscenario2phys14_BDT.weights.xml',
        ]
    if not use25ns:
        for wt in trigMVAWeights+nonTrigMVAWeights:
            wt.replace('25ns','50ns')
    process.miniAODElectronMVAID = cms.EDProducer(
        "MiniAODElectronMVAIDEmbedder",
        src=cms.InputTag(eSrc),
        trigWeights = cms.vstring(*trigMVAWeights),
        trigLabel = cms.string('BDTIDTrig'), # triggering MVA ID userfloat key
        nonTrigWeights = cms.vstring(*nonTrigMVAWeights),
        nonTrigLabel = cms.string('BDTIDNonTrig') # nontriggering MVA ID userfloat key
        )
    eSrc = 'miniAODElectronMVAID'
    
    process.miniAODElectrons = cms.Path(
        process.egmGsfElectronIDSequence+
        process.miniAODElectronCutBasedID+
        process.miniAODElectronMVAID
        )
    process.schedule.append(process.miniAODElectrons)

    return eSrc

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.PatTools.fsaRandomSeeds import add_fsa_random_seeds
from FinalStateAnalysis.Utilities.version import cmssw_major_version,\
    cmssw_minor_version

def rerunRecoObjects(process):
    ''' Reruns objects as needed '''

    output_commands = []
    #Drop taus cause they are messing up everything
    process.source.dropDescendantsOfDroppedBranches = cms.untracked.bool(False)
    process.source.inputCommands = cms.untracked.vstring(
        'keep *',
        'drop recoPFTaus_*_*_*'                      
    )
    process.rerecoObjects = cms.Sequence()

    ########################
    ##                    ##
    ##  STD Services      ##
    ##                    ##
    ########################
    # Standard services
    process.load('Configuration.StandardSequences.Services_cff')
    # tack on seeds for FSA PATTuple modules
    add_fsa_random_seeds(process)

    if cmssw_major_version() == 5 and cmssw_minor_version() >= 3:
        process.load('Configuration.Geometry.GeometryDB_cff')
    else:
        process.load('Configuration.StandardSequences.GeometryDB_cff')

    process.load('Configuration.StandardSequences.MagneticField_cff')
    process.load(
        'Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

    ########################
    ##                    ##
    ##  RE-RECO           ##
    ##                    ##
    ########################

    # Select vertices
    process.load("FinalStateAnalysis.RecoTools.vertexSelection_cff")
    output_commands.append('*_selectedPrimaryVertex*_*_*')
    output_commands.append('*_selectPrimaryVerticesQuality*_*_*')
    process.rerecoObjects += process.selectPrimaryVertices

    # Run the ZZ recipe for rho
    from RecoJets.JetProducers.kt4PFJets_cfi import kt4PFJets \
        as zzCantDoAnythingRight

    process.kt6PFJetsForIso = zzCantDoAnythingRight.clone(
        rParam=cms.double(0.6),
        doAreaFastjet=cms.bool(True),
        doRhoFastjet=cms.bool(True),
        Rho_EtaMax=cms.double(2.5),
        Ghost_EtaMax=cms.double(2.5),
    )
    process.rerecoObjects += process.kt6PFJetsForIso

    ## Run rho computation.  Only necessary in 42X
    if cmssw_major_version() == 4:
        # This function call can klobber everything if it isn't done
        # before the other things are attached to the process, so do it now.
        # The klobbering would occur through usePFIso->setupPFIso->_loadPFBRECO
        from CommonTools.ParticleFlow.Tools.pfIsolation import _loadPFBRECO
        _loadPFBRECO(process)
        process.load("RecoJets.Configuration.RecoPFJets_cff")
        process.kt6PFJets.Rho_EtaMax = cms.double(4.4)
        process.kt6PFJets.doRhoFastjet = True
        process.rerecoObjects += process.kt6PFJets

    # In 4_X we have to rerun ak5PFJets with area computation enabled.
    if cmssw_major_version() == 4:
        process.load("RecoJets.Configuration.RecoPFJets_cff")
        process.ak5PFJets.doAreaFastjet = True
        process.rerecoObjects += process.ak5PFJets
        # Only keep the new ak5PFJets
        output_commands.append('*_ak5PFJets_*_%s' % process.name_())
    else:
        # Just keep the normal ones
        output_commands.append('*_ak5PFJets_*_*')

    # Rerun tau ID
    process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
    # Don't build junky taus below 17 GeV
    process.combinatoricRecoTaus.builders[0].minPtToBuild = cms.double(17)
    process.rerecoObjects += process.recoTauClassicHPSSequence

    #Run PF NoPu Jets

#    from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
#    process.goodOfflinePrimaryVertices = cms.EDFilter(
#          "PrimaryVertexObjectFilter",
#        filterParams = pvSelector.clone( maxZ = cms.double(24.0),
#        minNdof = cms.double(4.0) # this is >= 4
#        ),
#        src=cms.InputTag("offlinePrimaryVertices")
#        )
#   We are using the default collection in FSA for vertices (which has a cut on Rho as well)


    process.load("CommonTools.ParticleFlow.PFBRECO_cff")
    process.pfPileUp.Vertices = cms.InputTag("selectPrimaryVerticesQuality")
    process.pfPileUp.checkClosestZVertex = False

    process.ak5PFchsJets = process.pfJets.clone()
    process.ak5PFchsJets.doAreaFastjet = True
    process.ak5PFchsJets.src = 'pfNoPileUp'

    process.makeAK5PFNoPUJets = cms.Sequence(
#        process.goodOfflinePrimaryVertices*
        process.pfNoPileUpSequence*
        process.ak5PFchsJets)
    
    #chs JECs
    process.load("JetMETCorrections.Configuration.DefaultJEC_cff")
    process.load("JetMETCorrections.Configuration.JetCorrectionServices_cff")

    # Setting up JEC ESProducers for ak5PFchs. This block will be included in the JetCorrectionServices_cff
    # in a future tag by JetMET (March 13, 2014)
    process.ak5PFchsL1Fastjet  = process.ak5PFL1Fastjet.clone(algorithm = cms.string('AK5PFchs'))
    process.ak5PFchsL2Relative = process.ak5PFL2Relative.clone(algorithm = cms.string('AK5PFchs'))
    process.ak5PFchsL3Absolute = process.ak5PFL3Absolute.clone(algorithm = cms.string('AK5PFchs'))
    process.ak5PFchsResidual   = process.ak5PFResidual.clone(algorithm = cms.string('AK5PFchs'))
    process.ak5PFchsL2L3   = cms.ESProducer(
        'JetCorrectionESChain',
        correctors = cms.vstring('ak5PFchsL2Relative', 'ak5PFchsL3Absolute')
    )
    
    process.ak5PFchsL2L3Residual = process.ak5PFchsL2L3.clone()
    process.ak5PFchsL2L3Residual.correctors.append('ak5PFchsResidual')
    process.ak5PFchsL1FastL2L3 = process.ak5PFchsL2L3.clone()
    process.ak5PFchsL1FastL2L3.correctors.insert(0, 'ak5PFchsL1Fastjet')
    process.ak5PFchsL1FastL2L3Residual = process.ak5PFchsL1FastL2L3.clone()
    process.ak5PFchsL1FastL2L3Residual.correctors.append('ak5PFchsResidual')


    process.rerecoObjects +=process.makeAK5PFNoPUJets 

    return process.rerecoObjects, output_commands

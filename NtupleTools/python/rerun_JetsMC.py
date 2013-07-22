import FWCore.ParameterSet.Config as cms

def rerun_JetsMC(process):

  process.load("RecoJets.Configuration.RecoPFJets_cff")
  import PhysicsTools.PatAlgos.tools.jetTools as jettools
  process.load("PhysicsTools.PatAlgos.patSequences_cff")
  process.load("FinalStateAnalysis.PatTools.jets.patJetPUId_cfi")
  process.pileupJetIdProducer.applyJec = cms.bool(True)

  # Define options for BTagging - these are release dependent.
  btag_options = {'doBTagging': True}
  btag_options['btagInfo'] = [
            'secondaryVertexTagInfos',
  ]
  btag_options['btagdiscriminators'] = [
            'combinedSecondaryVertexMVABJetTags',
            'combinedSecondaryVertexBJetTags',
  ]

  jec = ['L1FastJet', 'L2Relative', 'L3Absolute']
  # For Data jec.extend(['L2L3Residual'])
  
  jettools.switchJetCollection(
        process,
        cms.InputTag('ak5PFJets'),
        doJTA=False,
        jetCorrLabel=('AK5PF', jec),
        #jetCorrLabel = None,
        doType1MET=False,
        doJetID=True,
        genJetCollection=cms.InputTag("ak5GenJets"),
        outputModules=[],
        **btag_options
  )
  process.patJets.embedPFCandidates = False
  process.patJets.embedCaloTowers = False
  process.patJets.embedGenJetMatch = False
  process.patJets.addAssociatedTracks = False
  process.patJets.embedGenPartonMatch = False
  process.patJets.tagInfoSources = cms.VInputTag(cms.InputTag("secondaryVertexTagInfos"))
  process.patJets.discriminatorSources = cms.VInputTag(cms.InputTag("combinedSecondaryVertexMVABJetTags"), cms.InputTag("combinedSecondaryVertexBJetTags"))
  process.patJets.addBTagInfo = cms.bool(True)
  
  process.ak5JetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
   	  tracks       = cms.InputTag("generalTracks"),
      jets         = cms.InputTag("ak5PFJets"),
      coneSize     = cms.double(0.5)
  )
  
  process.load('FinalStateAnalysis.PatTools.jets.RecoBTag_cff') 
  process.patJetCharge.src = cms.InputTag("ak5JetTracksAssociatorAtVertex")
  process.NewSelectedPatJets = process.selectedPatJets.clone(src = cms.InputTag("patJetId"))
  process.rerun_JetsMC = cms.Path(
  					process.ak5PFJets*
  					process.ak5JetTracksAssociatorAtVertex*
  					process.btagging*
  					process.pileupJetIdProducer*
  					process.makePatJets*
  					process.patJetsPUID*
  					process.patJetId*
  					process.NewSelectedPatJets  					
  					)
  return process.rerun_JetsMC

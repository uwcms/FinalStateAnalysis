import FWCore.ParameterSet.Config as cms

from RecoBTag.ImpactParameter.impactParameter_cff import \
    impactParameterTagInfos, \
    trackCountingHighEffBJetTags, \
    trackCountingHighPurBJetTags, \
    jetProbabilityBJetTags, \
    jetBProbabilityBJetTags

from RecoBTag.SecondaryVertex.secondaryVertex_cff import \
    secondaryVertexTagInfos, \
    simpleSecondaryVertexHighEffBJetTags, \
    simpleSecondaryVertexHighPurBJetTags, \
    combinedSecondaryVertexBJetTags, \
    combinedSecondaryVertexMVABJetTags, \
    secondaryVertexNegativeTagInfos, \
    simpleSecondaryVertexNegativeHighEffBJetTags, \
    ghostTrackBJetTags, ghostTrackVertexTagInfos


def rerun_jets(process, isData=False):
    process.load("RecoJets.Configuration.RecoPFJets_cff")
    import PhysicsTools.PatAlgos.tools.jetTools as jettools
    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    process.load("FinalStateAnalysis.PatTools.jets.patJetPUId_cfi")
    process.pileupJetIdProducer.applyJec = cms.bool(True)

    # We need this to produce the SVs
    process.simpleSecondaryVertex = cms.ESProducer(
        "SimpleSecondaryVertexESProducer",
        use3d=cms.bool(True),
        unBoost=cms.bool(False),
        useSignificance=cms.bool(True),
        minTracks=cms.uint32(2)
    )

    # define the b-tag squences for offline reconstruction
    process.load("RecoBTag.SecondaryVertex.secondaryVertex_cff")
    process.load("RecoBTau.JetTagComputer.combinedMVA_cff")
    process.load('RecoVertex/AdaptiveVertexFinder/inclusiveVertexing_cff')
    process.load('RecoBTag/SecondaryVertex/bToCharmDecayVertexMerger_cfi')

    btag_options = {'doBTagging': True}
    btag_options['btagInfo'] = [
        'impactParameterTagInfos',
        'secondaryVertexTagInfos',
        'softMuonTagInfos'
    ]
    btag_options['btagdiscriminators'] = [
        'trackCountingHighEffBJetTags',
        'simpleSecondaryVertexHighEffBJetTags',
        'combinedSecondaryVertexMVABJetTags',
        'combinedSecondaryVertexBJetTags',
    ]

    # This is the key to produce the JES
    jec = ['L1FastJet', 'L2Relative', 'L3Absolute']
    # For Data
    if isData:
        jec.extend(['L2L3Residual'])
    pass
    # This just creates the patJet collection
    jettools.switchJetCollection(
        process,
        cms.InputTag('ak5PFJets'),
        doJTA=False,
        jetCorrLabel=('AK5PF', jec),
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
    process.patJets.tagInfoSources = cms.VInputTag(
        cms.InputTag("impactParameterTagInfos"),
        cms.InputTag("secondaryVertexTagInfos"),
        cms.InputTag("secondaryVertexNegativeTagInfos"))
    process.patJets.discriminatorSources = cms.VInputTag(
        cms.InputTag("jetBProbabilityBJetTags"),
        cms.InputTag("jetProbabilityBJetTags"),
        cms.InputTag("trackCountingHighPurBJetTags"),
        cms.InputTag("trackCountingHighEffBJetTags"),
        cms.InputTag("simpleSecondaryVertexHighEffBJetTags"),
        cms.InputTag("simpleSecondaryVertexHighPurBJetTags"),
        cms.InputTag("combinedSecondaryVertexBJetTags"),
        cms.InputTag("combinedSecondaryVertexMVABJetTags"),
        cms.InputTag("simpleInclusiveSecondaryVertexHighEffBJetTags"),
        cms.InputTag("simpleInclusiveSecondaryVertexHighPurBJetTags")
    )
    process.patJets.trackAssociationSource = cms.InputTag(
        "ak5JetTracksAssociatorAtVertex")
    process.patJets.addBTagInfo = cms.bool(True)
    process.patJets.addDiscriminators = cms.bool(True)
    process.patJets.addTagInfos = cms.bool(True)

    process.ak5JetTracksAssociatorAtVertex = cms.EDProducer(
        "JetTracksAssociatorAtVertex",
        tracks=cms.InputTag("generalTracks"),
        jets=cms.InputTag("ak5PFJets"),
        coneSize=cms.double(0.5)
    )
    process.patJetCharge.src = cms.InputTag("ak5JetTracksAssociatorAtVertex")
    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    process.NewSelectedPatJets = process.selectedPatJets.clone(
        src=cms.InputTag("patSSVJetEmbedder")
    )
    #  All the btagging bits should go to a btag.cff  to be cleaner...
    process.btagging = cms.Sequence((
        # impact parameters and IP-only algorithms
        impactParameterTagInfos *
        (trackCountingHighEffBJetTags +
         trackCountingHighPurBJetTags +
         jetProbabilityBJetTags +
         jetBProbabilityBJetTags +
         # SV tag infos depending on IP tag infos, and SV (+IP) based algos
         secondaryVertexTagInfos *
         (simpleSecondaryVertexHighEffBJetTags +
          simpleSecondaryVertexHighPurBJetTags +
          combinedSecondaryVertexBJetTags +
          combinedSecondaryVertexMVABJetTags) +
         secondaryVertexNegativeTagInfos *
         simpleSecondaryVertexNegativeHighEffBJetTags
         + ghostTrackVertexTagInfos *
         ghostTrackBJetTags)))
    process.patSSVJetEmbedder = cms.EDProducer(
        "PATSSVJetEmbedder",
        src=cms.InputTag("patJetId")
    )
    process.rerun_jets = cms.Path(
        process.inclusiveVertexing *
        process.inclusiveMergedVerticesFiltered *
        process.bToCharmDecayVertexMerged *
        process.ak5PFJets *
        process.ak5JetTracksAssociatorAtVertex *
        process.btagging *
        process.inclusiveSecondaryVertexFinderTagInfosFiltered *
        process.simpleInclusiveSecondaryVertexHighEffBJetTags *
        process.simpleInclusiveSecondaryVertexHighPurBJetTags *
        process.pileupJetIdProducer *
        process.makePatJets *
        process.patJetsPUID *
        process.patJetId *
        process.patSSVJetEmbedder *
        process.NewSelectedPatJets
    )
    return process.rerun_jets

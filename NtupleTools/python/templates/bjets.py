'''

Ntuple branch template sets for bjet objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.


'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

btagging = PSet(
	#Btagging
        objectCSVBtag     = '{object}.bDiscriminator("combinedSecondaryVertexBJetTags")',
        objectPFJBPBtag   = '{object}.bDiscriminator("pfJetBProbabilityBJetTags")',
        objectPFJPBtag    = '{object}.bDiscriminator("pfJetProbabilityBJetTags")',
        objectPFTCHPBtag  = '{object}.bDiscriminator("pfTrackCountingHighPurBJetTags")',
        objectPFTCHEBtag  = '{object}.bDiscriminator("pfTrackCountingHighEffBJetTags")',
        objectPFSSVHEBtag = '{object}.bDiscriminator("pfSimpleSecondaryVertexHighEffBJetTags")',
        objectPFSSVHPBtag = '{object}.bDiscriminator("pfSimpleSecondaryVertexHighPurBJetTags")',
        objectPFCSVBtag   = '{object}.bDiscriminator("pfCombinedSecondaryVertexV2BJetTags")',
        objectPFCISVBtag  = '{object}.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")',
        objectPFCSVSLBtag = '{object}.bDiscriminator("pfCombinedSecondaryVertexSoftLeptonBJetTags")',
        objectPFCMVABtag  = '{object}.bDiscriminator("pfCombinedMVABJetTags")',

        # sv variables in miniAOD
        objectSVMass    = '{object}.userFloat("vtxMass")',
        objectSVNTracks = '{object}.userFloat("vtxNtracks")',
        objectSV3DVal   = '{object}.userFloat("vtx3DVal")',
        objectSV3DSig   = '{object}.userFloat("vtx3DSig")',

	#Flavour
	objectJetFlavour ='{object}.partonFlavour()',
)

pujets = PSet(
        objectIDTight='{object}.userFloat("idTight")',
        objectIDTightLepVeto='{object}.userFloat("idTightLepVeto")',
        objectIDLoose='{object}.userFloat("idLoose")',
	objectPUIDFullDiscriminant='{object}.userFloat("pileupJetId:fullDiscriminant")',
)













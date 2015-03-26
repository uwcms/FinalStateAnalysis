'''

Ntuple branch template sets for bjet objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.


'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

btagging = PSet(
	#Btagging
        objectSSVHEBtag = '{object}.bDiscriminator("simpleSecondaryVertexHighEffBJetTags")',
	objectSSVHPBtag = '{object}.bDiscriminator("simpleSecondaryVertexHighPurBJetTags")',
        objectJBPBJtag  = '{object}.bDiscriminator("jetBProbabilityBJetTags")',
        objectJPBJtag   = '{object}.bDiscriminator("jetProbabilityBJetTags")',
        objectTCHPBTag  = '{object}.bDiscriminator("trackCountingHighPurBJetTags")',
        objectTCHEBtag  = '{object}.bDiscriminator("trackCountingHighEffBJetTags")',
        objectCISVBtag  = '{object}.bDiscriminator("combinedInclusiveSecondaryVertexV2BJetTags")',
        objectPFCSVBtag = '{object}.bDiscriminator("pfCombinedSecondaryVertexBJetTags")',
        objectCMVABtag  = '{object}.bDiscriminator("combinedMVABJetTags")',

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
	objectPUIDFullDiscriminant='{object}.userFloat("pileupJetId:fullDiscriminant")',
)













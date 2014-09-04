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
        objectCSVBtag ='{object}.bDiscriminator("combinedSecondaryVertexBJetTags")',
        objectJBPBJtag = '{object}.bDiscriminator("jetBProbabilityBJetTags")',
        objectJPBJtag = '{object}.bDiscriminator("jetProbabilityBJetTags")',
        objectTCHPBTag = '{object}.bDiscriminator("trackCountingHighPurBJetTags")',
        objectTCHEBtag = '{object}.bDiscriminator("trackCountingHighEffBJetTags")',
        objectCISVBtag = '{object}.bDiscriminator("combinedInclusiveSecondaryVertexBJetTags")',

        # sv variables in miniAOD
        objectSVMass = '{object}.userFloat("vtxMass")',
        objectSVNTracks = '{object}.userFloat("vtxNtracks")',
        objectSV3DVal = '{object}.userFloat("vtx3DVal")',
        objectSV3DSig = '{object}.userFloat("vtx3DSig")',

	#Custom Btagging, based on SV
        #objectSVMassBtag ='{object}.userFloat("mass_SSV")',
	#objectSVChargeBtag ='{object}.userFloat("chargeSSV")',
	#objectSVNtracksBtag ='{object}.userFloat("nTracksSSV")',
        #objectNSVsBtag ='{object}.userFloat("nTracksSSV")',
	#objectSVFlightDistanceBtag ='{object}.userFloat("flightDistance")',
        #objectSVErrFlightDistanceBtag ='{object}.userFloat("errorFlightDistance")',
        #objectSVMassDPMBtag ='{object}.userFloat("massD_SSV")',
        #objectSVMassD0Btag ='{object}.userFloat("massD0_SSV")',
        #objectSVMassUnweightedBtag ='{object}.userFloat("mass_SV_unweighted")',
        #objectSVMassWeightedBtag ='{object}.userFloat("mass_SV_weighted")',
        #objectSVMassCorrectedBtag ='{object}.userFloat("mass_SV_corrected")',

	#Custom Btagging, based on Muons-In-Jets
	#objectMuonInJetPtBtag ='{object}.userFloat("MuonInJetPt")',
        #objectMuonInJetPtRelBtag ='{object}.userFloat("MuonInJetPtRel")',

	#Flavour
	objectJetFlavour ='{object}.partonFlavour()',
)

pujets = PSet(
        objectIDTight='{object}.userFloat("idTight")',
	objectPUIDFullDiscriminant='{object}.userFloat("pileupJetId:fullDiscriminant")',
	#objectPUIDFullIDTight='{object}.userInt("fullIdTight")',
)













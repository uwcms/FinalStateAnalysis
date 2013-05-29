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

	#Custom Btagging, based on SV
        objectSVMassBtag ='{object}.userFloat("mass_SSV")',
	objectSVChargeBtag ='{object}.userFloat("chargeSSV")',
	objectSVNtracksBtag ='{object}.userFloat("nTracksSSV")',
        objectNSVsBtag ='{object}.userFloat("nTracksSSV")',
	objectSVFlightDistanceBtag ='{object}.userFloat("flightDistance")',
        objectSVErrFlightDistanceBtag ='{object}.userFloat("errorFlightDistance")',

	#Custom Btagging, based on Muons-In-Jets
	objectMuonInJetPtBtag ='{object}.userFloat("MuonInJetPt")',
        objectMuonInJetPtRelBtag ='{object}.userFloat("MuonInJetPtRel")',

	#Flavour
	objectsJetFlavour ='{object}.partonFlavour()',
)



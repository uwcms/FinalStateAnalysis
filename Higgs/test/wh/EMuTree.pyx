

# Load relevant ROOT C++ headers
cdef extern from "TObject.h":
    cdef cppclass TObject:
        pass

cdef extern from "TBranch.h":
    cdef cppclass TBranch:
        int GetEntry(long, int)
        void SetAddress(void*)

cdef extern from "TTree.h":
    cdef cppclass TTree:
        TTree()
        int GetEntry(long, int)
        long LoadTree(long)
        long GetEntries()
        TBranch* GetBranch(char*)

cdef extern from "TFile.h":
    cdef cppclass TFile:
        TFile(char*, char*, char*, int)
        TObject* Get(char*)

# Used for filtering with a string
cdef extern from "TTreeFormula.h":
    cdef cppclass TTreeFormula:
        TTreeFormula(char*, char*, TTree*)
        double EvalInstance(int, char**)

from cpython cimport PyCObject_AsVoidPtr

cdef class EMuTree:
    # Pointers to tree and current entry
    cdef TTree* tree
    cdef long ientry

    # Branches and address for all

    cdef TBranch* LT_branch
    cdef float LT_value

    cdef TBranch* Mass_branch
    cdef float Mass_value

    cdef TBranch* Pt_branch
    cdef float Pt_value

    cdef TBranch* bjetCSVVeto_branch
    cdef float bjetCSVVeto_value

    cdef TBranch* bjetVeto_branch
    cdef float bjetVeto_value

    cdef TBranch* charge_branch
    cdef float charge_value

    cdef TBranch* electronAbsEta_branch
    cdef float electronAbsEta_value

    cdef TBranch* electronCharge_branch
    cdef float electronCharge_value

    cdef TBranch* electronChargeIdLoose_branch
    cdef float electronChargeIdLoose_value

    cdef TBranch* electronChargeIdMed_branch
    cdef float electronChargeIdMed_value

    cdef TBranch* electronChargeIdTight_branch
    cdef float electronChargeIdTight_value

    cdef TBranch* electronCiCTight_branch
    cdef float electronCiCTight_value

    cdef TBranch* electronDZ_branch
    cdef float electronDZ_value

    cdef TBranch* electronEta_branch
    cdef float electronEta_value

    cdef TBranch* electronHasConversion_branch
    cdef float electronHasConversion_value

    cdef TBranch* electronIP3DS_branch
    cdef float electronIP3DS_value

    cdef TBranch* electronJetBtag_branch
    cdef float electronJetBtag_value

    cdef TBranch* electronJetPt_branch
    cdef float electronJetPt_value

    cdef TBranch* electronMITID_branch
    cdef float electronMITID_value

    cdef TBranch* electronMVAIDH2TauWP_branch
    cdef float electronMVAIDH2TauWP_value

    cdef TBranch* electronMVANonTrig_branch
    cdef float electronMVANonTrig_value

    cdef TBranch* electronMVATrig_branch
    cdef float electronMVATrig_value

    cdef TBranch* electronMass_branch
    cdef float electronMass_value

    cdef TBranch* electronMissingHits_branch
    cdef float electronMissingHits_value

    cdef TBranch* electronMtToMET_branch
    cdef float electronMtToMET_value

    cdef TBranch* electronMuOverlap_branch
    cdef float electronMuOverlap_value

    cdef TBranch* electronPhi_branch
    cdef float electronPhi_value

    cdef TBranch* electronPt_branch
    cdef float electronPt_value

    cdef TBranch* electronRelIso_branch
    cdef float electronRelIso_value

    cdef TBranch* electronRelPFIsoDB_branch
    cdef float electronRelPFIsoDB_value

    cdef TBranch* electronVZ_branch
    cdef float electronVZ_value

    cdef TBranch* electronWWID_branch
    cdef float electronWWID_value

    cdef TBranch* electron_muon_DPhi_branch
    cdef float electron_muon_DPhi_value

    cdef TBranch* electron_muon_DR_branch
    cdef float electron_muon_DR_value

    cdef TBranch* electron_muon_Mass_branch
    cdef float electron_muon_Mass_value

    cdef TBranch* electron_muon_PZeta_branch
    cdef float electron_muon_PZeta_value

    cdef TBranch* electron_muon_PZetaVis_branch
    cdef float electron_muon_PZetaVis_value

    cdef TBranch* electron_muon_Pt_branch
    cdef float electron_muon_Pt_value

    cdef TBranch* electron_muon_SS_branch
    cdef float electron_muon_SS_value

    cdef TBranch* evt_branch
    cdef int evt_value

    cdef TBranch* isdata_branch
    cdef int isdata_value

    cdef TBranch* isoMuGroup_branch
    cdef float isoMuGroup_value

    cdef TBranch* isoMuPass_branch
    cdef float isoMuPass_value

    cdef TBranch* isoMuPrescale_branch
    cdef float isoMuPrescale_value

    cdef TBranch* jetVeto20_branch
    cdef float jetVeto20_value

    cdef TBranch* jetVeto40_branch
    cdef float jetVeto40_value

    cdef TBranch* lumi_branch
    cdef int lumi_value

    cdef TBranch* metEt_branch
    cdef float metEt_value

    cdef TBranch* metPhi_branch
    cdef float metPhi_value

    cdef TBranch* metSignificance_branch
    cdef float metSignificance_value

    cdef TBranch* mu17ele8Group_branch
    cdef float mu17ele8Group_value

    cdef TBranch* mu17ele8Pass_branch
    cdef float mu17ele8Pass_value

    cdef TBranch* mu17ele8Prescale_branch
    cdef float mu17ele8Prescale_value

    cdef TBranch* mu8ele17Group_branch
    cdef float mu8ele17Group_value

    cdef TBranch* mu8ele17Pass_branch
    cdef float mu8ele17Pass_value

    cdef TBranch* mu8ele17Prescale_branch
    cdef float mu8ele17Prescale_value

    cdef TBranch* muGlbIsoVetoPt10_branch
    cdef float muGlbIsoVetoPt10_value

    cdef TBranch* muVetoPt5_branch
    cdef float muVetoPt5_value

    cdef TBranch* muonAbsEta_branch
    cdef float muonAbsEta_value

    cdef TBranch* muonCharge_branch
    cdef float muonCharge_value

    cdef TBranch* muonD0_branch
    cdef float muonD0_value

    cdef TBranch* muonDZ_branch
    cdef float muonDZ_value

    cdef TBranch* muonEta_branch
    cdef float muonEta_value

    cdef TBranch* muonGlbTrkHits_branch
    cdef float muonGlbTrkHits_value

    cdef TBranch* muonIP3DS_branch
    cdef float muonIP3DS_value

    cdef TBranch* muonIsGlobal_branch
    cdef float muonIsGlobal_value

    cdef TBranch* muonIsTracker_branch
    cdef float muonIsTracker_value

    cdef TBranch* muonJetBtag_branch
    cdef float muonJetBtag_value

    cdef TBranch* muonJetPt_branch
    cdef float muonJetPt_value

    cdef TBranch* muonMass_branch
    cdef float muonMass_value

    cdef TBranch* muonMtToMET_branch
    cdef float muonMtToMET_value

    cdef TBranch* muonNormTrkChi2_branch
    cdef float muonNormTrkChi2_value

    cdef TBranch* muonPFIDTight_branch
    cdef float muonPFIDTight_value

    cdef TBranch* muonPhi_branch
    cdef float muonPhi_value

    cdef TBranch* muonPixHits_branch
    cdef float muonPixHits_value

    cdef TBranch* muonPt_branch
    cdef float muonPt_value

    cdef TBranch* muonPtUncorr_branch
    cdef float muonPtUncorr_value

    cdef TBranch* muonRelPFIsoDB_branch
    cdef float muonRelPFIsoDB_value

    cdef TBranch* muonVBTFID_branch
    cdef float muonVBTFID_value

    cdef TBranch* muonVZ_branch
    cdef float muonVZ_value

    cdef TBranch* muonWWID_branch
    cdef float muonWWID_value

    cdef TBranch* nTruePU_branch
    cdef float nTruePU_value

    cdef TBranch* nvtx_branch
    cdef float nvtx_value

    cdef TBranch* puWeightData2011A_branch
    cdef float puWeightData2011A_value

    cdef TBranch* puWeightData2011AB_branch
    cdef float puWeightData2011AB_value

    cdef TBranch* puWeightData2011B_branch
    cdef float puWeightData2011B_value

    cdef TBranch* rho_branch
    cdef float rho_value

    cdef TBranch* run_branch
    cdef int run_value

    cdef TBranch* singleMuGroup_branch
    cdef float singleMuGroup_value

    cdef TBranch* singleMuPass_branch
    cdef float singleMuPass_value

    cdef TBranch* singleMuPrescale_branch
    cdef float singleMuPrescale_value

    cdef TBranch* tauVetoPt20_branch
    cdef float tauVetoPt20_value

    cdef TBranch* idx_branch
    cdef int idx_value


    def __cinit__(self, ttree):
        # Constructor from a ROOT.TTree
        from ROOT import AsCObject
        self.tree = <TTree*>PyCObject_AsVoidPtr(AsCObject(ttree))
        self.ientry = 0
        # Now set all the branch address

        self.LT_branch = self.tree.GetBranch("LT")
        self.LT_branch.SetAddress(<void*>&self.LT_value)

        self.Mass_branch = self.tree.GetBranch("Mass")
        self.Mass_branch.SetAddress(<void*>&self.Mass_value)

        self.Pt_branch = self.tree.GetBranch("Pt")
        self.Pt_branch.SetAddress(<void*>&self.Pt_value)

        self.bjetCSVVeto_branch = self.tree.GetBranch("bjetCSVVeto")
        self.bjetCSVVeto_branch.SetAddress(<void*>&self.bjetCSVVeto_value)

        self.bjetVeto_branch = self.tree.GetBranch("bjetVeto")
        self.bjetVeto_branch.SetAddress(<void*>&self.bjetVeto_value)

        self.charge_branch = self.tree.GetBranch("charge")
        self.charge_branch.SetAddress(<void*>&self.charge_value)

        self.electronAbsEta_branch = self.tree.GetBranch("electronAbsEta")
        self.electronAbsEta_branch.SetAddress(<void*>&self.electronAbsEta_value)

        self.electronCharge_branch = self.tree.GetBranch("electronCharge")
        self.electronCharge_branch.SetAddress(<void*>&self.electronCharge_value)

        self.electronChargeIdLoose_branch = self.tree.GetBranch("electronChargeIdLoose")
        self.electronChargeIdLoose_branch.SetAddress(<void*>&self.electronChargeIdLoose_value)

        self.electronChargeIdMed_branch = self.tree.GetBranch("electronChargeIdMed")
        self.electronChargeIdMed_branch.SetAddress(<void*>&self.electronChargeIdMed_value)

        self.electronChargeIdTight_branch = self.tree.GetBranch("electronChargeIdTight")
        self.electronChargeIdTight_branch.SetAddress(<void*>&self.electronChargeIdTight_value)

        self.electronCiCTight_branch = self.tree.GetBranch("electronCiCTight")
        self.electronCiCTight_branch.SetAddress(<void*>&self.electronCiCTight_value)

        self.electronDZ_branch = self.tree.GetBranch("electronDZ")
        self.electronDZ_branch.SetAddress(<void*>&self.electronDZ_value)

        self.electronEta_branch = self.tree.GetBranch("electronEta")
        self.electronEta_branch.SetAddress(<void*>&self.electronEta_value)

        self.electronHasConversion_branch = self.tree.GetBranch("electronHasConversion")
        self.electronHasConversion_branch.SetAddress(<void*>&self.electronHasConversion_value)

        self.electronIP3DS_branch = self.tree.GetBranch("electronIP3DS")
        self.electronIP3DS_branch.SetAddress(<void*>&self.electronIP3DS_value)

        self.electronJetBtag_branch = self.tree.GetBranch("electronJetBtag")
        self.electronJetBtag_branch.SetAddress(<void*>&self.electronJetBtag_value)

        self.electronJetPt_branch = self.tree.GetBranch("electronJetPt")
        self.electronJetPt_branch.SetAddress(<void*>&self.electronJetPt_value)

        self.electronMITID_branch = self.tree.GetBranch("electronMITID")
        self.electronMITID_branch.SetAddress(<void*>&self.electronMITID_value)

        self.electronMVAIDH2TauWP_branch = self.tree.GetBranch("electronMVAIDH2TauWP")
        self.electronMVAIDH2TauWP_branch.SetAddress(<void*>&self.electronMVAIDH2TauWP_value)

        self.electronMVANonTrig_branch = self.tree.GetBranch("electronMVANonTrig")
        self.electronMVANonTrig_branch.SetAddress(<void*>&self.electronMVANonTrig_value)

        self.electronMVATrig_branch = self.tree.GetBranch("electronMVATrig")
        self.electronMVATrig_branch.SetAddress(<void*>&self.electronMVATrig_value)

        self.electronMass_branch = self.tree.GetBranch("electronMass")
        self.electronMass_branch.SetAddress(<void*>&self.electronMass_value)

        self.electronMissingHits_branch = self.tree.GetBranch("electronMissingHits")
        self.electronMissingHits_branch.SetAddress(<void*>&self.electronMissingHits_value)

        self.electronMtToMET_branch = self.tree.GetBranch("electronMtToMET")
        self.electronMtToMET_branch.SetAddress(<void*>&self.electronMtToMET_value)

        self.electronMuOverlap_branch = self.tree.GetBranch("electronMuOverlap")
        self.electronMuOverlap_branch.SetAddress(<void*>&self.electronMuOverlap_value)

        self.electronPhi_branch = self.tree.GetBranch("electronPhi")
        self.electronPhi_branch.SetAddress(<void*>&self.electronPhi_value)

        self.electronPt_branch = self.tree.GetBranch("electronPt")
        self.electronPt_branch.SetAddress(<void*>&self.electronPt_value)

        self.electronRelIso_branch = self.tree.GetBranch("electronRelIso")
        self.electronRelIso_branch.SetAddress(<void*>&self.electronRelIso_value)

        self.electronRelPFIsoDB_branch = self.tree.GetBranch("electronRelPFIsoDB")
        self.electronRelPFIsoDB_branch.SetAddress(<void*>&self.electronRelPFIsoDB_value)

        self.electronVZ_branch = self.tree.GetBranch("electronVZ")
        self.electronVZ_branch.SetAddress(<void*>&self.electronVZ_value)

        self.electronWWID_branch = self.tree.GetBranch("electronWWID")
        self.electronWWID_branch.SetAddress(<void*>&self.electronWWID_value)

        self.electron_muon_DPhi_branch = self.tree.GetBranch("electron_muon_DPhi")
        self.electron_muon_DPhi_branch.SetAddress(<void*>&self.electron_muon_DPhi_value)

        self.electron_muon_DR_branch = self.tree.GetBranch("electron_muon_DR")
        self.electron_muon_DR_branch.SetAddress(<void*>&self.electron_muon_DR_value)

        self.electron_muon_Mass_branch = self.tree.GetBranch("electron_muon_Mass")
        self.electron_muon_Mass_branch.SetAddress(<void*>&self.electron_muon_Mass_value)

        self.electron_muon_PZeta_branch = self.tree.GetBranch("electron_muon_PZeta")
        self.electron_muon_PZeta_branch.SetAddress(<void*>&self.electron_muon_PZeta_value)

        self.electron_muon_PZetaVis_branch = self.tree.GetBranch("electron_muon_PZetaVis")
        self.electron_muon_PZetaVis_branch.SetAddress(<void*>&self.electron_muon_PZetaVis_value)

        self.electron_muon_Pt_branch = self.tree.GetBranch("electron_muon_Pt")
        self.electron_muon_Pt_branch.SetAddress(<void*>&self.electron_muon_Pt_value)

        self.electron_muon_SS_branch = self.tree.GetBranch("electron_muon_SS")
        self.electron_muon_SS_branch.SetAddress(<void*>&self.electron_muon_SS_value)

        self.evt_branch = self.tree.GetBranch("evt")
        self.evt_branch.SetAddress(<void*>&self.evt_value)

        self.isdata_branch = self.tree.GetBranch("isdata")
        self.isdata_branch.SetAddress(<void*>&self.isdata_value)

        self.isoMuGroup_branch = self.tree.GetBranch("isoMuGroup")
        self.isoMuGroup_branch.SetAddress(<void*>&self.isoMuGroup_value)

        self.isoMuPass_branch = self.tree.GetBranch("isoMuPass")
        self.isoMuPass_branch.SetAddress(<void*>&self.isoMuPass_value)

        self.isoMuPrescale_branch = self.tree.GetBranch("isoMuPrescale")
        self.isoMuPrescale_branch.SetAddress(<void*>&self.isoMuPrescale_value)

        self.jetVeto20_branch = self.tree.GetBranch("jetVeto20")
        self.jetVeto20_branch.SetAddress(<void*>&self.jetVeto20_value)

        self.jetVeto40_branch = self.tree.GetBranch("jetVeto40")
        self.jetVeto40_branch.SetAddress(<void*>&self.jetVeto40_value)

        self.lumi_branch = self.tree.GetBranch("lumi")
        self.lumi_branch.SetAddress(<void*>&self.lumi_value)

        self.metEt_branch = self.tree.GetBranch("metEt")
        self.metEt_branch.SetAddress(<void*>&self.metEt_value)

        self.metPhi_branch = self.tree.GetBranch("metPhi")
        self.metPhi_branch.SetAddress(<void*>&self.metPhi_value)

        self.metSignificance_branch = self.tree.GetBranch("metSignificance")
        self.metSignificance_branch.SetAddress(<void*>&self.metSignificance_value)

        self.mu17ele8Group_branch = self.tree.GetBranch("mu17ele8Group")
        self.mu17ele8Group_branch.SetAddress(<void*>&self.mu17ele8Group_value)

        self.mu17ele8Pass_branch = self.tree.GetBranch("mu17ele8Pass")
        self.mu17ele8Pass_branch.SetAddress(<void*>&self.mu17ele8Pass_value)

        self.mu17ele8Prescale_branch = self.tree.GetBranch("mu17ele8Prescale")
        self.mu17ele8Prescale_branch.SetAddress(<void*>&self.mu17ele8Prescale_value)

        self.mu8ele17Group_branch = self.tree.GetBranch("mu8ele17Group")
        self.mu8ele17Group_branch.SetAddress(<void*>&self.mu8ele17Group_value)

        self.mu8ele17Pass_branch = self.tree.GetBranch("mu8ele17Pass")
        self.mu8ele17Pass_branch.SetAddress(<void*>&self.mu8ele17Pass_value)

        self.mu8ele17Prescale_branch = self.tree.GetBranch("mu8ele17Prescale")
        self.mu8ele17Prescale_branch.SetAddress(<void*>&self.mu8ele17Prescale_value)

        self.muGlbIsoVetoPt10_branch = self.tree.GetBranch("muGlbIsoVetoPt10")
        self.muGlbIsoVetoPt10_branch.SetAddress(<void*>&self.muGlbIsoVetoPt10_value)

        self.muVetoPt5_branch = self.tree.GetBranch("muVetoPt5")
        self.muVetoPt5_branch.SetAddress(<void*>&self.muVetoPt5_value)

        self.muonAbsEta_branch = self.tree.GetBranch("muonAbsEta")
        self.muonAbsEta_branch.SetAddress(<void*>&self.muonAbsEta_value)

        self.muonCharge_branch = self.tree.GetBranch("muonCharge")
        self.muonCharge_branch.SetAddress(<void*>&self.muonCharge_value)

        self.muonD0_branch = self.tree.GetBranch("muonD0")
        self.muonD0_branch.SetAddress(<void*>&self.muonD0_value)

        self.muonDZ_branch = self.tree.GetBranch("muonDZ")
        self.muonDZ_branch.SetAddress(<void*>&self.muonDZ_value)

        self.muonEta_branch = self.tree.GetBranch("muonEta")
        self.muonEta_branch.SetAddress(<void*>&self.muonEta_value)

        self.muonGlbTrkHits_branch = self.tree.GetBranch("muonGlbTrkHits")
        self.muonGlbTrkHits_branch.SetAddress(<void*>&self.muonGlbTrkHits_value)

        self.muonIP3DS_branch = self.tree.GetBranch("muonIP3DS")
        self.muonIP3DS_branch.SetAddress(<void*>&self.muonIP3DS_value)

        self.muonIsGlobal_branch = self.tree.GetBranch("muonIsGlobal")
        self.muonIsGlobal_branch.SetAddress(<void*>&self.muonIsGlobal_value)

        self.muonIsTracker_branch = self.tree.GetBranch("muonIsTracker")
        self.muonIsTracker_branch.SetAddress(<void*>&self.muonIsTracker_value)

        self.muonJetBtag_branch = self.tree.GetBranch("muonJetBtag")
        self.muonJetBtag_branch.SetAddress(<void*>&self.muonJetBtag_value)

        self.muonJetPt_branch = self.tree.GetBranch("muonJetPt")
        self.muonJetPt_branch.SetAddress(<void*>&self.muonJetPt_value)

        self.muonMass_branch = self.tree.GetBranch("muonMass")
        self.muonMass_branch.SetAddress(<void*>&self.muonMass_value)

        self.muonMtToMET_branch = self.tree.GetBranch("muonMtToMET")
        self.muonMtToMET_branch.SetAddress(<void*>&self.muonMtToMET_value)

        self.muonNormTrkChi2_branch = self.tree.GetBranch("muonNormTrkChi2")
        self.muonNormTrkChi2_branch.SetAddress(<void*>&self.muonNormTrkChi2_value)

        self.muonPFIDTight_branch = self.tree.GetBranch("muonPFIDTight")
        self.muonPFIDTight_branch.SetAddress(<void*>&self.muonPFIDTight_value)

        self.muonPhi_branch = self.tree.GetBranch("muonPhi")
        self.muonPhi_branch.SetAddress(<void*>&self.muonPhi_value)

        self.muonPixHits_branch = self.tree.GetBranch("muonPixHits")
        self.muonPixHits_branch.SetAddress(<void*>&self.muonPixHits_value)

        self.muonPt_branch = self.tree.GetBranch("muonPt")
        self.muonPt_branch.SetAddress(<void*>&self.muonPt_value)

        self.muonPtUncorr_branch = self.tree.GetBranch("muonPtUncorr")
        self.muonPtUncorr_branch.SetAddress(<void*>&self.muonPtUncorr_value)

        self.muonRelPFIsoDB_branch = self.tree.GetBranch("muonRelPFIsoDB")
        self.muonRelPFIsoDB_branch.SetAddress(<void*>&self.muonRelPFIsoDB_value)

        self.muonVBTFID_branch = self.tree.GetBranch("muonVBTFID")
        self.muonVBTFID_branch.SetAddress(<void*>&self.muonVBTFID_value)

        self.muonVZ_branch = self.tree.GetBranch("muonVZ")
        self.muonVZ_branch.SetAddress(<void*>&self.muonVZ_value)

        self.muonWWID_branch = self.tree.GetBranch("muonWWID")
        self.muonWWID_branch.SetAddress(<void*>&self.muonWWID_value)

        self.nTruePU_branch = self.tree.GetBranch("nTruePU")
        self.nTruePU_branch.SetAddress(<void*>&self.nTruePU_value)

        self.nvtx_branch = self.tree.GetBranch("nvtx")
        self.nvtx_branch.SetAddress(<void*>&self.nvtx_value)

        self.puWeightData2011A_branch = self.tree.GetBranch("puWeightData2011A")
        self.puWeightData2011A_branch.SetAddress(<void*>&self.puWeightData2011A_value)

        self.puWeightData2011AB_branch = self.tree.GetBranch("puWeightData2011AB")
        self.puWeightData2011AB_branch.SetAddress(<void*>&self.puWeightData2011AB_value)

        self.puWeightData2011B_branch = self.tree.GetBranch("puWeightData2011B")
        self.puWeightData2011B_branch.SetAddress(<void*>&self.puWeightData2011B_value)

        self.rho_branch = self.tree.GetBranch("rho")
        self.rho_branch.SetAddress(<void*>&self.rho_value)

        self.run_branch = self.tree.GetBranch("run")
        self.run_branch.SetAddress(<void*>&self.run_value)

        self.singleMuGroup_branch = self.tree.GetBranch("singleMuGroup")
        self.singleMuGroup_branch.SetAddress(<void*>&self.singleMuGroup_value)

        self.singleMuPass_branch = self.tree.GetBranch("singleMuPass")
        self.singleMuPass_branch.SetAddress(<void*>&self.singleMuPass_value)

        self.singleMuPrescale_branch = self.tree.GetBranch("singleMuPrescale")
        self.singleMuPrescale_branch.SetAddress(<void*>&self.singleMuPrescale_value)

        self.tauVetoPt20_branch = self.tree.GetBranch("tauVetoPt20")
        self.tauVetoPt20_branch.SetAddress(<void*>&self.tauVetoPt20_value)

        self.idx_branch = self.tree.GetBranch("idx")
        self.idx_branch.SetAddress(<void*>&self.idx_value)


    # Iterating over the tree
    def __iter__(self):
        self.ientry = 0
        while self.ientry < self.tree.GetEntries():
            yield self
            self.ientry += 1

    # Iterate over rows which pass the filter
    def where(self, filter):
        cdef TTreeFormula* formula = new TTreeFormula(
            "cyiter", filter, self.tree)
        self.ientry = 0
        while self.ientry < self.tree.GetEntries():
            self.tree.LoadTree(self.ientry)
            if formula.EvalInstance(0, NULL):
                yield self
            self.ientry += 1
        del formula

    # Getting/setting the Tree entry number
    property entry:
        def __get__(self):
            return self.ientry
        def __set__(self, int i):
            self.ientry = i

    # Access to the current branch values

    property LT:
        def __get__(self):
            self.LT_branch.GetEntry(self.ientry, 0)
            return self.LT_value

    property Mass:
        def __get__(self):
            self.Mass_branch.GetEntry(self.ientry, 0)
            return self.Mass_value

    property Pt:
        def __get__(self):
            self.Pt_branch.GetEntry(self.ientry, 0)
            return self.Pt_value

    property bjetCSVVeto:
        def __get__(self):
            self.bjetCSVVeto_branch.GetEntry(self.ientry, 0)
            return self.bjetCSVVeto_value

    property bjetVeto:
        def __get__(self):
            self.bjetVeto_branch.GetEntry(self.ientry, 0)
            return self.bjetVeto_value

    property charge:
        def __get__(self):
            self.charge_branch.GetEntry(self.ientry, 0)
            return self.charge_value

    property electronAbsEta:
        def __get__(self):
            self.electronAbsEta_branch.GetEntry(self.ientry, 0)
            return self.electronAbsEta_value

    property electronCharge:
        def __get__(self):
            self.electronCharge_branch.GetEntry(self.ientry, 0)
            return self.electronCharge_value

    property electronChargeIdLoose:
        def __get__(self):
            self.electronChargeIdLoose_branch.GetEntry(self.ientry, 0)
            return self.electronChargeIdLoose_value

    property electronChargeIdMed:
        def __get__(self):
            self.electronChargeIdMed_branch.GetEntry(self.ientry, 0)
            return self.electronChargeIdMed_value

    property electronChargeIdTight:
        def __get__(self):
            self.electronChargeIdTight_branch.GetEntry(self.ientry, 0)
            return self.electronChargeIdTight_value

    property electronCiCTight:
        def __get__(self):
            self.electronCiCTight_branch.GetEntry(self.ientry, 0)
            return self.electronCiCTight_value

    property electronDZ:
        def __get__(self):
            self.electronDZ_branch.GetEntry(self.ientry, 0)
            return self.electronDZ_value

    property electronEta:
        def __get__(self):
            self.electronEta_branch.GetEntry(self.ientry, 0)
            return self.electronEta_value

    property electronHasConversion:
        def __get__(self):
            self.electronHasConversion_branch.GetEntry(self.ientry, 0)
            return self.electronHasConversion_value

    property electronIP3DS:
        def __get__(self):
            self.electronIP3DS_branch.GetEntry(self.ientry, 0)
            return self.electronIP3DS_value

    property electronJetBtag:
        def __get__(self):
            self.electronJetBtag_branch.GetEntry(self.ientry, 0)
            return self.electronJetBtag_value

    property electronJetPt:
        def __get__(self):
            self.electronJetPt_branch.GetEntry(self.ientry, 0)
            return self.electronJetPt_value

    property electronMITID:
        def __get__(self):
            self.electronMITID_branch.GetEntry(self.ientry, 0)
            return self.electronMITID_value

    property electronMVAIDH2TauWP:
        def __get__(self):
            self.electronMVAIDH2TauWP_branch.GetEntry(self.ientry, 0)
            return self.electronMVAIDH2TauWP_value

    property electronMVANonTrig:
        def __get__(self):
            self.electronMVANonTrig_branch.GetEntry(self.ientry, 0)
            return self.electronMVANonTrig_value

    property electronMVATrig:
        def __get__(self):
            self.electronMVATrig_branch.GetEntry(self.ientry, 0)
            return self.electronMVATrig_value

    property electronMass:
        def __get__(self):
            self.electronMass_branch.GetEntry(self.ientry, 0)
            return self.electronMass_value

    property electronMissingHits:
        def __get__(self):
            self.electronMissingHits_branch.GetEntry(self.ientry, 0)
            return self.electronMissingHits_value

    property electronMtToMET:
        def __get__(self):
            self.electronMtToMET_branch.GetEntry(self.ientry, 0)
            return self.electronMtToMET_value

    property electronMuOverlap:
        def __get__(self):
            self.electronMuOverlap_branch.GetEntry(self.ientry, 0)
            return self.electronMuOverlap_value

    property electronPhi:
        def __get__(self):
            self.electronPhi_branch.GetEntry(self.ientry, 0)
            return self.electronPhi_value

    property electronPt:
        def __get__(self):
            self.electronPt_branch.GetEntry(self.ientry, 0)
            return self.electronPt_value

    property electronRelIso:
        def __get__(self):
            self.electronRelIso_branch.GetEntry(self.ientry, 0)
            return self.electronRelIso_value

    property electronRelPFIsoDB:
        def __get__(self):
            self.electronRelPFIsoDB_branch.GetEntry(self.ientry, 0)
            return self.electronRelPFIsoDB_value

    property electronVZ:
        def __get__(self):
            self.electronVZ_branch.GetEntry(self.ientry, 0)
            return self.electronVZ_value

    property electronWWID:
        def __get__(self):
            self.electronWWID_branch.GetEntry(self.ientry, 0)
            return self.electronWWID_value

    property electron_muon_DPhi:
        def __get__(self):
            self.electron_muon_DPhi_branch.GetEntry(self.ientry, 0)
            return self.electron_muon_DPhi_value

    property electron_muon_DR:
        def __get__(self):
            self.electron_muon_DR_branch.GetEntry(self.ientry, 0)
            return self.electron_muon_DR_value

    property electron_muon_Mass:
        def __get__(self):
            self.electron_muon_Mass_branch.GetEntry(self.ientry, 0)
            return self.electron_muon_Mass_value

    property electron_muon_PZeta:
        def __get__(self):
            self.electron_muon_PZeta_branch.GetEntry(self.ientry, 0)
            return self.electron_muon_PZeta_value

    property electron_muon_PZetaVis:
        def __get__(self):
            self.electron_muon_PZetaVis_branch.GetEntry(self.ientry, 0)
            return self.electron_muon_PZetaVis_value

    property electron_muon_Pt:
        def __get__(self):
            self.electron_muon_Pt_branch.GetEntry(self.ientry, 0)
            return self.electron_muon_Pt_value

    property electron_muon_SS:
        def __get__(self):
            self.electron_muon_SS_branch.GetEntry(self.ientry, 0)
            return self.electron_muon_SS_value

    property evt:
        def __get__(self):
            self.evt_branch.GetEntry(self.ientry, 0)
            return self.evt_value

    property isdata:
        def __get__(self):
            self.isdata_branch.GetEntry(self.ientry, 0)
            return self.isdata_value

    property isoMuGroup:
        def __get__(self):
            self.isoMuGroup_branch.GetEntry(self.ientry, 0)
            return self.isoMuGroup_value

    property isoMuPass:
        def __get__(self):
            self.isoMuPass_branch.GetEntry(self.ientry, 0)
            return self.isoMuPass_value

    property isoMuPrescale:
        def __get__(self):
            self.isoMuPrescale_branch.GetEntry(self.ientry, 0)
            return self.isoMuPrescale_value

    property jetVeto20:
        def __get__(self):
            self.jetVeto20_branch.GetEntry(self.ientry, 0)
            return self.jetVeto20_value

    property jetVeto40:
        def __get__(self):
            self.jetVeto40_branch.GetEntry(self.ientry, 0)
            return self.jetVeto40_value

    property lumi:
        def __get__(self):
            self.lumi_branch.GetEntry(self.ientry, 0)
            return self.lumi_value

    property metEt:
        def __get__(self):
            self.metEt_branch.GetEntry(self.ientry, 0)
            return self.metEt_value

    property metPhi:
        def __get__(self):
            self.metPhi_branch.GetEntry(self.ientry, 0)
            return self.metPhi_value

    property metSignificance:
        def __get__(self):
            self.metSignificance_branch.GetEntry(self.ientry, 0)
            return self.metSignificance_value

    property mu17ele8Group:
        def __get__(self):
            self.mu17ele8Group_branch.GetEntry(self.ientry, 0)
            return self.mu17ele8Group_value

    property mu17ele8Pass:
        def __get__(self):
            self.mu17ele8Pass_branch.GetEntry(self.ientry, 0)
            return self.mu17ele8Pass_value

    property mu17ele8Prescale:
        def __get__(self):
            self.mu17ele8Prescale_branch.GetEntry(self.ientry, 0)
            return self.mu17ele8Prescale_value

    property mu8ele17Group:
        def __get__(self):
            self.mu8ele17Group_branch.GetEntry(self.ientry, 0)
            return self.mu8ele17Group_value

    property mu8ele17Pass:
        def __get__(self):
            self.mu8ele17Pass_branch.GetEntry(self.ientry, 0)
            return self.mu8ele17Pass_value

    property mu8ele17Prescale:
        def __get__(self):
            self.mu8ele17Prescale_branch.GetEntry(self.ientry, 0)
            return self.mu8ele17Prescale_value

    property muGlbIsoVetoPt10:
        def __get__(self):
            self.muGlbIsoVetoPt10_branch.GetEntry(self.ientry, 0)
            return self.muGlbIsoVetoPt10_value

    property muVetoPt5:
        def __get__(self):
            self.muVetoPt5_branch.GetEntry(self.ientry, 0)
            return self.muVetoPt5_value

    property muonAbsEta:
        def __get__(self):
            self.muonAbsEta_branch.GetEntry(self.ientry, 0)
            return self.muonAbsEta_value

    property muonCharge:
        def __get__(self):
            self.muonCharge_branch.GetEntry(self.ientry, 0)
            return self.muonCharge_value

    property muonD0:
        def __get__(self):
            self.muonD0_branch.GetEntry(self.ientry, 0)
            return self.muonD0_value

    property muonDZ:
        def __get__(self):
            self.muonDZ_branch.GetEntry(self.ientry, 0)
            return self.muonDZ_value

    property muonEta:
        def __get__(self):
            self.muonEta_branch.GetEntry(self.ientry, 0)
            return self.muonEta_value

    property muonGlbTrkHits:
        def __get__(self):
            self.muonGlbTrkHits_branch.GetEntry(self.ientry, 0)
            return self.muonGlbTrkHits_value

    property muonIP3DS:
        def __get__(self):
            self.muonIP3DS_branch.GetEntry(self.ientry, 0)
            return self.muonIP3DS_value

    property muonIsGlobal:
        def __get__(self):
            self.muonIsGlobal_branch.GetEntry(self.ientry, 0)
            return self.muonIsGlobal_value

    property muonIsTracker:
        def __get__(self):
            self.muonIsTracker_branch.GetEntry(self.ientry, 0)
            return self.muonIsTracker_value

    property muonJetBtag:
        def __get__(self):
            self.muonJetBtag_branch.GetEntry(self.ientry, 0)
            return self.muonJetBtag_value

    property muonJetPt:
        def __get__(self):
            self.muonJetPt_branch.GetEntry(self.ientry, 0)
            return self.muonJetPt_value

    property muonMass:
        def __get__(self):
            self.muonMass_branch.GetEntry(self.ientry, 0)
            return self.muonMass_value

    property muonMtToMET:
        def __get__(self):
            self.muonMtToMET_branch.GetEntry(self.ientry, 0)
            return self.muonMtToMET_value

    property muonNormTrkChi2:
        def __get__(self):
            self.muonNormTrkChi2_branch.GetEntry(self.ientry, 0)
            return self.muonNormTrkChi2_value

    property muonPFIDTight:
        def __get__(self):
            self.muonPFIDTight_branch.GetEntry(self.ientry, 0)
            return self.muonPFIDTight_value

    property muonPhi:
        def __get__(self):
            self.muonPhi_branch.GetEntry(self.ientry, 0)
            return self.muonPhi_value

    property muonPixHits:
        def __get__(self):
            self.muonPixHits_branch.GetEntry(self.ientry, 0)
            return self.muonPixHits_value

    property muonPt:
        def __get__(self):
            self.muonPt_branch.GetEntry(self.ientry, 0)
            return self.muonPt_value

    property muonPtUncorr:
        def __get__(self):
            self.muonPtUncorr_branch.GetEntry(self.ientry, 0)
            return self.muonPtUncorr_value

    property muonRelPFIsoDB:
        def __get__(self):
            self.muonRelPFIsoDB_branch.GetEntry(self.ientry, 0)
            return self.muonRelPFIsoDB_value

    property muonVBTFID:
        def __get__(self):
            self.muonVBTFID_branch.GetEntry(self.ientry, 0)
            return self.muonVBTFID_value

    property muonVZ:
        def __get__(self):
            self.muonVZ_branch.GetEntry(self.ientry, 0)
            return self.muonVZ_value

    property muonWWID:
        def __get__(self):
            self.muonWWID_branch.GetEntry(self.ientry, 0)
            return self.muonWWID_value

    property nTruePU:
        def __get__(self):
            self.nTruePU_branch.GetEntry(self.ientry, 0)
            return self.nTruePU_value

    property nvtx:
        def __get__(self):
            self.nvtx_branch.GetEntry(self.ientry, 0)
            return self.nvtx_value

    property puWeightData2011A:
        def __get__(self):
            self.puWeightData2011A_branch.GetEntry(self.ientry, 0)
            return self.puWeightData2011A_value

    property puWeightData2011AB:
        def __get__(self):
            self.puWeightData2011AB_branch.GetEntry(self.ientry, 0)
            return self.puWeightData2011AB_value

    property puWeightData2011B:
        def __get__(self):
            self.puWeightData2011B_branch.GetEntry(self.ientry, 0)
            return self.puWeightData2011B_value

    property rho:
        def __get__(self):
            self.rho_branch.GetEntry(self.ientry, 0)
            return self.rho_value

    property run:
        def __get__(self):
            self.run_branch.GetEntry(self.ientry, 0)
            return self.run_value

    property singleMuGroup:
        def __get__(self):
            self.singleMuGroup_branch.GetEntry(self.ientry, 0)
            return self.singleMuGroup_value

    property singleMuPass:
        def __get__(self):
            self.singleMuPass_branch.GetEntry(self.ientry, 0)
            return self.singleMuPass_value

    property singleMuPrescale:
        def __get__(self):
            self.singleMuPrescale_branch.GetEntry(self.ientry, 0)
            return self.singleMuPrescale_value

    property tauVetoPt20:
        def __get__(self):
            self.tauVetoPt20_branch.GetEntry(self.ientry, 0)
            return self.tauVetoPt20_value

    property idx:
        def __get__(self):
            self.idx_branch.GetEntry(self.ientry, 0)
            return self.idx_value



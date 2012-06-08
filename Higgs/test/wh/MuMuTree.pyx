

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

cdef class MuMuTree:
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

    cdef TBranch* doubleMuGroup_branch
    cdef float doubleMuGroup_value

    cdef TBranch* doubleMuPass_branch
    cdef float doubleMuPass_value

    cdef TBranch* doubleMuPrescale_branch
    cdef float doubleMuPrescale_value

    cdef TBranch* doubleMuTrkGroup_branch
    cdef float doubleMuTrkGroup_value

    cdef TBranch* doubleMuTrkPass_branch
    cdef float doubleMuTrkPass_value

    cdef TBranch* doubleMuTrkPrescale_branch
    cdef float doubleMuTrkPrescale_value

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

    cdef TBranch* muGlbIsoVetoPt10_branch
    cdef float muGlbIsoVetoPt10_value

    cdef TBranch* muVetoPt5_branch
    cdef float muVetoPt5_value

    cdef TBranch* muon1AbsEta_branch
    cdef float muon1AbsEta_value

    cdef TBranch* muon1Charge_branch
    cdef float muon1Charge_value

    cdef TBranch* muon1D0_branch
    cdef float muon1D0_value

    cdef TBranch* muon1DZ_branch
    cdef float muon1DZ_value

    cdef TBranch* muon1Eta_branch
    cdef float muon1Eta_value

    cdef TBranch* muon1GlbTrkHits_branch
    cdef float muon1GlbTrkHits_value

    cdef TBranch* muon1IP3DS_branch
    cdef float muon1IP3DS_value

    cdef TBranch* muon1IsGlobal_branch
    cdef float muon1IsGlobal_value

    cdef TBranch* muon1IsTracker_branch
    cdef float muon1IsTracker_value

    cdef TBranch* muon1JetBtag_branch
    cdef float muon1JetBtag_value

    cdef TBranch* muon1JetPt_branch
    cdef float muon1JetPt_value

    cdef TBranch* muon1Mass_branch
    cdef float muon1Mass_value

    cdef TBranch* muon1MtToMET_branch
    cdef float muon1MtToMET_value

    cdef TBranch* muon1NormTrkChi2_branch
    cdef float muon1NormTrkChi2_value

    cdef TBranch* muon1PFIDTight_branch
    cdef float muon1PFIDTight_value

    cdef TBranch* muon1Phi_branch
    cdef float muon1Phi_value

    cdef TBranch* muon1PixHits_branch
    cdef float muon1PixHits_value

    cdef TBranch* muon1Pt_branch
    cdef float muon1Pt_value

    cdef TBranch* muon1PtUncorr_branch
    cdef float muon1PtUncorr_value

    cdef TBranch* muon1RelPFIsoDB_branch
    cdef float muon1RelPFIsoDB_value

    cdef TBranch* muon1VBTFID_branch
    cdef float muon1VBTFID_value

    cdef TBranch* muon1VZ_branch
    cdef float muon1VZ_value

    cdef TBranch* muon1WWID_branch
    cdef float muon1WWID_value

    cdef TBranch* muon1_muon2_DPhi_branch
    cdef float muon1_muon2_DPhi_value

    cdef TBranch* muon1_muon2_DR_branch
    cdef float muon1_muon2_DR_value

    cdef TBranch* muon1_muon2_Mass_branch
    cdef float muon1_muon2_Mass_value

    cdef TBranch* muon1_muon2_PZeta_branch
    cdef float muon1_muon2_PZeta_value

    cdef TBranch* muon1_muon2_PZetaVis_branch
    cdef float muon1_muon2_PZetaVis_value

    cdef TBranch* muon1_muon2_Pt_branch
    cdef float muon1_muon2_Pt_value

    cdef TBranch* muon1_muon2_SS_branch
    cdef float muon1_muon2_SS_value

    cdef TBranch* muon2AbsEta_branch
    cdef float muon2AbsEta_value

    cdef TBranch* muon2Charge_branch
    cdef float muon2Charge_value

    cdef TBranch* muon2D0_branch
    cdef float muon2D0_value

    cdef TBranch* muon2DZ_branch
    cdef float muon2DZ_value

    cdef TBranch* muon2Eta_branch
    cdef float muon2Eta_value

    cdef TBranch* muon2GlbTrkHits_branch
    cdef float muon2GlbTrkHits_value

    cdef TBranch* muon2IP3DS_branch
    cdef float muon2IP3DS_value

    cdef TBranch* muon2IsGlobal_branch
    cdef float muon2IsGlobal_value

    cdef TBranch* muon2IsTracker_branch
    cdef float muon2IsTracker_value

    cdef TBranch* muon2JetBtag_branch
    cdef float muon2JetBtag_value

    cdef TBranch* muon2JetPt_branch
    cdef float muon2JetPt_value

    cdef TBranch* muon2Mass_branch
    cdef float muon2Mass_value

    cdef TBranch* muon2MtToMET_branch
    cdef float muon2MtToMET_value

    cdef TBranch* muon2NormTrkChi2_branch
    cdef float muon2NormTrkChi2_value

    cdef TBranch* muon2PFIDTight_branch
    cdef float muon2PFIDTight_value

    cdef TBranch* muon2Phi_branch
    cdef float muon2Phi_value

    cdef TBranch* muon2PixHits_branch
    cdef float muon2PixHits_value

    cdef TBranch* muon2Pt_branch
    cdef float muon2Pt_value

    cdef TBranch* muon2PtUncorr_branch
    cdef float muon2PtUncorr_value

    cdef TBranch* muon2RelPFIsoDB_branch
    cdef float muon2RelPFIsoDB_value

    cdef TBranch* muon2VBTFID_branch
    cdef float muon2VBTFID_value

    cdef TBranch* muon2VZ_branch
    cdef float muon2VZ_value

    cdef TBranch* muon2WWID_branch
    cdef float muon2WWID_value

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

        self.doubleMuGroup_branch = self.tree.GetBranch("doubleMuGroup")
        self.doubleMuGroup_branch.SetAddress(<void*>&self.doubleMuGroup_value)

        self.doubleMuPass_branch = self.tree.GetBranch("doubleMuPass")
        self.doubleMuPass_branch.SetAddress(<void*>&self.doubleMuPass_value)

        self.doubleMuPrescale_branch = self.tree.GetBranch("doubleMuPrescale")
        self.doubleMuPrescale_branch.SetAddress(<void*>&self.doubleMuPrescale_value)

        self.doubleMuTrkGroup_branch = self.tree.GetBranch("doubleMuTrkGroup")
        self.doubleMuTrkGroup_branch.SetAddress(<void*>&self.doubleMuTrkGroup_value)

        self.doubleMuTrkPass_branch = self.tree.GetBranch("doubleMuTrkPass")
        self.doubleMuTrkPass_branch.SetAddress(<void*>&self.doubleMuTrkPass_value)

        self.doubleMuTrkPrescale_branch = self.tree.GetBranch("doubleMuTrkPrescale")
        self.doubleMuTrkPrescale_branch.SetAddress(<void*>&self.doubleMuTrkPrescale_value)

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

        self.muGlbIsoVetoPt10_branch = self.tree.GetBranch("muGlbIsoVetoPt10")
        self.muGlbIsoVetoPt10_branch.SetAddress(<void*>&self.muGlbIsoVetoPt10_value)

        self.muVetoPt5_branch = self.tree.GetBranch("muVetoPt5")
        self.muVetoPt5_branch.SetAddress(<void*>&self.muVetoPt5_value)

        self.muon1AbsEta_branch = self.tree.GetBranch("muon1AbsEta")
        self.muon1AbsEta_branch.SetAddress(<void*>&self.muon1AbsEta_value)

        self.muon1Charge_branch = self.tree.GetBranch("muon1Charge")
        self.muon1Charge_branch.SetAddress(<void*>&self.muon1Charge_value)

        self.muon1D0_branch = self.tree.GetBranch("muon1D0")
        self.muon1D0_branch.SetAddress(<void*>&self.muon1D0_value)

        self.muon1DZ_branch = self.tree.GetBranch("muon1DZ")
        self.muon1DZ_branch.SetAddress(<void*>&self.muon1DZ_value)

        self.muon1Eta_branch = self.tree.GetBranch("muon1Eta")
        self.muon1Eta_branch.SetAddress(<void*>&self.muon1Eta_value)

        self.muon1GlbTrkHits_branch = self.tree.GetBranch("muon1GlbTrkHits")
        self.muon1GlbTrkHits_branch.SetAddress(<void*>&self.muon1GlbTrkHits_value)

        self.muon1IP3DS_branch = self.tree.GetBranch("muon1IP3DS")
        self.muon1IP3DS_branch.SetAddress(<void*>&self.muon1IP3DS_value)

        self.muon1IsGlobal_branch = self.tree.GetBranch("muon1IsGlobal")
        self.muon1IsGlobal_branch.SetAddress(<void*>&self.muon1IsGlobal_value)

        self.muon1IsTracker_branch = self.tree.GetBranch("muon1IsTracker")
        self.muon1IsTracker_branch.SetAddress(<void*>&self.muon1IsTracker_value)

        self.muon1JetBtag_branch = self.tree.GetBranch("muon1JetBtag")
        self.muon1JetBtag_branch.SetAddress(<void*>&self.muon1JetBtag_value)

        self.muon1JetPt_branch = self.tree.GetBranch("muon1JetPt")
        self.muon1JetPt_branch.SetAddress(<void*>&self.muon1JetPt_value)

        self.muon1Mass_branch = self.tree.GetBranch("muon1Mass")
        self.muon1Mass_branch.SetAddress(<void*>&self.muon1Mass_value)

        self.muon1MtToMET_branch = self.tree.GetBranch("muon1MtToMET")
        self.muon1MtToMET_branch.SetAddress(<void*>&self.muon1MtToMET_value)

        self.muon1NormTrkChi2_branch = self.tree.GetBranch("muon1NormTrkChi2")
        self.muon1NormTrkChi2_branch.SetAddress(<void*>&self.muon1NormTrkChi2_value)

        self.muon1PFIDTight_branch = self.tree.GetBranch("muon1PFIDTight")
        self.muon1PFIDTight_branch.SetAddress(<void*>&self.muon1PFIDTight_value)

        self.muon1Phi_branch = self.tree.GetBranch("muon1Phi")
        self.muon1Phi_branch.SetAddress(<void*>&self.muon1Phi_value)

        self.muon1PixHits_branch = self.tree.GetBranch("muon1PixHits")
        self.muon1PixHits_branch.SetAddress(<void*>&self.muon1PixHits_value)

        self.muon1Pt_branch = self.tree.GetBranch("muon1Pt")
        self.muon1Pt_branch.SetAddress(<void*>&self.muon1Pt_value)

        self.muon1PtUncorr_branch = self.tree.GetBranch("muon1PtUncorr")
        self.muon1PtUncorr_branch.SetAddress(<void*>&self.muon1PtUncorr_value)

        self.muon1RelPFIsoDB_branch = self.tree.GetBranch("muon1RelPFIsoDB")
        self.muon1RelPFIsoDB_branch.SetAddress(<void*>&self.muon1RelPFIsoDB_value)

        self.muon1VBTFID_branch = self.tree.GetBranch("muon1VBTFID")
        self.muon1VBTFID_branch.SetAddress(<void*>&self.muon1VBTFID_value)

        self.muon1VZ_branch = self.tree.GetBranch("muon1VZ")
        self.muon1VZ_branch.SetAddress(<void*>&self.muon1VZ_value)

        self.muon1WWID_branch = self.tree.GetBranch("muon1WWID")
        self.muon1WWID_branch.SetAddress(<void*>&self.muon1WWID_value)

        self.muon1_muon2_DPhi_branch = self.tree.GetBranch("muon1_muon2_DPhi")
        self.muon1_muon2_DPhi_branch.SetAddress(<void*>&self.muon1_muon2_DPhi_value)

        self.muon1_muon2_DR_branch = self.tree.GetBranch("muon1_muon2_DR")
        self.muon1_muon2_DR_branch.SetAddress(<void*>&self.muon1_muon2_DR_value)

        self.muon1_muon2_Mass_branch = self.tree.GetBranch("muon1_muon2_Mass")
        self.muon1_muon2_Mass_branch.SetAddress(<void*>&self.muon1_muon2_Mass_value)

        self.muon1_muon2_PZeta_branch = self.tree.GetBranch("muon1_muon2_PZeta")
        self.muon1_muon2_PZeta_branch.SetAddress(<void*>&self.muon1_muon2_PZeta_value)

        self.muon1_muon2_PZetaVis_branch = self.tree.GetBranch("muon1_muon2_PZetaVis")
        self.muon1_muon2_PZetaVis_branch.SetAddress(<void*>&self.muon1_muon2_PZetaVis_value)

        self.muon1_muon2_Pt_branch = self.tree.GetBranch("muon1_muon2_Pt")
        self.muon1_muon2_Pt_branch.SetAddress(<void*>&self.muon1_muon2_Pt_value)

        self.muon1_muon2_SS_branch = self.tree.GetBranch("muon1_muon2_SS")
        self.muon1_muon2_SS_branch.SetAddress(<void*>&self.muon1_muon2_SS_value)

        self.muon2AbsEta_branch = self.tree.GetBranch("muon2AbsEta")
        self.muon2AbsEta_branch.SetAddress(<void*>&self.muon2AbsEta_value)

        self.muon2Charge_branch = self.tree.GetBranch("muon2Charge")
        self.muon2Charge_branch.SetAddress(<void*>&self.muon2Charge_value)

        self.muon2D0_branch = self.tree.GetBranch("muon2D0")
        self.muon2D0_branch.SetAddress(<void*>&self.muon2D0_value)

        self.muon2DZ_branch = self.tree.GetBranch("muon2DZ")
        self.muon2DZ_branch.SetAddress(<void*>&self.muon2DZ_value)

        self.muon2Eta_branch = self.tree.GetBranch("muon2Eta")
        self.muon2Eta_branch.SetAddress(<void*>&self.muon2Eta_value)

        self.muon2GlbTrkHits_branch = self.tree.GetBranch("muon2GlbTrkHits")
        self.muon2GlbTrkHits_branch.SetAddress(<void*>&self.muon2GlbTrkHits_value)

        self.muon2IP3DS_branch = self.tree.GetBranch("muon2IP3DS")
        self.muon2IP3DS_branch.SetAddress(<void*>&self.muon2IP3DS_value)

        self.muon2IsGlobal_branch = self.tree.GetBranch("muon2IsGlobal")
        self.muon2IsGlobal_branch.SetAddress(<void*>&self.muon2IsGlobal_value)

        self.muon2IsTracker_branch = self.tree.GetBranch("muon2IsTracker")
        self.muon2IsTracker_branch.SetAddress(<void*>&self.muon2IsTracker_value)

        self.muon2JetBtag_branch = self.tree.GetBranch("muon2JetBtag")
        self.muon2JetBtag_branch.SetAddress(<void*>&self.muon2JetBtag_value)

        self.muon2JetPt_branch = self.tree.GetBranch("muon2JetPt")
        self.muon2JetPt_branch.SetAddress(<void*>&self.muon2JetPt_value)

        self.muon2Mass_branch = self.tree.GetBranch("muon2Mass")
        self.muon2Mass_branch.SetAddress(<void*>&self.muon2Mass_value)

        self.muon2MtToMET_branch = self.tree.GetBranch("muon2MtToMET")
        self.muon2MtToMET_branch.SetAddress(<void*>&self.muon2MtToMET_value)

        self.muon2NormTrkChi2_branch = self.tree.GetBranch("muon2NormTrkChi2")
        self.muon2NormTrkChi2_branch.SetAddress(<void*>&self.muon2NormTrkChi2_value)

        self.muon2PFIDTight_branch = self.tree.GetBranch("muon2PFIDTight")
        self.muon2PFIDTight_branch.SetAddress(<void*>&self.muon2PFIDTight_value)

        self.muon2Phi_branch = self.tree.GetBranch("muon2Phi")
        self.muon2Phi_branch.SetAddress(<void*>&self.muon2Phi_value)

        self.muon2PixHits_branch = self.tree.GetBranch("muon2PixHits")
        self.muon2PixHits_branch.SetAddress(<void*>&self.muon2PixHits_value)

        self.muon2Pt_branch = self.tree.GetBranch("muon2Pt")
        self.muon2Pt_branch.SetAddress(<void*>&self.muon2Pt_value)

        self.muon2PtUncorr_branch = self.tree.GetBranch("muon2PtUncorr")
        self.muon2PtUncorr_branch.SetAddress(<void*>&self.muon2PtUncorr_value)

        self.muon2RelPFIsoDB_branch = self.tree.GetBranch("muon2RelPFIsoDB")
        self.muon2RelPFIsoDB_branch.SetAddress(<void*>&self.muon2RelPFIsoDB_value)

        self.muon2VBTFID_branch = self.tree.GetBranch("muon2VBTFID")
        self.muon2VBTFID_branch.SetAddress(<void*>&self.muon2VBTFID_value)

        self.muon2VZ_branch = self.tree.GetBranch("muon2VZ")
        self.muon2VZ_branch.SetAddress(<void*>&self.muon2VZ_value)

        self.muon2WWID_branch = self.tree.GetBranch("muon2WWID")
        self.muon2WWID_branch.SetAddress(<void*>&self.muon2WWID_value)

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

    property doubleMuGroup:
        def __get__(self):
            self.doubleMuGroup_branch.GetEntry(self.ientry, 0)
            return self.doubleMuGroup_value

    property doubleMuPass:
        def __get__(self):
            self.doubleMuPass_branch.GetEntry(self.ientry, 0)
            return self.doubleMuPass_value

    property doubleMuPrescale:
        def __get__(self):
            self.doubleMuPrescale_branch.GetEntry(self.ientry, 0)
            return self.doubleMuPrescale_value

    property doubleMuTrkGroup:
        def __get__(self):
            self.doubleMuTrkGroup_branch.GetEntry(self.ientry, 0)
            return self.doubleMuTrkGroup_value

    property doubleMuTrkPass:
        def __get__(self):
            self.doubleMuTrkPass_branch.GetEntry(self.ientry, 0)
            return self.doubleMuTrkPass_value

    property doubleMuTrkPrescale:
        def __get__(self):
            self.doubleMuTrkPrescale_branch.GetEntry(self.ientry, 0)
            return self.doubleMuTrkPrescale_value

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

    property muGlbIsoVetoPt10:
        def __get__(self):
            self.muGlbIsoVetoPt10_branch.GetEntry(self.ientry, 0)
            return self.muGlbIsoVetoPt10_value

    property muVetoPt5:
        def __get__(self):
            self.muVetoPt5_branch.GetEntry(self.ientry, 0)
            return self.muVetoPt5_value

    property muon1AbsEta:
        def __get__(self):
            self.muon1AbsEta_branch.GetEntry(self.ientry, 0)
            return self.muon1AbsEta_value

    property muon1Charge:
        def __get__(self):
            self.muon1Charge_branch.GetEntry(self.ientry, 0)
            return self.muon1Charge_value

    property muon1D0:
        def __get__(self):
            self.muon1D0_branch.GetEntry(self.ientry, 0)
            return self.muon1D0_value

    property muon1DZ:
        def __get__(self):
            self.muon1DZ_branch.GetEntry(self.ientry, 0)
            return self.muon1DZ_value

    property muon1Eta:
        def __get__(self):
            self.muon1Eta_branch.GetEntry(self.ientry, 0)
            return self.muon1Eta_value

    property muon1GlbTrkHits:
        def __get__(self):
            self.muon1GlbTrkHits_branch.GetEntry(self.ientry, 0)
            return self.muon1GlbTrkHits_value

    property muon1IP3DS:
        def __get__(self):
            self.muon1IP3DS_branch.GetEntry(self.ientry, 0)
            return self.muon1IP3DS_value

    property muon1IsGlobal:
        def __get__(self):
            self.muon1IsGlobal_branch.GetEntry(self.ientry, 0)
            return self.muon1IsGlobal_value

    property muon1IsTracker:
        def __get__(self):
            self.muon1IsTracker_branch.GetEntry(self.ientry, 0)
            return self.muon1IsTracker_value

    property muon1JetBtag:
        def __get__(self):
            self.muon1JetBtag_branch.GetEntry(self.ientry, 0)
            return self.muon1JetBtag_value

    property muon1JetPt:
        def __get__(self):
            self.muon1JetPt_branch.GetEntry(self.ientry, 0)
            return self.muon1JetPt_value

    property muon1Mass:
        def __get__(self):
            self.muon1Mass_branch.GetEntry(self.ientry, 0)
            return self.muon1Mass_value

    property muon1MtToMET:
        def __get__(self):
            self.muon1MtToMET_branch.GetEntry(self.ientry, 0)
            return self.muon1MtToMET_value

    property muon1NormTrkChi2:
        def __get__(self):
            self.muon1NormTrkChi2_branch.GetEntry(self.ientry, 0)
            return self.muon1NormTrkChi2_value

    property muon1PFIDTight:
        def __get__(self):
            self.muon1PFIDTight_branch.GetEntry(self.ientry, 0)
            return self.muon1PFIDTight_value

    property muon1Phi:
        def __get__(self):
            self.muon1Phi_branch.GetEntry(self.ientry, 0)
            return self.muon1Phi_value

    property muon1PixHits:
        def __get__(self):
            self.muon1PixHits_branch.GetEntry(self.ientry, 0)
            return self.muon1PixHits_value

    property muon1Pt:
        def __get__(self):
            self.muon1Pt_branch.GetEntry(self.ientry, 0)
            return self.muon1Pt_value

    property muon1PtUncorr:
        def __get__(self):
            self.muon1PtUncorr_branch.GetEntry(self.ientry, 0)
            return self.muon1PtUncorr_value

    property muon1RelPFIsoDB:
        def __get__(self):
            self.muon1RelPFIsoDB_branch.GetEntry(self.ientry, 0)
            return self.muon1RelPFIsoDB_value

    property muon1VBTFID:
        def __get__(self):
            self.muon1VBTFID_branch.GetEntry(self.ientry, 0)
            return self.muon1VBTFID_value

    property muon1VZ:
        def __get__(self):
            self.muon1VZ_branch.GetEntry(self.ientry, 0)
            return self.muon1VZ_value

    property muon1WWID:
        def __get__(self):
            self.muon1WWID_branch.GetEntry(self.ientry, 0)
            return self.muon1WWID_value

    property muon1_muon2_DPhi:
        def __get__(self):
            self.muon1_muon2_DPhi_branch.GetEntry(self.ientry, 0)
            return self.muon1_muon2_DPhi_value

    property muon1_muon2_DR:
        def __get__(self):
            self.muon1_muon2_DR_branch.GetEntry(self.ientry, 0)
            return self.muon1_muon2_DR_value

    property muon1_muon2_Mass:
        def __get__(self):
            self.muon1_muon2_Mass_branch.GetEntry(self.ientry, 0)
            return self.muon1_muon2_Mass_value

    property muon1_muon2_PZeta:
        def __get__(self):
            self.muon1_muon2_PZeta_branch.GetEntry(self.ientry, 0)
            return self.muon1_muon2_PZeta_value

    property muon1_muon2_PZetaVis:
        def __get__(self):
            self.muon1_muon2_PZetaVis_branch.GetEntry(self.ientry, 0)
            return self.muon1_muon2_PZetaVis_value

    property muon1_muon2_Pt:
        def __get__(self):
            self.muon1_muon2_Pt_branch.GetEntry(self.ientry, 0)
            return self.muon1_muon2_Pt_value

    property muon1_muon2_SS:
        def __get__(self):
            self.muon1_muon2_SS_branch.GetEntry(self.ientry, 0)
            return self.muon1_muon2_SS_value

    property muon2AbsEta:
        def __get__(self):
            self.muon2AbsEta_branch.GetEntry(self.ientry, 0)
            return self.muon2AbsEta_value

    property muon2Charge:
        def __get__(self):
            self.muon2Charge_branch.GetEntry(self.ientry, 0)
            return self.muon2Charge_value

    property muon2D0:
        def __get__(self):
            self.muon2D0_branch.GetEntry(self.ientry, 0)
            return self.muon2D0_value

    property muon2DZ:
        def __get__(self):
            self.muon2DZ_branch.GetEntry(self.ientry, 0)
            return self.muon2DZ_value

    property muon2Eta:
        def __get__(self):
            self.muon2Eta_branch.GetEntry(self.ientry, 0)
            return self.muon2Eta_value

    property muon2GlbTrkHits:
        def __get__(self):
            self.muon2GlbTrkHits_branch.GetEntry(self.ientry, 0)
            return self.muon2GlbTrkHits_value

    property muon2IP3DS:
        def __get__(self):
            self.muon2IP3DS_branch.GetEntry(self.ientry, 0)
            return self.muon2IP3DS_value

    property muon2IsGlobal:
        def __get__(self):
            self.muon2IsGlobal_branch.GetEntry(self.ientry, 0)
            return self.muon2IsGlobal_value

    property muon2IsTracker:
        def __get__(self):
            self.muon2IsTracker_branch.GetEntry(self.ientry, 0)
            return self.muon2IsTracker_value

    property muon2JetBtag:
        def __get__(self):
            self.muon2JetBtag_branch.GetEntry(self.ientry, 0)
            return self.muon2JetBtag_value

    property muon2JetPt:
        def __get__(self):
            self.muon2JetPt_branch.GetEntry(self.ientry, 0)
            return self.muon2JetPt_value

    property muon2Mass:
        def __get__(self):
            self.muon2Mass_branch.GetEntry(self.ientry, 0)
            return self.muon2Mass_value

    property muon2MtToMET:
        def __get__(self):
            self.muon2MtToMET_branch.GetEntry(self.ientry, 0)
            return self.muon2MtToMET_value

    property muon2NormTrkChi2:
        def __get__(self):
            self.muon2NormTrkChi2_branch.GetEntry(self.ientry, 0)
            return self.muon2NormTrkChi2_value

    property muon2PFIDTight:
        def __get__(self):
            self.muon2PFIDTight_branch.GetEntry(self.ientry, 0)
            return self.muon2PFIDTight_value

    property muon2Phi:
        def __get__(self):
            self.muon2Phi_branch.GetEntry(self.ientry, 0)
            return self.muon2Phi_value

    property muon2PixHits:
        def __get__(self):
            self.muon2PixHits_branch.GetEntry(self.ientry, 0)
            return self.muon2PixHits_value

    property muon2Pt:
        def __get__(self):
            self.muon2Pt_branch.GetEntry(self.ientry, 0)
            return self.muon2Pt_value

    property muon2PtUncorr:
        def __get__(self):
            self.muon2PtUncorr_branch.GetEntry(self.ientry, 0)
            return self.muon2PtUncorr_value

    property muon2RelPFIsoDB:
        def __get__(self):
            self.muon2RelPFIsoDB_branch.GetEntry(self.ientry, 0)
            return self.muon2RelPFIsoDB_value

    property muon2VBTFID:
        def __get__(self):
            self.muon2VBTFID_branch.GetEntry(self.ientry, 0)
            return self.muon2VBTFID_value

    property muon2VZ:
        def __get__(self):
            self.muon2VZ_branch.GetEntry(self.ientry, 0)
            return self.muon2VZ_value

    property muon2WWID:
        def __get__(self):
            self.muon2WWID_branch.GetEntry(self.ientry, 0)
            return self.muon2WWID_value

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



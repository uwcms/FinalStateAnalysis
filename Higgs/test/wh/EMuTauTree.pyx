

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

cdef class EMuTauTree:
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

    cdef TBranch* doubleEExtraGroup_branch
    cdef float doubleEExtraGroup_value

    cdef TBranch* doubleEExtraPass_branch
    cdef float doubleEExtraPass_value

    cdef TBranch* doubleEExtraPrescale_branch
    cdef float doubleEExtraPrescale_value

    cdef TBranch* doubleEGroup_branch
    cdef float doubleEGroup_value

    cdef TBranch* doubleEPass_branch
    cdef float doubleEPass_value

    cdef TBranch* doubleEPrescale_branch
    cdef float doubleEPrescale_value

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

    cdef TBranch* eAbsEta_branch
    cdef float eAbsEta_value

    cdef TBranch* eCharge_branch
    cdef float eCharge_value

    cdef TBranch* eChargeIdLoose_branch
    cdef float eChargeIdLoose_value

    cdef TBranch* eChargeIdMed_branch
    cdef float eChargeIdMed_value

    cdef TBranch* eChargeIdTight_branch
    cdef float eChargeIdTight_value

    cdef TBranch* eCiCTight_branch
    cdef float eCiCTight_value

    cdef TBranch* eDZ_branch
    cdef float eDZ_value

    cdef TBranch* eEta_branch
    cdef float eEta_value

    cdef TBranch* eHasConversion_branch
    cdef float eHasConversion_value

    cdef TBranch* eIP3DS_branch
    cdef float eIP3DS_value

    cdef TBranch* eJetBtag_branch
    cdef float eJetBtag_value

    cdef TBranch* eJetPt_branch
    cdef float eJetPt_value

    cdef TBranch* eMITID_branch
    cdef float eMITID_value

    cdef TBranch* eMVAIDH2TauWP_branch
    cdef float eMVAIDH2TauWP_value

    cdef TBranch* eMVANonTrig_branch
    cdef float eMVANonTrig_value

    cdef TBranch* eMVATrig_branch
    cdef float eMVATrig_value

    cdef TBranch* eMass_branch
    cdef float eMass_value

    cdef TBranch* eMissingHits_branch
    cdef float eMissingHits_value

    cdef TBranch* eMtToMET_branch
    cdef float eMtToMET_value

    cdef TBranch* ePhi_branch
    cdef float ePhi_value

    cdef TBranch* ePt_branch
    cdef float ePt_value

    cdef TBranch* eRelIso_branch
    cdef float eRelIso_value

    cdef TBranch* eRelPFIsoDB_branch
    cdef float eRelPFIsoDB_value

    cdef TBranch* eVZ_branch
    cdef float eVZ_value

    cdef TBranch* eWWID_branch
    cdef float eWWID_value

    cdef TBranch* e_m_DPhi_branch
    cdef float e_m_DPhi_value

    cdef TBranch* e_m_DR_branch
    cdef float e_m_DR_value

    cdef TBranch* e_m_Mass_branch
    cdef float e_m_Mass_value

    cdef TBranch* e_m_PZeta_branch
    cdef float e_m_PZeta_value

    cdef TBranch* e_m_PZetaVis_branch
    cdef float e_m_PZetaVis_value

    cdef TBranch* e_m_Pt_branch
    cdef float e_m_Pt_value

    cdef TBranch* e_m_SS_branch
    cdef float e_m_SS_value

    cdef TBranch* e_m_Zcompat_branch
    cdef float e_m_Zcompat_value

    cdef TBranch* e_t_DPhi_branch
    cdef float e_t_DPhi_value

    cdef TBranch* e_t_DR_branch
    cdef float e_t_DR_value

    cdef TBranch* e_t_Mass_branch
    cdef float e_t_Mass_value

    cdef TBranch* e_t_PZeta_branch
    cdef float e_t_PZeta_value

    cdef TBranch* e_t_PZetaVis_branch
    cdef float e_t_PZetaVis_value

    cdef TBranch* e_t_Pt_branch
    cdef float e_t_Pt_value

    cdef TBranch* e_t_SS_branch
    cdef float e_t_SS_value

    cdef TBranch* e_t_Zcompat_branch
    cdef float e_t_Zcompat_value

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

    cdef TBranch* mAbsEta_branch
    cdef float mAbsEta_value

    cdef TBranch* mCharge_branch
    cdef float mCharge_value

    cdef TBranch* mD0_branch
    cdef float mD0_value

    cdef TBranch* mDZ_branch
    cdef float mDZ_value

    cdef TBranch* mEta_branch
    cdef float mEta_value

    cdef TBranch* mGlbTrkHits_branch
    cdef float mGlbTrkHits_value

    cdef TBranch* mIP3DS_branch
    cdef float mIP3DS_value

    cdef TBranch* mIsGlobal_branch
    cdef float mIsGlobal_value

    cdef TBranch* mIsTracker_branch
    cdef float mIsTracker_value

    cdef TBranch* mJetBtag_branch
    cdef float mJetBtag_value

    cdef TBranch* mJetPt_branch
    cdef float mJetPt_value

    cdef TBranch* mMass_branch
    cdef float mMass_value

    cdef TBranch* mMtToMET_branch
    cdef float mMtToMET_value

    cdef TBranch* mNormTrkChi2_branch
    cdef float mNormTrkChi2_value

    cdef TBranch* mPFIDTight_branch
    cdef float mPFIDTight_value

    cdef TBranch* mPhi_branch
    cdef float mPhi_value

    cdef TBranch* mPixHits_branch
    cdef float mPixHits_value

    cdef TBranch* mPt_branch
    cdef float mPt_value

    cdef TBranch* mPtUncorr_branch
    cdef float mPtUncorr_value

    cdef TBranch* mRelPFIsoDB_branch
    cdef float mRelPFIsoDB_value

    cdef TBranch* mVBTFID_branch
    cdef float mVBTFID_value

    cdef TBranch* mVZ_branch
    cdef float mVZ_value

    cdef TBranch* mWWID_branch
    cdef float mWWID_value

    cdef TBranch* m_t_DPhi_branch
    cdef float m_t_DPhi_value

    cdef TBranch* m_t_DR_branch
    cdef float m_t_DR_value

    cdef TBranch* m_t_Mass_branch
    cdef float m_t_Mass_value

    cdef TBranch* m_t_PZeta_branch
    cdef float m_t_PZeta_value

    cdef TBranch* m_t_PZetaVis_branch
    cdef float m_t_PZetaVis_value

    cdef TBranch* m_t_Pt_branch
    cdef float m_t_Pt_value

    cdef TBranch* m_t_SS_branch
    cdef float m_t_SS_value

    cdef TBranch* m_t_Zcompat_branch
    cdef float m_t_Zcompat_value

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

    cdef TBranch* nTruePU_branch
    cdef float nTruePU_value

    cdef TBranch* nvtx_branch
    cdef float nvtx_value

    cdef TBranch* processID_branch
    cdef float processID_value

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

    cdef TBranch* tAbsEta_branch
    cdef float tAbsEta_value

    cdef TBranch* tAntiElectronLoose_branch
    cdef float tAntiElectronLoose_value

    cdef TBranch* tAntiElectronMVA_branch
    cdef float tAntiElectronMVA_value

    cdef TBranch* tAntiElectronMedium_branch
    cdef float tAntiElectronMedium_value

    cdef TBranch* tAntiElectronTight_branch
    cdef float tAntiElectronTight_value

    cdef TBranch* tAntiMuonLoose_branch
    cdef float tAntiMuonLoose_value

    cdef TBranch* tAntiMuonTight_branch
    cdef float tAntiMuonTight_value

    cdef TBranch* tCharge_branch
    cdef float tCharge_value

    cdef TBranch* tDZ_branch
    cdef float tDZ_value

    cdef TBranch* tDecayFinding_branch
    cdef float tDecayFinding_value

    cdef TBranch* tDecayMode_branch
    cdef float tDecayMode_value

    cdef TBranch* tEta_branch
    cdef float tEta_value

    cdef TBranch* tGenDecayMode_branch
    cdef float tGenDecayMode_value

    cdef TBranch* tIP3DS_branch
    cdef float tIP3DS_value

    cdef TBranch* tJetBtag_branch
    cdef float tJetBtag_value

    cdef TBranch* tJetPt_branch
    cdef float tJetPt_value

    cdef TBranch* tLeadTrackPt_branch
    cdef float tLeadTrackPt_value

    cdef TBranch* tLooseIso_branch
    cdef float tLooseIso_value

    cdef TBranch* tLooseMVAIso_branch
    cdef float tLooseMVAIso_value

    cdef TBranch* tMass_branch
    cdef float tMass_value

    cdef TBranch* tMediumIso_branch
    cdef float tMediumIso_value

    cdef TBranch* tMediumMVAIso_branch
    cdef float tMediumMVAIso_value

    cdef TBranch* tMtToMET_branch
    cdef float tMtToMET_value

    cdef TBranch* tMuOverlap_branch
    cdef float tMuOverlap_value

    cdef TBranch* tPhi_branch
    cdef float tPhi_value

    cdef TBranch* tPt_branch
    cdef float tPt_value

    cdef TBranch* tTNPId_branch
    cdef float tTNPId_value

    cdef TBranch* tVZ_branch
    cdef float tVZ_value

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

        self.doubleEExtraGroup_branch = self.tree.GetBranch("doubleEExtraGroup")
        self.doubleEExtraGroup_branch.SetAddress(<void*>&self.doubleEExtraGroup_value)

        self.doubleEExtraPass_branch = self.tree.GetBranch("doubleEExtraPass")
        self.doubleEExtraPass_branch.SetAddress(<void*>&self.doubleEExtraPass_value)

        self.doubleEExtraPrescale_branch = self.tree.GetBranch("doubleEExtraPrescale")
        self.doubleEExtraPrescale_branch.SetAddress(<void*>&self.doubleEExtraPrescale_value)

        self.doubleEGroup_branch = self.tree.GetBranch("doubleEGroup")
        self.doubleEGroup_branch.SetAddress(<void*>&self.doubleEGroup_value)

        self.doubleEPass_branch = self.tree.GetBranch("doubleEPass")
        self.doubleEPass_branch.SetAddress(<void*>&self.doubleEPass_value)

        self.doubleEPrescale_branch = self.tree.GetBranch("doubleEPrescale")
        self.doubleEPrescale_branch.SetAddress(<void*>&self.doubleEPrescale_value)

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

        self.eAbsEta_branch = self.tree.GetBranch("eAbsEta")
        self.eAbsEta_branch.SetAddress(<void*>&self.eAbsEta_value)

        self.eCharge_branch = self.tree.GetBranch("eCharge")
        self.eCharge_branch.SetAddress(<void*>&self.eCharge_value)

        self.eChargeIdLoose_branch = self.tree.GetBranch("eChargeIdLoose")
        self.eChargeIdLoose_branch.SetAddress(<void*>&self.eChargeIdLoose_value)

        self.eChargeIdMed_branch = self.tree.GetBranch("eChargeIdMed")
        self.eChargeIdMed_branch.SetAddress(<void*>&self.eChargeIdMed_value)

        self.eChargeIdTight_branch = self.tree.GetBranch("eChargeIdTight")
        self.eChargeIdTight_branch.SetAddress(<void*>&self.eChargeIdTight_value)

        self.eCiCTight_branch = self.tree.GetBranch("eCiCTight")
        self.eCiCTight_branch.SetAddress(<void*>&self.eCiCTight_value)

        self.eDZ_branch = self.tree.GetBranch("eDZ")
        self.eDZ_branch.SetAddress(<void*>&self.eDZ_value)

        self.eEta_branch = self.tree.GetBranch("eEta")
        self.eEta_branch.SetAddress(<void*>&self.eEta_value)

        self.eHasConversion_branch = self.tree.GetBranch("eHasConversion")
        self.eHasConversion_branch.SetAddress(<void*>&self.eHasConversion_value)

        self.eIP3DS_branch = self.tree.GetBranch("eIP3DS")
        self.eIP3DS_branch.SetAddress(<void*>&self.eIP3DS_value)

        self.eJetBtag_branch = self.tree.GetBranch("eJetBtag")
        self.eJetBtag_branch.SetAddress(<void*>&self.eJetBtag_value)

        self.eJetPt_branch = self.tree.GetBranch("eJetPt")
        self.eJetPt_branch.SetAddress(<void*>&self.eJetPt_value)

        self.eMITID_branch = self.tree.GetBranch("eMITID")
        self.eMITID_branch.SetAddress(<void*>&self.eMITID_value)

        self.eMVAIDH2TauWP_branch = self.tree.GetBranch("eMVAIDH2TauWP")
        self.eMVAIDH2TauWP_branch.SetAddress(<void*>&self.eMVAIDH2TauWP_value)

        self.eMVANonTrig_branch = self.tree.GetBranch("eMVANonTrig")
        self.eMVANonTrig_branch.SetAddress(<void*>&self.eMVANonTrig_value)

        self.eMVATrig_branch = self.tree.GetBranch("eMVATrig")
        self.eMVATrig_branch.SetAddress(<void*>&self.eMVATrig_value)

        self.eMass_branch = self.tree.GetBranch("eMass")
        self.eMass_branch.SetAddress(<void*>&self.eMass_value)

        self.eMissingHits_branch = self.tree.GetBranch("eMissingHits")
        self.eMissingHits_branch.SetAddress(<void*>&self.eMissingHits_value)

        self.eMtToMET_branch = self.tree.GetBranch("eMtToMET")
        self.eMtToMET_branch.SetAddress(<void*>&self.eMtToMET_value)

        self.ePhi_branch = self.tree.GetBranch("ePhi")
        self.ePhi_branch.SetAddress(<void*>&self.ePhi_value)

        self.ePt_branch = self.tree.GetBranch("ePt")
        self.ePt_branch.SetAddress(<void*>&self.ePt_value)

        self.eRelIso_branch = self.tree.GetBranch("eRelIso")
        self.eRelIso_branch.SetAddress(<void*>&self.eRelIso_value)

        self.eRelPFIsoDB_branch = self.tree.GetBranch("eRelPFIsoDB")
        self.eRelPFIsoDB_branch.SetAddress(<void*>&self.eRelPFIsoDB_value)

        self.eVZ_branch = self.tree.GetBranch("eVZ")
        self.eVZ_branch.SetAddress(<void*>&self.eVZ_value)

        self.eWWID_branch = self.tree.GetBranch("eWWID")
        self.eWWID_branch.SetAddress(<void*>&self.eWWID_value)

        self.e_m_DPhi_branch = self.tree.GetBranch("e_m_DPhi")
        self.e_m_DPhi_branch.SetAddress(<void*>&self.e_m_DPhi_value)

        self.e_m_DR_branch = self.tree.GetBranch("e_m_DR")
        self.e_m_DR_branch.SetAddress(<void*>&self.e_m_DR_value)

        self.e_m_Mass_branch = self.tree.GetBranch("e_m_Mass")
        self.e_m_Mass_branch.SetAddress(<void*>&self.e_m_Mass_value)

        self.e_m_PZeta_branch = self.tree.GetBranch("e_m_PZeta")
        self.e_m_PZeta_branch.SetAddress(<void*>&self.e_m_PZeta_value)

        self.e_m_PZetaVis_branch = self.tree.GetBranch("e_m_PZetaVis")
        self.e_m_PZetaVis_branch.SetAddress(<void*>&self.e_m_PZetaVis_value)

        self.e_m_Pt_branch = self.tree.GetBranch("e_m_Pt")
        self.e_m_Pt_branch.SetAddress(<void*>&self.e_m_Pt_value)

        self.e_m_SS_branch = self.tree.GetBranch("e_m_SS")
        self.e_m_SS_branch.SetAddress(<void*>&self.e_m_SS_value)

        self.e_m_Zcompat_branch = self.tree.GetBranch("e_m_Zcompat")
        self.e_m_Zcompat_branch.SetAddress(<void*>&self.e_m_Zcompat_value)

        self.e_t_DPhi_branch = self.tree.GetBranch("e_t_DPhi")
        self.e_t_DPhi_branch.SetAddress(<void*>&self.e_t_DPhi_value)

        self.e_t_DR_branch = self.tree.GetBranch("e_t_DR")
        self.e_t_DR_branch.SetAddress(<void*>&self.e_t_DR_value)

        self.e_t_Mass_branch = self.tree.GetBranch("e_t_Mass")
        self.e_t_Mass_branch.SetAddress(<void*>&self.e_t_Mass_value)

        self.e_t_PZeta_branch = self.tree.GetBranch("e_t_PZeta")
        self.e_t_PZeta_branch.SetAddress(<void*>&self.e_t_PZeta_value)

        self.e_t_PZetaVis_branch = self.tree.GetBranch("e_t_PZetaVis")
        self.e_t_PZetaVis_branch.SetAddress(<void*>&self.e_t_PZetaVis_value)

        self.e_t_Pt_branch = self.tree.GetBranch("e_t_Pt")
        self.e_t_Pt_branch.SetAddress(<void*>&self.e_t_Pt_value)

        self.e_t_SS_branch = self.tree.GetBranch("e_t_SS")
        self.e_t_SS_branch.SetAddress(<void*>&self.e_t_SS_value)

        self.e_t_Zcompat_branch = self.tree.GetBranch("e_t_Zcompat")
        self.e_t_Zcompat_branch.SetAddress(<void*>&self.e_t_Zcompat_value)

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

        self.mAbsEta_branch = self.tree.GetBranch("mAbsEta")
        self.mAbsEta_branch.SetAddress(<void*>&self.mAbsEta_value)

        self.mCharge_branch = self.tree.GetBranch("mCharge")
        self.mCharge_branch.SetAddress(<void*>&self.mCharge_value)

        self.mD0_branch = self.tree.GetBranch("mD0")
        self.mD0_branch.SetAddress(<void*>&self.mD0_value)

        self.mDZ_branch = self.tree.GetBranch("mDZ")
        self.mDZ_branch.SetAddress(<void*>&self.mDZ_value)

        self.mEta_branch = self.tree.GetBranch("mEta")
        self.mEta_branch.SetAddress(<void*>&self.mEta_value)

        self.mGlbTrkHits_branch = self.tree.GetBranch("mGlbTrkHits")
        self.mGlbTrkHits_branch.SetAddress(<void*>&self.mGlbTrkHits_value)

        self.mIP3DS_branch = self.tree.GetBranch("mIP3DS")
        self.mIP3DS_branch.SetAddress(<void*>&self.mIP3DS_value)

        self.mIsGlobal_branch = self.tree.GetBranch("mIsGlobal")
        self.mIsGlobal_branch.SetAddress(<void*>&self.mIsGlobal_value)

        self.mIsTracker_branch = self.tree.GetBranch("mIsTracker")
        self.mIsTracker_branch.SetAddress(<void*>&self.mIsTracker_value)

        self.mJetBtag_branch = self.tree.GetBranch("mJetBtag")
        self.mJetBtag_branch.SetAddress(<void*>&self.mJetBtag_value)

        self.mJetPt_branch = self.tree.GetBranch("mJetPt")
        self.mJetPt_branch.SetAddress(<void*>&self.mJetPt_value)

        self.mMass_branch = self.tree.GetBranch("mMass")
        self.mMass_branch.SetAddress(<void*>&self.mMass_value)

        self.mMtToMET_branch = self.tree.GetBranch("mMtToMET")
        self.mMtToMET_branch.SetAddress(<void*>&self.mMtToMET_value)

        self.mNormTrkChi2_branch = self.tree.GetBranch("mNormTrkChi2")
        self.mNormTrkChi2_branch.SetAddress(<void*>&self.mNormTrkChi2_value)

        self.mPFIDTight_branch = self.tree.GetBranch("mPFIDTight")
        self.mPFIDTight_branch.SetAddress(<void*>&self.mPFIDTight_value)

        self.mPhi_branch = self.tree.GetBranch("mPhi")
        self.mPhi_branch.SetAddress(<void*>&self.mPhi_value)

        self.mPixHits_branch = self.tree.GetBranch("mPixHits")
        self.mPixHits_branch.SetAddress(<void*>&self.mPixHits_value)

        self.mPt_branch = self.tree.GetBranch("mPt")
        self.mPt_branch.SetAddress(<void*>&self.mPt_value)

        self.mPtUncorr_branch = self.tree.GetBranch("mPtUncorr")
        self.mPtUncorr_branch.SetAddress(<void*>&self.mPtUncorr_value)

        self.mRelPFIsoDB_branch = self.tree.GetBranch("mRelPFIsoDB")
        self.mRelPFIsoDB_branch.SetAddress(<void*>&self.mRelPFIsoDB_value)

        self.mVBTFID_branch = self.tree.GetBranch("mVBTFID")
        self.mVBTFID_branch.SetAddress(<void*>&self.mVBTFID_value)

        self.mVZ_branch = self.tree.GetBranch("mVZ")
        self.mVZ_branch.SetAddress(<void*>&self.mVZ_value)

        self.mWWID_branch = self.tree.GetBranch("mWWID")
        self.mWWID_branch.SetAddress(<void*>&self.mWWID_value)

        self.m_t_DPhi_branch = self.tree.GetBranch("m_t_DPhi")
        self.m_t_DPhi_branch.SetAddress(<void*>&self.m_t_DPhi_value)

        self.m_t_DR_branch = self.tree.GetBranch("m_t_DR")
        self.m_t_DR_branch.SetAddress(<void*>&self.m_t_DR_value)

        self.m_t_Mass_branch = self.tree.GetBranch("m_t_Mass")
        self.m_t_Mass_branch.SetAddress(<void*>&self.m_t_Mass_value)

        self.m_t_PZeta_branch = self.tree.GetBranch("m_t_PZeta")
        self.m_t_PZeta_branch.SetAddress(<void*>&self.m_t_PZeta_value)

        self.m_t_PZetaVis_branch = self.tree.GetBranch("m_t_PZetaVis")
        self.m_t_PZetaVis_branch.SetAddress(<void*>&self.m_t_PZetaVis_value)

        self.m_t_Pt_branch = self.tree.GetBranch("m_t_Pt")
        self.m_t_Pt_branch.SetAddress(<void*>&self.m_t_Pt_value)

        self.m_t_SS_branch = self.tree.GetBranch("m_t_SS")
        self.m_t_SS_branch.SetAddress(<void*>&self.m_t_SS_value)

        self.m_t_Zcompat_branch = self.tree.GetBranch("m_t_Zcompat")
        self.m_t_Zcompat_branch.SetAddress(<void*>&self.m_t_Zcompat_value)

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

        self.nTruePU_branch = self.tree.GetBranch("nTruePU")
        self.nTruePU_branch.SetAddress(<void*>&self.nTruePU_value)

        self.nvtx_branch = self.tree.GetBranch("nvtx")
        self.nvtx_branch.SetAddress(<void*>&self.nvtx_value)

        self.processID_branch = self.tree.GetBranch("processID")
        self.processID_branch.SetAddress(<void*>&self.processID_value)

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

        self.tAbsEta_branch = self.tree.GetBranch("tAbsEta")
        self.tAbsEta_branch.SetAddress(<void*>&self.tAbsEta_value)

        self.tAntiElectronLoose_branch = self.tree.GetBranch("tAntiElectronLoose")
        self.tAntiElectronLoose_branch.SetAddress(<void*>&self.tAntiElectronLoose_value)

        self.tAntiElectronMVA_branch = self.tree.GetBranch("tAntiElectronMVA")
        self.tAntiElectronMVA_branch.SetAddress(<void*>&self.tAntiElectronMVA_value)

        self.tAntiElectronMedium_branch = self.tree.GetBranch("tAntiElectronMedium")
        self.tAntiElectronMedium_branch.SetAddress(<void*>&self.tAntiElectronMedium_value)

        self.tAntiElectronTight_branch = self.tree.GetBranch("tAntiElectronTight")
        self.tAntiElectronTight_branch.SetAddress(<void*>&self.tAntiElectronTight_value)

        self.tAntiMuonLoose_branch = self.tree.GetBranch("tAntiMuonLoose")
        self.tAntiMuonLoose_branch.SetAddress(<void*>&self.tAntiMuonLoose_value)

        self.tAntiMuonTight_branch = self.tree.GetBranch("tAntiMuonTight")
        self.tAntiMuonTight_branch.SetAddress(<void*>&self.tAntiMuonTight_value)

        self.tCharge_branch = self.tree.GetBranch("tCharge")
        self.tCharge_branch.SetAddress(<void*>&self.tCharge_value)

        self.tDZ_branch = self.tree.GetBranch("tDZ")
        self.tDZ_branch.SetAddress(<void*>&self.tDZ_value)

        self.tDecayFinding_branch = self.tree.GetBranch("tDecayFinding")
        self.tDecayFinding_branch.SetAddress(<void*>&self.tDecayFinding_value)

        self.tDecayMode_branch = self.tree.GetBranch("tDecayMode")
        self.tDecayMode_branch.SetAddress(<void*>&self.tDecayMode_value)

        self.tEta_branch = self.tree.GetBranch("tEta")
        self.tEta_branch.SetAddress(<void*>&self.tEta_value)

        self.tGenDecayMode_branch = self.tree.GetBranch("tGenDecayMode")
        self.tGenDecayMode_branch.SetAddress(<void*>&self.tGenDecayMode_value)

        self.tIP3DS_branch = self.tree.GetBranch("tIP3DS")
        self.tIP3DS_branch.SetAddress(<void*>&self.tIP3DS_value)

        self.tJetBtag_branch = self.tree.GetBranch("tJetBtag")
        self.tJetBtag_branch.SetAddress(<void*>&self.tJetBtag_value)

        self.tJetPt_branch = self.tree.GetBranch("tJetPt")
        self.tJetPt_branch.SetAddress(<void*>&self.tJetPt_value)

        self.tLeadTrackPt_branch = self.tree.GetBranch("tLeadTrackPt")
        self.tLeadTrackPt_branch.SetAddress(<void*>&self.tLeadTrackPt_value)

        self.tLooseIso_branch = self.tree.GetBranch("tLooseIso")
        self.tLooseIso_branch.SetAddress(<void*>&self.tLooseIso_value)

        self.tLooseMVAIso_branch = self.tree.GetBranch("tLooseMVAIso")
        self.tLooseMVAIso_branch.SetAddress(<void*>&self.tLooseMVAIso_value)

        self.tMass_branch = self.tree.GetBranch("tMass")
        self.tMass_branch.SetAddress(<void*>&self.tMass_value)

        self.tMediumIso_branch = self.tree.GetBranch("tMediumIso")
        self.tMediumIso_branch.SetAddress(<void*>&self.tMediumIso_value)

        self.tMediumMVAIso_branch = self.tree.GetBranch("tMediumMVAIso")
        self.tMediumMVAIso_branch.SetAddress(<void*>&self.tMediumMVAIso_value)

        self.tMtToMET_branch = self.tree.GetBranch("tMtToMET")
        self.tMtToMET_branch.SetAddress(<void*>&self.tMtToMET_value)

        self.tMuOverlap_branch = self.tree.GetBranch("tMuOverlap")
        self.tMuOverlap_branch.SetAddress(<void*>&self.tMuOverlap_value)

        self.tPhi_branch = self.tree.GetBranch("tPhi")
        self.tPhi_branch.SetAddress(<void*>&self.tPhi_value)

        self.tPt_branch = self.tree.GetBranch("tPt")
        self.tPt_branch.SetAddress(<void*>&self.tPt_value)

        self.tTNPId_branch = self.tree.GetBranch("tTNPId")
        self.tTNPId_branch.SetAddress(<void*>&self.tTNPId_value)

        self.tVZ_branch = self.tree.GetBranch("tVZ")
        self.tVZ_branch.SetAddress(<void*>&self.tVZ_value)

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

    property doubleEExtraGroup:
        def __get__(self):
            self.doubleEExtraGroup_branch.GetEntry(self.ientry, 0)
            return self.doubleEExtraGroup_value

    property doubleEExtraPass:
        def __get__(self):
            self.doubleEExtraPass_branch.GetEntry(self.ientry, 0)
            return self.doubleEExtraPass_value

    property doubleEExtraPrescale:
        def __get__(self):
            self.doubleEExtraPrescale_branch.GetEntry(self.ientry, 0)
            return self.doubleEExtraPrescale_value

    property doubleEGroup:
        def __get__(self):
            self.doubleEGroup_branch.GetEntry(self.ientry, 0)
            return self.doubleEGroup_value

    property doubleEPass:
        def __get__(self):
            self.doubleEPass_branch.GetEntry(self.ientry, 0)
            return self.doubleEPass_value

    property doubleEPrescale:
        def __get__(self):
            self.doubleEPrescale_branch.GetEntry(self.ientry, 0)
            return self.doubleEPrescale_value

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

    property eAbsEta:
        def __get__(self):
            self.eAbsEta_branch.GetEntry(self.ientry, 0)
            return self.eAbsEta_value

    property eCharge:
        def __get__(self):
            self.eCharge_branch.GetEntry(self.ientry, 0)
            return self.eCharge_value

    property eChargeIdLoose:
        def __get__(self):
            self.eChargeIdLoose_branch.GetEntry(self.ientry, 0)
            return self.eChargeIdLoose_value

    property eChargeIdMed:
        def __get__(self):
            self.eChargeIdMed_branch.GetEntry(self.ientry, 0)
            return self.eChargeIdMed_value

    property eChargeIdTight:
        def __get__(self):
            self.eChargeIdTight_branch.GetEntry(self.ientry, 0)
            return self.eChargeIdTight_value

    property eCiCTight:
        def __get__(self):
            self.eCiCTight_branch.GetEntry(self.ientry, 0)
            return self.eCiCTight_value

    property eDZ:
        def __get__(self):
            self.eDZ_branch.GetEntry(self.ientry, 0)
            return self.eDZ_value

    property eEta:
        def __get__(self):
            self.eEta_branch.GetEntry(self.ientry, 0)
            return self.eEta_value

    property eHasConversion:
        def __get__(self):
            self.eHasConversion_branch.GetEntry(self.ientry, 0)
            return self.eHasConversion_value

    property eIP3DS:
        def __get__(self):
            self.eIP3DS_branch.GetEntry(self.ientry, 0)
            return self.eIP3DS_value

    property eJetBtag:
        def __get__(self):
            self.eJetBtag_branch.GetEntry(self.ientry, 0)
            return self.eJetBtag_value

    property eJetPt:
        def __get__(self):
            self.eJetPt_branch.GetEntry(self.ientry, 0)
            return self.eJetPt_value

    property eMITID:
        def __get__(self):
            self.eMITID_branch.GetEntry(self.ientry, 0)
            return self.eMITID_value

    property eMVAIDH2TauWP:
        def __get__(self):
            self.eMVAIDH2TauWP_branch.GetEntry(self.ientry, 0)
            return self.eMVAIDH2TauWP_value

    property eMVANonTrig:
        def __get__(self):
            self.eMVANonTrig_branch.GetEntry(self.ientry, 0)
            return self.eMVANonTrig_value

    property eMVATrig:
        def __get__(self):
            self.eMVATrig_branch.GetEntry(self.ientry, 0)
            return self.eMVATrig_value

    property eMass:
        def __get__(self):
            self.eMass_branch.GetEntry(self.ientry, 0)
            return self.eMass_value

    property eMissingHits:
        def __get__(self):
            self.eMissingHits_branch.GetEntry(self.ientry, 0)
            return self.eMissingHits_value

    property eMtToMET:
        def __get__(self):
            self.eMtToMET_branch.GetEntry(self.ientry, 0)
            return self.eMtToMET_value

    property ePhi:
        def __get__(self):
            self.ePhi_branch.GetEntry(self.ientry, 0)
            return self.ePhi_value

    property ePt:
        def __get__(self):
            self.ePt_branch.GetEntry(self.ientry, 0)
            return self.ePt_value

    property eRelIso:
        def __get__(self):
            self.eRelIso_branch.GetEntry(self.ientry, 0)
            return self.eRelIso_value

    property eRelPFIsoDB:
        def __get__(self):
            self.eRelPFIsoDB_branch.GetEntry(self.ientry, 0)
            return self.eRelPFIsoDB_value

    property eVZ:
        def __get__(self):
            self.eVZ_branch.GetEntry(self.ientry, 0)
            return self.eVZ_value

    property eWWID:
        def __get__(self):
            self.eWWID_branch.GetEntry(self.ientry, 0)
            return self.eWWID_value

    property e_m_DPhi:
        def __get__(self):
            self.e_m_DPhi_branch.GetEntry(self.ientry, 0)
            return self.e_m_DPhi_value

    property e_m_DR:
        def __get__(self):
            self.e_m_DR_branch.GetEntry(self.ientry, 0)
            return self.e_m_DR_value

    property e_m_Mass:
        def __get__(self):
            self.e_m_Mass_branch.GetEntry(self.ientry, 0)
            return self.e_m_Mass_value

    property e_m_PZeta:
        def __get__(self):
            self.e_m_PZeta_branch.GetEntry(self.ientry, 0)
            return self.e_m_PZeta_value

    property e_m_PZetaVis:
        def __get__(self):
            self.e_m_PZetaVis_branch.GetEntry(self.ientry, 0)
            return self.e_m_PZetaVis_value

    property e_m_Pt:
        def __get__(self):
            self.e_m_Pt_branch.GetEntry(self.ientry, 0)
            return self.e_m_Pt_value

    property e_m_SS:
        def __get__(self):
            self.e_m_SS_branch.GetEntry(self.ientry, 0)
            return self.e_m_SS_value

    property e_m_Zcompat:
        def __get__(self):
            self.e_m_Zcompat_branch.GetEntry(self.ientry, 0)
            return self.e_m_Zcompat_value

    property e_t_DPhi:
        def __get__(self):
            self.e_t_DPhi_branch.GetEntry(self.ientry, 0)
            return self.e_t_DPhi_value

    property e_t_DR:
        def __get__(self):
            self.e_t_DR_branch.GetEntry(self.ientry, 0)
            return self.e_t_DR_value

    property e_t_Mass:
        def __get__(self):
            self.e_t_Mass_branch.GetEntry(self.ientry, 0)
            return self.e_t_Mass_value

    property e_t_PZeta:
        def __get__(self):
            self.e_t_PZeta_branch.GetEntry(self.ientry, 0)
            return self.e_t_PZeta_value

    property e_t_PZetaVis:
        def __get__(self):
            self.e_t_PZetaVis_branch.GetEntry(self.ientry, 0)
            return self.e_t_PZetaVis_value

    property e_t_Pt:
        def __get__(self):
            self.e_t_Pt_branch.GetEntry(self.ientry, 0)
            return self.e_t_Pt_value

    property e_t_SS:
        def __get__(self):
            self.e_t_SS_branch.GetEntry(self.ientry, 0)
            return self.e_t_SS_value

    property e_t_Zcompat:
        def __get__(self):
            self.e_t_Zcompat_branch.GetEntry(self.ientry, 0)
            return self.e_t_Zcompat_value

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

    property mAbsEta:
        def __get__(self):
            self.mAbsEta_branch.GetEntry(self.ientry, 0)
            return self.mAbsEta_value

    property mCharge:
        def __get__(self):
            self.mCharge_branch.GetEntry(self.ientry, 0)
            return self.mCharge_value

    property mD0:
        def __get__(self):
            self.mD0_branch.GetEntry(self.ientry, 0)
            return self.mD0_value

    property mDZ:
        def __get__(self):
            self.mDZ_branch.GetEntry(self.ientry, 0)
            return self.mDZ_value

    property mEta:
        def __get__(self):
            self.mEta_branch.GetEntry(self.ientry, 0)
            return self.mEta_value

    property mGlbTrkHits:
        def __get__(self):
            self.mGlbTrkHits_branch.GetEntry(self.ientry, 0)
            return self.mGlbTrkHits_value

    property mIP3DS:
        def __get__(self):
            self.mIP3DS_branch.GetEntry(self.ientry, 0)
            return self.mIP3DS_value

    property mIsGlobal:
        def __get__(self):
            self.mIsGlobal_branch.GetEntry(self.ientry, 0)
            return self.mIsGlobal_value

    property mIsTracker:
        def __get__(self):
            self.mIsTracker_branch.GetEntry(self.ientry, 0)
            return self.mIsTracker_value

    property mJetBtag:
        def __get__(self):
            self.mJetBtag_branch.GetEntry(self.ientry, 0)
            return self.mJetBtag_value

    property mJetPt:
        def __get__(self):
            self.mJetPt_branch.GetEntry(self.ientry, 0)
            return self.mJetPt_value

    property mMass:
        def __get__(self):
            self.mMass_branch.GetEntry(self.ientry, 0)
            return self.mMass_value

    property mMtToMET:
        def __get__(self):
            self.mMtToMET_branch.GetEntry(self.ientry, 0)
            return self.mMtToMET_value

    property mNormTrkChi2:
        def __get__(self):
            self.mNormTrkChi2_branch.GetEntry(self.ientry, 0)
            return self.mNormTrkChi2_value

    property mPFIDTight:
        def __get__(self):
            self.mPFIDTight_branch.GetEntry(self.ientry, 0)
            return self.mPFIDTight_value

    property mPhi:
        def __get__(self):
            self.mPhi_branch.GetEntry(self.ientry, 0)
            return self.mPhi_value

    property mPixHits:
        def __get__(self):
            self.mPixHits_branch.GetEntry(self.ientry, 0)
            return self.mPixHits_value

    property mPt:
        def __get__(self):
            self.mPt_branch.GetEntry(self.ientry, 0)
            return self.mPt_value

    property mPtUncorr:
        def __get__(self):
            self.mPtUncorr_branch.GetEntry(self.ientry, 0)
            return self.mPtUncorr_value

    property mRelPFIsoDB:
        def __get__(self):
            self.mRelPFIsoDB_branch.GetEntry(self.ientry, 0)
            return self.mRelPFIsoDB_value

    property mVBTFID:
        def __get__(self):
            self.mVBTFID_branch.GetEntry(self.ientry, 0)
            return self.mVBTFID_value

    property mVZ:
        def __get__(self):
            self.mVZ_branch.GetEntry(self.ientry, 0)
            return self.mVZ_value

    property mWWID:
        def __get__(self):
            self.mWWID_branch.GetEntry(self.ientry, 0)
            return self.mWWID_value

    property m_t_DPhi:
        def __get__(self):
            self.m_t_DPhi_branch.GetEntry(self.ientry, 0)
            return self.m_t_DPhi_value

    property m_t_DR:
        def __get__(self):
            self.m_t_DR_branch.GetEntry(self.ientry, 0)
            return self.m_t_DR_value

    property m_t_Mass:
        def __get__(self):
            self.m_t_Mass_branch.GetEntry(self.ientry, 0)
            return self.m_t_Mass_value

    property m_t_PZeta:
        def __get__(self):
            self.m_t_PZeta_branch.GetEntry(self.ientry, 0)
            return self.m_t_PZeta_value

    property m_t_PZetaVis:
        def __get__(self):
            self.m_t_PZetaVis_branch.GetEntry(self.ientry, 0)
            return self.m_t_PZetaVis_value

    property m_t_Pt:
        def __get__(self):
            self.m_t_Pt_branch.GetEntry(self.ientry, 0)
            return self.m_t_Pt_value

    property m_t_SS:
        def __get__(self):
            self.m_t_SS_branch.GetEntry(self.ientry, 0)
            return self.m_t_SS_value

    property m_t_Zcompat:
        def __get__(self):
            self.m_t_Zcompat_branch.GetEntry(self.ientry, 0)
            return self.m_t_Zcompat_value

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

    property nTruePU:
        def __get__(self):
            self.nTruePU_branch.GetEntry(self.ientry, 0)
            return self.nTruePU_value

    property nvtx:
        def __get__(self):
            self.nvtx_branch.GetEntry(self.ientry, 0)
            return self.nvtx_value

    property processID:
        def __get__(self):
            self.processID_branch.GetEntry(self.ientry, 0)
            return self.processID_value

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

    property tAbsEta:
        def __get__(self):
            self.tAbsEta_branch.GetEntry(self.ientry, 0)
            return self.tAbsEta_value

    property tAntiElectronLoose:
        def __get__(self):
            self.tAntiElectronLoose_branch.GetEntry(self.ientry, 0)
            return self.tAntiElectronLoose_value

    property tAntiElectronMVA:
        def __get__(self):
            self.tAntiElectronMVA_branch.GetEntry(self.ientry, 0)
            return self.tAntiElectronMVA_value

    property tAntiElectronMedium:
        def __get__(self):
            self.tAntiElectronMedium_branch.GetEntry(self.ientry, 0)
            return self.tAntiElectronMedium_value

    property tAntiElectronTight:
        def __get__(self):
            self.tAntiElectronTight_branch.GetEntry(self.ientry, 0)
            return self.tAntiElectronTight_value

    property tAntiMuonLoose:
        def __get__(self):
            self.tAntiMuonLoose_branch.GetEntry(self.ientry, 0)
            return self.tAntiMuonLoose_value

    property tAntiMuonTight:
        def __get__(self):
            self.tAntiMuonTight_branch.GetEntry(self.ientry, 0)
            return self.tAntiMuonTight_value

    property tCharge:
        def __get__(self):
            self.tCharge_branch.GetEntry(self.ientry, 0)
            return self.tCharge_value

    property tDZ:
        def __get__(self):
            self.tDZ_branch.GetEntry(self.ientry, 0)
            return self.tDZ_value

    property tDecayFinding:
        def __get__(self):
            self.tDecayFinding_branch.GetEntry(self.ientry, 0)
            return self.tDecayFinding_value

    property tDecayMode:
        def __get__(self):
            self.tDecayMode_branch.GetEntry(self.ientry, 0)
            return self.tDecayMode_value

    property tEta:
        def __get__(self):
            self.tEta_branch.GetEntry(self.ientry, 0)
            return self.tEta_value

    property tGenDecayMode:
        def __get__(self):
            self.tGenDecayMode_branch.GetEntry(self.ientry, 0)
            return self.tGenDecayMode_value

    property tIP3DS:
        def __get__(self):
            self.tIP3DS_branch.GetEntry(self.ientry, 0)
            return self.tIP3DS_value

    property tJetBtag:
        def __get__(self):
            self.tJetBtag_branch.GetEntry(self.ientry, 0)
            return self.tJetBtag_value

    property tJetPt:
        def __get__(self):
            self.tJetPt_branch.GetEntry(self.ientry, 0)
            return self.tJetPt_value

    property tLeadTrackPt:
        def __get__(self):
            self.tLeadTrackPt_branch.GetEntry(self.ientry, 0)
            return self.tLeadTrackPt_value

    property tLooseIso:
        def __get__(self):
            self.tLooseIso_branch.GetEntry(self.ientry, 0)
            return self.tLooseIso_value

    property tLooseMVAIso:
        def __get__(self):
            self.tLooseMVAIso_branch.GetEntry(self.ientry, 0)
            return self.tLooseMVAIso_value

    property tMass:
        def __get__(self):
            self.tMass_branch.GetEntry(self.ientry, 0)
            return self.tMass_value

    property tMediumIso:
        def __get__(self):
            self.tMediumIso_branch.GetEntry(self.ientry, 0)
            return self.tMediumIso_value

    property tMediumMVAIso:
        def __get__(self):
            self.tMediumMVAIso_branch.GetEntry(self.ientry, 0)
            return self.tMediumMVAIso_value

    property tMtToMET:
        def __get__(self):
            self.tMtToMET_branch.GetEntry(self.ientry, 0)
            return self.tMtToMET_value

    property tMuOverlap:
        def __get__(self):
            self.tMuOverlap_branch.GetEntry(self.ientry, 0)
            return self.tMuOverlap_value

    property tPhi:
        def __get__(self):
            self.tPhi_branch.GetEntry(self.ientry, 0)
            return self.tPhi_value

    property tPt:
        def __get__(self):
            self.tPt_branch.GetEntry(self.ientry, 0)
            return self.tPt_value

    property tTNPId:
        def __get__(self):
            self.tTNPId_branch.GetEntry(self.ientry, 0)
            return self.tTNPId_value

    property tVZ:
        def __get__(self):
            self.tVZ_branch.GetEntry(self.ientry, 0)
            return self.tVZ_value

    property tauVetoPt20:
        def __get__(self):
            self.tauVetoPt20_branch.GetEntry(self.ientry, 0)
            return self.tauVetoPt20_value

    property idx:
        def __get__(self):
            self.idx_branch.GetEntry(self.ientry, 0)
            return self.idx_value



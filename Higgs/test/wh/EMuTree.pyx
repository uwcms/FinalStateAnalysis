

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
        TTree* GetTree()
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
        void UpdateFormulaLeaves()
        void SetTree(TTree*)

from cpython cimport PyCObject_AsVoidPtr

cdef class EMuTree:
    # Pointers to tree (may be a chain), current active tree, and current entry
    cdef TTree* tree
    cdef TTree* currentTree
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

    cdef TBranch* eSCEnergy_branch
    cdef float eSCEnergy_value

    cdef TBranch* eSCEta_branch
    cdef float eSCEta_value

    cdef TBranch* eSCPhi_branch
    cdef float eSCPhi_value

    cdef TBranch* eVZ_branch
    cdef float eVZ_value

    cdef TBranch* eVetoCicTightIso_branch
    cdef float eVetoCicTightIso_value

    cdef TBranch* eVetoMVAIso_branch
    cdef float eVetoMVAIso_value

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

    cdef TBranch* puWeightData2011AB_branch
    cdef float puWeightData2011AB_value

    cdef TBranch* puWeightData2012A_branch
    cdef float puWeightData2012A_value

    cdef TBranch* puWeightData2012AB_branch
    cdef float puWeightData2012AB_value

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

    cdef TBranch* vbfDeta_branch
    cdef float vbfDeta_value

    cdef TBranch* vbfJetVeto20_branch
    cdef float vbfJetVeto20_value

    cdef TBranch* vbfJetVeto30_branch
    cdef float vbfJetVeto30_value

    cdef TBranch* vbfMVA_branch
    cdef float vbfMVA_value

    cdef TBranch* vbfMass_branch
    cdef float vbfMass_value

    cdef TBranch* vbfNJets_branch
    cdef float vbfNJets_value

    cdef TBranch* idx_branch
    cdef int idx_value


    def __cinit__(self, ttree):
        print "cinit"
        # Constructor from a ROOT.TTree
        from ROOT import AsCObject
        self.tree = <TTree*>PyCObject_AsVoidPtr(AsCObject(ttree))
        self.ientry = 0
        self.load_entry(0)

    cdef load_entry(self, long i):
        print "load", i
        # Load the correct tree and setup the branches
        self.tree.LoadTree(i)
        new_tree = self.tree.GetTree()
        if new_tree != self.currentTree:
            self.currentTree = new_tree
            self.setup_branches(new_tree)

    cdef setup_branches(self, TTree* the_tree):
        print "setup"

        #print "making LT"
        self.LT_branch = the_tree.GetBranch("LT")
        self.LT_branch.SetAddress(<void*>&self.LT_value)

        #print "making Mass"
        self.Mass_branch = the_tree.GetBranch("Mass")
        self.Mass_branch.SetAddress(<void*>&self.Mass_value)

        #print "making Pt"
        self.Pt_branch = the_tree.GetBranch("Pt")
        self.Pt_branch.SetAddress(<void*>&self.Pt_value)

        #print "making bjetCSVVeto"
        self.bjetCSVVeto_branch = the_tree.GetBranch("bjetCSVVeto")
        self.bjetCSVVeto_branch.SetAddress(<void*>&self.bjetCSVVeto_value)

        #print "making bjetVeto"
        self.bjetVeto_branch = the_tree.GetBranch("bjetVeto")
        self.bjetVeto_branch.SetAddress(<void*>&self.bjetVeto_value)

        #print "making charge"
        self.charge_branch = the_tree.GetBranch("charge")
        self.charge_branch.SetAddress(<void*>&self.charge_value)

        #print "making doubleEExtraGroup"
        self.doubleEExtraGroup_branch = the_tree.GetBranch("doubleEExtraGroup")
        self.doubleEExtraGroup_branch.SetAddress(<void*>&self.doubleEExtraGroup_value)

        #print "making doubleEExtraPass"
        self.doubleEExtraPass_branch = the_tree.GetBranch("doubleEExtraPass")
        self.doubleEExtraPass_branch.SetAddress(<void*>&self.doubleEExtraPass_value)

        #print "making doubleEExtraPrescale"
        self.doubleEExtraPrescale_branch = the_tree.GetBranch("doubleEExtraPrescale")
        self.doubleEExtraPrescale_branch.SetAddress(<void*>&self.doubleEExtraPrescale_value)

        #print "making doubleEGroup"
        self.doubleEGroup_branch = the_tree.GetBranch("doubleEGroup")
        self.doubleEGroup_branch.SetAddress(<void*>&self.doubleEGroup_value)

        #print "making doubleEPass"
        self.doubleEPass_branch = the_tree.GetBranch("doubleEPass")
        self.doubleEPass_branch.SetAddress(<void*>&self.doubleEPass_value)

        #print "making doubleEPrescale"
        self.doubleEPrescale_branch = the_tree.GetBranch("doubleEPrescale")
        self.doubleEPrescale_branch.SetAddress(<void*>&self.doubleEPrescale_value)

        #print "making doubleMuGroup"
        self.doubleMuGroup_branch = the_tree.GetBranch("doubleMuGroup")
        self.doubleMuGroup_branch.SetAddress(<void*>&self.doubleMuGroup_value)

        #print "making doubleMuPass"
        self.doubleMuPass_branch = the_tree.GetBranch("doubleMuPass")
        self.doubleMuPass_branch.SetAddress(<void*>&self.doubleMuPass_value)

        #print "making doubleMuPrescale"
        self.doubleMuPrescale_branch = the_tree.GetBranch("doubleMuPrescale")
        self.doubleMuPrescale_branch.SetAddress(<void*>&self.doubleMuPrescale_value)

        #print "making doubleMuTrkGroup"
        self.doubleMuTrkGroup_branch = the_tree.GetBranch("doubleMuTrkGroup")
        self.doubleMuTrkGroup_branch.SetAddress(<void*>&self.doubleMuTrkGroup_value)

        #print "making doubleMuTrkPass"
        self.doubleMuTrkPass_branch = the_tree.GetBranch("doubleMuTrkPass")
        self.doubleMuTrkPass_branch.SetAddress(<void*>&self.doubleMuTrkPass_value)

        #print "making doubleMuTrkPrescale"
        self.doubleMuTrkPrescale_branch = the_tree.GetBranch("doubleMuTrkPrescale")
        self.doubleMuTrkPrescale_branch.SetAddress(<void*>&self.doubleMuTrkPrescale_value)

        #print "making eAbsEta"
        self.eAbsEta_branch = the_tree.GetBranch("eAbsEta")
        self.eAbsEta_branch.SetAddress(<void*>&self.eAbsEta_value)

        #print "making eCharge"
        self.eCharge_branch = the_tree.GetBranch("eCharge")
        self.eCharge_branch.SetAddress(<void*>&self.eCharge_value)

        #print "making eChargeIdLoose"
        self.eChargeIdLoose_branch = the_tree.GetBranch("eChargeIdLoose")
        self.eChargeIdLoose_branch.SetAddress(<void*>&self.eChargeIdLoose_value)

        #print "making eChargeIdMed"
        self.eChargeIdMed_branch = the_tree.GetBranch("eChargeIdMed")
        self.eChargeIdMed_branch.SetAddress(<void*>&self.eChargeIdMed_value)

        #print "making eChargeIdTight"
        self.eChargeIdTight_branch = the_tree.GetBranch("eChargeIdTight")
        self.eChargeIdTight_branch.SetAddress(<void*>&self.eChargeIdTight_value)

        #print "making eCiCTight"
        self.eCiCTight_branch = the_tree.GetBranch("eCiCTight")
        self.eCiCTight_branch.SetAddress(<void*>&self.eCiCTight_value)

        #print "making eDZ"
        self.eDZ_branch = the_tree.GetBranch("eDZ")
        self.eDZ_branch.SetAddress(<void*>&self.eDZ_value)

        #print "making eEta"
        self.eEta_branch = the_tree.GetBranch("eEta")
        self.eEta_branch.SetAddress(<void*>&self.eEta_value)

        #print "making eHasConversion"
        self.eHasConversion_branch = the_tree.GetBranch("eHasConversion")
        self.eHasConversion_branch.SetAddress(<void*>&self.eHasConversion_value)

        #print "making eIP3DS"
        self.eIP3DS_branch = the_tree.GetBranch("eIP3DS")
        self.eIP3DS_branch.SetAddress(<void*>&self.eIP3DS_value)

        #print "making eJetBtag"
        self.eJetBtag_branch = the_tree.GetBranch("eJetBtag")
        self.eJetBtag_branch.SetAddress(<void*>&self.eJetBtag_value)

        #print "making eJetPt"
        self.eJetPt_branch = the_tree.GetBranch("eJetPt")
        self.eJetPt_branch.SetAddress(<void*>&self.eJetPt_value)

        #print "making eMITID"
        self.eMITID_branch = the_tree.GetBranch("eMITID")
        self.eMITID_branch.SetAddress(<void*>&self.eMITID_value)

        #print "making eMVAIDH2TauWP"
        self.eMVAIDH2TauWP_branch = the_tree.GetBranch("eMVAIDH2TauWP")
        self.eMVAIDH2TauWP_branch.SetAddress(<void*>&self.eMVAIDH2TauWP_value)

        #print "making eMVANonTrig"
        self.eMVANonTrig_branch = the_tree.GetBranch("eMVANonTrig")
        self.eMVANonTrig_branch.SetAddress(<void*>&self.eMVANonTrig_value)

        #print "making eMVATrig"
        self.eMVATrig_branch = the_tree.GetBranch("eMVATrig")
        self.eMVATrig_branch.SetAddress(<void*>&self.eMVATrig_value)

        #print "making eMass"
        self.eMass_branch = the_tree.GetBranch("eMass")
        self.eMass_branch.SetAddress(<void*>&self.eMass_value)

        #print "making eMissingHits"
        self.eMissingHits_branch = the_tree.GetBranch("eMissingHits")
        self.eMissingHits_branch.SetAddress(<void*>&self.eMissingHits_value)

        #print "making eMtToMET"
        self.eMtToMET_branch = the_tree.GetBranch("eMtToMET")
        self.eMtToMET_branch.SetAddress(<void*>&self.eMtToMET_value)

        #print "making ePhi"
        self.ePhi_branch = the_tree.GetBranch("ePhi")
        self.ePhi_branch.SetAddress(<void*>&self.ePhi_value)

        #print "making ePt"
        self.ePt_branch = the_tree.GetBranch("ePt")
        self.ePt_branch.SetAddress(<void*>&self.ePt_value)

        #print "making eRelIso"
        self.eRelIso_branch = the_tree.GetBranch("eRelIso")
        self.eRelIso_branch.SetAddress(<void*>&self.eRelIso_value)

        #print "making eRelPFIsoDB"
        self.eRelPFIsoDB_branch = the_tree.GetBranch("eRelPFIsoDB")
        self.eRelPFIsoDB_branch.SetAddress(<void*>&self.eRelPFIsoDB_value)

        #print "making eSCEnergy"
        self.eSCEnergy_branch = the_tree.GetBranch("eSCEnergy")
        self.eSCEnergy_branch.SetAddress(<void*>&self.eSCEnergy_value)

        #print "making eSCEta"
        self.eSCEta_branch = the_tree.GetBranch("eSCEta")
        self.eSCEta_branch.SetAddress(<void*>&self.eSCEta_value)

        #print "making eSCPhi"
        self.eSCPhi_branch = the_tree.GetBranch("eSCPhi")
        self.eSCPhi_branch.SetAddress(<void*>&self.eSCPhi_value)

        #print "making eVZ"
        self.eVZ_branch = the_tree.GetBranch("eVZ")
        self.eVZ_branch.SetAddress(<void*>&self.eVZ_value)

        #print "making eVetoCicTightIso"
        self.eVetoCicTightIso_branch = the_tree.GetBranch("eVetoCicTightIso")
        self.eVetoCicTightIso_branch.SetAddress(<void*>&self.eVetoCicTightIso_value)

        #print "making eVetoMVAIso"
        self.eVetoMVAIso_branch = the_tree.GetBranch("eVetoMVAIso")
        self.eVetoMVAIso_branch.SetAddress(<void*>&self.eVetoMVAIso_value)

        #print "making eWWID"
        self.eWWID_branch = the_tree.GetBranch("eWWID")
        self.eWWID_branch.SetAddress(<void*>&self.eWWID_value)

        #print "making e_m_DPhi"
        self.e_m_DPhi_branch = the_tree.GetBranch("e_m_DPhi")
        self.e_m_DPhi_branch.SetAddress(<void*>&self.e_m_DPhi_value)

        #print "making e_m_DR"
        self.e_m_DR_branch = the_tree.GetBranch("e_m_DR")
        self.e_m_DR_branch.SetAddress(<void*>&self.e_m_DR_value)

        #print "making e_m_Mass"
        self.e_m_Mass_branch = the_tree.GetBranch("e_m_Mass")
        self.e_m_Mass_branch.SetAddress(<void*>&self.e_m_Mass_value)

        #print "making e_m_PZeta"
        self.e_m_PZeta_branch = the_tree.GetBranch("e_m_PZeta")
        self.e_m_PZeta_branch.SetAddress(<void*>&self.e_m_PZeta_value)

        #print "making e_m_PZetaVis"
        self.e_m_PZetaVis_branch = the_tree.GetBranch("e_m_PZetaVis")
        self.e_m_PZetaVis_branch.SetAddress(<void*>&self.e_m_PZetaVis_value)

        #print "making e_m_Pt"
        self.e_m_Pt_branch = the_tree.GetBranch("e_m_Pt")
        self.e_m_Pt_branch.SetAddress(<void*>&self.e_m_Pt_value)

        #print "making e_m_SS"
        self.e_m_SS_branch = the_tree.GetBranch("e_m_SS")
        self.e_m_SS_branch.SetAddress(<void*>&self.e_m_SS_value)

        #print "making e_m_Zcompat"
        self.e_m_Zcompat_branch = the_tree.GetBranch("e_m_Zcompat")
        self.e_m_Zcompat_branch.SetAddress(<void*>&self.e_m_Zcompat_value)

        #print "making evt"
        self.evt_branch = the_tree.GetBranch("evt")
        self.evt_branch.SetAddress(<void*>&self.evt_value)

        #print "making isdata"
        self.isdata_branch = the_tree.GetBranch("isdata")
        self.isdata_branch.SetAddress(<void*>&self.isdata_value)

        #print "making isoMuGroup"
        self.isoMuGroup_branch = the_tree.GetBranch("isoMuGroup")
        self.isoMuGroup_branch.SetAddress(<void*>&self.isoMuGroup_value)

        #print "making isoMuPass"
        self.isoMuPass_branch = the_tree.GetBranch("isoMuPass")
        self.isoMuPass_branch.SetAddress(<void*>&self.isoMuPass_value)

        #print "making isoMuPrescale"
        self.isoMuPrescale_branch = the_tree.GetBranch("isoMuPrescale")
        self.isoMuPrescale_branch.SetAddress(<void*>&self.isoMuPrescale_value)

        #print "making jetVeto20"
        self.jetVeto20_branch = the_tree.GetBranch("jetVeto20")
        self.jetVeto20_branch.SetAddress(<void*>&self.jetVeto20_value)

        #print "making jetVeto40"
        self.jetVeto40_branch = the_tree.GetBranch("jetVeto40")
        self.jetVeto40_branch.SetAddress(<void*>&self.jetVeto40_value)

        #print "making lumi"
        self.lumi_branch = the_tree.GetBranch("lumi")
        self.lumi_branch.SetAddress(<void*>&self.lumi_value)

        #print "making mAbsEta"
        self.mAbsEta_branch = the_tree.GetBranch("mAbsEta")
        self.mAbsEta_branch.SetAddress(<void*>&self.mAbsEta_value)

        #print "making mCharge"
        self.mCharge_branch = the_tree.GetBranch("mCharge")
        self.mCharge_branch.SetAddress(<void*>&self.mCharge_value)

        #print "making mD0"
        self.mD0_branch = the_tree.GetBranch("mD0")
        self.mD0_branch.SetAddress(<void*>&self.mD0_value)

        #print "making mDZ"
        self.mDZ_branch = the_tree.GetBranch("mDZ")
        self.mDZ_branch.SetAddress(<void*>&self.mDZ_value)

        #print "making mEta"
        self.mEta_branch = the_tree.GetBranch("mEta")
        self.mEta_branch.SetAddress(<void*>&self.mEta_value)

        #print "making mGlbTrkHits"
        self.mGlbTrkHits_branch = the_tree.GetBranch("mGlbTrkHits")
        self.mGlbTrkHits_branch.SetAddress(<void*>&self.mGlbTrkHits_value)

        #print "making mIP3DS"
        self.mIP3DS_branch = the_tree.GetBranch("mIP3DS")
        self.mIP3DS_branch.SetAddress(<void*>&self.mIP3DS_value)

        #print "making mIsGlobal"
        self.mIsGlobal_branch = the_tree.GetBranch("mIsGlobal")
        self.mIsGlobal_branch.SetAddress(<void*>&self.mIsGlobal_value)

        #print "making mIsTracker"
        self.mIsTracker_branch = the_tree.GetBranch("mIsTracker")
        self.mIsTracker_branch.SetAddress(<void*>&self.mIsTracker_value)

        #print "making mJetBtag"
        self.mJetBtag_branch = the_tree.GetBranch("mJetBtag")
        self.mJetBtag_branch.SetAddress(<void*>&self.mJetBtag_value)

        #print "making mJetPt"
        self.mJetPt_branch = the_tree.GetBranch("mJetPt")
        self.mJetPt_branch.SetAddress(<void*>&self.mJetPt_value)

        #print "making mMass"
        self.mMass_branch = the_tree.GetBranch("mMass")
        self.mMass_branch.SetAddress(<void*>&self.mMass_value)

        #print "making mMtToMET"
        self.mMtToMET_branch = the_tree.GetBranch("mMtToMET")
        self.mMtToMET_branch.SetAddress(<void*>&self.mMtToMET_value)

        #print "making mNormTrkChi2"
        self.mNormTrkChi2_branch = the_tree.GetBranch("mNormTrkChi2")
        self.mNormTrkChi2_branch.SetAddress(<void*>&self.mNormTrkChi2_value)

        #print "making mPFIDTight"
        self.mPFIDTight_branch = the_tree.GetBranch("mPFIDTight")
        self.mPFIDTight_branch.SetAddress(<void*>&self.mPFIDTight_value)

        #print "making mPhi"
        self.mPhi_branch = the_tree.GetBranch("mPhi")
        self.mPhi_branch.SetAddress(<void*>&self.mPhi_value)

        #print "making mPixHits"
        self.mPixHits_branch = the_tree.GetBranch("mPixHits")
        self.mPixHits_branch.SetAddress(<void*>&self.mPixHits_value)

        #print "making mPt"
        self.mPt_branch = the_tree.GetBranch("mPt")
        self.mPt_branch.SetAddress(<void*>&self.mPt_value)

        #print "making mPtUncorr"
        self.mPtUncorr_branch = the_tree.GetBranch("mPtUncorr")
        self.mPtUncorr_branch.SetAddress(<void*>&self.mPtUncorr_value)

        #print "making mRelPFIsoDB"
        self.mRelPFIsoDB_branch = the_tree.GetBranch("mRelPFIsoDB")
        self.mRelPFIsoDB_branch.SetAddress(<void*>&self.mRelPFIsoDB_value)

        #print "making mVBTFID"
        self.mVBTFID_branch = the_tree.GetBranch("mVBTFID")
        self.mVBTFID_branch.SetAddress(<void*>&self.mVBTFID_value)

        #print "making mVZ"
        self.mVZ_branch = the_tree.GetBranch("mVZ")
        self.mVZ_branch.SetAddress(<void*>&self.mVZ_value)

        #print "making mWWID"
        self.mWWID_branch = the_tree.GetBranch("mWWID")
        self.mWWID_branch.SetAddress(<void*>&self.mWWID_value)

        #print "making metEt"
        self.metEt_branch = the_tree.GetBranch("metEt")
        self.metEt_branch.SetAddress(<void*>&self.metEt_value)

        #print "making metPhi"
        self.metPhi_branch = the_tree.GetBranch("metPhi")
        self.metPhi_branch.SetAddress(<void*>&self.metPhi_value)

        #print "making metSignificance"
        self.metSignificance_branch = the_tree.GetBranch("metSignificance")
        self.metSignificance_branch.SetAddress(<void*>&self.metSignificance_value)

        #print "making mu17ele8Group"
        self.mu17ele8Group_branch = the_tree.GetBranch("mu17ele8Group")
        self.mu17ele8Group_branch.SetAddress(<void*>&self.mu17ele8Group_value)

        #print "making mu17ele8Pass"
        self.mu17ele8Pass_branch = the_tree.GetBranch("mu17ele8Pass")
        self.mu17ele8Pass_branch.SetAddress(<void*>&self.mu17ele8Pass_value)

        #print "making mu17ele8Prescale"
        self.mu17ele8Prescale_branch = the_tree.GetBranch("mu17ele8Prescale")
        self.mu17ele8Prescale_branch.SetAddress(<void*>&self.mu17ele8Prescale_value)

        #print "making mu8ele17Group"
        self.mu8ele17Group_branch = the_tree.GetBranch("mu8ele17Group")
        self.mu8ele17Group_branch.SetAddress(<void*>&self.mu8ele17Group_value)

        #print "making mu8ele17Pass"
        self.mu8ele17Pass_branch = the_tree.GetBranch("mu8ele17Pass")
        self.mu8ele17Pass_branch.SetAddress(<void*>&self.mu8ele17Pass_value)

        #print "making mu8ele17Prescale"
        self.mu8ele17Prescale_branch = the_tree.GetBranch("mu8ele17Prescale")
        self.mu8ele17Prescale_branch.SetAddress(<void*>&self.mu8ele17Prescale_value)

        #print "making muGlbIsoVetoPt10"
        self.muGlbIsoVetoPt10_branch = the_tree.GetBranch("muGlbIsoVetoPt10")
        self.muGlbIsoVetoPt10_branch.SetAddress(<void*>&self.muGlbIsoVetoPt10_value)

        #print "making muVetoPt5"
        self.muVetoPt5_branch = the_tree.GetBranch("muVetoPt5")
        self.muVetoPt5_branch.SetAddress(<void*>&self.muVetoPt5_value)

        #print "making nTruePU"
        self.nTruePU_branch = the_tree.GetBranch("nTruePU")
        self.nTruePU_branch.SetAddress(<void*>&self.nTruePU_value)

        #print "making nvtx"
        self.nvtx_branch = the_tree.GetBranch("nvtx")
        self.nvtx_branch.SetAddress(<void*>&self.nvtx_value)

        #print "making processID"
        self.processID_branch = the_tree.GetBranch("processID")
        self.processID_branch.SetAddress(<void*>&self.processID_value)

        #print "making puWeightData2011AB"
        self.puWeightData2011AB_branch = the_tree.GetBranch("puWeightData2011AB")
        self.puWeightData2011AB_branch.SetAddress(<void*>&self.puWeightData2011AB_value)

        #print "making puWeightData2012A"
        self.puWeightData2012A_branch = the_tree.GetBranch("puWeightData2012A")
        self.puWeightData2012A_branch.SetAddress(<void*>&self.puWeightData2012A_value)

        #print "making puWeightData2012AB"
        self.puWeightData2012AB_branch = the_tree.GetBranch("puWeightData2012AB")
        self.puWeightData2012AB_branch.SetAddress(<void*>&self.puWeightData2012AB_value)

        #print "making rho"
        self.rho_branch = the_tree.GetBranch("rho")
        self.rho_branch.SetAddress(<void*>&self.rho_value)

        #print "making run"
        self.run_branch = the_tree.GetBranch("run")
        self.run_branch.SetAddress(<void*>&self.run_value)

        #print "making singleMuGroup"
        self.singleMuGroup_branch = the_tree.GetBranch("singleMuGroup")
        self.singleMuGroup_branch.SetAddress(<void*>&self.singleMuGroup_value)

        #print "making singleMuPass"
        self.singleMuPass_branch = the_tree.GetBranch("singleMuPass")
        self.singleMuPass_branch.SetAddress(<void*>&self.singleMuPass_value)

        #print "making singleMuPrescale"
        self.singleMuPrescale_branch = the_tree.GetBranch("singleMuPrescale")
        self.singleMuPrescale_branch.SetAddress(<void*>&self.singleMuPrescale_value)

        #print "making tauVetoPt20"
        self.tauVetoPt20_branch = the_tree.GetBranch("tauVetoPt20")
        self.tauVetoPt20_branch.SetAddress(<void*>&self.tauVetoPt20_value)

        #print "making vbfDeta"
        self.vbfDeta_branch = the_tree.GetBranch("vbfDeta")
        self.vbfDeta_branch.SetAddress(<void*>&self.vbfDeta_value)

        #print "making vbfJetVeto20"
        self.vbfJetVeto20_branch = the_tree.GetBranch("vbfJetVeto20")
        self.vbfJetVeto20_branch.SetAddress(<void*>&self.vbfJetVeto20_value)

        #print "making vbfJetVeto30"
        self.vbfJetVeto30_branch = the_tree.GetBranch("vbfJetVeto30")
        self.vbfJetVeto30_branch.SetAddress(<void*>&self.vbfJetVeto30_value)

        #print "making vbfMVA"
        self.vbfMVA_branch = the_tree.GetBranch("vbfMVA")
        self.vbfMVA_branch.SetAddress(<void*>&self.vbfMVA_value)

        #print "making vbfMass"
        self.vbfMass_branch = the_tree.GetBranch("vbfMass")
        self.vbfMass_branch.SetAddress(<void*>&self.vbfMass_value)

        #print "making vbfNJets"
        self.vbfNJets_branch = the_tree.GetBranch("vbfNJets")
        self.vbfNJets_branch.SetAddress(<void*>&self.vbfNJets_value)

        #print "making idx"
        self.idx_branch = the_tree.GetBranch("idx")
        self.idx_branch.SetAddress(<void*>&self.idx_value)


    # Iterating over the tree
    def __iter__(self):
        self.ientry = 0
        while self.ientry < self.tree.GetEntries():
            self.load_entry(self.ientry)
            yield self
            self.ientry += 1

    # Iterate over rows which pass the filter
    def where(self, filter):
        print "where"
        cdef TTreeFormula* formula = new TTreeFormula(
            "cyiter", filter, self.tree)
        self.ientry = 0
        cdef TTree* currentTree = self.tree.GetTree()
        while self.ientry < self.tree.GetEntries():
            self.tree.LoadTree(self.ientry)
            if currentTree != self.tree.GetTree():
                currentTree = self.tree.GetTree()
                formula.SetTree(currentTree)
                formula.UpdateFormulaLeaves()
            if formula.EvalInstance(0, NULL):
                yield self
            self.ientry += 1
        del formula

    # Getting/setting the Tree entry number
    property entry:
        def __get__(self):
            return self.ientry
        def __set__(self, int i):
            print i
            self.ientry = i
            self.load_entry(i)

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

    property eSCEnergy:
        def __get__(self):
            self.eSCEnergy_branch.GetEntry(self.ientry, 0)
            return self.eSCEnergy_value

    property eSCEta:
        def __get__(self):
            self.eSCEta_branch.GetEntry(self.ientry, 0)
            return self.eSCEta_value

    property eSCPhi:
        def __get__(self):
            self.eSCPhi_branch.GetEntry(self.ientry, 0)
            return self.eSCPhi_value

    property eVZ:
        def __get__(self):
            self.eVZ_branch.GetEntry(self.ientry, 0)
            return self.eVZ_value

    property eVetoCicTightIso:
        def __get__(self):
            self.eVetoCicTightIso_branch.GetEntry(self.ientry, 0)
            return self.eVetoCicTightIso_value

    property eVetoMVAIso:
        def __get__(self):
            self.eVetoMVAIso_branch.GetEntry(self.ientry, 0)
            return self.eVetoMVAIso_value

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

    property puWeightData2011AB:
        def __get__(self):
            self.puWeightData2011AB_branch.GetEntry(self.ientry, 0)
            return self.puWeightData2011AB_value

    property puWeightData2012A:
        def __get__(self):
            self.puWeightData2012A_branch.GetEntry(self.ientry, 0)
            return self.puWeightData2012A_value

    property puWeightData2012AB:
        def __get__(self):
            self.puWeightData2012AB_branch.GetEntry(self.ientry, 0)
            return self.puWeightData2012AB_value

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

    property vbfDeta:
        def __get__(self):
            self.vbfDeta_branch.GetEntry(self.ientry, 0)
            return self.vbfDeta_value

    property vbfJetVeto20:
        def __get__(self):
            self.vbfJetVeto20_branch.GetEntry(self.ientry, 0)
            return self.vbfJetVeto20_value

    property vbfJetVeto30:
        def __get__(self):
            self.vbfJetVeto30_branch.GetEntry(self.ientry, 0)
            return self.vbfJetVeto30_value

    property vbfMVA:
        def __get__(self):
            self.vbfMVA_branch.GetEntry(self.ientry, 0)
            return self.vbfMVA_value

    property vbfMass:
        def __get__(self):
            self.vbfMass_branch.GetEntry(self.ientry, 0)
            return self.vbfMass_value

    property vbfNJets:
        def __get__(self):
            self.vbfNJets_branch.GetEntry(self.ientry, 0)
            return self.vbfNJets_value

    property idx:
        def __get__(self):
            self.idx_branch.GetEntry(self.ientry, 0)
            return self.idx_value



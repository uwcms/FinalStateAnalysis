

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

cdef class MuTauTree:
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

    cdef TBranch* muon_tau_DPhi_branch
    cdef float muon_tau_DPhi_value

    cdef TBranch* muon_tau_DR_branch
    cdef float muon_tau_DR_value

    cdef TBranch* muon_tau_Mass_branch
    cdef float muon_tau_Mass_value

    cdef TBranch* muon_tau_PZeta_branch
    cdef float muon_tau_PZeta_value

    cdef TBranch* muon_tau_PZetaVis_branch
    cdef float muon_tau_PZetaVis_value

    cdef TBranch* muon_tau_Pt_branch
    cdef float muon_tau_Pt_value

    cdef TBranch* muon_tau_SS_branch
    cdef float muon_tau_SS_value

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

    cdef TBranch* tauAbsEta_branch
    cdef float tauAbsEta_value

    cdef TBranch* tauAntiElectronLoose_branch
    cdef float tauAntiElectronLoose_value

    cdef TBranch* tauAntiElectronMVA_branch
    cdef float tauAntiElectronMVA_value

    cdef TBranch* tauAntiElectronMedium_branch
    cdef float tauAntiElectronMedium_value

    cdef TBranch* tauAntiElectronTight_branch
    cdef float tauAntiElectronTight_value

    cdef TBranch* tauAntiMuonLoose_branch
    cdef float tauAntiMuonLoose_value

    cdef TBranch* tauAntiMuonTight_branch
    cdef float tauAntiMuonTight_value

    cdef TBranch* tauCharge_branch
    cdef float tauCharge_value

    cdef TBranch* tauDZ_branch
    cdef float tauDZ_value

    cdef TBranch* tauDecayFinding_branch
    cdef float tauDecayFinding_value

    cdef TBranch* tauDecayMode_branch
    cdef float tauDecayMode_value

    cdef TBranch* tauEta_branch
    cdef float tauEta_value

    cdef TBranch* tauGenDecayMode_branch
    cdef float tauGenDecayMode_value

    cdef TBranch* tauIP3DS_branch
    cdef float tauIP3DS_value

    cdef TBranch* tauJetBtag_branch
    cdef float tauJetBtag_value

    cdef TBranch* tauJetPt_branch
    cdef float tauJetPt_value

    cdef TBranch* tauLeadTrackPt_branch
    cdef float tauLeadTrackPt_value

    cdef TBranch* tauLooseIso_branch
    cdef float tauLooseIso_value

    cdef TBranch* tauLooseMVAIso_branch
    cdef float tauLooseMVAIso_value

    cdef TBranch* tauMass_branch
    cdef float tauMass_value

    cdef TBranch* tauMediumIso_branch
    cdef float tauMediumIso_value

    cdef TBranch* tauMediumMVAIso_branch
    cdef float tauMediumMVAIso_value

    cdef TBranch* tauMuOverlap_branch
    cdef float tauMuOverlap_value

    cdef TBranch* tauPhi_branch
    cdef float tauPhi_value

    cdef TBranch* tauPt_branch
    cdef float tauPt_value

    cdef TBranch* tauTNPId_branch
    cdef float tauTNPId_value

    cdef TBranch* tauVZ_branch
    cdef float tauVZ_value

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

        self.muon_tau_DPhi_branch = self.tree.GetBranch("muon_tau_DPhi")
        self.muon_tau_DPhi_branch.SetAddress(<void*>&self.muon_tau_DPhi_value)

        self.muon_tau_DR_branch = self.tree.GetBranch("muon_tau_DR")
        self.muon_tau_DR_branch.SetAddress(<void*>&self.muon_tau_DR_value)

        self.muon_tau_Mass_branch = self.tree.GetBranch("muon_tau_Mass")
        self.muon_tau_Mass_branch.SetAddress(<void*>&self.muon_tau_Mass_value)

        self.muon_tau_PZeta_branch = self.tree.GetBranch("muon_tau_PZeta")
        self.muon_tau_PZeta_branch.SetAddress(<void*>&self.muon_tau_PZeta_value)

        self.muon_tau_PZetaVis_branch = self.tree.GetBranch("muon_tau_PZetaVis")
        self.muon_tau_PZetaVis_branch.SetAddress(<void*>&self.muon_tau_PZetaVis_value)

        self.muon_tau_Pt_branch = self.tree.GetBranch("muon_tau_Pt")
        self.muon_tau_Pt_branch.SetAddress(<void*>&self.muon_tau_Pt_value)

        self.muon_tau_SS_branch = self.tree.GetBranch("muon_tau_SS")
        self.muon_tau_SS_branch.SetAddress(<void*>&self.muon_tau_SS_value)

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

        self.tauAbsEta_branch = self.tree.GetBranch("tauAbsEta")
        self.tauAbsEta_branch.SetAddress(<void*>&self.tauAbsEta_value)

        self.tauAntiElectronLoose_branch = self.tree.GetBranch("tauAntiElectronLoose")
        self.tauAntiElectronLoose_branch.SetAddress(<void*>&self.tauAntiElectronLoose_value)

        self.tauAntiElectronMVA_branch = self.tree.GetBranch("tauAntiElectronMVA")
        self.tauAntiElectronMVA_branch.SetAddress(<void*>&self.tauAntiElectronMVA_value)

        self.tauAntiElectronMedium_branch = self.tree.GetBranch("tauAntiElectronMedium")
        self.tauAntiElectronMedium_branch.SetAddress(<void*>&self.tauAntiElectronMedium_value)

        self.tauAntiElectronTight_branch = self.tree.GetBranch("tauAntiElectronTight")
        self.tauAntiElectronTight_branch.SetAddress(<void*>&self.tauAntiElectronTight_value)

        self.tauAntiMuonLoose_branch = self.tree.GetBranch("tauAntiMuonLoose")
        self.tauAntiMuonLoose_branch.SetAddress(<void*>&self.tauAntiMuonLoose_value)

        self.tauAntiMuonTight_branch = self.tree.GetBranch("tauAntiMuonTight")
        self.tauAntiMuonTight_branch.SetAddress(<void*>&self.tauAntiMuonTight_value)

        self.tauCharge_branch = self.tree.GetBranch("tauCharge")
        self.tauCharge_branch.SetAddress(<void*>&self.tauCharge_value)

        self.tauDZ_branch = self.tree.GetBranch("tauDZ")
        self.tauDZ_branch.SetAddress(<void*>&self.tauDZ_value)

        self.tauDecayFinding_branch = self.tree.GetBranch("tauDecayFinding")
        self.tauDecayFinding_branch.SetAddress(<void*>&self.tauDecayFinding_value)

        self.tauDecayMode_branch = self.tree.GetBranch("tauDecayMode")
        self.tauDecayMode_branch.SetAddress(<void*>&self.tauDecayMode_value)

        self.tauEta_branch = self.tree.GetBranch("tauEta")
        self.tauEta_branch.SetAddress(<void*>&self.tauEta_value)

        self.tauGenDecayMode_branch = self.tree.GetBranch("tauGenDecayMode")
        self.tauGenDecayMode_branch.SetAddress(<void*>&self.tauGenDecayMode_value)

        self.tauIP3DS_branch = self.tree.GetBranch("tauIP3DS")
        self.tauIP3DS_branch.SetAddress(<void*>&self.tauIP3DS_value)

        self.tauJetBtag_branch = self.tree.GetBranch("tauJetBtag")
        self.tauJetBtag_branch.SetAddress(<void*>&self.tauJetBtag_value)

        self.tauJetPt_branch = self.tree.GetBranch("tauJetPt")
        self.tauJetPt_branch.SetAddress(<void*>&self.tauJetPt_value)

        self.tauLeadTrackPt_branch = self.tree.GetBranch("tauLeadTrackPt")
        self.tauLeadTrackPt_branch.SetAddress(<void*>&self.tauLeadTrackPt_value)

        self.tauLooseIso_branch = self.tree.GetBranch("tauLooseIso")
        self.tauLooseIso_branch.SetAddress(<void*>&self.tauLooseIso_value)

        self.tauLooseMVAIso_branch = self.tree.GetBranch("tauLooseMVAIso")
        self.tauLooseMVAIso_branch.SetAddress(<void*>&self.tauLooseMVAIso_value)

        self.tauMass_branch = self.tree.GetBranch("tauMass")
        self.tauMass_branch.SetAddress(<void*>&self.tauMass_value)

        self.tauMediumIso_branch = self.tree.GetBranch("tauMediumIso")
        self.tauMediumIso_branch.SetAddress(<void*>&self.tauMediumIso_value)

        self.tauMediumMVAIso_branch = self.tree.GetBranch("tauMediumMVAIso")
        self.tauMediumMVAIso_branch.SetAddress(<void*>&self.tauMediumMVAIso_value)

        self.tauMuOverlap_branch = self.tree.GetBranch("tauMuOverlap")
        self.tauMuOverlap_branch.SetAddress(<void*>&self.tauMuOverlap_value)

        self.tauPhi_branch = self.tree.GetBranch("tauPhi")
        self.tauPhi_branch.SetAddress(<void*>&self.tauPhi_value)

        self.tauPt_branch = self.tree.GetBranch("tauPt")
        self.tauPt_branch.SetAddress(<void*>&self.tauPt_value)

        self.tauTNPId_branch = self.tree.GetBranch("tauTNPId")
        self.tauTNPId_branch.SetAddress(<void*>&self.tauTNPId_value)

        self.tauVZ_branch = self.tree.GetBranch("tauVZ")
        self.tauVZ_branch.SetAddress(<void*>&self.tauVZ_value)

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

    property muon_tau_DPhi:
        def __get__(self):
            self.muon_tau_DPhi_branch.GetEntry(self.ientry, 0)
            return self.muon_tau_DPhi_value

    property muon_tau_DR:
        def __get__(self):
            self.muon_tau_DR_branch.GetEntry(self.ientry, 0)
            return self.muon_tau_DR_value

    property muon_tau_Mass:
        def __get__(self):
            self.muon_tau_Mass_branch.GetEntry(self.ientry, 0)
            return self.muon_tau_Mass_value

    property muon_tau_PZeta:
        def __get__(self):
            self.muon_tau_PZeta_branch.GetEntry(self.ientry, 0)
            return self.muon_tau_PZeta_value

    property muon_tau_PZetaVis:
        def __get__(self):
            self.muon_tau_PZetaVis_branch.GetEntry(self.ientry, 0)
            return self.muon_tau_PZetaVis_value

    property muon_tau_Pt:
        def __get__(self):
            self.muon_tau_Pt_branch.GetEntry(self.ientry, 0)
            return self.muon_tau_Pt_value

    property muon_tau_SS:
        def __get__(self):
            self.muon_tau_SS_branch.GetEntry(self.ientry, 0)
            return self.muon_tau_SS_value

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

    property tauAbsEta:
        def __get__(self):
            self.tauAbsEta_branch.GetEntry(self.ientry, 0)
            return self.tauAbsEta_value

    property tauAntiElectronLoose:
        def __get__(self):
            self.tauAntiElectronLoose_branch.GetEntry(self.ientry, 0)
            return self.tauAntiElectronLoose_value

    property tauAntiElectronMVA:
        def __get__(self):
            self.tauAntiElectronMVA_branch.GetEntry(self.ientry, 0)
            return self.tauAntiElectronMVA_value

    property tauAntiElectronMedium:
        def __get__(self):
            self.tauAntiElectronMedium_branch.GetEntry(self.ientry, 0)
            return self.tauAntiElectronMedium_value

    property tauAntiElectronTight:
        def __get__(self):
            self.tauAntiElectronTight_branch.GetEntry(self.ientry, 0)
            return self.tauAntiElectronTight_value

    property tauAntiMuonLoose:
        def __get__(self):
            self.tauAntiMuonLoose_branch.GetEntry(self.ientry, 0)
            return self.tauAntiMuonLoose_value

    property tauAntiMuonTight:
        def __get__(self):
            self.tauAntiMuonTight_branch.GetEntry(self.ientry, 0)
            return self.tauAntiMuonTight_value

    property tauCharge:
        def __get__(self):
            self.tauCharge_branch.GetEntry(self.ientry, 0)
            return self.tauCharge_value

    property tauDZ:
        def __get__(self):
            self.tauDZ_branch.GetEntry(self.ientry, 0)
            return self.tauDZ_value

    property tauDecayFinding:
        def __get__(self):
            self.tauDecayFinding_branch.GetEntry(self.ientry, 0)
            return self.tauDecayFinding_value

    property tauDecayMode:
        def __get__(self):
            self.tauDecayMode_branch.GetEntry(self.ientry, 0)
            return self.tauDecayMode_value

    property tauEta:
        def __get__(self):
            self.tauEta_branch.GetEntry(self.ientry, 0)
            return self.tauEta_value

    property tauGenDecayMode:
        def __get__(self):
            self.tauGenDecayMode_branch.GetEntry(self.ientry, 0)
            return self.tauGenDecayMode_value

    property tauIP3DS:
        def __get__(self):
            self.tauIP3DS_branch.GetEntry(self.ientry, 0)
            return self.tauIP3DS_value

    property tauJetBtag:
        def __get__(self):
            self.tauJetBtag_branch.GetEntry(self.ientry, 0)
            return self.tauJetBtag_value

    property tauJetPt:
        def __get__(self):
            self.tauJetPt_branch.GetEntry(self.ientry, 0)
            return self.tauJetPt_value

    property tauLeadTrackPt:
        def __get__(self):
            self.tauLeadTrackPt_branch.GetEntry(self.ientry, 0)
            return self.tauLeadTrackPt_value

    property tauLooseIso:
        def __get__(self):
            self.tauLooseIso_branch.GetEntry(self.ientry, 0)
            return self.tauLooseIso_value

    property tauLooseMVAIso:
        def __get__(self):
            self.tauLooseMVAIso_branch.GetEntry(self.ientry, 0)
            return self.tauLooseMVAIso_value

    property tauMass:
        def __get__(self):
            self.tauMass_branch.GetEntry(self.ientry, 0)
            return self.tauMass_value

    property tauMediumIso:
        def __get__(self):
            self.tauMediumIso_branch.GetEntry(self.ientry, 0)
            return self.tauMediumIso_value

    property tauMediumMVAIso:
        def __get__(self):
            self.tauMediumMVAIso_branch.GetEntry(self.ientry, 0)
            return self.tauMediumMVAIso_value

    property tauMuOverlap:
        def __get__(self):
            self.tauMuOverlap_branch.GetEntry(self.ientry, 0)
            return self.tauMuOverlap_value

    property tauPhi:
        def __get__(self):
            self.tauPhi_branch.GetEntry(self.ientry, 0)
            return self.tauPhi_value

    property tauPt:
        def __get__(self):
            self.tauPt_branch.GetEntry(self.ientry, 0)
            return self.tauPt_value

    property tauTNPId:
        def __get__(self):
            self.tauTNPId_branch.GetEntry(self.ientry, 0)
            return self.tauTNPId_value

    property tauVZ:
        def __get__(self):
            self.tauVZ_branch.GetEntry(self.ientry, 0)
            return self.tauVZ_value

    property tauVetoPt20:
        def __get__(self):
            self.tauVetoPt20_branch.GetEntry(self.ientry, 0)
            return self.tauVetoPt20_value

    property idx:
        def __get__(self):
            self.idx_branch.GetEntry(self.ientry, 0)
            return self.idx_value



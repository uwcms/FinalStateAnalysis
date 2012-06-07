

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

cdef class ETauTree:
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

    cdef TBranch* electron_tau_DPhi_branch
    cdef float electron_tau_DPhi_value

    cdef TBranch* electron_tau_DR_branch
    cdef float electron_tau_DR_value

    cdef TBranch* electron_tau_Mass_branch
    cdef float electron_tau_Mass_value

    cdef TBranch* electron_tau_PZeta_branch
    cdef float electron_tau_PZeta_value

    cdef TBranch* electron_tau_PZetaVis_branch
    cdef float electron_tau_PZetaVis_value

    cdef TBranch* electron_tau_Pt_branch
    cdef float electron_tau_Pt_value

    cdef TBranch* electron_tau_SS_branch
    cdef float electron_tau_SS_value

    cdef TBranch* evt_branch
    cdef int evt_value

    cdef TBranch* isdata_branch
    cdef int isdata_value

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

        self.electron_tau_DPhi_branch = self.tree.GetBranch("electron_tau_DPhi")
        self.electron_tau_DPhi_branch.SetAddress(<void*>&self.electron_tau_DPhi_value)

        self.electron_tau_DR_branch = self.tree.GetBranch("electron_tau_DR")
        self.electron_tau_DR_branch.SetAddress(<void*>&self.electron_tau_DR_value)

        self.electron_tau_Mass_branch = self.tree.GetBranch("electron_tau_Mass")
        self.electron_tau_Mass_branch.SetAddress(<void*>&self.electron_tau_Mass_value)

        self.electron_tau_PZeta_branch = self.tree.GetBranch("electron_tau_PZeta")
        self.electron_tau_PZeta_branch.SetAddress(<void*>&self.electron_tau_PZeta_value)

        self.electron_tau_PZetaVis_branch = self.tree.GetBranch("electron_tau_PZetaVis")
        self.electron_tau_PZetaVis_branch.SetAddress(<void*>&self.electron_tau_PZetaVis_value)

        self.electron_tau_Pt_branch = self.tree.GetBranch("electron_tau_Pt")
        self.electron_tau_Pt_branch.SetAddress(<void*>&self.electron_tau_Pt_value)

        self.electron_tau_SS_branch = self.tree.GetBranch("electron_tau_SS")
        self.electron_tau_SS_branch.SetAddress(<void*>&self.electron_tau_SS_value)

        self.evt_branch = self.tree.GetBranch("evt")
        self.evt_branch.SetAddress(<void*>&self.evt_value)

        self.isdata_branch = self.tree.GetBranch("isdata")
        self.isdata_branch.SetAddress(<void*>&self.isdata_value)

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

    property electron_tau_DPhi:
        def __get__(self):
            self.electron_tau_DPhi_branch.GetEntry(self.ientry, 0)
            return self.electron_tau_DPhi_value

    property electron_tau_DR:
        def __get__(self):
            self.electron_tau_DR_branch.GetEntry(self.ientry, 0)
            return self.electron_tau_DR_value

    property electron_tau_Mass:
        def __get__(self):
            self.electron_tau_Mass_branch.GetEntry(self.ientry, 0)
            return self.electron_tau_Mass_value

    property electron_tau_PZeta:
        def __get__(self):
            self.electron_tau_PZeta_branch.GetEntry(self.ientry, 0)
            return self.electron_tau_PZeta_value

    property electron_tau_PZetaVis:
        def __get__(self):
            self.electron_tau_PZetaVis_branch.GetEntry(self.ientry, 0)
            return self.electron_tau_PZetaVis_value

    property electron_tau_Pt:
        def __get__(self):
            self.electron_tau_Pt_branch.GetEntry(self.ientry, 0)
            return self.electron_tau_Pt_value

    property electron_tau_SS:
        def __get__(self):
            self.electron_tau_SS_branch.GetEntry(self.ientry, 0)
            return self.electron_tau_SS_value

    property evt:
        def __get__(self):
            self.evt_branch.GetEntry(self.ientry, 0)
            return self.evt_value

    property isdata:
        def __get__(self):
            self.isdata_branch.GetEntry(self.ientry, 0)
            return self.isdata_value

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



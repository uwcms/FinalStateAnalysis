
'''

Ntuple branch template sets for tau objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

info = PSet(
    objectGenDecayMode = '{object}.userInt("genDecayMode")',
    objectLeadTrackPt = '{object}.userFloat("ps_ldTrkPt")',
    objectDecayMode = '{object}.decayMode',
    objectTNPId = '{object}.userInt("ps_sel_nom")',
)

# ID and isolation
id = PSet(
    #Against Electron
    #STD
    objectAntiElectronLoose   = '{object}.tauID("againstElectronLoose")',
    objectAntiElectronMedium  = '{object}.tauID("againstElectronMedium")',
    objectAntiElectronTight   = '{object}.tauID("againstElectronTight")',
    
    objectAntiElectronMVA5VLoose = '{object}.tauID("againstElectronVLooseMVA5")',
    objectAntiElectronMVA5Loose  = '{object}.tauID("againstElectronLooseMVA5")',
    objectAntiElectronMVA5Medium = '{object}.tauID("againstElectronMediumMVA5")',
    objectAntiElectronMVA5Tight  = '{object}.tauID("againstElectronTightMVA5")',
    objectAntiElectronMVA5VTight = '{object}.tauID("againstElectronVTightMVA5")',

    objectAntiMuonLoose  = '{object}.tauID("againstMuonLoose")',
    objectAntiMuonMedium = '{object}.tauID("againstMuonMedium")',
    objectAntiMuonTight  = '{object}.tauID("againstMuonTight")',
    
    objectAntiMuon2Loose   = '{object}.tauID("againstMuonLoose2")',
    objectAntiMuon2Medium  = '{object}.tauID("againstMuonMedium2")',
    objectAntiMuon2Tight   = '{object}.tauID("againstMuonTight2")',
    
    objectAntiMuon3Loose  = '{object}.tauID("againstMuonLoose3")',
    objectAntiMuon3Tight  = '{object}.tauID("againstMuonTight3")',
    
    objectAntiMuonMVALoose   = '{object}.tauID("againstMuonLooseMVA")',
    objectAntiMuonMVAMedium  = '{object}.tauID("againstMuonMediumMVA")',
    objectAntiMuonMVATight   = '{object}.tauID("againstMuonTightMVA")',

    #DM
    objectDecayFinding       = '{object}.tauID("decayModeFinding")',
    objectDecayFindingNewDMs = '{object}.tauID("decayModeFindingNewDMs")',
    objectDecayFindingOldDMs = '{object}.tauID("decayModeFindingOldDMs")',

    #ISO DB
    objectVLooseIso = '{object}.tauID("byVLooseCombinedIsolationDeltaBetaCorr")',
    objectLooseIso  = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr")',
    objectMediumIso = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr")',
    objectTightIso  = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr")',

    #ISO DB 3Hits
    objectLooseIso3Hits  = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")',
    objectMediumIso3Hits = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")',
    objectTightIso3Hits  = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits")',

    #ISO no correction 3Hits
    objectLooseIso3HitsNoCorr  = '{object}.tauID("byCombinedIsolation3HitsLoose")',
    objectMediumIso3HitsNoCorr = '{object}.tauID("byCombinedIsolation3HitsMedium")',
    objectTightIso3HitsNoCorr  = '{object}.tauID("byCombinedIsolation3HitsTight")',

    #MVA 3 oldDM
    objectVLooseIsoMVA3OldDMNoLT  = '{object}.tauID("byVLooseIsolationMVA3oldDMwoLT")',
    objectLooseIsoMVA3OldDMNoLT   = '{object}.tauID("byLooseIsolationMVA3oldDMwoLT")',
    objectMediumIsoMVA3OldDMNoLT  = '{object}.tauID("byMediumIsolationMVA3oldDMwoLT")',
    objectTightIsoMVA3OldDMNoLT   = '{object}.tauID("byTightIsolationMVA3oldDMwoLT")',
    objectVTightIsoMVA3OldDMNoLT  = '{object}.tauID("byVTightIsolationMVA3oldDMwoLT")',
    objectVVTightIsoMVA3OldDMNoLT = '{object}.tauID("byVVTightIsolationMVA3oldDMwoLT")',
    
    #MVA 3 oldDM & LifeTime
    objectVLooseIsoMVA3OldDMLT  = '{object}.tauID("byVLooseIsolationMVA3oldDMwLT")',
    objectLooseIsoMVA3OldDMLT   = '{object}.tauID("byLooseIsolationMVA3oldDMwLT")',
    objectMediumIsoMVA3OldDMLT  = '{object}.tauID("byMediumIsolationMVA3oldDMwLT")',
    objectTightIsoMVA3OldDMLT   = '{object}.tauID("byTightIsolationMVA3oldDMwLT")',
    objectVTightIsoMVA3OldDMLT  = '{object}.tauID("byVTightIsolationMVA3oldDMwLT")',
    objectVVTightIsoMVA3OldDMLT = '{object}.tauID("byVVTightIsolationMVA3oldDMwLT")',

    #MVA 3 newDM
    objectVLooseIsoMVA3NewDMNoLT  = '{object}.tauID("byVLooseIsolationMVA3newDMwoLT")',
    objectLooseIsoMVA3NewDMNoLT   = '{object}.tauID("byLooseIsolationMVA3newDMwoLT")',
    objectMediumIsoMVA3NewDMNoLT  = '{object}.tauID("byMediumIsolationMVA3newDMwoLT")',
    objectTightIsoMVA3NewDMNoLT   = '{object}.tauID("byTightIsolationMVA3newDMwoLT")',
    objectVTightIsoMVA3NewDMNoLT  = '{object}.tauID("byVTightIsolationMVA3newDMwoLT")',
    objectVVTightIsoMVA3NewDMNoLT = '{object}.tauID("byVVTightIsolationMVA3newDMwoLT")',
    
    #MVA 3 newDM & LifeTime
    objectVLooseIsoMVA3NewDMLT  = '{object}.tauID("byVLooseIsolationMVA3newDMwLT")',
    objectLooseIsoMVA3NewDMLT   = '{object}.tauID("byLooseIsolationMVA3newDMwLT")',
    objectMediumIsoMVA3NewDMLT  = '{object}.tauID("byMediumIsolationMVA3newDMwLT")',
    objectTightIsoMVA3NewDMLT   = '{object}.tauID("byTightIsolationMVA3newDMwLT")',
    objectVTightIsoMVA3NewDMLT  = '{object}.tauID("byVTightIsolationMVA3newDMwLT")',
    objectVVTightIsoMVA3NewDMLT = '{object}.tauID("byVVTightIsolationMVA3newDMwLT")',
    
)



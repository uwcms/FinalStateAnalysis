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
    objectAntiElectronMVA2loose   = '{object}.tauID("againstElectronLooseMVA2")',
    objectAntiElectronMVA2Tight   = '{object}.tauID("againstElectronTightMVA2")',
    objectAntiElectronMVA2Vloose  = '{object}.tauID("againstElectronVLooseMVA2")',
    objectAntiMuonMedium          = '{object}.tauID("againstMuonMedium")',
    objectVLooseIso               = '{object}.tauID("byVLooseCombinedIsolationDeltaBetaCorr")',
    objectDecayFinding            = '{object}.tauID("decayModeFinding")',
    objectLooseIso                = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr")',
    objectMediumIso               = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr")',
    objectTightIso                = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr")',
    objectLooseMVAIso             = '{object}.tauID("byLooseIsolationMVA")',
    objectMediumMVAIso            = '{object}.tauID("byMediumIsolationMVA")',
    objectTightMVAIso             = '{object}.tauID("byTightIsolationMVA")',
    objectAntiElectronLoose       = '{object}.tauID("againstElectronLoose")',
    objectAntiElectronMedium      = '{object}.tauID("againstElectronMedium")',
    objectAntiElectronTight       = '{object}.tauID("againstElectronTight")',
    objectAntiElectronMVA         = '{object}.tauID("againstElectronMVA")',
    objectAntiMuonLoose           = '{object}.tauID("againstMuonLoose")',
    objectAntiMuonTight           = '{object}.tauID("againstMuonTight")',
)

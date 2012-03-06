'''

Ntuple branch template sets for tau objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

info = PSet(
    objectGenDecayMode = '{object}.userInt("genDecayMode")',
    objectLeadTrackPt = '{object}.userFloat("ps_ldTrkPt")',
    objectDecayMode = '{object}.decayMode',
    objectTNPId = '{object}.userInt("ps_sel_nom")',
)

# ID and isolation
id = PSet(
    objectDecayFinding = '{object}.tauID("decayModeFinding")',
    objectLooseIso = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr")',
    objectMediumIso = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr")',
    objectAntiElectronLoose = '{object}.tauID("againstElectronLoose")',
    objectAntiElectronMedium = '{object}.tauID("againstElectronMedium")',
    objectAntiElectronMVA = '{object}.tauID("againstElectronMVA")',
    objectAntiMuonLoose = '{object}.tauID("againstMuonLoose")',
    objectAntiMuonTight = '{object}.tauID("againstMuonTight")',
)

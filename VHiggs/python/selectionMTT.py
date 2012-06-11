import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.NtupleTools.selectors.selectors as selectors
from FinalStateAnalysis.VHiggs.selectionCommon import common
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate

leg1 = {
    'name' : 'Mu', 'getter' :'daughter(0).', 'nicename' : 'Muon',
    'index' : 0,
}
leg2 = {
    'name' : 'Tau1', 'getter' :'daughter(1).', 'nicename' : 'Tau (1)',
    'index' : 1,
}
leg3 = {
    'name' : 'Tau2', 'getter' :'daughter(2).', 'nicename' : 'Tau (2)',
    'index' : 2,
}

selections = cms.VPSet(
    ###########################################################################
    # Uniqueness cut
    ###########################################################################
    PSetTemplate(selectors.topology.descending_pt).replace(
        name = 'Tau1GtTau2', nicename = 'Tau 1 > Tau 2',
        getter1 = leg2['getter'], getter2 = leg3['getter']),

    ###########################################################################
    # Basic acceptance cuts
    ###########################################################################
    # Select electron leg 1 pt
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '16', **leg1),
    # Select electron leg 1 eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg1),

    # Select tau pt leg 1
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '20', **leg2),
    # Select tau eta leg 1
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg2),

    # Select tau pt leg 1
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '20', **leg3),
    # Select tau eta leg 1
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg3),

    ###########################################################################
    # ID and Iso cuts
    ###########################################################################

    PSetTemplate(selectors.muons.id).replace(
        muID = 'WWID', **leg1),
    PSetTemplate(selectors.muons.reliso).replace(
        threshold = '0.1', **leg1),

    PSetTemplate(selectors.taus.id).replace(
        tauID = 'decayModeFinding', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'byLooseCombinedIsolationDeltaBetaCorr', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstElectronLoose', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstMuonTight', **leg2),

    PSetTemplate(selectors.taus.id).replace(
        tauID = 'decayModeFinding', **leg3),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'byLooseCombinedIsolationDeltaBetaCorr', **leg3),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstElectronLoose', **leg3),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstMuonTight', **leg3),

    PSetTemplate(selectors.candidate.charge).replace(
        getter = '', name = 'finalState', nicename='Final State', charge = '1'),

    PSetTemplate(selectors.extras.e_veto).replace(
        name = 'finalState', nicename='Final State',
        pt_threshold=common['eveto_pt_threshold'], eta_threshold='2.5',
        eID='WWID', getter='', threshold=common['eveto_iso_threshold']),

    PSetTemplate(selectors.extras.mu_veto).replace(
        name = 'finalState', nicename='Final State',
        pt_threshold=common['muveto_pt_threshold'], eta_threshold='2.5',
        muID='WWID', getter='', threshold=common['muveto_iso_threshold']),

    PSetTemplate(selectors.topology.z_veto).replace(
        name = 'Leg1Leg2', nicename='Leg 1-Leg 2',
        index1 = 0, index2 = 1
    ),
    PSetTemplate(selectors.topology.z_veto).replace(
        name = 'Leg1Leg3', nicename='Leg 1-Leg 3',
        index1 = 0, index2 = 2
    ),
    PSetTemplate(selectors.topology.z_veto).replace(
        name = 'Leg2Leg3', nicename='Leg 2-Leg 3',
        index1 = 1, index2 = 2
    ),

    PSetTemplate(selectors.extras.bjet_veto).replace(
        name = 'finalState', nicename='Final State',
        pt_threshold = common['bveto_pt_threshold'], eta_threshold='2.5',
        btag_threshold = common['btag_threshold']),
)

###########################################################################
# Define plots
###########################################################################

from FinalStateAnalysis.NtupleTools.plotBuilder import makePlots
all_plots, ntuple = makePlots(leg1, leg2, leg3)

# Split into OS/SS regions
plots = cms.PSet(
    histos = cms.VPSet(),
    ntuple = ntuple,
)

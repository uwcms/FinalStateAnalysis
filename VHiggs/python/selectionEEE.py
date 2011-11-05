import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Selectors.selectors.selectors as selectors
from FinalStateAnalysis.VHiggs.selectionCommon import common
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate

leg1 = {
    'name' : 'Elec1', 'getter' :'daughter(0).', 'nicename' : 'Electron (1)',
    'index' : 0,
}
leg2 = {
    'name' : 'Elec2', 'getter' :'daughter(1).', 'nicename' : 'Electron (2)',
    'index' : 1,
}

leg3 = {
    'name' : 'Elec3', 'getter' :'daughter(2).', 'nicename' : 'Electron (3)',
    'index' : 2,
}

###########################################################################
# Define analysis sequence
###########################################################################

selections = cms.VPSet(
    ###########################################################################
    # Uniqueness cut
    ###########################################################################
    PSetTemplate(selectors.topology.descending_pt).replace(
        name = 'Elec1GtElec2', nicename = 'Electron 1 > Electron 2',
        getter1 = leg1['getter'], getter2 = leg2['getter']),
    PSetTemplate(selectors.topology.descending_pt).replace(
        name = 'Elec2GtElec3', nicename = 'Electron 2 > Electron 3',
        getter1 = leg2['getter'], getter2 = leg3['getter']),

    ###########################################################################
    # Basic acceptance cuts
    ###########################################################################
    # Select electron leg 1 pt
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '12', **leg1),
    # Select electron leg 1 eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg1),

    # Select electron leg 2 pt
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '12', **leg2),
    # Select electron leg 2 eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg2),

    # Select electron leg 3 pt
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '12', **leg3),
    # Select electron leg 3 eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg3),

    ###########################################################################
    # ID and Iso cuts
    ###########################################################################
    PSetTemplate(selectors.electrons.id).replace(
        eID = 'WWID', **leg1),
    PSetTemplate(selectors.electrons.reliso).replace(
        threshold = '0.1', **leg1),

    PSetTemplate(selectors.electrons.id).replace(
        eID = 'WWID', **leg2),
    PSetTemplate(selectors.electrons.reliso).replace(
        threshold = '0.15', **leg2),

    PSetTemplate(selectors.electrons.id).replace(
        eID = 'WWID', **leg3),
    PSetTemplate(selectors.electrons.reliso).replace(
        threshold = '0.15', **leg3),

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
        pt_threshold=common['bveto_pt_threshold'], eta_threshold='2.5',
        btag_threshold = common['btag_threshold']),
)

###########################################################################
# Define plots
###########################################################################

from FinalStateAnalysis.Selectors.plotBuilder import makePlots
plots, ntuple = makePlots(leg1, leg2, leg3)

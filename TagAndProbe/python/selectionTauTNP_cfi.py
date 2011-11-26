import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Selectors.selectors.selectors as selectors
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate

leg1 = {
    'name' : 'Muon', 'getter' :'daughter(0).', 'nicename' : 'Muon',
    'index' : 0,
}
leg2 = {
    'name' : 'Tau', 'getter' :'daughter(1).', 'nicename' : 'Tau',
    'index' : 1,
}

selections = cms.VPSet(
    ###########################################################################
    # Basic acceptance cuts
    ###########################################################################

    # Select muon eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.1', **leg1),
    # Select muon pt
    PSetTemplate(selectors.candidate.pt).replace(threshold = '15', **leg1),

    # Select tau eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg2),
    # Select tau pt
    PSetTemplate(selectors.candidate.pt).replace(threshold = '15', **leg2),

    ###########################################################################
    # Muon ID cuts
    ###########################################################################
    PSetTemplate(selectors.muons.id).replace(
        muID = 'WWID', **leg1),

    ############################################################################
    ## Tau ID cuts
    ############################################################################
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'decayModeFinding', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstElectronMedium', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstMuonTight', **leg2),
)

################################################################################
# Define plots
################################################################################

puWeights = [
    '3bx_S42011A',
    '3bx_S42011AB178078',
    '3bx_S42011B178078',
]

triggers = [
    ('HLTIsoMu17', 'Iso Mu 17', r'HLT_IsoMu17_v\\d+'),
    ('HLTMu15', 'Mu 15', r'HLT_Mu15_v\\d+'),
    ('HLTMu30', 'Mu 30', r'HLT_Mu30_v\\d+'),
]

from FinalStateAnalysis.Selectors.plotBuilder import makePlots
all_plots, ntuple = makePlots(leg1, leg2, triggers=triggers, puWeights=puWeights)

# Add an extra plot of the mass using the tau jet pt and the muon
ntuple.muTauJetMass = cms.string("subcand('@,patJet').get.mass")

# Split into OS/SS regions
plots = cms.PSet(
    histos = cms.VPSet(),
    ntuple = ntuple,
)

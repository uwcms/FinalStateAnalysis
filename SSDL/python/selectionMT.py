import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Selectors.selectors.selectors as selectors
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate
from FinalStateAnalysis.SSDL.plotBuilder import dileptonFinalPlots

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
        threshold = '2.4', **leg1),
    # Select muon pt
    PSetTemplate(selectors.candidate.pt).replace(threshold = '5', **leg1),

    # Select tau eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg2),
    # Select tau pt
    PSetTemplate(selectors.candidate.pt).replace(threshold = '15', **leg2),

    ###########################################################################
    # Muon ID cuts
    ###########################################################################

    PSetTemplate(selectors.muons.globalTrk).replace(**leg1),
    PSetTemplate(selectors.muons.trkNormChi2).replace(
        threshold = 10,  **leg1),
    PSetTemplate(selectors.muons.d0).replace(
        threshold = 0.02, **leg1),

    PSetTemplate(selectors.muons.relSubDetIso).replace(
        threshold = 0.15, **leg1),
    PSetTemplate(selectors.muons.ecalIso).replace(
        threshold = 4, **leg1),
    PSetTemplate(selectors.muons.hcalIso).replace(
        threshold = 6, **leg1),

    PSetTemplate(selectors.muons.id).replace(
        muID = 'WWID', **leg1),
    PSetTemplate(selectors.muons.reliso).replace(
        threshold = '0.15', **leg1),

    ############################################################################
    ## Tau ID cuts
    ############################################################################
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'decayModeFinding', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstElectronMedium', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstMuonLoose', **leg2),
)


all_plots, ntuple = dileptonFinalPlots(leg1, leg2)
# Split into OS/SS regions
plots = cms.PSet(
    histos = cms.VPSet(),
    ntuple = ntuple,
)

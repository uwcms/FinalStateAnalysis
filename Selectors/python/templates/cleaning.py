'''

Ntuple branch template sets for applying cleaning and extra object vetoes

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

# Vetos on extra stuff in the event
vetos = PSet(
    muVetoPt5 = 'extras("extMuons", "pt > 5 & abs(eta) < 2.4").size()',
    muGlbIsoVetoPt10 = 'extras("extMuons", "isGlobalMuon & isTrackerMuon & pt > 10 & abs(eta) < 2.4 & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*userIso(0), 0))/pt < 0.25").size()',
    tauVetoPt20 = 'extras("extTaus", "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseCombinedIsolationDeltaBetaCorr\')").size()',
    eVetoWP95Iso = 'extras("extElecs", "pt > 10 & abs(eta) < 2.5 & userFloat(\'wp95\') > 0.5 & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*userIso(0), 0))/pt < 0.3").size()',
    eVetoCicTightIso = 'extras("extElecs", "pt > 10 & abs(eta) < 2.5 &  test_bit(electronID(\'cicTight\'), 0) > 0.5 & (chargedHadronIso + max(photonIso + neutralHadronIso - 0.5*userIso(0), 0))/pt < 0.25").size()',
    bjetVeto = 'extras("extJets", "pt > 20 & abs(eta) < 2.5 & bDiscriminator(\'\') > 3.3").size()',
)

overlaps = PSet(
    objectMuOverlap = 'filteredOverlaps({object_idx}, "muons", "pt > 5").size()',
    objectElecOverlap = 'filteredOverlaps({object_idx}, "electrons", "pt > 10").size()',
    objectCiCTightElecOverlap = 'filteredOverlaps({object_idx}, "electrons", "pt > 10 & test_bit(electronID(\'cicTight\'), 0)").size()',
)

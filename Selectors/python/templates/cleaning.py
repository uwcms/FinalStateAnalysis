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
    muVetoPt5 = 'vetoMuons(0.3, "pt > 5 & abs(eta) < 2.4").size()',
    muGlbIsoVetoPt10 = 'vetoMuons(0.3, "isGlobalMuon & isTrackerMuon & pt > 10 & abs(eta) < 2.4 & (userIso(0) + max(photonIso + neutralHadronIso - 0.5*pfPUChargedHadrons, 0))/pt < 0.3").size()',
    tauVetoPt20 = 'vetoTaus(0.3, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseIsolationMVA\')").size()',
    # Electrons embedding currently broken
    #eVetoWP95Iso = 'vetoElectrons(0.3, "pt > 10 & abs(eta) < 2.5 & userFloat(\'wp95\') > 0.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
    #eVetoCicTightIso = 'vetoElectrons(0.3, "pt > 10 & abs(eta) < 2.5 &  test_bit(electronID(\'cicTight\'), 0) > 0.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
    bjetVeto = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.5 & bDiscriminator(\'\') > 3.3").size()',
    bjetCSVVeto = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.5 & bDiscriminator(\'combinedSecondaryVertexBJetTagsAOD\') > 0.679").size()',
    jetVeto20 = 'vetoJets(0.4, "pt > 20 & abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size()',
    jetVeto40 = 'vetoJets(0.4, "pt > 40 & abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size()',
)

overlaps = PSet(
    objectMuOverlap = 'overlapMuons({object_idx}, "pt > 5").size()',
    # Electrons embedding currently broken
    #objectElecOverlap = 'overlapElectrons({object_idx}, "pt > 10").size()',
    #objectCiCTightElecOverlap = 'overlapElectrons({object_idx}, "pt > 10 & test_bit(electronID(\'cicTight\'), 0)").size()',
)

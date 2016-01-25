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
    #MUON VETOS
    muVetoPt5 = 'vetoMuons(0.4, "pt > 5 & abs(eta) < 2.4").size()',
    muGlbIsoVetoPt10 = 'vetoMuons(0.4, "isGlobalMuon & isTrackerMuon & pt > 10 & abs(eta) < 2.4 & (userIso(0) + max(photonIso + neutralHadronIso - 0.5*puChargedHadronIso, 0))/pt < 0.4").size()',
    muVetoPt5IsoIdVtx = 'vetoMuons(0.4, "pt > 5 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    muVetoPt15IsoIdVtx = 'vetoMuons(0.4, "pt > 15 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    
    #TAU VETOS
    #OLD DMs
    tauVetoPt20Loose3HitsVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseCombinedIsolationDeltaBetaCorr3Hits\') & userFloat(\'dz\') < 0.2").size()',
    tauVetoPt20TightMVALTVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byTightIsolationMVA3oldDMwLT\') & userFloat(\'dz\') < 0.2").size()',

    #NEW DMs
    tauVetoPt20Loose3HitsNewDMVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFindingNewDMs\') & tauID(\'byLooseCombinedIsolationDeltaBetaCorr3Hits\') & userFloat(\'dz\') < 0.2").size()',
    tauVetoPt20TightMVALTNewDMVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byTightIsolationMVA3newDMwLT\') & userFloat(\'dz\') < 0.2").size()',
    
    #ELECTRON VETOS
    #eVetoMVAIsoVtx = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & userFloat(\'dz\') < 0.2").size()',
    #eVetoMVAIso = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
    
    #B-JET Vetos
    bjetCISVVeto20Loose = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.423").size()',
    bjetCISVVeto30Loose = 'vetoJets(0.4, "pt > 30 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.423").size()',
    bjetCISVVeto20Medium = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.814").size()',
    bjetCISVVeto30Medium = 'vetoJets(0.4, "pt > 30 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.814").size()',
    bjetCISVVeto20Tight = 'vetoJets(0.4, "pt > 20 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.941").size()',
    bjetCISVVeto30Tight = 'vetoJets(0.4, "pt > 30 & abs(eta) < 2.4 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.941").size()',

    #JET VETOS
    jetVeto20 = 'vetoJets(0.4, "pt > 20 & abs(eta) < 5.0").size()',
    jetVeto20_DR05 = 'vetoJets(0.5, "pt > 20 & abs(eta) < 5.0").size()',
    jetVeto30 = 'vetoJets(0.4, "pt > 30 & abs(eta) < 5.0").size()',
    jetVeto30_JetEnDown = 'vetoJets(0.4, "userCand(\'jes-\').pt > 30 & abs(eta) < 5.0").size()',
    jetVeto30_JetEnUp = 'vetoJets(0.4, "userCand(\'jes+\').pt > 30 & abs(eta) < 5.0").size()',
    jetVeto30Eta3 = 'vetoJets(0.4, "pt > 30 & abs(eta) < 3.0").size()',
    jetVeto30Eta3_JetEnDown = 'vetoJets(0.4, "userCand(\'jes-\').pt > 30 & abs(eta) < 3.0").size()',
    jetVeto30Eta3_JetEnUp = 'vetoJets(0.4, "userCand(\'jes+\').pt > 30 & abs(eta) < 3.0").size()',
    jetVeto30_DR05 = 'vetoJets(0.5, "pt > 30 & abs(eta) < 5.0").size()',
    jetVeto40 = 'vetoJets(0.4, "pt > 40 & abs(eta) < 5.0").size()',
    jetVeto40_DR05 = 'vetoJets(0.5, "pt > 40 & abs(eta) < 5.0").size()',
    #leadingJetPt = '? (vetoJets(0.4, "abs(eta) < 5.0 & userInt(\'fullIdLoose\')").size() > 0) ? vetoJets(0.4, "abs(eta) < 5.0 & userInt(\'fullIdLoose\')").at(0).pt() : -1.',
)

overlaps = PSet(
    #objectElectronPt15IdIsoVtxOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 15 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2").size()', 
    #objectElectronPt10IdIsoVtxOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & abs(userFloat(\'dz\')) < 0.2").size()', 
    #objectElectronPt15IdVtxOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 15 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & abs(userFloat(\'dz\')) < 0.2").size()',
    #objectElectronPt10IdVtxOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.5 & userInt(\'mvaidwp\') > 0.5 & abs(userFloat(\'dz\')) < 0.2").size()',
   
    objectMuonIdIsoVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    objectMuonIdVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & userFloat(\'dz\') < 0.2").size()',
    objectMuonIdIsoStdVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((chargedHadronIso() + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    objectGlobalMuonVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & isGlobalMuon & userFloat(\'dz\') < 0.2").size()',

    objectMuOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 5").size()',
    objectElecOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10").size()',
)

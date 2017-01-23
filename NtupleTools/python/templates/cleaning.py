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

    muVetoZTTp001dxyz = 'vetoMuons(0.001, "pt > 10 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    muVetoZTTp001dxyzR0 = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    dimuonVeto = 'vetoSecondMuon(0.15,"pt > 15 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isGlobalMuon > 0 & isTrackerMuon > 0 & isPFMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    
    #TAU VETOS
    tauVetoPt20Loose3HitsVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byLooseCombinedIsolationDeltaBetaCorr3Hits\') & userFloat(\'dz\') < 0.2").size()',
    tauVetoPt20TightMVALTVtx = 'vetoTaus(0.4, "pt > 20 & abs(eta) < 2.5 & tauID(\'decayModeFinding\') & tauID(\'byTightIsolationMVArun2v1DBoldDMwLT\') & userFloat(\'dz\') < 0.2").size()',

    #ELECTRON VETOS
    eVetoMVAIsoVtx = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & userFloat(\'MVANonTrigWP90\') > 0.5 & ((userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt) < 0.3 & userFloat(\'dz\') < 0.2").size()',
    eVetoMVAIso = 'vetoElectrons(0.4, "pt > 10 & abs(eta) < 2.5 & userFloat(\'MVANonTrigWP90\') > 0.5 & (userIso(0) + max(userIso(1) + neutralHadronIso - 0.5*userIso(2), 0))/pt < 0.3").size()',
    eVetoZTTp001dxyz = 'vetoElectrons(0.001, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    eVetoZTTp001dxyzR0 = 'vetoElectrons(0.0, "pt > 10 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'MVANonTrigWP90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    dielectronVeto = 'vetoSecondElectron(0.15, "pt > 15 & abs(eta) < 2.5 & ( ( pfIsolationVariables().sumChargedHadronPt + max( pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - 0.5 * pfIsolationVariables().sumPUPt, 0.0)) / pt() ) < 0.3 & userFloat(\'CBIDVeto\') > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',


    #B-JET Vetos
    bjetCISVVeto20Loose = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.5426").size()',
    bjetCISVVeto20Medium = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484").size()',
    bjetCISVVeto20Tight = 'vetoJets(0.5, "pt > 20 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.9535").size()',
    bjetCISVVeto30Loose = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.5426").size()',
    bjetCISVVeto30Medium = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.8484").size()',
    bjetCISVVeto30Tight = 'vetoJets(0.5, "pt > 30 & abs(eta) < 2.4 & userFloat(\'idLoose\') > 0.5 & bDiscriminator(\'pfCombinedInclusiveSecondaryVertexV2BJetTags\') > 0.9535").size()',

    #JET VETOS
    jetVeto20 = 'vetoJets(0.5, "pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    jetVeto20_JetEnUp = 'vetoJets(0.5, "userCand(\'jes+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    jetVeto20_JetEnDown = 'vetoJets(0.5, "userCand(\'jes-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    #jetVeto20_JetResUp = 'vetoJets(0.5, "userCand(\'jres+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    #jetVeto20_JetResDown = 'vetoJets(0.5, "userCand(\'jres+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    jetVeto30 = 'vetoJets(0.5, "pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    jetVeto30_JetEnUp = 'vetoJets(0.5, "userCand(\'jes+\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    jetVeto30_JetEnDown = 'vetoJets(0.5, "userCand(\'jes-\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    #jetVeto30_JetResUp = 'vetoJets(0.5, "userCand(\'jres+\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',
    #jetVeto30_JetResDown = 'vetoJets(0.5, "userCand(\'jres-\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idLoose\') > 0.5").size()',

)

overlaps = PSet(
   
    objectMuonIdIsoVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((userIso(0) + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    objectMuonIdVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & userFloat(\'dz\') < 0.2").size()',
    objectMuonIdIsoStdVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & userInt(\'tightID\') > 0.5 & ((chargedHadronIso() + max(photonIso()+neutralHadronIso()-0.5*puChargedHadronIso,0.0))/pt()) < 0.15 & userFloat(\'dz\') < 0.2").size()',
    objectGlobalMuonVtxOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 10 & abs(eta) < 2.4 & isGlobalMuon & userFloat(\'dz\') < 0.2").size()',

    objectMuOverlap = 'overlapMuons({object_idx}, 0.4, "pt > 5").size()',
    objectElecOverlap = 'overlapElectrons({object_idx}, 0.4, "pt > 10").size()',
)

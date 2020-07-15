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

    #muVetoZTTp001dxyzR0 = 'vetoMuons(0.0, "pt > 10 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isMediumMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    #dimuonVeto = 'vetoSecondMuon(0.15,"pt > 15 & abs(eta) < 2.4 & ( ( pfIsolationR04().sumChargedHadronPt + max( pfIsolationR04().sumNeutralHadronEt + pfIsolationR04().sumPhotonEt - 0.5 * pfIsolationR04().sumPUPt, 0.0)) / pt() ) < 0.3 & isGlobalMuon > 0 & isTrackerMuon > 0 & isPFMuon > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    
    ##ELECTRON VETOS

    #eVetoZTTp001dxyzR0 = 'vetoElectrons(0.0, "pt > 10 & abs(eta) < 2.5 & ( pfIsolationVariables().sumChargedHadronPt + max(0.0,pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - userFloat(\'rho_fastjet\')*userFloat(\'EffectiveArea\'))) / pt() < 0.3 & electronID(\'mvaEleID-Fall17-noIso-V2-wp90\') > 0 & passConversionVeto() > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',
    #dielectronVeto = 'vetoSecondElectron(0.15, "pt > 15 & abs(eta) < 2.5 & ( pfIsolationVariables().sumChargedHadronPt + max(0.0,pfIsolationVariables().sumNeutralHadronEt + pfIsolationVariables().sumPhotonEt - userFloat(\'rho_fastjet\')*userFloat(\'EffectiveArea\'))) / pt() < 0.3 & electronID(\'cutBasedElectronID-Fall17-94X-V2-veto\') > 0 & abs( userFloat(\'ipDXY\') ) < 0.045 & abs( userFloat(\'dz\') ) < 0.2").size()',

    #(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & 
    #B-JET Vetos
    bjetDeepCSVVeto20Loose_2016_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.2217").size()',
    bjetDeepCSVVeto20Medium_2016_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321").size()',
    bjetDeepCSVVeto20Tight_2016_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.8953").size()',
    bjetDeepCSVVeto20Medium_2016_DR0 = 'vetoJets(0.0, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.6321").size()',

    bjetDeepCSVVeto20Loose_2017_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.1522").size()',
    bjetDeepCSVVeto20Medium_2017_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941").size()',
    bjetDeepCSVVeto20Tight_2017_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.8001").size()',
    bjetDeepCSVVeto20Medium_2017_DR0 = 'vetoJets(0.0, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4941").size()',

    bjetDeepCSVVeto20Loose_2018_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.1241").size()',
    bjetDeepCSVVeto20Medium_2018_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184").size()',
    bjetDeepCSVVeto20Tight_2018_DR0p5 = 'vetoJets(0.5, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.7527").size()',
    bjetDeepCSVVeto20Medium_2018_DR0 = 'vetoJets(0.0, "pt > 25 & abs(eta) < 2.4 & userFloat(\'idTight\') > 0.5 & (bDiscriminator(\'pfDeepCSVJetTags:probb\') + bDiscriminator(\'pfDeepCSVJetTags:probbb\')) > 0.4184").size()',


    #JET VETOS
    jetVeto20 = 'vetoJets(0.5, "pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
    jetVeto20_JetEnUp = 'vetoJets(0.5, "userCand(\'jes+\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
    jetVeto20_JetEnDown = 'vetoJets(0.5, "userCand(\'jes-\').pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
    jetVeto30 = 'vetoJets(0.5, "pt > 30 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
    jetVeto30_JetEnUp = 'vetoJets(0.5, "userCand(\'jes+\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
    jetVeto30_JetEnDown = 'vetoJets(0.5, "userCand(\'jes-\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',

    jetVeto20WoNoisyJets = 'vetoJets(0.5, "(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 20 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
    jetVeto30WoNoisyJets = 'vetoJets(0.5, "(pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & pt > 30 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
    jetVeto30WoNoisyJets_JetEnUp = 'vetoJets(0.5, "(userCand(\'jes+\').pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & userCand(\'jes+\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
    jetVeto30WoNoisyJets_JetEnDown = 'vetoJets(0.5, "(userCand(\'jes-\').pt > 50 | (abs(eta) < 2.65 | abs(eta) > 3.139)) & userCand(\'jes-\').pt > 30 & abs(eta) < 4.7 & userFloat(\'idTight\') > 0.5 & (userInt(\'pileupJetId:fullId\')>3 | pt>50)").size()',
)

overlaps = PSet(
   
)

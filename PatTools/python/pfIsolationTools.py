'''

Muck about with the PFIsolation for leptons to add the H2Tau defintions.

Author: Evan K. Friis, UW

Isolation Veto cones, from

https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#Object_ID_AN1

Electrons
---------

Iso              Type                        src  particles Veto  Threshold (GeV)
ChargedIso       pfAllChargedParticles       0.01 ***(EB)   0.015 (EE)      0
PhotonIso        pfAllPhotons                0.08 (EB,      EE)   0
NeutralHadronIso pfAllNeutralHadrons         none 0
DeltaBeta        pfPileUpAllChargedParticles none 0

Muons
Iso Type	 src particles	 Veto	 Threshold (GeV)
ChargedIso	 pfAllChargedParticles	 0.0001	 0
PhotonIso	 pfAllPhotons	 0.01	 0.5
NeutralHadronIso	 pfAllNeutralHadrons	 0.01	 0.5
DeltaBeta	 pfPileUpAllChargedParticles	 0.01	 0.5


'''

import FWCore.ParameterSet.Config as cms

def setup_h2tau_iso(process):
    print "Building H2Tau custom lepton isolations"

    process.h2TauIsoSequence = cms.Sequence()
    process.patElectrons.isolationValues.user = cms.VInputTag()
    process.patElectrons.isolationValuesNoPFId.user = cms.VInputTag()
    process.patMuons.isolationValues.user = cms.VInputTag()

    ######################################################################
    ### Electron isolation ###############################################
    ######################################################################

    # Electron charged isolation
    process.elPFIsoValueChargedAll04PFIdPFIsoH2Tau = \
            process.elPFIsoValueChargedAll04PFIdPFIso.clone()
    process.elPFIsoValueChargedAll04PFIdPFIsoH2Tau.deposits[0].vetos = \
            cms.vstring(
                'EcalBarrel:ConeVeto(0.01)','EcalEndcaps:ConeVeto(0.015)',
            )
    process.h2TauIsoSequence += process.elPFIsoValueChargedAll04PFIdPFIsoH2Tau
    process.patElectrons.isolationValues.user.append(
        cms.InputTag("elPFIsoValueChargedAll04PFIdPFIsoH2Tau"))

    # Gamma isolation - larger cone to prevent badly reco'd PF Electrons
    # from spoiling the reco electron isolation
    process.elPFIsoValueGamma04PFIdPFIsoH2Tau = \
            process.elPFIsoValueGamma04PFIdPFIso.clone()
    process.elPFIsoValueGamma04PFIdPFIsoH2Tau.deposits[0].vetos = \
            cms.vstring(
                'EcalBarrel:ConeVeto(0.08)','EcalEndcaps:ConeVeto(0.08)',
            )
    process.h2TauIsoSequence += process.elPFIsoValueGamma04PFIdPFIsoH2Tau
    process.patElectrons.isolationValues.user.append(
        cms.InputTag("elPFIsoValueGamma04PFIdPFIsoH2Tau"))

    # No veto for PU
    process.elPFIsoValuePU04PFIdPFIsoH2Tau = \
            process.elPFIsoValuePU04PFIdPFIso.clone()
    process.elPFIsoValuePU04PFIdPFIsoH2Tau.deposits[0].vetos = cms.vstring(
    )
    process.h2TauIsoSequence += process.elPFIsoValuePU04PFIdPFIsoH2Tau
    process.patElectrons.isolationValues.user.append(
        cms.InputTag("elPFIsoValuePU04PFIdPFIsoH2Tau"))

    # Now we need to do the same thing for the NoPFId case...
    # Electron charged isolation
    process.elPFIsoValueChargedAll04NoPFIdPFIsoH2Tau = \
            process.elPFIsoValueChargedAll04NoPFIdPFIso.clone()
    process.elPFIsoValueChargedAll04NoPFIdPFIsoH2Tau.deposits[0].vetos = \
            cms.vstring(
                'EcalBarrel:ConeVeto(0.01)','EcalEndcaps:ConeVeto(0.015)',
            )
    process.h2TauIsoSequence += process.elPFIsoValueChargedAll04NoPFIdPFIsoH2Tau
    process.patElectrons.isolationValuesNoPFId.user.append(
        cms.InputTag("elPFIsoValueChargedAll04NoPFIdPFIsoH2Tau"))

    # Gamma isolation - larger cone to prevent badly reco'd PF Electrons
    # from spoiling the reco electron isolation
    process.elPFIsoValueGamma04NoPFIdPFIsoH2Tau = \
            process.elPFIsoValueGamma04NoPFIdPFIso.clone()
    process.elPFIsoValueGamma04NoPFIdPFIsoH2Tau.deposits[0].vetos = \
            cms.vstring(
                'EcalBarrel:ConeVeto(0.08)','EcalEndcaps:ConeVeto(0.08)',
            )
    process.h2TauIsoSequence += process.elPFIsoValueGamma04NoPFIdPFIsoH2Tau
    process.patElectrons.isolationValuesNoPFId.user.append(
        cms.InputTag("elPFIsoValueGamma04NoPFIdPFIsoH2Tau"))

    # No veto for PU
    process.elPFIsoValuePU04NoPFIdPFIsoH2Tau = \
            process.elPFIsoValuePU04NoPFIdPFIso.clone()
    process.elPFIsoValuePU04NoPFIdPFIsoH2Tau.deposits[0].vetos = cms.vstring(
    )
    process.h2TauIsoSequence += process.elPFIsoValuePU04NoPFIdPFIsoH2Tau
    process.patElectrons.isolationValuesNoPFId.user.append(
        cms.InputTag("elPFIsoValuePU04NoPFIdPFIsoH2Tau"))

    ######################################################################
    ### Muon isolation  ##################################################
    ######################################################################

    # All charged particle isolation
    process.muPFIsoValueChargedAll04PFIsoH2Tau = \
            process.muPFIsoValueChargedAll04PFIso.clone()
    process.muPFIsoValueChargedAll04PFIsoH2Tau.deposits[0].vetos = \
            cms.vstring(
                'EcalBarrel:ConeVeto(0.0001)','EcalEndcaps:ConeVeto(0.0001)',
            )
    process.h2TauIsoSequence += process.muPFIsoValueChargedAll04PFIsoH2Tau
    process.patMuons.isolationValues.user.append(
        cms.InputTag("muPFIsoValueChargedAll04PFIsoH2Tau"))

    # Insert into PAT default sequence, after all the other iso stuff is run.
    # We have to put this at the end since it depends on the IsoDeposits
    # Lets replace some stupid thing we don't use
    process.h2TauIsoSequence += process.muPFIsoValueGamma03PFIso    
    replace_result = process.patDefaultSequence.replace(
        process.muPFIsoValueGamma03PFIso,        
        process.h2TauIsoSequence
        )

def add_hZg_iso_needs(process):
    print "Adding rhos and collections needs for 2011 data in hZg"

    process.load("RecoJets.JetProducers.kt4PFJets_cfi")

    process.pfAllNeutralHadronsAndPhotons = cms.EDProducer(
        "CandViewMerger",
        src = cms.VInputTag(cms.InputTag("pfAllNeutralHadrons"),
                            cms.InputTag("pfAllPhotons"))
        )

    process.kt6PFJetsCentralHZGEle = process.kt4PFJets.clone(
        rParam = cms.double(0.6),
        Rho_EtaMax = cms.double(2.5),        
        doRhoFastjet  = cms.bool(True)
        )
    
    process.kt6PFJetsCentralNeutralHZGMu = process.kt4PFJets.clone(
        rParam        = cms.double(0.6),
        src           = cms.InputTag("pfAllNeutralHadronsAndPhotons"),
        Ghost_EtaMax  = cms.double(3.1),
        Rho_EtaMax    = cms.double(2.5),
        inputEtMin    = cms.double(0.5),
        doAreaFastjet = cms.bool(True),
        doRhoFastjet  = cms.bool(True)
        )

    process.kt6PFJetsCentralHZGMu = process.kt4PFJets.clone(
        rParam = cms.double(0.6),
        Ghost_EtaMax = cms.double(2.5),
        Rho_EtaMax = cms.double(2.5),
        doAreaFastjet = cms.bool(True),
        doRhoFastjet  = cms.bool(True)
        )

    process.hZg_muons = cms.Sequence(
        process.pfAllNeutralHadronsAndPhotons+
        process.kt6PFJetsCentralHZGEle
        process.kt6PFJetsCentralNeutralHZGMu+
        process.kt6PFJetsCentralHZGMu)

    #add in isolations with the wrong vetos in case some people are using them
    
    # Charged particle isolation
    process.muPFIsoValueCharged04PFIsoHZGWrongVeto = \
            process.muPFIsoValueChargedAll04PFIso.clone()
    process.muPFIsoValueNeutral04PFIsoHZGWrongVeto = \
            process.muPFIsoValueNeutral04PFIso.clone()
    process.muPFIsoValueGamma04PFIsoHZGWrongVeto = \
            process.muPFIsoValueGamma04PFIso.clone()

    process.muPFIsoValueCharged04PFIsoHZGWrongVeto.deposits[0].vetos = cms.vstring('')
    process.muPFIsoValueNeutral04PFIsoHZGWrongVeto.deposits[0].vetos = cms.vstring('Threshold(0.5)')
    process.muPFIsoValueGamma04PFIsoHZGWrongVeto.deposits[0].vetos = cms.vstring('Threshold(0.5)')

    process.hZg_muons += process.muPFIsoValueCharged04PFIsoHZGWrongVeto
    process.hZg_muons += process.muPFIsoValueNeutral04PFIsoHZGWrongVeto
    process.hZg_muons += process.muPFIsoValueGamma04PFIsoHZGWrongVeto
        
    process.patMuons.isolationValues.user.append(
        cms.InputTag("muPFIsoValueCharged04PFIsoHZGWrongVeto"))
    process.patMuons.isolationValues.user.append(
        cms.InputTag("muPFIsoValueNeutral04PFIsoHZGWrongVeto"))
    process.patMuons.isolationValues.user.append(
        cms.InputTag("muPFIsoValueGamma04PFIsoHZGWrongVeto"))

    process.hZg_muons += process.muPFIsoValueGamma03PFIso    
    
    replace_result = process.patDefaultSequence.replace(
        process.muPFIsoValueGamma03PFIso,        
        process.hZg_muons
        )

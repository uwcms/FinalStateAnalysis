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

    # Electron charged isolation
    process.muPFIsoValueChargedAll04PFIsoH2Tau = \
            process.muPFIsoValueChargedAll04PFIso.clone()
    process.muPFIsoValueChargedAll04PFIsoH2Tau.deposits[0].vetos = \
            cms.vstring(
                'EcalBarrel:ConeVeto(0.0001)','EcalEndcaps:ConeVeto(0.0001)',
            )
    process.h2TauIsoSequence += process.muPFIsoValueChargedAll04PFIsoH2Tau
    process.patMuons.isolationValues.user.append(
        cms.InputTag("muPFIsoValueChargedAll04PFIsoH2Tau"))

    # Gamma isolation - larger cone to prevent badly reco'd PF Electrons
    # from spoiling the reco electron isolation
    process.muPFIsoValueGamma04PFIsoH2Tau = \
            process.muPFIsoValueGamma04PFIso.clone()
    process.muPFIsoValueGamma04PFIsoH2Tau.deposits[0].vetos = \
            cms.vstring(
                'EcalBarrel:ConeVeto(0.01)','EcalEndcaps:ConeVeto(0.01)',
            )
    process.h2TauIsoSequence += process.muPFIsoValueGamma04PFIsoH2Tau
    process.patMuons.isolationValues.user.append(
        cms.InputTag("muPFIsoValueGamma04PFIsoH2Tau"))

    # No veto for PU
    process.muPFIsoValuePU04PFIsoH2Tau = \
            process.muPFIsoValuePU04PFIso.clone()
    process.muPFIsoValuePU04PFIsoH2Tau.deposits[0].vetos = cms.vstring(
    )
    process.h2TauIsoSequence += process.muPFIsoValuePU04PFIsoH2Tau
    process.patMuons.isolationValues.user.append(
        cms.InputTag("muPFIsoValuePU04PFIsoH2Tau"))

    # Insert into PAT default sequence, after all the other iso stuff is run.
    # We have to put this at the end since it depends on the IsoDeposits
    # Lets replace some stupid thing we don't use
    replace_result = process.patDefaultSequence.replace(
        process.muPFIsoValueGamma03PFIso, process.h2TauIsoSequence)

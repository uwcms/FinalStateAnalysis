'''
Configure PFNoPileup

Returns PFNoPileup sequence to be run.

Original author: M. Bachtis

'''

import FWCore.ParameterSet.Config as cms

def configurePFNoPileup(process):
    process.load(
        "CommonTools.ParticleFlow.ParticleSelectors.pfCandsForIsolation_cff")

    process.pfPileUpCandidates = cms.EDProducer(
        "TPPFCandidatesOnPFCandidates",
        enable =  cms.bool( True ),
        verbose = cms.untracked.bool( False ),
        name = cms.untracked.string("pileUpCandidates"),
        topCollection = cms.InputTag("pfNoPileUp"),
        bottomCollection = cms.InputTag("particleFlow"),
    )
    #enable PF no Pile Up
    process.pfPileUp.Enable = cms.bool(True)
    #Put all charged particles in charged hadron collection(electrons and muons)
    process.pfAllChargedHadrons.pdgId = cms.vint32(
        211,-211,321,-321,999211,2212,-2212,11,-11,13,-13)
    assert(process.pfAllChargedHadrons.src.value() == "pfNoPileUp")
    process.pileUpHadrons = cms.EDFilter(
        "PdgIdPFCandidateSelector",
        src = cms.InputTag("pfPileUpCandidates"),
        pdgId = cms.vint32(211,-211,321,-321,999211,2212,-2212,11,-11,13,-13)
    )
    process.pfAllElectrons.src = cms.InputTag("pfNoPileUp")

    process.pfAllMuons = cms.EDFilter(
        "PdgIdPFCandidateSelector",
        src = cms.InputTag("pfNoPileUp"),
        pdgId = cms.vint32(13,-13)
    )

    process.pfPostSequence = cms.Sequence(
        process.pfCandsForIsolationSequence+
        process.pfAllMuons+
        process.pfPileUpCandidates+
        process.pileUpHadrons
    )
    return process.pfPostSequence

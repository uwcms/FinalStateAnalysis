'''

Adapt the path to use PF isolation for pat::Electrons
Original author: M. Bachtis

'''
import FWCore.ParameterSet.Config as cms
from CommonTools.ParticleFlow.Isolation.tools_cfi import isoDepositReplace

def addElecPFIsolation(process, patSequence):
    electrons = 'gsfElectrons'
    process.elePFIsoDepositAll     = isoDepositReplace(electrons,cms.InputTag("pfNoPileUp"))
    process.elePFIsoDepositCharged = isoDepositReplace(electrons,"pfAllChargedHadrons")
    process.elePFIsoDepositNeutral = isoDepositReplace(electrons,"pfAllNeutralHadrons")
    process.elePFIsoDepositGamma = isoDepositReplace(electrons,"pfAllPhotons")
    process.elePFIsoDepositPU = isoDepositReplace(electrons,cms.InputTag("pileUpHadrons"))
    process.elePFIsoDeposits = cms.Sequence(
        process.elePFIsoDepositAll*
        process.elePFIsoDepositCharged*
        process.elePFIsoDepositNeutral*
        process.elePFIsoDepositGamma*
        process.elePFIsoDepositPU
    )
    #And Values
    process.elePFIsoValueAll = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("elePFIsoDepositAll"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.03','Threshold(1.0)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.elePFIsoValueCharged = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("elePFIsoDepositCharged"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.03','Threshold(0.0)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.elePFIsoValueNeutral = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("elePFIsoDepositNeutral"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.08','Threshold(0.5)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.elePFIsoValueGamma = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("elePFIsoDepositGamma"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.05','Threshold(0.5)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.elePFIsoValuePU = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("elePFIsoDepositPU"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.0','Threshold(0.5)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.elePFIsoValues =  cms.Sequence(
        process.elePFIsoValueAll
        * process.elePFIsoValueCharged
        * process.elePFIsoValueNeutral
        * process.elePFIsoValueGamma
        * process.elePFIsoValuePU
    )
    #
    #KLUDGE : Since PAT electron does not support custom iso deposits
    #put the pileup in the place of all candidates
    #
    process.patElectrons.isoDeposits = cms.PSet(
        pfAllParticles   = cms.InputTag("elePFIsoDepositAll"),
        pfChargedHadrons = cms.InputTag("elePFIsoDepositCharged"),
        pfNeutralHadrons = cms.InputTag("elePFIsoDepositNeutral"),
        pfPhotons        = cms.InputTag("elePFIsoDepositGamma")
    )
    ###KLUDGE -> Add DB in UserIso
    process.patElectrons.isolationValues = cms.PSet(
        pfAllParticles   = cms.InputTag("elePFIsoValuePU"),
        pfChargedHadrons = cms.InputTag("elePFIsoValueCharged"),
        pfNeutralHadrons = cms.InputTag("elePFIsoValueNeutral"),
        pfPhotons        = cms.InputTag("elePFIsoValueGamma")
    )
    # Inject into sequence
    process.eleisolationSequence = cms.Sequence(
        process.elePFIsoDeposits*
        process.elePFIsoValues*
        process.patElectrons
    )
    inserted = patSequence.replace(process.patElectrons, process.eleisolationSequence)
    assert(inserted)

'''

Adapt the path to use PF isolation for pat::Muons

Original author: M. Bachtis

'''
import FWCore.ParameterSet.Config as cms
from CommonTools.ParticleFlow.Isolation.tools_cfi import isoDepositReplace

def addMuPFIsolation(process, patSequence):
    muons = 'muons'
    process.muPFIsoDepositAll     = isoDepositReplace(
        muons,cms.InputTag("pfNoPileUp"))
    process.muPFIsoDepositCharged = isoDepositReplace(
        muons,"pfAllChargedHadrons")
    process.muPFIsoDepositNeutral = isoDepositReplace(
        muons,"pfAllNeutralHadrons")
    process.muPFIsoDepositGamma = isoDepositReplace(
        muons,"pfAllPhotons")
    #Isodeposit from PileUp- For Vertex subtraction!!!!
    process.muPFIsoDepositPU = isoDepositReplace(
        muons,cms.InputTag("pileUpHadrons"))

    process.muPFIsoDeposits = cms.Sequence(
        process.muPFIsoDepositAll*
        process.muPFIsoDepositCharged*
        process.muPFIsoDepositPU*
        process.muPFIsoDepositNeutral*
        process.muPFIsoDepositGamma
    )
    #And Values
    process.muPFIsoValueAll = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("muPFIsoDepositAll"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.001','Threshold(0.5)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.muPFIsoValueCharged = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("muPFIsoDepositCharged"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.0001','Threshold(0.0)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.muPFIsoValueNeutral = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("muPFIsoDepositNeutral"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.01','Threshold(0.5)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.muPFIsoValueGamma = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("muPFIsoDepositGamma"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.01','Threshold(0.5)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.muPFIsoValuePU = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("muPFIsoDepositPU"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.0001','Threshold(0.5)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.muPFIsoValuePULow = cms.EDProducer(
        "CandIsolatorFromDeposits",
        deposits = cms.VPSet(
            cms.PSet(
                src = cms.InputTag("muPFIsoDepositPU"),
                deltaR = cms.double(0.4),
                weight = cms.string('1'),
                vetos = cms.vstring('0.0001','Threshold(0.0)'),
                skipDefaultVeto = cms.bool(True),
                mode = cms.string('sum')
            )
        )
    )
    process.muPFIsoValues =  cms.Sequence(
        process.muPFIsoValueAll
        * process.muPFIsoValueCharged
        * process.muPFIsoValueNeutral
        * process.muPFIsoValueGamma
        * process.muPFIsoValuePU
        * process.muPFIsoValuePULow
    )
    process.patMuons.isoDeposits = cms.PSet(
        particle         = cms.InputTag("muPFIsoDepositAll"),
        pfChargedHadrons = cms.InputTag("muPFIsoDepositCharged"),
        pfNeutralHadrons = cms.InputTag("muPFIsoDepositNeutral"),
        pfPhotons        = cms.InputTag("muPFIsoDepositGamma")
    )
    process.patMuons.isolationValues = cms.PSet(
        particle         = cms.InputTag("muPFIsoValueAll"),
        pfChargedHadrons = cms.InputTag("muPFIsoValueCharged"),
        pfNeutralHadrons = cms.InputTag("muPFIsoValueNeutral"),
        pfPhotons        = cms.InputTag("muPFIsoValueGamma"),
        user = cms.VInputTag(
            cms.InputTag("muPFIsoValuePU"),
            cms.InputTag("muPFIsoValuePULow")
        )
    )
    # Inject into the sequence
    process.muPFIsolation = cms.Sequence(
        process.muPFIsoDeposits*
        process.muPFIsoValues*
        process.patMuons
    )
    inserted = patSequence.replace(process.patMuons, process.muPFIsolation)
    assert(inserted)

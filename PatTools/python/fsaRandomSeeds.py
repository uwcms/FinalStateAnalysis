'''
Random number seeds needed by FSA modules.
'''

import FWCore.ParameterSet.Config as cms


def add_fsa_random_seeds(process):
    #add seed for electron energy corrections
    process.RandomNumberGeneratorService.patElectronEnergyCorrections = \
        cms.PSet(
            initialSeed=cms.untracked.uint32(1234556789),
            engineName=cms.untracked.string('TRandom3')
        )
    process.RandomNumberGeneratorService.patMuonRochesterCorrectionEmbedder = \
        cms.PSet(
            initialSeed=cms.untracked.uint32(987654321),
            engineName=cms.untracked.string('TRandom3')
        )
    process.RandomNumberGeneratorService.calibratedPatElectrons = \
        cms.PSet(
            initialSeed=cms.untracked.uint32(987654321),
            engineName=cms.untracked.string('TRandom3')
        )

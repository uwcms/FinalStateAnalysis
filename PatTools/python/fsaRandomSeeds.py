import FWCore.ParameterSet.Config as cms

##
#
# A file for adding random number seeds needed by FSA modules.
#
##

def add_fsa_random_seeds(process):

    #add seed for electron energy corrections
    process.RandomNumberGeneratorService.patElectronEnergyCorrections = \
        cms.PSet(
        initialSeed = cms.untracked.uint32(1234556789),
        engineName = cms.untracked.string('TRandom3')
        )

#!/usr/bin/env cmsRun
#flake8: noqa
'''

Make a GEN-SIM-RAW-RECO file using a particle gun.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms

# Get command line options
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing('analysis')
# Set useful defaults
options.outputFile = "uct_efficiency_tree.root"
options.register(
    'pdgId',
    11,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'PDG of simulated particle')
options.register(
    'minE',
    45,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'Minimum energy of simulated particle')
options.register(
    'maxE',
    46,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'Maximum energy of simulated particle')
options.register(
    'minEta',
    -3,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.float,
    'Minimum eta of simulated particle')
options.register(
    'maxEta',
    3,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.float,
    'Maximum eta of simulated particle')
options.register(
    'minPhi',
    -3.14159265359,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.float,
    'Minimum phi of simulated particle')
options.register(
    'maxPhi',
    3.14159265359,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.float,
    'Maximum phi of simulated particle')
options.register(
    'seed',
    1,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    'Random seed')

options.parseArguments()

# with command line options: Configuration/Generator/python/SingleElectronE120EHCAL_cfi.py -s GEN,SIM,DIGI,L1,DIGI2RAW,RAW2DIGI,RECO --conditions auto:mc -n 100 --no_exec --eventcontent FEVT
import FWCore.ParameterSet.Config as cms

process = cms.Process('RECO')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

process.RandomNumberGeneratorService.generator.initialSeed = options.seed

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.381.2.13 $'),
    annotation = cms.untracked.string('Configuration/Generator/python/SingleElectronE120EHCAL_cfi.py nevts:100'),
    name = cms.untracked.string('PyReleaseValidation')
)

# Output definition

process.FEVToutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.FEVTEventContent.outputCommands,
    fileName = cms.untracked.string(options.outputFile),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

process.generator = cms.EDProducer("FlatRandomEGunProducer",
    PGunParameters = cms.PSet(
        PartID = cms.vint32(options.pdgId),
        MaxEta = cms.double(options.maxEta),
        MaxPhi = cms.double(options.maxPhi),
        MinEta = cms.double(options.minEta),
        MinE = cms.double(options.minE),
        MinPhi = cms.double(options.minPhi),
        MaxE = cms.double(options.maxE)
    ),
    Verbosity = cms.untracked.int32(0),
    psethack = cms.string('single electron E 120 EHCAL'),
    AddAntiParticle = cms.bool(False),
    firstRun = cms.untracked.uint32(1)
)


# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.raw2digi_step = cms.Path(process.RawToDigi)
process.reconstruction_step = cms.Path(process.reconstruction)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVToutput_step = cms.EndPath(process.FEVToutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.digi2raw_step,process.raw2digi_step,process.reconstruction_step,process.endjob_step,process.FEVToutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq



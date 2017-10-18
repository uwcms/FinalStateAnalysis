#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms


process = cms.Process('PAT')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.PATMC_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

files = ['/store/relval/CMSSW_7_0_0/RelValTTbar_13/GEN-SIM-RECO/PU50ns_POSTLS170_V4-v2/00000/265B9219-FF98-E311-BF4A-02163E00EA95.root']

# Input source
process.source = cms.Source("PoolSource",
    fileNames=cms.untracked.vstring(files), 
    skipEvents=cms.untracked.uint32(0),
)

process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True)
)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.19 $'),
    annotation = cms.untracked.string('miniAOD-prod nevts:1'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.MINIAODSIMoutput = cms.OutputModule("PoolOutputModule",
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('miniAOD-prod_PAT.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PLS170_V7AN1::All', '')

# Path and EndPath definitions
process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.goodVertices)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions

import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
from FinalStateAnalysis.Utilities.EventList import EventList

# Create our option set, with some extra options
options = TauVarParsing.TauVarParsing(
    evtList='/afs/hep.wisc.edu/home/efriis/event_lists/mikes_LP_MuTauInclusiveEvents.reformatted.txt'
)


example_files = [
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v6/000/175/770/783A319B-AADA-E011-8136-BCAEC5329713.root",
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v6/000/175/755/8EA1A088-6CDA-E011-9322-BCAEC532970D.root",
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v6/000/175/754/8AE67E46-6CDA-E011-A35A-BCAEC532972D.root",
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v6/000/175/744/38CE631A-69DA-E011-BDCC-BCAEC5329731.root",
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v6/000/175/742/520ABDD8-69DA-E011-B14A-003048F118C4.root",
    "/store/data/Run2011A/SingleMu/AOD/PromptReco-v6/000/175/735/A8F2188D-70DA-E011-920C-003048F024E0.root",
]

for example_file in example_files:
    options.inputFiles = example_file

options.parseArguments()

evt_list_file = open(options.evtList, 'r')
evt_list = EventList(evt_list_file)

process = cms.Process("PAT")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    eventsToProcess = evt_list.eventRange()
)

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string(options.outputFile),
    outputCommands = cms.untracked.vstring('keep *')
)

process.o = cms.EndPath(process.out)

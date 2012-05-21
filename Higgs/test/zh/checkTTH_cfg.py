import FWCore.ParameterSet.Config as cms
import glob
import json

input_data = '/hdfs/store/user/efriis/2012-03-05-EWKPatTuple/VH_120/*/*root'
event_list = 'results/analysis/*/VH_120.events'
outputFile = 'plot_vhtt_after_bjet.root'

input_data = '/hdfs/store/user/efriis/2012-03-05-EWKPatTuple/VH_120_HWW/*/*root'
event_list = 'results/analysis/*/VH_120_HWW.events'
outputFile = 'plot_vhww_after_bjet.root'

process = cms.Process("TUPLETEST")

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(
        ['file:' + x for x in glob.glob(input_data)]
    ),
)

event_list_files = glob.glob(event_list)
events_to_process = []

for file in event_list_files:
    evt_data = json.load(open(file, 'r'))
    for evt in evt_data:
        the_evt = tuple(evt['evt'])
        events_to_process.append("%i:%i:%i" % the_evt)

process.source.eventsToProcess = cms.untracked.VEventRange(events_to_process)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(outputFile)
)

process.plotGenStuff = cms.EDAnalyzer(
    "PATFinalStateEventHistoAnalyzer",
    src = cms.InputTag("patFinalStateEventProducer"),
    histograms = cms.VPSet(
        cms.PSet(
            min = cms.untracked.double(-0.5),
            max = cms.untracked.double(200.5),
            nbins = cms.untracked.int32(201),
            name = cms.untracked.string("procID"),
            description = cms.untracked.string("procID"),
            plotquantity = cms.untracked.string("genEventInfo.signalProcessID"),
            lazyParsing = cms.untracked.bool(True),
        )
    )
)

process.p = cms.Path(process.plotGenStuff)

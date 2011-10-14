import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing()

import sys

#options.inputFiles = 'file:/hdfs/store/user/efriis//2011-08-02-TauIdPatTuple-Ztautau_pythia-tauID_patTuple_cfg/1/tauID_patTuple_cfg-skimTauIdEffSample2_cfg-B25A4C08-B87C-E011-9692-002481E1026A.root'

options.inputFiles = 'file:/hdfs/store/user/efriis//2011-08-16-v2-TauIdPatTuple-Ztautau_pythia-tauID_patTuple_cfg/1/tauID_patTuple_cfg-skimTauIdEffSample2_cfg-0047896C-D77C-E011-B861-00215AD4D670.root'
options.inputFiles = 'file:/hdfs/store/user/efriis//2011-08-16-v2-TauIdPatTuple-Ztautau_pythia-tauID_patTuple_cfg/1/tauID_patTuple_cfg-skimTauIdEffSample2_cfg-00A48019-BD7C-E011-8B0C-003048C69292.root'
options.inputFiles = 'file:/hdfs/store/user/efriis//2011-08-16-v2-TauIdPatTuple-Ztautau_pythia-tauID_patTuple_cfg/1/tauID_patTuple_cfg-skimTauIdEffSample2_cfg-02000238-B57C-E011-ABBE-003048D4DFB8.root'
options.inputFiles = 'file:/hdfs/store/user/efriis//2011-08-16-v2-TauIdPatTuple-Ztautau_pythia-tauID_patTuple_cfg/1/tauID_patTuple_cfg-skimTauIdEffSample2_cfg-02674660-AA7C-E011-9BB8-003048C69292.root'

options.outputFile="histos.root"
print sys.argv
options.parseArguments()

process = cms.Process("FWLitePlots")

process.fwliteInput = cms.PSet(
    fileNames = cms.vstring(options.inputFiles),  ## mandatory
    maxEvents   = cms.int32(-1),                              ## optional
    outputEvery = cms.uint32(200),                             ## optional
)

process.fwliteOutput = cms.PSet(
    fileName = cms.string(options.outputFile)      ## mandatory
)

import FinalStateAnalysis.TagAndProbe.analysisRegions_cfi as regions

# Define all the regions

process.myAnalyzer = cms.PSet(
    muTauPairs = cms.InputTag('muTauPairs'), ## input for the simple example above
    zMuMuSrc = cms.InputTag("zMuMuHypotheses"),
    regions = cms.PSet(
        qcdOS = regions.qcdEnrichedRegionOS,
        qcdSS = regions.qcdEnrichedRegionSS,
        qcdPassSS = regions.qcdEnrichedRegionSSPassing,
        qcdFailSS = regions.qcdEnrichedRegionSSFailing,
        qcdPassOS = regions.qcdEnrichedRegionOSPassing,
        qcdFailOS = regions.qcdEnrichedRegionOSFailing,

        sigOS = regions.signalRegionOS,
        sigSS = regions.signalRegionSS,
        sigPassOS = regions.signalRegionOSPassing,
        sigPassSS = regions.signalRegionSSPassing,
        sigFailOS = regions.signalRegionOSFailing,
        sigFailSS = regions.signalRegionSSFailing,

        sigTightPassOS = regions.signalRegionTightOSPassing,
        sigTightPassSS = regions.signalRegionTightSSPassing,

        wjetsOS = regions.wjetsEnrichedRegionOS,
        wjetsSS = regions.wjetsEnrichedRegionSS,
        wjetsPassSS = regions.wjetsEnrichedRegionSSPassing,
        wjetsFailSS = regions.wjetsEnrichedRegionSSFailing,
        wjetsPassOS = regions.wjetsEnrichedRegionOSPassing,
        wjetsFailOS = regions.wjetsEnrichedRegionOSFailing,
    ),
    skimCounter = cms.InputTag("totalEventsProcessed"),
    weightSrcs = cms.VInputTag(
        cms.InputTag("lumiWeights", "3bx")
    ),
)

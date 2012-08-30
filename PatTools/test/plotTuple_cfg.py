#!/usr/bin/env cmsRun
import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    ewkSkim=1,    # Apply EWK skim conditions
    skipEvents=0, # For debugging
)

options.inputFiles = "file:output.root"
options.outputFile = 'plots.root'

options.parseArguments()

process = cms.Process("TUPLETEST")

process.source = cms.Source(
    "PoolSource",
    fileNames = cms.untracked.vstring(options.inputFiles),
    skipEvents = cms.untracked.uint32(options.skipEvents),
)
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string(options.outputFile)
)

pt = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("Pt"),
    description = cms.untracked.string("p_{T}"),
    plotquantity = cms.untracked.string("pt"),
    lazyParsing = cms.untracked.bool(True),
)

hasMuTightID = pt.clone(
    min = -0.5,
    max = 1.5,
    nbins = 2,
    name = "hasMuTightID",
    plotquantity = "daughter(0).hasUserInt('tightID')"
)

muTightID = pt.clone(
    min = -0.5,
    max = 1.5,
    nbins = 2,
    name = "muTightID",
    plotquantity = "daughter(0).userInt('tightID')"
)

muWWID = pt.clone(
    min = -0.5,
    max = 1.5,
    nbins = 2,
    name = "muWWID",
    plotquantity = "daughter(0).userInt('WWID')"
)

hasMVAIsoWP = pt.clone(
    min = -0.5,
    max = 1.5,
    nbins = 2,
    name = "mvaIsoWP1",
    plotquantity = "daughter(0).userInt('mvaisowp1')"
)

isPF = pt.clone(
    min = -0.5,
    max = 1.5,
    nbins = 2,
    name = "isPF",
    plotquantity = "daughter(0).pfCandidateRef.isNonnull"
)

hasMuons = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("hasExtMuons"),
    description = cms.untracked.string("Has Ext Muons"),
    plotquantity = cms.untracked.string("hasOverlaps('extMuons')"),
    lazyParsing = cms.untracked.bool(True),
)

hasElectrons = hasMuons.clone(
    description = "Has Ext Electrons",
    name = "hasExtElectrons",
    plotquantity = "hasOverlaps('extElecs')"
)

hasTaus = hasMuons.clone(
    description = "Has Ext Taus",
    name = "hasExtTaus",
    plotquantity = "hasOverlaps('extTaus')",
)

muon_jetpt = pt.clone(
    name = "MuJetPt",
    plotquantity = "daughter(0).userFloat('jetPt')"
)

tau_disc = pt.clone(
    name = "TauIso",
    plotquantity = "daughter(1).tauID('byVLooseCombinedIsolationDeltaBetaCorr')"
)

tau_trigger = pt.clone(
    name = "TauIso",
    plotquantity = "daughter(1).tauID('byVLooseCombinedIsolationDeltaBetaCorr')"
)

muon_reljetpt = pt.clone(
    min = 0,
    max = 5,
    nbins = 100,
    name = "RelMuJetPt",
    plotquantity = "daughter(0).pt/daughter(0).userFloat('jetPt')"
)

extras_jetpt = pt.clone(
    description = "Ext Jet Pt",
    name = "extJetPt",
    plotquantity = "? extras('extTaus', '').size() ? extras('extTaus', '')[0].userCand(\'patJet\').pt : -1"
)

extras_jetbtag = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "Ext Jet Btag",
    name = "extBtag",
    plotquantity = "? extras('extTaus', '').size() ? extras('extTaus', '')[0].userCand(\'patJet\').bDiscriminator(\'\') : -1"
)

jetbtag = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "CSV Jet Btag",
    name = "csvJet",
    plotquantity = "? extras('extTaus', '').size() ? extras('extJets', '')[0].bDiscriminator(\'combinedSecondaryVertexBJetTags\') : -5 "
)

hltPass = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "HLT_15_or_30",
    name = "hlt",
    plotquantity = r"evt.hltResult('HLT_Mu15_v\d+,HLT_Mu30_v\d+')"
)

hltGroup = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "HLT_15_or_30",
    name = "hltGrp",
    plotquantity = r"evt.hltGroup('HLT_Mu15_v\\d+,HLT_Mu30_v\\d+')"
)

hltPrescale = pt.clone(
    min = -5,
    max = 5,
    nbins = 100,
    description = "HLT_15_or_30",
    name = "hltPrescale",
    plotquantity = r"evt.hltPrescale('HLT_Mu15_v\\d+,HLT_Mu30_v\\d+')"
)

lhe_info = pt.clone(
    min = 0,
    max = 100,
    nbins = 100,
    description = "LHE flag",
    name = "LHEFlag",
    plotquantity = "evt().lesHouches().NUP"
)

process_id = pt.clone(
    min = 0,
    max = 100,
    nbins = 100,
    description = "Process ID",
    name = "ProcessID",
    plotquantity = "evt().genEventInfo.signalProcessID()"
)

process.mt = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("finalStateMuTau"),
    histograms = cms.VPSet(
        pt,
        hasMuons,
        hasMVAIsoWP,
        isPF,
        hasMuTightID,
        muTightID,
        muWWID,
        hasElectrons,
        muon_jetpt,
        tau_disc,
        muon_reljetpt,
        hasTaus,
        extras_jetbtag,
        jetbtag,
        extras_jetpt,
        lhe_info,
        hltPass,
        hltGroup,
        hltPrescale,
        process_id,
    )
)

process.et = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("finalStateElecTau"),
    histograms = cms.VPSet(
        calib_pt_diff
    )
)

# MVA MET debugging tools - to eventually be deleted
process.wtf = cms.EDAnalyzer(
    "CandViewHistoAnalyzer",
    src = cms.InputTag("pfMEtMVA"),
    histograms = cms.VPSet(
        pt
    )
)

process.checkMET = cms.EDAnalyzer(
    "CandComparator",
    src1 = cms.InputTag("pfMEtMVA2"),
    src2 = cms.InputTag("pfMEtMVA"),
    comparisons = cms.PSet(
        px = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(-50),
            max = cms.double(50),
            func = cms.string('px'),
        ),
        py = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(-50),
            max = cms.double(50),
            func = cms.string('py'),
        ),
        pt = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(0),
            max = cms.double(100),
            func = cms.string('pt'),
        ),
        phi = cms.PSet(
            nbins = cms.uint32(100),
            min = cms.double(0),
            max = cms.double(3.14),
            func = cms.string('phi'),
        ),
    )
)

process.p = cms.Path(
    process.mt*
    process.et*
    #process.checkMET*
    #process.wtf
)

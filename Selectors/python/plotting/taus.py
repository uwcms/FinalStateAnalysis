import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.selectors.selectors as selectors
import FinalStateAnalysis.Selectors.plotting.candidate as candidate

decayMode = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(14.5),
    nbins = cms.untracked.int32(15),
    name = cms.untracked.string("${name}_DecayMode"),
    description = cms.untracked.string("${nicename} Decay Mode"),
    plotquantity = cms.untracked.string('${getter}decayMode()'),
    lazyParsing = cms.untracked.bool(True),
)

jetpt = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("${name}JetPt"),
    description = cms.untracked.string("${nicename} seed jet p_{T}"),
    plotquantity = cms.untracked.string("${getter}userCand('patJet').pt"),
    lazyParsing = cms.untracked.bool(True),
)

decayFinding = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("${name}_DecayModeFinding"),
    description = cms.untracked.string("${nicename} Decay Mode Finding"),
    plotquantity = cms.untracked.string('${getter}tauID("decayModeFinding")'),
    lazyParsing = cms.untracked.bool(True),
)

vlooseID = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("${name}_VLooseHPS"),
    description = cms.untracked.string("${nicename} VLoose HPS (#Delta #beta)"),
    plotquantity = cms.untracked.string('${getter}tauID("byVLooseCombinedIsolationDeltaBetaCorr")'),
    lazyParsing = cms.untracked.bool(True),
)

looseID = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("${name}_LooseHPS"),
    description = cms.untracked.string("${nicename} Loose HPS (#Delta #beta)"),
    plotquantity = cms.untracked.string('${getter}tauID("byLooseCombinedIsolationDeltaBetaCorr")'),
    lazyParsing = cms.untracked.bool(True),
)

mediumID = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("${name}_MediumHPS"),
    description = cms.untracked.string("${nicename} Medium HPS (#Delta #beta)"),
    plotquantity = cms.untracked.string('${getter}tauID("byMediumCombinedIsolationDeltaBetaCorr")'),
    lazyParsing = cms.untracked.bool(True),
)

btag = cms.PSet(
    min = cms.untracked.double(-10),
    max = cms.untracked.double(10),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_TauBtag"),
    description = cms.untracked.string("${nicename} tau seed jet b-tag"),
    plotquantity = cms.untracked.string('${getter}userCand("patJet").bDiscriminator("")'),
    lazyParsing = cms.untracked.bool(True),
)

tnpPresel = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(0.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("${name}_TauTNPPresel"),
    description = cms.untracked.string("${nicename} tau seed jet b-tag"),
    plotquantity = cms.untracked.string('${getter}userInt("ps_sel_nom")'),
    lazyParsing = cms.untracked.bool(True),
)

genDecayMode = cms.PSet(
    min = cms.untracked.double(-2.5),
    max = cms.untracked.double(16.5),
    nbins = cms.untracked.int32(19),
    name = cms.untracked.string("${name}_GenDecayMode"),
    description = cms.untracked.string("${nicename} tau gen decay mode"),
    plotquantity = cms.untracked.string('${getter}userInt("genDecayMode")'),
    lazyParsing = cms.untracked.bool(True),
)

all = [decayMode, decayModeFinding, vlooseID, looseID, mediumID, jetpt, btag,
       tnpPresel, genDecayMode]

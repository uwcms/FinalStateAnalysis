import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.selectors.selectors as selectors

_binary_bins = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
)

id = cms.PSet(
    _binary_bins,
    name = cms.untracked.string("${name}_MuID_${muID}"),
    description = cms.untracked.string("${nicename} Muon ID"),
    plotquantity = cms.untracked.string(selectors.muons.id.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

reliso = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(2),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_MuRelIso"),
    description = cms.untracked.string("${nicename} Muon Rel. Iso"),
    plotquantity = cms.untracked.string(
        selectors.muons.reliso.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

def get_trigger_matching(trg_name):
    output = cms.PSet(
        _binary_bins,
        name = cms.untracked.string(
            getattr(selectors.muons, trg_name).name.value()),
        description = cms.untracked.string(
            getattr(selectors.muons, trg_name).description.value()),
        plotquantity = cms.untracked.string(
            getattr(selectors.muons, trg_name).plottable.value()),
        lazyParsing = cms.untracked.bool(False),
    )
    return output

hltSingleMu13L3Filtered13  = get_trigger_matching('hltSingleMu13L3Filtered13')
hltDiMuonL3p5PreFiltered8  = get_trigger_matching('hltDiMuonL3p5PreFiltered8')
hltDiMuonL3PreFiltered7  = get_trigger_matching('hltDiMuonL3PreFiltered7')
hltSingleMu30L3Filtered30  = get_trigger_matching('hltSingleMu30L3Filtered30')
hltSingleMuIsoL3IsoFiltered24  = get_trigger_matching('hltSingleMuIsoL3IsoFiltered24')
hltL1Mu3EG5L3Filtered8  = get_trigger_matching('hltL1Mu3EG5L3Filtered8')
hltL1Mu3EG5L3Filtered17  = get_trigger_matching('hltL1Mu3EG5L3Filtered17')

all = [reliso,
       hltSingleMu13L3Filtered13, hltDiMuonL3p5PreFiltered8,
       hltDiMuonL3PreFiltered7, hltSingleMu30L3Filtered30,
       hltSingleMuIsoL3IsoFiltered24,
       hltL1Mu3EG5L3Filtered17, hltL1Mu3EG5L3Filtered8 ]

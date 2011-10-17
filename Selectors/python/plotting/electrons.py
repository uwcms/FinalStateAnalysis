import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.selectors.selectors as selectors

_binary_bins = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
)

def get_trigger_matching(trg_name):
    output = cms.PSet(
        _binary_bins,
        name = cms.untracked.string(
            getattr(selectors.electrons, trg_name).name.value()),
        description = cms.untracked.string(
            getattr(selectors.electrons, trg_name).description.value()),
        plotquantity = cms.untracked.string(
            getattr(selectors.electrons, trg_name).plottable.value()),
        lazyParsing = cms.untracked.bool(False),
    )
    return output

id = cms.PSet(
    _binary_bins,
    name = cms.untracked.string("${name}_EID_${eID}"),
    description = cms.untracked.string("${nicename} Electron ID"),
    plotquantity = cms.untracked.string(selectors.electrons.id.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

reliso = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(2),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_ERelIso"),
    description = cms.untracked.string("${nicename} Electron Rel. Iso"),
    plotquantity = cms.untracked.string(
        selectors.electrons.reliso.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

# Add all the interesting electron trigger filter matchings

hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter = get_trigger_matching(
    'hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter')

hltMu17Ele8CaloIdTPixelMatchFilter = get_trigger_matching(
    'hltMu17Ele8CaloIdTPixelMatchFilter')

hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter = get_trigger_matching(
    'hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter')

hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter = get_trigger_matching(
    'hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter')

all = [
    reliso,
    hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter,
    hltMu17Ele8CaloIdTPixelMatchFilter,
    hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter,
    hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter,
]

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

wwid = cms.PSet(
    _binary_bins,
    name = cms.untracked.string("${name}_MuID_WWID"),
    description = cms.untracked.string("${nicename} Muon WWID"),
    plotquantity = cms.untracked.string(
        selectors.muons.id.plottable.value().replace('${muID}', 'WWID')),
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

relSubDetIso = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(2),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_MuSubDetRelIso"),
    description = cms.untracked.string("${nicename} Muon Sub. Det. Rel. Iso"),
    plotquantity = cms.untracked.string(
        selectors.muons.relSubDetIso.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)


ecalIso = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(20),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_ECALIso"),
    description = cms.untracked.string("${nicename} Abs. ECAL Iso"),
    plotquantity = cms.untracked.string(
        selectors.muons.ecalIso.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

hcalIso = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(20),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_HCALIso"),
    description = cms.untracked.string("${nicename} Abs. HCAL Iso"),
    plotquantity = cms.untracked.string(
        selectors.muons.hcalIso.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

trkNormChi2 = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(20),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_TrkNormChi2"),
    description = cms.untracked.string("${nicename} Norm. #chi^{2}"),
    plotquantity = cms.untracked.string(
        selectors.muons.trkNormChi2.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

pixelHits = cms.PSet(
    min = cms.untracked.double(-1.5),
    max = cms.untracked.double(6.5),
    nbins = cms.untracked.int32(8),
    name = cms.untracked.string("${name}_NPixHits"),
    description = cms.untracked.string("${nicename} Num. Pixel Hits"),
    plotquantity = cms.untracked.string(
        selectors.muons.pixelHits.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

innerTrackPixHits = cms.PSet(
    min = cms.untracked.double(-1.5),
    max = cms.untracked.double(6.5),
    nbins = cms.untracked.int32(8),
    name = cms.untracked.string("${name}_InnerNPixHits"),
    description = cms.untracked.string("${nicename} Inner Track Pixel Hits"),
    plotquantity = cms.untracked.string(
        selectors.muons.innerTrk.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

d0 = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(2),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_D0"),
    description = cms.untracked.string("${nicename} 3D IP"),
    plotquantity = cms.untracked.string(
        selectors.muons.d0.plottable.value()),
    lazyParsing = cms.untracked.bool(True),
)

jetPt = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_JetPt"),
    description = cms.untracked.string("${nicename} JetPt"),
    plotquantity = cms.untracked.string("userFloat('jetPt')"),
    lazyParsing = cms.untracked.bool(True),
)

btag = cms.PSet(
    min = cms.untracked.double(-10),
    max = cms.untracked.double(10),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_MuBtag"),
    description = cms.untracked.string("${nicename} muon seed jet b-tag"),
    plotquantity = cms.untracked.string(
        '? ${getter}userCand("patJet").isNonnull ? '
        '${getter}userCand("patJet").bDiscriminator("") : -5'),
    lazyParsing = cms.untracked.bool(True),
)

btagmuon = cms.PSet(
    min = cms.untracked.double(-10),
    max = cms.untracked.double(10),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_MuBtagSoftMuon"),
    description = cms.untracked.string("${nicename} muon seed jet b-tag"),
    plotquantity = cms.untracked.string(
        '? ${getter}userCand("patJet").isNonnull ? '
        '${getter}userCand("patJet").bDiscriminator("softMuonByIP3dBJetTagsAOD") : -5'),
    lazyParsing = cms.untracked.bool(True),
)

# Define all the trigger matching quantities
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

all = [wwid, reliso, relSubDetIso, ecalIso, hcalIso,
       jetPt, btag, btagmuon,
       pixelHits, innerTrackPixHits, trkNormChi2, d0,
       hltSingleMu13L3Filtered13, hltDiMuonL3p5PreFiltered8,
       hltDiMuonL3PreFiltered7, hltSingleMu30L3Filtered30,
       hltSingleMuIsoL3IsoFiltered24,
       hltL1Mu3EG5L3Filtered17, hltL1Mu3EG5L3Filtered8 ]

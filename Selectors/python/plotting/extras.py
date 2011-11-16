import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.selectors.extras as extras

nelectrons = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(10.5),
    nbins = cms.untracked.int32(11),
    name = cms.untracked.string("${name}_Nelectrons"),
    description = cms.untracked.string("${nicename} N_{e}"),
    plotquantity = cms.untracked.string(extras.e_veto.plottable.value()),
)

nmuons = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(10.5),
    nbins = cms.untracked.int32(11),
    name = cms.untracked.string("${name}_Nmuons"),
    description = cms.untracked.string("${nicename} N_{#muon}"),
    plotquantity = cms.untracked.string(extras.mu_veto.plottable.value()),
)

nglbmuons = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(10.5),
    nbins = cms.untracked.int32(11),
    name = cms.untracked.string("${name}_NGlbmuons"),
    description = cms.untracked.string("${nicename} N_{Global #muon}"),
    plotquantity = cms.untracked.string(extras.glbmu_veto.plottable.value()),
)

njets = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(10.5),
    nbins = cms.untracked.int32(11),
    name = cms.untracked.string("${name}_Njets"),
    description = cms.untracked.string("${nicename} N_{jets}"),
    plotquantity = cms.untracked.string(extras.jet_veto.plottable.value()),
)

njets = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(10.5),
    nbins = cms.untracked.int32(11),
    name = cms.untracked.string("${name}_Njets"),
    description = cms.untracked.string("${nicename} N_{jets}"),
    plotquantity = cms.untracked.string(extras.jet_veto.plottable.value()),
)

nbjets = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(10.5),
    nbins = cms.untracked.int32(11),
    name = cms.untracked.string("${name}_Nbjets"),
    description = cms.untracked.string("${nicename} N_{b-jets}"),
    plotquantity = cms.untracked.string(extras.bjet_veto.plottable.value()),
)

ntaus = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(10.5),
    nbins = cms.untracked.int32(11),
    name = cms.untracked.string("${name}_NIsoTaus"),
    description = cms.untracked.string("${nicename} Num. Iso Taus"),
    plotquantity = cms.untracked.string(extras.tau_veto.plottable.value()),
)

nvtx = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(20.5),
    nbins = cms.untracked.int32(21),
    name = cms.untracked.string("${name}_NVtx"),
    description = cms.untracked.string("${nicename} Num. Vtx"),
    plotquantity = cms.untracked.string("evt.recoVertices.size()"),
)

rho = cms.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(20),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_Rho"),
    description = cms.untracked.string("${nicename} #rho"),
    plotquantity = cms.untracked.string("evt.rho()"),
)

# Number of bjets passing hps loose
bjet_tauid = 'userCand(\'patJet\').pt > ${pt_threshold} &' \
        'abs(userCand(\'patJet\').eta) < ${eta_threshold} & ' \
        'userCand(\'patJet\').bDiscriminator(\'\') > ${btag_threshold} & ' \
        'tauID(\'byLooseCombinedIsolationDeltaBetaCorr\')'

plottable = cms.string('extras("extTaus", "%s").size()' % bjet_tauid)

nbjetsHPSLoose = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(10.5),
    nbins = cms.untracked.int32(11),
    name = cms.untracked.string("${name}_NbjetsHPSLoose"),
    description = cms.untracked.string("${nicename} N_{b-jets} passing HPS loose"),
    plotquantity = cms.untracked.string(plottable.value()),
)

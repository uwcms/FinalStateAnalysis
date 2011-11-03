import FWCore.ParameterSet.Config as cms
import string
import FinalStateAnalysis.Selectors.selectors.electrons as electrons
import FinalStateAnalysis.Selectors.selectors.muons as muons

################################################################################
### Define multi-electron veto #################################################
################################################################################

e_id_for_veto = electrons.id.cut.value()
e_iso_for_veto = electrons.reliso.cut.value()
e_sel_for_veto = "pt > ${pt_threshold} & abs(eta) < ${eta_threshold} & (%s) & (%s)" % (e_id_for_veto, e_iso_for_veto)
# Escape the quote characters correctly
e_sel_for_veto = e_sel_for_veto.replace("'", '\'')

e_veto = cms.PSet(
    name = cms.string("${name}_ElectronVeto"),
    description = cms.string("$nicename no extra iso. electrons"),
    cut = cms.string('extras("extElecs", "%s").size() == 0' % e_sel_for_veto),
    plottable = cms.string('extras("extElecs", "%s").size()' % e_sel_for_veto),
    invert = cms.bool(False),
)

################################################################################
### Define multi-muon veto     #################################################
################################################################################

mu_id_for_veto = muons.id.cut.value()
mu_iso_for_veto = muons.reliso.cut.value()

mu_sel_for_veto = "pt > ${pt_threshold} & abs(eta) < ${eta_threshold} & (%s) & (%s)" % (mu_id_for_veto, mu_iso_for_veto)
# Escape the quote characters correctly
mu_sel_for_veto = mu_sel_for_veto.replace("'", '\'')

mu_veto = cms.PSet(
    name = cms.string("${name}_MuonVeto"),
    description = cms.string("$nicename no extra iso. muons"),
    cut = cms.string('extras("extMuons", "%s").size() == 0' % mu_sel_for_veto),
    plottable = cms.string('extras("extMuons", "%s").size()' % mu_sel_for_veto),
    invert = cms.bool(False),
)

glbmu_sel_for_veto = "pt > ${pt_threshold} & abs(eta) < ${eta_threshold}"
glbmu_veto = cms.PSet(
    name = cms.string("${name}_GlbMuonVeto"),
    description = cms.string("$nicename no extra global muons"),
    cut = cms.string('extras("extMuons", "%s").size() == 0' % glbmu_sel_for_veto),
    plottable = cms.string('extras("extMuons", "%s").size()' % glbmu_sel_for_veto),
    invert = cms.bool(False),
)

tau_sel_for_veto = (
    'pt > ${pt_threshold} & abs(eta) < ${eta_threshold} &'
    ' tauID(\'decayModeFinding\') & '
    'tauID(\'byLooseCombinedIsolationDeltaBetaCorr\')')

tau_veto = cms.PSet(
    name = cms.string("${name}_TauVeto"),
    description = cms.string("$nicename no extra iso. taus"),
    cut = cms.string('extras("extTaus", "%s").size() == 0' % tau_sel_for_veto),
    plottable = cms.string('extras("extTaus", "%s").size()' % tau_sel_for_veto),
    invert = cms.bool(False),
)

jet_id_for_veto = 'userCand(\'patJet\').pt > ${pt_threshold} & abs(userCand(\'patJet\').eta) < ${eta_threshold}'
jet_veto = cms.PSet(
    name = cms.string("${name}_JetVeto"),
    description = cms.string("$nicename no extra jets"),
    cut = cms.string('extras("extTaus", "%s").size() == 0' % jet_id_for_veto),
    plottable = cms.string('extras("extTaus", "%s").size()' % jet_id_for_veto),
    invert = cms.bool(False),
)

bjet_id_for_veto = 'userCand(\'patJet\').pt > ${pt_threshold} & abs(userCand(\'patJet\').eta) < ${eta_threshold} & userCand(\'patJet\').bDiscriminator(\'\') > ${btag_threshold}'
bjet_veto = cms.PSet(
    name = cms.string("${name}_BJetVeto"),
    description = cms.string("$nicename no extra b-jets"),
    cut = cms.string('extras("extTaus", "%s").size() == 0' % bjet_id_for_veto),
    plottable = cms.string('extras("extTaus", "%s").size()' % bjet_id_for_veto),
    invert = cms.bool(False),
)

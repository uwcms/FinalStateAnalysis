'''

Add the general set of plots in the ntuple.

Returns (histos, ntuple), where histos is a cms.PSet() for a HistoFolder
and ntuple is a PSet() of ntuple commands.

Inputs are a list of dicts which define how each leg works.

Options:
--------

* puWeight = [ list of pu weights to add ]
* triggers = [ list of triggers to add ]


'''

import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.plotting.plotting as plotting
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate

def makePlots(*legs, **kwargs):
    histos = cms.PSet(histos=cms.VPSet())
    ntuple = cms.PSet()
    def add_ntuple(name, function):
        setattr(ntuple, name, cms.string(function))

    for leg in legs:
        # Make a folder for this leg
        leg_folder = cms.PSet()
        setattr(histos, leg['name'], leg_folder)
        leg_folder.histos = cms.VPSet()
        for plot in plotting.candidate.all:
            plot_cfg = PSetTemplate(plot).replace(**leg)
            leg_folder.histos.append(plot_cfg)
            # Add the plot to the ntuple
            add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())

        # Check if we want to add object type specific plots
        specific = None

        if 'Mu' in leg['name']:
            specific = plotting.muons.all
        if 'Tau' in leg['name']:
            specific = plotting.taus.all
        if 'Elec' in leg['name']:
            specific = plotting.electrons.all

        for plot in specific:
            plot_cfg = PSetTemplate(plot).replace(**leg)
            leg_folder.histos.append(plot_cfg)
            add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())

    # Make a MET folder
    met_folder = cms.PSet(histos=cms.VPSet())
    setattr(histos, "MET", met_folder)
    met_cfg = { 'name' : 'MET', 'getter' : 'evt().met().', 'nicename' : 'MET'}
    for plot in plotting.candidate.all:
        plot_cfg = PSetTemplate(plot).replace(**met_cfg)
        met_folder.histos.append(plot_cfg)
        add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())

    # Make a folder for the final state
    histos.finalState = cms.PSet(histos = cms.VPSet())
    for plot in plotting.candidate.all:
        plot_cfg = PSetTemplate(plot).replace(
            name = 'finalStateVisP4',
            nicename = 'Visible final state',
            getter = ''
        )
        histos.finalState.histos.append(plot_cfg)
        add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())

    add_ntuple('vtxChi2', 'userFloat("vtxChi2")')
    add_ntuple('vtxNDOF', 'userFloat("vtxNDOF")')

    for index, leg in enumerate(legs):
        mtMET_cfg = PSetTemplate(plotting.topology.mtMET).replace(
                name = leg['name'], nicename = leg['nicename'], index = index
        )
        histos.finalState.histos.append(mtMET_cfg)
        add_ntuple(mtMET_cfg.name.value(), mtMET_cfg.plotquantity.value())

    ht_cfg = PSetTemplate(plotting.topology.ht).replace(
        name = 'VisFinalState', nicename = 'Final State',
        getter = '',
    )
    histos.finalState.histos.append(ht_cfg)
    add_ntuple(ht_cfg.name.value(), ht_cfg.plotquantity.value())

    # Add pileup re-weights
    puWeights = kwargs.get('puWeights', [])
    for weight in puWeights:
        add_ntuple('puWeight_%s' % weight, 'evt.weight("%s")' % weight)

    # Add triggers
    trig_cfgs = kwargs.get('triggers', [])
    for trig_cfg in trig_cfgs:
        name, nicename, path = trig_cfg
        # Add HLT pass result
        hlt_cfg = PSetTemplate(plotting.trigger.hlt).replace(
            name = name, nicename = nicename,
            hlt_path = path)
        add_ntuple(hlt_cfg.name.value(), hlt_cfg.plotquantity.value())
        # Add HLT group result
        hlt_cfg = PSetTemplate(plotting.trigger.hltGroup).replace(
            name = name, nicename = nicename,
            hlt_path = path)
        add_ntuple(hlt_cfg.name.value(), hlt_cfg.plotquantity.value())
        # Add HLT prescale result
        hlt_cfg = PSetTemplate(plotting.trigger.hltPrescale).replace(
            name = name, nicename = nicename,
            hlt_path = path)
        add_ntuple(hlt_cfg.name.value(), hlt_cfg.plotquantity.value())

    histos.extras = cms.PSet(histos = cms.VPSet())
    muon_veto_cfg = PSetTemplate(plotting.extras.nmuons).replace(
        name = 'NIsoMuonsPt5', nicename = 'p_{T} > 5, Iso < 0.3, WWID',
        threshold = '0.3',
        pt_threshold = '5', eta_threshold = '2.5',
        getter = '', muID = 'WWID')
    histos.extras.histos.append(muon_veto_cfg)
    add_ntuple(muon_veto_cfg.name.value(), muon_veto_cfg.plotquantity.value())

    muon_veto_cfg = PSetTemplate(plotting.extras.nglbmuons).replace(
        name = 'NGlobalMuonsPt5', nicename = 'p_{T} > 5',
        pt_threshold = '5', eta_threshold = '2.5', getter = '',)
    histos.extras.histos.append(muon_veto_cfg)
    add_ntuple(muon_veto_cfg.name.value(), muon_veto_cfg.plotquantity.value())

    e_veto_cfg = PSetTemplate(plotting.extras.nelectrons).replace(
            name = 'NIsoElecPt10', nicename = 'p_{T} > 10, Iso < 0.3, WP95',
            threshold = '0.3',
            pt_threshold = '10', eta_threshold = '2.5',
            getter = '', eID = 'wp95')
    histos.extras.histos.append(e_veto_cfg)
    add_ntuple(e_veto_cfg.name.value(), e_veto_cfg.plotquantity.value())

    jet_veto_cfg = PSetTemplate(plotting.extras.njets).replace(
        name = 'NjetsPt20', nicename = 'p_{T} > 20',
        pt_threshold = '20', eta_threshold = '2.5',)
    histos.extras.histos.append(jet_veto_cfg)
    add_ntuple(jet_veto_cfg.name.value(), jet_veto_cfg.plotquantity.value())

    tau_veto_cfg = PSetTemplate(plotting.extras.ntaus).replace(
        name = 'NIsoTausPt20', nicename = 'p_{T} > 20',
        pt_threshold = '20', eta_threshold = '2.5',)
    histos.extras.histos.append(tau_veto_cfg)
    add_ntuple(tau_veto_cfg.name.value(), tau_veto_cfg.plotquantity.value())

    b_veto_cfg = PSetTemplate(plotting.extras.nbjets).replace(
            name = 'NBjetsPt20', nicename = 'p_{T} > 20',
            pt_threshold = '20', eta_threshold = '2.5',
            btag_threshold = '3.3' )
    histos.extras.histos.append(b_veto_cfg)
    add_ntuple(b_veto_cfg.name.value(), b_veto_cfg.plotquantity.value())

    return histos, ntuple

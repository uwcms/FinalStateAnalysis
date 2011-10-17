import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.plotting.plotting as plotting
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate

def trileptonFinalPlots(leg1, leg2, leg3):
    # Build the Histo Folder
    output = cms.PSet()
    output.histos = cms.VPSet()
    # Optional ntuple
    ntuple = cms.PSet()
    # Function to add a column to the ntuple
    def add_ntuple(name, function):
        setattr(ntuple, name, cms.string(function))

    for leg in [leg1, leg2, leg3]:
        # Make a folder for this leg
        leg_folder = cms.PSet()
        setattr(output, leg['name'], leg_folder)
        leg_folder.histos = cms.VPSet()
        for plot in plotting.candidate.all:
            plot_cfg = PSetTemplate(plot).replace(**leg)
            leg_folder.histos.append(plot_cfg)
            add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())

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
    setattr(output, "MET", met_folder)
    met_cfg = { 'name' : 'MET', 'getter' : 'evt().met().', 'nicename' : 'MET'}
    for plot in plotting.candidate.all:
        plot_cfg = PSetTemplate(plot).replace(**met_cfg)
        met_folder.histos.append(plot_cfg)
        add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())


    # Make a folder for the final state
    output.finalState = cms.PSet(histos = cms.VPSet())
    for plot in plotting.candidate.all:
        output.finalState.histos.append(
            PSetTemplate(plot).replace(
                name = 'finalStateVisP4',
                nicename = 'Visible final state',
                getter = ''
            )
        )

    # Add the evt#, run# and idx
    # TODO change paths fix this on next pat tuple iteration
    add_ntuple('evt', 'userInt("evt")')
    add_ntuple('run', 'userInt("run")')

    add_ntuple('vtxChi2', 'userFloat("vtxChi2")')
    add_ntuple('vtxNDOF', 'userFloat("vtxNDOF")')

    # Make HT hisotgram
    output.finalState.histos.append(
        PSetTemplate(plotting.topology.ht).replace(
            name = 'finalState', nicename = 'Final state',
        )
    )

    output.finalState.histos.append(
        PSetTemplate(plotting.topology.phiTopology).replace(
            name = 'finalState', nicename = 'Final state',
        )
    )

    output.finalState.histos.append(
        PSetTemplate(plotting.topology.lowestTwoAreOS).replace(
            name = 'finalState', nicename = 'Final state',
        )
    )

    for index, legname in enumerate(['Leg1', 'Leg2', 'Leg3']):
        mtMET_cfg = PSetTemplate(plotting.topology.mtMET).replace(
                name = legname, nicename = legname, index = index
        )
        output.finalState.histos.append(mtMET_cfg)
        add_ntuple(mtMET_cfg.name.value(), mtMET_cfg.plotquantity.value())

    ht_cfg = PSetTemplate(plotting.topology.ht).replace(
        name = 'FinalState', nicename = 'Final State',
    )
    output.finalState.histos.append(ht_cfg)
    add_ntuple(ht_cfg.name.value(), ht_cfg.plotquantity.value())

    for pair_plot in [plotting.topology.ss, plotting.topology.pairMass,
                      plotting.topology.pairDPhi]:
        leg1leg2_cfg = PSetTemplate(pair_plot).replace(
            name = 'Leg1Leg2', nicename = 'Leg1 - Leg2',
            index1 = 0, index2 = 1)
        output.finalState.histos.append(leg1leg2_cfg)
        add_ntuple(leg1leg2_cfg.name.value(), leg1leg2_cfg.plotquantity.value())

        leg1leg3_cfg = PSetTemplate(pair_plot).replace(
            name = 'Leg1Leg3', nicename = 'Leg1 - Leg3',
            index1 = 0, index2 = 2)
        output.finalState.histos.append(leg1leg3_cfg)
        add_ntuple(leg1leg3_cfg.name.value(), leg1leg3_cfg.plotquantity.value())

        leg2leg3_cfg = PSetTemplate(pair_plot).replace(
            name = 'Leg2Leg3', nicename = 'Leg2 - Leg3',
            index1 = 1, index2 = 2)
        output.finalState.histos.append(leg2leg3_cfg)
        add_ntuple(leg2leg3_cfg.name.value(), leg2leg3_cfg.plotquantity.value())


    output.extras = cms.PSet(histos = cms.VPSet())
    muon_veto_cfg = PSetTemplate(plotting.extras.nmuons).replace(
        name = 'NIsoMuonsPt5', nicename = 'p_{T} > 5, Iso < 0.3, WWID',
        threshold = '0.3',
        pt_threshold = '10', eta_threshold = '2.5',
        getter = '', muID = 'WWID')
    output.extras.histos.append(muon_veto_cfg)
    add_ntuple(muon_veto_cfg.name.value(), muon_veto_cfg.plotquantity.value())

    e_veto_cfg = PSetTemplate(plotting.extras.nelectrons).replace(
            name = 'NIsoElecPt5', nicename = 'p_{T} > 10, Iso < 0.3, WWID',
            threshold = '0.3',
            pt_threshold = '10', eta_threshold = '2.5',
            getter = '', eID = 'WWID')
    output.extras.histos.append(e_veto_cfg)
    add_ntuple(e_veto_cfg.name.value(), e_veto_cfg.plotquantity.value())

    jet_veto_cfg = PSetTemplate(plotting.extras.njets).replace(
        name = 'NjetsPt20', nicename = 'p_{T} > 20',
        pt_threshold = '20', eta_threshold = '2.5',)
    output.extras.histos.append(jet_veto_cfg)
    add_ntuple(jet_veto_cfg.name.value(), jet_veto_cfg.plotquantity.value())

    b_veto_cfg = PSetTemplate(plotting.extras.nbjets).replace(
            name = 'NBjetsPt20', nicename = 'p_{T} > 20',
            pt_threshold = '20', eta_threshold = '2.5',
            btag_threshold = '3.3' )
    output.extras.histos.append(b_veto_cfg)
    add_ntuple(b_veto_cfg.name.value(), b_veto_cfg.plotquantity.value())

    btau_veto_cfg = PSetTemplate(plotting.extras.nbjets).replace(
            name = 'NBjetsPt20HPSLoose', nicename = 'p_{T} > 20',
            pt_threshold = '20', eta_threshold = '2.5',
            btag_threshold = '3.3' )
    output.extras.histos.append(btau_veto_cfg)
    add_ntuple(btau_veto_cfg.name.value(), btau_veto_cfg.plotquantity.value())

    # Add in the lumi weight
    add_ntuple("puWeight", "evt().weight('puAvg')")

    # Add our trilepton HLT paths
    emu_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
        name = "Mu8Ele17", nicename = "Mu(8) Ele(17)",
        hlt_path = r"HLT_Mu8_Ele17_CaloId(T|L)(_CaloIsoVL|)_v\\d+")
    add_ntuple(emu_trig_cfg.name.value(), emu_trig_cfg.plotquantity.value())

    mue_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
        name = "Mu17Ele8", nicename = "Mu(17) Ele(8)",
        hlt_path = r"HLT_Mu17_Ele8_CaloId(T|L)(_CaloIsoVL|)_v\\d+")
    add_ntuple(mue_trig_cfg.name.value(), mue_trig_cfg.plotquantity.value())

    ee_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
        name = "E17E8", nicename = "Ele(17) E(8)",
        hlt_path = r'HLT_Ele17_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_Ele8_CaloIdT_TrkIdVL_CaloIsoVL_TrkIsoVL_v\\d+')
    add_ntuple(ee_trig_cfg.name.value(), ee_trig_cfg.plotquantity.value())

    mm_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
        name = "Mu13Mu8", nicename = "Mu(13) Mu(8)",
        hlt_path = r'HLT_Mu13_Mu8_v\\d+')
    add_ntuple(mm_trig_cfg.name.value(), mm_trig_cfg.plotquantity.value())

    mm77_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
        name = "DoubleMu7", nicename = "Double Muon 7",
        hlt_path = r'HLT_DoubleMu7_v\\d+')
    add_ntuple(mm77_trig_cfg.name.value(), mm77_trig_cfg.plotquantity.value())

    return output,ntuple

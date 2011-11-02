import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.plotting.plotting as plotting
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate

config = cms.PSet(
    subcand = cms.string('subcand("@,@", "extTaus", "%s")' % (
        'userCand(\'patJet\').pt > 40 & abs(userCand(\'patJet\').eta) < 2.5'
        ' & userCand(\'patJet\').userFloat(\'idLoose\') > 0.5')
    )
)

def dileptonFinalPlots(leg1, leg2):
    # Build the Histo Folder
    output = cms.PSet()
    output.histos = cms.VPSet()
    # Optional ntuple
    ntuple = cms.PSet()
    # Function to add a column to the ntuple
    def add_ntuple(name, function):
        setattr(ntuple, name, cms.string(function))

    for leg in [leg1, leg2]:
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
    #add_ntuple('evt', 'evt().id().event')
    #add_ntuple('run', 'evt().id().run')

    add_ntuple('vtxChi2', 'userFloat("vtxChi2")')
    add_ntuple('vtxNDOF', 'userFloat("vtxNDOF")')

    output.finalState.histos.append(
        PSetTemplate(plotting.topology.phiTopology).replace(
            name = 'finalState', nicename = 'Final state',
        )
    )

    #Make HT hisotgram
    add_ntuple('ht', '%s.get.ht' % config.subcand.value())

    output.finalState.histos.append(
        PSetTemplate(plotting.topology.lowestTwoAreOS).replace(
            name = 'finalState', nicename = 'Final state',
        )
    )

    for index, legname in enumerate(['Leg1', 'Leg2']):
        mtMET_cfg = PSetTemplate(plotting.topology.mtMET).replace(
                name = legname, nicename = legname, index = index
        )
        output.finalState.histos.append(mtMET_cfg)
        add_ntuple(mtMET_cfg.name.value(), mtMET_cfg.plotquantity.value())

    ht_cfg = PSetTemplate(plotting.topology.ht).replace(
        name = 'VisFinalState', nicename = 'Final State',
        getter = '',
    )
    output.finalState.histos.append(ht_cfg)
    add_ntuple(ht_cfg.name.value(), ht_cfg.plotquantity.value())

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

    jet_veto_cfg = PSetTemplate(plotting.extras.njets).replace(
        name = 'NjetsPt40', nicename = 'p_{T} > 40',
        pt_threshold = '40', eta_threshold = '2.5',)
    output.extras.histos.append(jet_veto_cfg)
    add_ntuple(jet_veto_cfg.name.value(), jet_veto_cfg.plotquantity.value())

    b_veto_cfg = PSetTemplate(plotting.extras.nbjets).replace(
            name = 'NBjetsPt20', nicename = 'p_{T} > 20',
            pt_threshold = '20', eta_threshold = '2.5',
            btag_threshold = '3.3' )
    output.extras.histos.append(b_veto_cfg)
    add_ntuple(b_veto_cfg.name.value(), b_veto_cfg.plotquantity.value())

    btau_veto_cfg = PSetTemplate(plotting.extras.nbjetsHPSLoose).replace(
            name = 'NBjetsPt20HPSLoose', nicename = 'p_{T} > 20',
            pt_threshold = '20', eta_threshold = '2.5',
            btag_threshold = '3.3' )
    output.extras.histos.append(btau_veto_cfg)
    add_ntuple(btau_veto_cfg.name.value(), btau_veto_cfg.plotquantity.value())

    # Add in the lumi weight
    add_ntuple("puWeight", "evt().weight('puAvg')")

    # Add some control paths
    im24_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
        name = "IsoMu24", nicename = "Iso Mu 24",
        hlt_path = r'HLT_IsoMu24_v\\d+')
    add_ntuple(im24_trig_cfg.name.value(), im24_trig_cfg.plotquantity.value())

    m30_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
        name = "Mu30", nicename = "Mu 30",
        hlt_path = r'HLT_Mu30_v\\d+')
    add_ntuple(m30_trig_cfg.name.value(), m30_trig_cfg.plotquantity.value())

    mht_trgs = PSetTemplate(plotting.trigger.hlt).replace(
        name = "Mu5_MHT", nicename = "Mu5 MHT Triggers",
        hlt_path = r'HLT_HT200_Mu5_PFMHT35_v\\d+,HLT_HT250_Mu5_PFMHT35_v\\d+,HLT_HT300_Mu5_PFMHT40_v\\d+,HLT_HT350_Mu5_PFMHT45_v\\d+')
    add_ntuple(mht_trgs.name.value(), mht_trgs.plotquantity.value())

    mht_trgs = PSetTemplate(plotting.trigger.hltGroup).replace(
        name = "Mu5_MHT", nicename = "Mu5 MHT Triggers",
        hlt_path = r'HLT_HT200_Mu5_PFMHT35_v\\d+,HLT_HT250_Mu5_PFMHT35_v\\d+,HLT_HT300_Mu5_PFMHT40_v\\d+,HLT_HT350_Mu5_PFMHT45_v\\d+')
    add_ntuple(mht_trgs.name.value(), mht_trgs.plotquantity.value())

    mht_trgs = PSetTemplate(plotting.trigger.hltPrescale).replace(
        name = "Mu5_MHT", nicename = "Mu5 MHT Triggers",
        hlt_path = r'HLT_HT200_Mu5_PFMHT35_v\\d+,HLT_HT250_Mu5_PFMHT35_v\\d+,HLT_HT300_Mu5_PFMHT40_v\\d+,HLT_HT350_Mu5_PFMHT45_v\\d+')
    add_ntuple(mht_trgs.name.value(), mht_trgs.plotquantity.value())

    return output,ntuple

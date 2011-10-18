import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate
from FinalStateAnalysis.Selectors.selectors import selectors
from FinalStateAnalysis.Selectors.plotting import plotting

options = TauVarParsing.TauVarParsing(
    skipEvents=0, # For debugging
)

options.outputFile="muon_tp.root"
options.parseArguments()

process = cms.Process("MuonTP")

# Input in FWLITE mode
process.fwliteInput = cms.PSet(fileNames = cms.vstring(options.inputFiles))

process.fwliteOutput = cms.PSet(fileName = cms.string(options.outputFile))

process.steering = cms.PSet(
    analyzers = cms.vstring(
        'mm'
    ),
    reportAfter = cms.uint32(1000),
    ignored_cuts = cms.vstring()
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

# Common among all analyzers
process.common = cms.PSet(
    weights = cms.VInputTag(
        cms.InputTag("lumiWeights", "3bx")
    ),
    skimCounter = cms.InputTag("eventCount", "", "TUPLE"),
)

process.steering.ignored_cuts = cms.vstring()

# Define the configuration for each leg.
leg1 = {
    'name' : 'Muon1', 'getter' :'daughter(0).', 'nicename' : 'Muon (1)',
    'index' : 0,
}
leg2 = {
    'name' : 'Muon2', 'getter' :'daughter(1).', 'nicename' : 'Muon (2)',
    'index' : 1,
}
# Define the selections
selections = cms.VPSet(
    ###########################################################################
    # Uniqueness cut
    ###########################################################################
    # Trigger on single muon events with HLT_Mu30
    PSetTemplate(selectors.trigger.hlt).replace(
        name = 'HLT_Mu30', nicename = 'HLT Muon 30 result',
        hlt_path = r'HLT_Mu30_v\\d+',
    ),

    # Initially, there is double counting in the FinalStates. i.e. for muons A
    # and B, there is an AB final state and a BA final state.  Here, we select
    # only those where A.phi < B.phi, which insures we select a random tag
    # object.
    PSetTemplate(selectors.topology.descending_phi).replace(
        name = 'TagMuonID', nicename = 'Muon 1 is TagMuon',
        getter1 = leg1['getter'], getter2 = leg2['getter']
    ),

    # Offline cuts on tag muon
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.1', **leg1),
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '31', **leg1),
    # Require WWID on the tag muon
    PSetTemplate(selectors.muons.id).replace(
        muID = 'WWID', **leg1),

    # Muon 0 is now defined as our tag muon.  Require it's matched to the firing
    # trigger.
    PSetTemplate(selectors.muons.hltSingleMu30L3Filtered30).replace(
        name = 'TagMuon', nicename = 'Tag muon',
        index = 0
    ),

    # Some stupid cuts on the probe muon
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg2),
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '5', **leg2),
)

# Define what we are going to plot
plots = cms.PSet(
    histos = cms.VPSet(),
    ntuple = cms.PSet(
    )
)

def add_ntuple(name, function):
    setattr(plots.ntuple, name, cms.string(function))

for leg in [leg1, leg2]:
    for plot in plotting.muons.all:
        plot_cfg = PSetTemplate(plot).replace(**leg)
        add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())
    for plot in plotting.candidate.all:
        plot_cfg = PSetTemplate(plot).replace(**leg)
        add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())
    plot_cfg = PSetTemplate(plotting.muons.id).replace(
        muID = 'WWID', **leg)
    add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())

for plot in plotting.candidate.all:
    plot_cfg = PSetTemplate(plot).replace(
            name = 'finalStateVisP4',
            nicename = 'Visible final state',
            getter = ''
        )
    add_ntuple(plot_cfg.name.value(), plot_cfg.plotquantity.value())

add_ntuple('evt', 'userInt("evt")')
add_ntuple('run', 'userInt("run")')

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

im24_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
    name = "IsoMu24", nicename = "Iso Mu 24",
    hlt_path = r'HLT_IsoMu24_v\\d+')
add_ntuple(im24_trig_cfg.name.value(), im24_trig_cfg.plotquantity.value())

m30_trig_cfg = PSetTemplate(plotting.trigger.hlt).replace(
    name = "Mu30", nicename = "Mu 30",
    hlt_path = r'HLT_Mu30_v\\d+')
add_ntuple(m30_trig_cfg.name.value(), m30_trig_cfg.plotquantity.value())


add_ntuple("puWeight", "evt().weight('puAvg')")

# Analyze MuMu states
process.mm = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuMu'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(1),
            plot = plots
        ),
        selections = selections
    )
)


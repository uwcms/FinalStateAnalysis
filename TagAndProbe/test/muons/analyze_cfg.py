'''

Construction of Ntuples for quantities measured with SingleMu dataset


'''

import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate
from FinalStateAnalysis.Selectors.selectors import selectors
from FinalStateAnalysis.Selectors.plotting import plotting
from FinalStateAnalysis.Selectors.plotBuilder import makePlots

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
        'mm',
        'em'
    ),
    reportAfter = cms.uint32(1000),
    ignored_cuts = cms.vstring()
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

# Common among all analyzers
process.common = cms.PSet(
    weights = cms.vstring(
        'weight("3bx_S42011A")'
    ),
    evtSrc = cms.InputTag("patFinalStateEventProducer"),
    skimCounter = cms.InputTag("eventCount", "", "TUPLE"),
)

process.steering.ignored_cuts = cms.vstring()

# Define the configuration for each leg.
mu_leg1 = {
    'name' : 'Muon1', 'getter' :'daughter(0).', 'nicename' : 'Muon (1)',
    'index' : 0,
}
mu_leg2 = {
    'name' : 'Muon2', 'getter' :'daughter(1).', 'nicename' : 'Muon (2)',
    'index' : 1,
}

e_leg1 = {
    'name' : 'Electron', 'getter' :'daughter(0).', 'nicename' : 'Electron',
    'index' : 0,
}

# Define the selections
mm_selections = cms.VPSet(
    # Take the best unprescaled SingleMu trigger
    #PSetTemplate(selectors.trigger.hlt).replace(
        #name = 'HLTSingleMu', nicename = 'Single Mu (no iso)',
        #hlt_path = r'HLT_Mu15_v\\d+, HLT_Mu24_v\\d+, HLT_Mu30_v\\d+',
    #),
    ###########################################################################
    # Uniqueness cut
    ###########################################################################

    # Initially, there is double counting in the FinalStates. i.e. for muons A
    # and B, there is an AB final state and a BA final state.  Here, we select
    # only those where A.phi < B.phi, which insures we select a random tag
    # object.
    PSetTemplate(selectors.topology.descending_phi).replace(
        name = 'TagMuonID', nicename = 'Muon 1 is TagMuon',
        getter1 = mu_leg1['getter'], getter2 = mu_leg2['getter']
    ),

    # Offline cuts on tag muon
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.1', **mu_leg1),
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '15', **mu_leg1),
    # Require WWID on the tag muon
    PSetTemplate(selectors.muons.id).replace(
        muID = 'WWID', **mu_leg1),
)

puWeights = [
    '3bx_S42011A',
    '3bx_S42011AB178078',
    '3bx_S42011B178078',
]

mu_triggers = [
    ('Mu15', 'Mu 15', r'HLT_Mu15_v\\d+'),
    ('Mu24', 'Mu 24', r'HLT_Mu24_v\\d+'),
    ('Mu30', 'Mu 30', r'HLT_Mu30_v\\d+'),
    ('SingleMus', 'SingleMu', r'HLT_Mu15_v\\d+, HLT_Mu24_v\\d+, HLT_Mu30_v\\d+'),

    ('IsoMu17', 'Iso Mu 17', r'HLT_IsoMu17_v\\d+'),
    ('IsoMu20', 'Iso Mu 20', r'HLT_IsoMu20_v\\d+'),
    ('IsoMu24', 'Iso Mu 24', r'HLT_IsoMu24_v\\d+'),
    ('IsoMus', 'Iso Mu Any', r'HLT_IsoMu17_v\\d+, HLT_IsoMu20_v\\d+, HLT_IsoMu24_v\\d+'),

    ('DoubleMu7', 'Double Mu 17', r'HLT_DoubleMu7_v\\d+'),
    ('Mu13Mu8', 'Mu (13) Mu (8)', r'HLT_Mu13_Mu8_v\\d+'),
    ('DoubleMus', 'DoubleMuTriggers', r'HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+'),
]

mm_plots, mm_ntuple = makePlots(mu_leg1, mu_leg2,
                                triggers = mu_triggers, puWeights=puWeights)

# Analyze MuMu states
process.mm = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuMu'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(1),
            plot = cms.PSet(histos = cms.VPSet(), ntuple = mm_ntuple)
        ),
        selections = mm_selections
    )
)

# Define selections for emu selections
em_selections = cms.VPSet(
    # Take the best unprescaled SingleMu trigger
    #PSetTemplate(selectors.trigger.hlt).replace(
        #name = 'HLTSingleMu', nicename = 'Single Mu (no iso)',
        #hlt_path = r'HLT_Mu15_v\\d+, HLT_Mu24_v\\d+, HLT_Mu30_v\\d+',
    #),
    # We don't need to worry about double counting here
    # Offline cuts on tag muon
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.1', **mu_leg2),
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '15', **mu_leg2),
    # Require WWID on the tag muon
    PSetTemplate(selectors.muons.id).replace(
        muID = 'WWID', **mu_leg2),
)

emu_triggers = [
    ('Mu8Ele17CaloIDL', 'Mu (8) Ele (17)', r"HLT_Mu8_Ele17_CaloIdL_v\\d+"),
    ('Mu8Ele17CaloIDT', 'Mu (8) Ele (17)', r"HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v\\d+"),
    ('Mu8Ele17All', 'Mu (8) Ele (17)', r"HLT_Mu8_Ele17_CaloIdL_v\\d+,HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v\\d+"),

    ('Mu17Ele8CaloIDL', 'Mu (17) Ele (8)', r"HLT_Mu17_Ele8_CaloIdL_v\\d+"),
    ('Mu17Ele8CaloIDT', 'Mu (17) Ele (8)', r"HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+"),
    ('Mu17Ele8All', 'Mu (17) Ele (8)', r"HLT_Mu17_Ele8_CaloIdL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+"),
]

em_plots, em_ntuple = makePlots(mu_leg2, e_leg1,
                                triggers = emu_triggers + mu_triggers,
                                puWeights = puWeights)

# Analyze MuMu states
process.em = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateElecMu'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(1),
            plot = cms.PSet(histos = cms.VPSet(), ntuple = em_ntuple)
        ),
        selections = em_selections
    )
)

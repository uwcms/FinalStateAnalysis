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
    puScenario='S4',
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
        'em',
        'mt',
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

tau_leg2 = {
    'name' : 'Tau', 'getter' :'daughter(1).', 'nicename' : 'Tau',
    'index' : 1,
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

mm_plots, mm_ntuple = makePlots(mu_leg1, mu_leg2)

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

em_plots, em_ntuple = makePlots(mu_leg2, e_leg1)

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

mt_plots, mt_ntuple = makePlots(mu_leg1, tau_leg2)

mt_selections = cms.VPSet(
    # Take the best unprescaled SingleMu trigger
    #PSetTemplate(selectors.trigger.hlt).replace(
        #name = 'HLTSingleMu', nicename = 'Single Mu (no iso)',
        #hlt_path = r'HLT_Mu15_v\\d+, HLT_Mu24_v\\d+, HLT_Mu30_v\\d+',
    #),
    # We don't need to worry about double counting here
    # Offline cuts on tag muon
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.1', **mu_leg1),
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '15', **mu_leg1),
    # Require WWID on the tag muon
    PSetTemplate(selectors.muons.id).replace(
        muID = 'WWID', **mu_leg1),
)

em_plots, em_ntuple = makePlots(mu_leg2, e_leg1)

# Analyze MuMu states
process.mt = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuTau'),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(2).pt'),
            take = cms.uint32(1),
            plot = cms.PSet(histos = cms.VPSet(), ntuple = mt_ntuple)
        ),
        selections = mt_selections
    )
)


# Build the filter selectors for skimming events.
for channel in process.steering.analyzers:
    module = getattr(process, channel)
    if options.isMC:
        scenario = options.puScenario
        print "Configuring %s ntuple for %s PU re-weighting" % (
            channel, scenario)
        module.analysis.final.plot.ntuple.pu2011A = cms.string(
            "evt.puWeight('2011A', '%s')" % scenario
        )
        module.analysis.final.plot.ntuple.pu2011B = cms.string(
            "evt.puWeight('2011B', '%s')" % scenario
        )
        module.analysis.final.plot.ntuple.pu2011AB = cms.string(
            "evt.puWeight('2011AB', '%s')" % scenario
        )
    else:
        module.analysis.final.plot.ntuple.pu2011A = cms.string("1.0")
        module.analysis.final.plot.ntuple.pu2011B = cms.string("1.0")
        module.analysis.final.plot.ntuple.pu2011AB = cms.string("1.0")

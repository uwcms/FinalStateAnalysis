'''

Generate the e-e ntuple, used for T&P studies

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import format

# Import the templates used to make the branches
import FinalStateAnalysis.Selectors.templates as templates

_name_map = {
    'electron1' : 'daughter(0)',
    'electron1_idx' : '0',
    'electron2' : 'daughter(1)',
    'electron2_idx' : '1',
}

ee = cms.EDFilter(
    "PATFinalStateAnalysisFilter",

    weights = cms.vstring(),

    # Object to build our ntuple with
    src = cms.InputTag("finalStateElecElec"),

    # Source of event level info
    evtSrc = cms.InputTag("patFinalStateEventProducer"),

    # Keep track of events killed in the skim
    skimCounter = cms.InputTag("eventCount", "", "TUPLE"),

    analysis = cms.PSet(
        # Define the basic selections we apply before making the ntuple
        selections = cms.VPSet(
            cms.PSet(
                name = cms.string('Elec1Pt'),
                cut = cms.string('{electron1}.pt > 10'),
            ),
            cms.PSet(
                name = cms.string('Elec1Eta'),
                cut = cms.string('abs({electron1}.eta) < 2.5'),
            ),
            cms.PSet(
                name = cms.string('Elec2Pt'),
                cut = cms.string('{electron2}.pt > 5'),
            ),
            cms.PSet(
                name = cms.string('Elec2Eta'),
                cut = cms.string('abs({electron2}.eta) < 2.5'),
            ),
        ),

        # Define what to do with the FSes that pass all selections
        final = cms.PSet(
            sort = cms.string('{electron2}.pt'), # sort output by TauPt
            take = cms.uint32(5),
            plot = cms.PSet(
                histos = cms.VPSet(), # Don't make any final plots
                ntuple = cms.PSet(
                    # Basic info about the final state
                    templates.topology.finalstate,
                    templates.topology.mtToMET.replace(object='electron1'),
                    templates.topology.mtToMET.replace(object='electron2'),

                    # templates.Mass/DR/Dphi/SS of pairs
                    templates.topology.pairs.replace(object1='electron1', object2='electron2'),

                    # templates.Event num/lumi/run
                    templates.event.num,
                    # templates.Rho, ntvtx, nTruePU
                    templates.event.pileup,
                    # templates.Info about the MET
                    templates.event.met,

                    # templates.Add electron1 branches
                    templates.candidates.kinematics.replace(object='electron1'),
                    templates.candidates.vertex_info.replace(object='electron1'),
                    templates.candidates.base_jet.replace(object='electron1'),
                    # templates.electron1 specific
                    templates.electrons.id.replace(object='electron1'),
                    templates.electrons.tracking.replace(object='electron1'),

                    # templates.Add electron2 branches
                    templates.candidates.kinematics.replace(object='electron2'),
                    templates.candidates.vertex_info.replace(object='electron2'),
                    templates.candidates.base_jet.replace(object='electron2'),
                    # templates.electron2 specific
                    templates.electrons.id.replace(object='electron2'),
                    templates.electrons.tracking.replace(object='electron2'),

                    # templates.Vetoes on extra objects
                    templates.cleaning.vetos,
                    #MuPt = cms.string('{muon}.pt'),
                )
            ),
        )
    )
)

format(ee, **_name_map)

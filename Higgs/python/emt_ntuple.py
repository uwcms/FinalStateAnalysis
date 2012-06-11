'''

Generate the e-mu-tau ntuple, used by the WH analysis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import format

# Import the templates used to make the branches
import FinalStateAnalysis.NtupleTools.templates as templates

_name_map = {
    'electron' : 'daughter(0)',
    'electron_idx' : '0',
    'muon' : 'daughter(1)',
    'muon_idx' : '1',
    'tau' : 'daughter(2)',
    'tau_idx' : '2',
}

emutau = cms.EDFilter(
    "PATFinalStateAnalysisFilter",

    weights = cms.vstring(),

    # Object to build our ntuple with
    src = cms.InputTag("finalStateElecMuTau"),

    # Source of event level info
    evtSrc = cms.InputTag("patFinalStateEventProducer"),

    # Keep track of events killed in the skim
    skimCounter = cms.InputTag("eventCount", "", "TUPLE"),

    analysis = cms.PSet(
        # Define the basic selections we apply before making the ntuple
        selections = cms.VPSet(
            cms.PSet(
                name = cms.string('MuPt'),
                cut = cms.string('{muon}.pt > 17'),
            ),
            cms.PSet(
                name = cms.string('MuEta'),
                cut = cms.string('abs({muon}.eta) < 2.5'),
            ),
            cms.PSet(
                name = cms.string('ElecPt'),
                cut = cms.string('{electron}.pt > 7'),
            ),
            cms.PSet(
                name = cms.string('ElecEta'),
                cut = cms.string('abs({electron}.eta) < 2.5'),
            ),
            cms.PSet(
                name = cms.string('TauPt'),
                cut = cms.string('{tau}.pt > 17'),
            ),
            cms.PSet(
                name = cms.string('TauEta'),
                cut = cms.string('abs({tau}.eta) < 2.3'),
            ),
        ),

        # Define what to do with the FSes that pass all selections
        final = cms.PSet(
            sort = cms.string('{tau}.pt'), # sort output by TauPt
            take = cms.uint32(5),
            plot = cms.PSet(
                histos = cms.VPSet(), # Don't make any final plots
                ntuple = cms.PSet(
                    # Basic info about the final state
                    templates.topology.finalstate,
                    templates.topology.mtToMET.replace(object='electron'),
                    templates.topology.mtToMET.replace(object='muon'),

                    # Triggers
                    templates.trigger.mueg,
                    templates.trigger.isomu,
                    templates.trigger.singlemu,

                    # templates.Mass/DR/Dphi/SS of pairs
                    templates.topology.pairs.replace(object1='electron', object2='tau'),
                    templates.topology.pairs.replace(object1='electron', object2='muon'),
                    templates.topology.pairs.replace(object1='muon', object2='tau'),

                    # templates.Event num/lumi/run
                    templates.event.num,
                    # templates.Rho, ntvtx, nTruePU
                    templates.event.pileup,
                    # templates.Info about the MET
                    templates.event.met,

                    # templates.Add muon branches
                    templates.candidates.kinematics.replace(object='muon'),
                    templates.candidates.vertex_info.replace(object='muon'),
                    templates.candidates.base_jet.replace(object='muon'),
                    # templates.Muon specific
                    templates.muons.id.replace(object='muon'),
                    templates.muons.tracking.replace(object='muon'),

                    # templates.Add electron branches
                    templates.candidates.kinematics.replace(object='electron'),
                    templates.candidates.vertex_info.replace(object='electron'),
                    templates.candidates.base_jet.replace(object='electron'),
                    # templates.Cleaning
                    templates.cleaning.overlaps.replace(object='electron'),
                    # templates.Electron specific
                    templates.electrons.id.replace(object='electron'),
                    templates.electrons.tracking.replace(object='electron'),

                    # templates.Add tau branches
                    templates.candidates.kinematics.replace(object='tau'),
                    templates.candidates.vertex_info.replace(object='tau'),
                    templates.candidates.base_jet.replace(object='tau'),
                    # templates.Cleaning
                    templates.cleaning.overlaps.replace(object='tau'),
                    # templates.Tau specific
                    templates.taus.info.replace(object='tau'),
                    templates.taus.id.replace(object='tau'),

                    # templates.Vetoes on extra objects
                    templates.cleaning.vetos,
                    #MuPt = cms.string('{muon}.pt'),
                )
            ),
        )
    )
)

format(emutau, **_name_map)

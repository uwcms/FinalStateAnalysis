'''

Generate the e-mu-tau ntuple, used by the WH analysis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import format

# Import the templates used to make the branches
import FinalStateAnalysis.Selectors.templates.candidates as candidates
import FinalStateAnalysis.Selectors.templates.muons as muons
import FinalStateAnalysis.Selectors.templates.electrons as electrons
import FinalStateAnalysis.Selectors.templates.taus as taus

_name_map = {
    'muon' : 'daughter(1)',
    'electron' : 'daughter(0)',
    'tau' : 'daughter(2)',
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
                cut = cms.string('abs({muon}.eta) < 2.1'),
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
                    #MuPt = cms.string('{muon}.pt'),
                    # Add muon branches
                    candidates.kinematics.replace(object='muon'),
                    candidates.vertex_info.replace(object='muon'),
                    candidates.base_jet.replace(object='muon'),
                    # Muon specific
                    muons.id.replace(object='muon'),
                    muons.tracking.replace(object='muon'),

                    # Add electron branches
                    candidates.kinematics.replace(object='electron'),
                    candidates.vertex_info.replace(object='electron'),
                    candidates.base_jet.replace(object='electron'),
                    # Electron specific
                    electrons.id.replace(object='electron'),
                    electrons.tracking.replace(object='electron'),

                    # Add tau branches
                    candidates.kinematics.replace(object='tau'),
                    candidates.vertex_info.replace(object='tau'),
                    candidates.base_jet.replace(object='tau'),
                    taus.info.replace(object='tau'),
                    taus.id.replace(object='tau'),
                )
            ),
        )
    )
)

format(emutau, **_name_map)

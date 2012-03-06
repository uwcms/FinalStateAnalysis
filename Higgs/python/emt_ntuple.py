'''

Generate the e-mu-tau ntuple, used by the WH analysis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import format
import FinalStateAnalysis.Selectors.templates.candidates as candidates

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
                    candidates.kinematics.replace(object='muon'),
                    candidates.vertex_info.replace(object='muon'),
                    candidates.base_jet.replace(object='muon'),
                )
            ),
        )
    )
)

format(emutau, **_name_map)

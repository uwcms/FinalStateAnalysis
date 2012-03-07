'''

Generate the mu-mu-mu ntuple, used by the WH analysis for measuring the
jet -> muon fake rate in Z->mumu + jet events.

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import format

# Import the templates used to make the branches
import FinalStateAnalysis.Selectors.templates as templates

_name_map = {
    'muon1' : 'daughter(0)',
    'muon1_idx' : '0',
    'muon2' : 'daughter(1)',
    'muon2_idx' : '1',
    'muon3' : 'daughter(2)',
    'muon3_idx' : '2',
}

mumumu = cms.EDFilter(
    "PATFinalStateAnalysisFilter",

    weights = cms.vstring(),

    # Object to build our ntuple with
    src = cms.InputTag("finalStateMuMuMu"),

    # Source of event level info
    evtSrc = cms.InputTag("patFinalStateEventProducer"),

    # Keep track of events killed in the skim
    skimCounter = cms.InputTag("eventCount", "", "TUPLE"),

    analysis = cms.PSet(
        # Define the basic selections we apply before making the ntuple
        selections = cms.VPSet(
            cms.PSet(
                name = cms.string('Mu1Pt'),
                cut = cms.string('{muon1}.pt > 17'),
            ),
            cms.PSet(
                name = cms.string('Mu1Eta'),
                cut = cms.string('abs({muon1}.eta) < 2.1'),
            ),
            cms.PSet(
                name = cms.string('Mu2Pt'),
                cut = cms.string('{muon2}.pt > 7'),
            ),
            cms.PSet(
                name = cms.string('Mu2Eta'),
                cut = cms.string('abs({muon2}.eta) < 2.1'),
            ),
            cms.PSet(
                name = cms.string('Mu3Pt'),
                cut = cms.string('{muon3}.pt > 5'),
            ),
            cms.PSet(
                name = cms.string('Mu3Eta'),
                cut = cms.string('abs({muon3}.eta) < 2.3'),
            ),
        ),

        # Define what to do with the FSes that pass all selections
        final = cms.PSet(
            sort = cms.string('{muon3}.pt'), # sort output by TauPt
            take = cms.uint32(5),
            plot = cms.PSet(
                histos = cms.VPSet(), # Don't make any final plots
                ntuple = cms.PSet(
                    # Basic info about the final state
                    templates.topology.finalstate,
                    templates.topology.mtToMET.replace(object='muon1'),
                    templates.topology.mtToMET.replace(object='muon2'),
                    templates.topology.mtToMET.replace(object='muon3'),

                    # Triggers
                    templates.trigger.doublemu,
                    templates.trigger.isomu,
                    templates.trigger.singlemu,

                    # templates.Mass/DR/Dphi/SS of pairs
                    templates.topology.pairs.replace(object1='muon1', object2='muon3'),
                    templates.topology.pairs.replace(object1='muon1', object2='muon2'),
                    templates.topology.pairs.replace(object1='muon2', object2='muon3'),

                    # Z compat. of two muons
                    templates.topology.zboson.replace(object1='muon1', object2='muon2'),
                    templates.topology.zboson.replace(object1='muon1', object2='muon3'),
                    templates.topology.zboson.replace(object1='muon2', object2='muon3'),

                    # templates.Event num/lumi/run
                    templates.event.num,
                    # templates.Rho, ntvtx, nTruePU
                    templates.event.pileup,
                    # templates.Info about the MET
                    templates.event.met,

                    # templates.Add muon1 branches
                    templates.candidates.kinematics.replace(object='muon1'),
                    templates.candidates.vertex_info.replace(object='muon1'),
                    templates.candidates.base_jet.replace(object='muon1'),
                    # templates.muon1 specific
                    templates.muons.id.replace(object='muon1'),
                    templates.muons.tracking.replace(object='muon1'),

                    # templates.Add muon2 branches
                    templates.candidates.kinematics.replace(object='muon2'),
                    templates.candidates.vertex_info.replace(object='muon2'),
                    templates.candidates.base_jet.replace(object='muon2'),
                    # templates.muon2 specific
                    templates.muons.id.replace(object='muon2'),
                    templates.muons.tracking.replace(object='muon2'),

                    # templates.Add tau branches
                    templates.candidates.kinematics.replace(object='muon3'),
                    templates.candidates.vertex_info.replace(object='muon3'),
                    templates.candidates.base_jet.replace(object='muon3'),
                    # templates.muon3 specific
                    templates.muons.id.replace(object='muon3'),
                    templates.muons.tracking.replace(object='muon3'),

                    # templates.Vetoes on extra objects
                    templates.cleaning.vetos,
                    #MuPt = cms.string('{muon}.pt'),
                )
            ),
        )
    )
)

format(mumumu, **_name_map)

'''

Generate the mu-mu-tau ntuple, used by the WH analysis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import format

# Import the templates used to make the branches
import FinalStateAnalysis.NtupleTools.templates as templates

_name_map = {
    'muon1' : 'daughter(0)',
    'muon1_idx' : '0',
    'muon2' : 'daughter(1)',
    'muon2_idx' : '1',
    'tau' : 'daughter(2)',
    'tau_idx' : '2',
}

mumutau = cms.EDFilter(
    "PATFinalStateAnalysisFilter",

    weights = cms.vstring(),

    # Object to build our ntuple with
    src = cms.InputTag("finalStateMuMuTau"),

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
                cut = cms.string('abs({muon1}.eta) < 2.5'),
            ),
            cms.PSet(
                name = cms.string('Mu2Pt'),
                cut = cms.string('{muon2}.pt > 7'),
            ),
            cms.PSet(
                name = cms.string('Mu2Eta'),
                cut = cms.string('abs({muon2}.eta) < 2.5'),
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
                    templates.topology.mtToMET.replace(object='muon1'),
                    templates.topology.mtToMET.replace(object='muon2'),

                    # Triggers
                    templates.trigger.doublemu,
                    templates.trigger.isomu,
                    templates.trigger.singlemu,

                    # templates.Mass/DR/Dphi/SS of pairs
                    templates.topology.pairs.replace(object1='muon1', object2='tau'),
                    templates.topology.pairs.replace(object1='muon1', object2='muon2'),
                    templates.topology.pairs.replace(object1='muon2', object2='tau'),

                    # Z compat. of two muons
                    templates.topology.zboson.replace(object1='muon1', object2='muon2'),

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

format(mumutau, **_name_map)

'''

Generate the analyzers for the quad lepton ntuples

Author: Evan K. Friis, UW Madison

'''

import itertools
import pdb
import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import format, PSet

# Import the templates used to make the branches
import FinalStateAnalysis.Selectors.templates as templates

# Define the branches that go in all ntuples
_common_template = PSet(
    # Basic info about the final state
    templates.topology.finalstate,
    # templates.Event num/lumi/run
    templates.event.num,
    # templates.Rho, ntvtx, nTruePU
    templates.event.pileup,
    # templates.Info about the MET
    templates.event.met,
    # templates.Vetoes on extra objects
    templates.cleaning.vetos,
    # We only need to worry about lepton triggers
    templates.trigger.mueg,
    templates.trigger.doublemu,
    templates.trigger.doublee,
    templates.trigger.isomu,
    templates.trigger.singlemu,
    rapidityGap = 'abs(subcand(0, 1).get.eta - subcand(2, 3).get.eta)',
)

# Define the branch templates for different object types.
_tau_template = PSet(
    templates.candidates.base_jet,
    templates.candidates.kinematics,
    templates.candidates.vertex_info,
    templates.cleaning.overlaps,
    templates.taus.info,
    templates.taus.id,
    templates.topology.mtToMET,
)

_muon_template = PSet(
    templates.candidates.base_jet,
    templates.candidates.kinematics,
    templates.candidates.vertex_info,
    templates.muons.id,
    templates.muons.tracking,
    templates.topology.mtToMET,
)

_electron_template = PSet(
    templates.candidates.base_jet,
    templates.candidates.kinematics,
    templates.candidates.vertex_info,
    templates.electrons.id,
    templates.electrons.tracking,
    templates.topology.mtToMET,
)

_leg_templates = {
    't' : _tau_template,
    'm' : _muon_template,
    'e' : _electron_template,
}

_pt_cuts = {
    'm' : '4',
    'e' : '5',
    't' : '15',
}

_eta_cuts = {
    'm' : '2.5',
    'e' : '2.5',
    't' : '2.5',
}

# How to get from a leg name to "finalStateElecMuMuMu" etc
_producer_translation = {
    'm' : 'Mu',
    'e' : 'Elec',
    't' : 'Tau'
}

def make_ntuple(*legs):
    assert(len(legs)==4)

    # Make sure we only use allowed leg types
    allowed = set(['m', 'e', 't'])
    assert(all(x in allowed for x in legs))

    # Make object labels
    object_labels = []
    format_labels = {
    }

    # Count how many objects of each type we put in
    counts = {
        't' : 0,
        'm' : 0,
        'e' : 0
    }

    ntuple_config = _common_template.clone()

    for i, leg in enumerate(legs):
        counts[leg] += 1
        # Check if we need to append an index (i.e. we have same flavor objects)
        label = leg
        if legs.count(leg) > 1:
            label = leg + str(counts[leg])
        format_labels[label] = 'daughter(%i)' % i
        format_labels[label+ '_idx'] = '%i' % i
        object_labels.append(label)

        # Get a PSet describing the branches for this leg
        leg_branches = _leg_templates[leg].replace(object=label)

        # Add to the total config
        ntuple_config = PSet(
            ntuple_config,
            leg_branches
        )
    #pdb.set_trace()

    # Now we need to add all the information about the pairs
    for leg_a, leg_b in itertools.combinations(object_labels, 2):
        ntuple_config = PSet(
            ntuple_config,
            templates.topology.pairs.replace(object1=leg_a, object2=leg_b),
            templates.topology.zboson.replace(object1=leg_a, object2=leg_b),
        )

    # Now build our analyzer EDFilter
    output = cms.EDFilter(
        "PATFinalStateAnalysisFilter",
        weights = cms.vstring(),
        src = cms.InputTag("finalState" + "".join(
            _producer_translation[x] for x in legs)),
        evtSrc = cms.InputTag("patFinalStateEventProducer"),
        skimCounter = cms.InputTag("eventCount", "", "TUPLE"),
        analysis = cms.PSet(
            selections = cms.VPSet(
                cms.PSet(
                    name = cms.string('Leg0Pt'),
                    cut = cms.string('daughter(0).pt>%s' % _pt_cuts[legs[0]]),
                ),
                cms.PSet(
                    name = cms.string('Leg0Eta'),
                    cut = cms.string('abs(daughter(0).eta) < %s' % _eta_cuts[legs[0]])
                ),
                cms.PSet(
                    name = cms.string('Leg1Pt'),
                    cut = cms.string('daughter(1).pt>%s' % _pt_cuts[legs[1]]),
                ),
                cms.PSet(
                    name = cms.string('Leg1Eta'),
                    cut = cms.string('abs(daughter(1).eta) < %s' % _eta_cuts[legs[1]])
                ),
                cms.PSet(
                    name = cms.string('Leg2Pt'),
                    cut = cms.string('daughter(2).pt>%s' % _pt_cuts[legs[2]]),
                ),
                cms.PSet(
                    name = cms.string('Leg2Eta'),
                    cut = cms.string('abs(daughter(2).eta) < %s' % _eta_cuts[legs[2]])
                ),
                cms.PSet(
                    name = cms.string('Leg3Pt'),
                    cut = cms.string('daughter(3).pt>%s' % _pt_cuts[legs[3]]),
                ),
                cms.PSet(
                    name = cms.string('Leg3Eta'),
                    cut = cms.string('abs(daughter(3).eta) < %s' % _eta_cuts[legs[3]])
                ),
            ),
            final = cms.PSet(
                sort = cms.string('daughter(3).pt'), # Doesn't really matter
                take = cms.uint32(50),
                plot = cms.PSet(
                    histos = cms.VPSet(), # Don't make any final plots
                    ntuple = ntuple_config.clone(),
                )
            ),
        )
    )

    # Apply "uniqueness requirements" to reduce final processing/storage.
    # This make sure there is only one ntuple entry per-final state.  The
    # combinatorics due to different orderings are removed.
    # Algorithm:
    # if there are 2 of any given type, order them by pt
    # if there are 3
    #   first put best Z in initial position
    #   then order first two by pt
    # if there are 4
    #   first put best Z in initial position
    #   then order first two by pt
    #   then order third and fourth by pt
    for type, count in counts.iteritems():
        if count == 2:
            leg1_idx = format_labels['%s1_idx' % type]
            leg2_idx = format_labels['%s2_idx' % type]
            output.analysis.selections.append(cms.PSet(
                name = cms.string('UniqueByPt'),
                cut = cms.string('orderedInPt(%s, %s)' % (leg1_idx, leg2_idx))
            ))
        if count == 3:
            leg1_idx_label = format_labels['%s1_idx' % type]
            leg2_idx_label = format_labels['%s2_idx' % type]
            leg3_idx_label = format_labels['%s3_idx' % type]

            # Require first two leptons make the best Z
            output.analysis.selections.append(cms.PSet(
                name = cms.string('Z12_Better_Z13'),
                cut = cms.string(
                    'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                    (leg1_idx_label, leg2_idx_label, leg1_idx_label,
                     leg3_idx_label)
                )
            ))

            output.analysis.selections.append(cms.PSet(
                name = cms.string('Z12_Better_Z23'),
                cut = cms.string(
                    'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                    (leg1_idx_label, leg2_idx_label, leg2_idx_label,
                     leg3_idx_label)
                )
            ))

            # Require first two leptons are ordered in PT
            output.analysis.selections.append(cms.PSet(
                name = cms.string('UniqueByPt'),
                cut = cms.string('orderedInPt(%s, %s)' %
                                 (leg1_idx_label, leg2_idx_label))
            ))
        if count == 4:
            leg1_idx_label = format_labels['%s1_idx' % type]
            leg2_idx_label = format_labels['%s2_idx' % type]
            leg3_idx_label = format_labels['%s3_idx' % type]
            leg4_idx_label = format_labels['%s4_idx' % type]

            # Require first two leptons make the best Z
            output.analysis.selections.append(cms.PSet(
                name = cms.string('Z12_Better_Z13'),
                cut = cms.string(
                    'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                    (leg1_idx_label, leg2_idx_label, leg1_idx_label,
                     leg3_idx_label)
                )
            ))

            output.analysis.selections.append(cms.PSet(
                name = cms.string('Z12_Better_Z23'),
                cut = cms.string(
                    'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                    (leg1_idx_label, leg2_idx_label, leg2_idx_label,
                     leg3_idx_label)
                )
            ))

            output.analysis.selections.append(cms.PSet(
                name = cms.string('Z12_Better_Z14'),
                cut = cms.string(
                    'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                    (leg1_idx_label, leg2_idx_label, leg1_idx_label,
                     leg4_idx_label)
                )
            ))

            output.analysis.selections.append(cms.PSet(
                name = cms.string('Z12_Better_Z24'),
                cut = cms.string(
                    'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                    (leg1_idx_label, leg2_idx_label, leg2_idx_label,
                     leg4_idx_label)
                )
            ))

            output.analysis.selections.append(cms.PSet(
                name = cms.string('Z12_Better_Z34'),
                cut = cms.string(
                    'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                    (leg1_idx_label, leg2_idx_label, leg3_idx_label,
                     leg4_idx_label)
                )
            ))

            # Require first two leptons are ordered in PT
            output.analysis.selections.append(cms.PSet(
                name = cms.string('UniqueByPt12'),
                cut = cms.string('orderedInPt(%s, %s)' %
                                 (leg1_idx_label, leg2_idx_label))
            ))
            # Require last two leptons are ordered in PT
            output.analysis.selections.append(cms.PSet(
                name = cms.string('UniqueByPt34'),
                cut = cms.string('orderedInPt(%s, %s)' %
                                 (leg3_idx_label, leg4_idx_label))
            ))


    # Now apply our formatting operations
    format(output, **format_labels)

    return output

if __name__ == "__main__":
    # Some quick tests
    #print repr(make_ntuple(*'emmt'))
    print repr(make_ntuple(*'mmmm'))

'''

Generate the analyzers for the quad lepton ntuples

Author: Evan K. Friis, UW Madison

'''

import itertools
import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import format, PSet
# Need regular expressions to get rid of non-miniAOD branches
import re

# Import the templates used to make the branches
import FinalStateAnalysis.NtupleTools.templates as templates

# Define the branches that go in all ntuples
_common_template = PSet(
    # Basic info about the final state
    templates.topology.finalstate,
    # templates.Event num/lumi/run
    templates.event.num,
    # templates.Rho, ntvtx, nTruePU
    templates.event.pileup,
    # information about the selected primary vertex
    templates.event.pv_info,
    # templates.Info about the MET
    templates.event.met,
    # templates.Info about the generator
    templates.event.gen,
    # templates.Vetoes on extra objects
    templates.cleaning.vetos,
    # VBF variables, because most analyses using FSA want them
    templates.topology.vbf,

    # PHYS14 lepton triggers
    templates.trigger.singleLepton,
    templates.trigger.doubleLepton,
    templates.trigger.tripleLepton, # tiple e only, for some reason
    # Need to fill out photon triggers
#     templates.trigger.isomu,
#     templates.trigger.isomu24eta2p1,
#     templates.trigger.singlePho,
#     templates.trigger.doublePho,
#     templates.trigger.isoMuTau
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
    templates.muons.energyCorrections,
    templates.muons.tracking,
    templates.muons.trigger,
    templates.topology.mtToMET,
)

_bjet_template= PSet(
    templates.bjets.btagging,
    templates.candidates.kinematics,
    templates.bjets.pujets,
#    templates.candidates.vertex_info, # Always filled with 0 as far as I can tell
)

_electron_template = PSet(
    templates.candidates.base_jet,
    templates.candidates.kinematics,
    templates.candidates.vertex_info,
    templates.electrons.id,
    templates.electrons.energyCorrections,
    templates.electrons.tracking,
    templates.electrons.supercluster,
    templates.electrons.trigger,
    templates.topology.mtToMET,
)

_photon_template = PSet(
    templates.candidates.base_jet,
    templates.candidates.kinematics,
    #templates.candidates.vertex_info, #photons have no tracking info
    templates.photons.id,
    templates.photons.tracking,
    templates.photons.energyCorrections,
    templates.photons.supercluster,
    #templates.photons.trigger, #add photons later
    templates.topology.mtToMET,
)


_leg_templates = {
    't': _tau_template,
    'm': _muon_template,
    'e': _electron_template,
    'g': _photon_template,
    'j': _bjet_template
}

_pt_cuts = {
    'm': '5',
    'e': '7',
    't': '18',
    'g': '10',
    'j': '20'
}

_eta_cuts = {
    'm': '2.5',
    'e': '3.0',
    't': '2.3',
    'g': '3.0',
    'j': '2.5'
}

# How to get from a leg name to "finalStateElecMuMuMu" etc
_producer_translation = {
    'm': 'Mu',
    'e': 'Elec',
    't': 'Tau',
    'g': 'Pho',
    'j': 'Jet'
}



def add_ntuple(name, analyzer, process, schedule, event_view=False):
    ''' Add an ntuple to the process with given name and schedule it

    A path for the ntuple will be created.
    '''
    if hasattr(process, name):
        raise ValueError("An ntuple builder module named %s has already"
                         " been attached to the process!" % name)
    setattr(process, name, analyzer)
    analyzer.analysis.EventView = cms.bool(bool(event_view))
    # Make a path for this ntuple
    p = cms.Path(analyzer)
    setattr(process, name + 'path', p)
    schedule.append(p)


def add_ntuple_filter(name, analyzer, filterSeq, process, schedule, event_view=False):
    ''' Add an ntuple to the process with given name and schedule it

    A path for the ntuple will be created.
    '''
    if hasattr(process, name):
        raise ValueError("An ntuple builder module named %s has already"
                         " been attached to the process!" % name)
    setattr(process, name, analyzer)
    analyzer.analysis.EventView = cms.bool(bool(event_view))
    # Make a path for this ntuple, adding the filter
    p=cms.Path(filterSeq*analyzer)
    #p = cms.Path(analyzer)
    setattr(process, name + 'path', p)
    schedule.append(p)




def make_ntuple(*legs, **kwargs):
    ''' Build an ntuple for a set of input legs.

    You can passes extra branches by passing a dict of branch:strings using the
    keyword argument: branches

    You can specify that no disambiguation can be applied (i.e. a dimuon
    candidate will appear twice in the mu-mu ntuple, in both orders)
    by setting 'noclean' to True in kwargs.

    '''
    # Make sure we only use allowed leg types
    allowed = set(['m', 'e', 't', 'g','j'])
    assert(all(x in allowed for x in legs))
    # Make object labels
    object_labels = []
    format_labels = {
    }

    pt_cuts = kwargs.get('ptCuts',{'e':'0','m':'0','t':'0','g':'0','j':'0'})
    eta_cuts = kwargs.get('etaCuts',{'e':'10','m':'10','t':'10','g':'10','j':'10'})

    # Count how many objects of each type we put in
    counts = {
        't': 0,
        'm': 0,
        'e': 0,
        'g': 0,
	'j': 0,
    }

    hzz = kwargs.get('hzz',False)

    ntuple_config = _common_template.clone()
    if kwargs.get('runTauSpinner', False):
        for parName in templates.event.tauSpinner.parameterNames_():
            setattr(
                ntuple_config, 
                parName, 
                getattr(
                    templates.event.tauSpinner, 
                    parName
                ) 
            )

    # Optionally apply extra branches in kwargs
    if 'branches' in kwargs:
        for branch, value in kwargs['branches'].iteritems():
            setattr(ntuple_config, branch, cms.string(value))

    # Check if we want to use special versions of the FSA producers
    # via a suffix on the producer name.
    producer_suffix = kwargs.get('suffix', '')

    # custom ntuple psets
    eventVariables = kwargs.get('eventVariables',PSet())
    ntuple_config = PSet(
        ntuple_config,
        eventVariables
    )

    candidateVariables = kwargs.get('candidateVariables',PSet())
    custVariables = {}
    custVariables['e'] = kwargs.get('electronVariables',PSet())
    custVariables['m'] = kwargs.get('muonVariables',PSet())
    custVariables['t'] = kwargs.get('tauVariables',PSet())
    custVariables['g'] = kwargs.get('photonVariables',PSet())
    custVariables['j'] = kwargs.get('jetVariables',PSet())

    for v in ['e','m','t','g','j']:
        _leg_templates[v] = PSet(
            _leg_templates[v],
            candidateVariables,
            custVariables[v]
        )


    for i, leg in enumerate(legs):
        counts[leg] += 1
        # Check if we need to append an index (we have same flavor objects)
        label = leg
        if legs.count(leg) > 1:
            label = leg + str(counts[leg])
        format_labels[label] = 'daughter(%i)' % i
        format_labels[label + '_idx'] = '%i' % i
        object_labels.append(label)

        # Get a PSet describing the branches for this leg
        leg_branches = _leg_templates[leg].replace(object=label)


        # Add to the total config
        ntuple_config = PSet(
            ntuple_config,
            leg_branches
        )
    #pdb.set_trace()

    # If basic jet information is desired for a non-jet final state, put it in
    for i in range(kwargs.get("nExtraJets", 0)):
        label = "jet%i"%(i+1)
        format_labels[label] = 'evt.jets.at(%i)' % i
        format_labels[label + '_idx'] = '%i' % i
        
        ntuple_config = PSet(
            ntuple_config,
            templates.topology.extraJet.replace(object=label)
            )
    
    dicandidateVariables = kwargs.get('dicandidateVariables',PSet())
    templates.topology.pairs = PSet(
        templates.topology.pairs,
        dicandidateVariables
    )

    # Now we need to add all the information about the pairs
    for leg_a, leg_b in itertools.combinations(object_labels, 2):
        if hzz:
            ntuple_config = PSet(
                ntuple_config,
                templates.topology.pairs.replace(object1=leg_a, object2=leg_b),
                templates.topology.zbosonMiniAOD.replace(object1=leg_a, object2=leg_b),
                )
        else:
            ntuple_config = PSet(
                ntuple_config,
                templates.topology.pairs.replace(object1=leg_a, object2=leg_b),
                )
        # Check if we want to enable SVfit
        # Only do SVfit in states with 2 or 4 leptons
        do_svfit = kwargs.get("svFit", False)
        if not len(legs) % 2 == 0:
            do_svfit = False

        leg_a_type = leg_a[0]
        leg_b_type = leg_b[0]
      
        leg_a_index = legs.index(leg_a_type) \
            if counts[leg_a_type] == 1 else legs.index(leg_a_type) + int(leg_a[1]) - 1
        leg_b_index = legs.index(leg_b_type) \
            if counts[leg_b_type] == 1 else legs.index(leg_b_type) + int(leg_b[1]) - 1

        # Never do SVfit on 'non-paired' leptons (eg legs 0 & 2), or legs 1&3
        # legs either adjacent or both ends (0 and 3)
        if leg_a_index % 2 != 0 or abs(leg_a_index - leg_b_index) % 2 != 1:
            do_svfit = False
        # Only do SVfit on mu + tau, e + tau, e + mu, & tau + tau combinations
        if leg_a_type == leg_b_type and leg_a_type in ('m', 'e'):
            do_svfit = False
        # Always ignore photons
        if 'g' in legs:
            do_svfit = False
        if do_svfit:
            print "SV fitting legs %s and %s in final state %s" % (
                leg_a, leg_b, ''.join(legs))
            ntuple_config = PSet(
                ntuple_config,
                templates.topology.svfit.replace(object1=leg_a, object2=leg_b)
            )

    analyzerSrc = "finalState" + "".join(
            _producer_translation[x] for x in legs ) + producer_suffix

    if hzz:
        ntuple_config = PSet(
            ntuple_config,
            templates.topology.fsrMiniAOD
            )
    
    # Some feature are not included in miniAOD or are currently broken. 
    # Remove them from the ntuples to prevent crashes.
    #!!! Take items off of this list as we unbreak them. !!!#
    notInMiniAOD = [
        # candidates.py
        "t[1-9]?PVDZ",
        "t[1-9]?S?IP[23]D(Err)?",
        ]

    allRemovals = re.compile("(" + ")|(".join(notInMiniAOD) + ")")
    
    ntuple_config = ntuple_config.remove(allRemovals)

    # Now build our analyzer EDFilter skeleton
    output = cms.EDFilter(
        "PATFinalStateAnalysisFilter",
        weights=cms.vstring(),
        # input final state collection.
        src=cms.InputTag( analyzerSrc ),
        evtSrc=cms.InputTag("patFinalStateEventProducer"),
        # counter of events before any selections
        skimCounter=cms.InputTag("eventCount", "", "TUPLE"),
        analysis=cms.PSet(
            selections=cms.VPSet(),
            EventView=cms.bool(False),
            final=cms.PSet(
                sort=cms.string('daughter(0).pt'),  # Doesn't really matter
                take=cms.uint32(50),
                plot=cms.PSet(
                    histos=cms.VPSet(),  # Don't make any final plots
                    # ntuple has all generated branches in it.
                    ntuple=ntuple_config.clone(),
                )
            ),
        )
    )

    # Apply the basic selection to each leg
    for i, leg in enumerate(legs):
        output.analysis.selections.append(
            cms.PSet(
                name=cms.string('Leg%iPt' % i),
                cut=cms.string('daughter(%i).pt>%s' % (
                    i, pt_cuts[legs[i]]),
                )
            )
        )
        output.analysis.selections.append(
            cms.PSet(
                name=cms.string('Leg%iEta' % i),
                cut=cms.string('abs(daughter(%i).eta) < %s' % (
                    i, eta_cuts[legs[i]]))
            ),
        )

    #Apply additional selections
    if 'skimCuts' in kwargs and kwargs['skimCuts']:
        for cut in kwargs['skimCuts']:
            output.analysis.selections.append(
                cms.PSet(
                    name = cms.string(cut),
                    cut  = cms.string(cut)
                ),
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
    #
    # Algorithm for dblhMode:
    # if there are 4
    #   first two leptons must be positive
    #   third and fourth leptons must be negative
    #   order first two by pt
    #   order third and fourth by pt
    noclean = kwargs.get('noclean', False)

    # ZZ-producer does not require this cleaning step
    make_unique = not noclean

    isDblH = kwargs.get('dblhMode', False)
    
    if make_unique:
        for type, count in counts.iteritems():
            if count == 2:
                leg1_idx = format_labels['%s1_idx' % type]
                leg2_idx = format_labels['%s2_idx' % type]
                output.analysis.selections.append(cms.PSet(
                    name=cms.string('%s_UniqueByPt' % type),
                    cut=cms.string('orderedInPt(%s, %s)' %
                                   (leg1_idx, leg2_idx))
                ))
            if count == 3:
                leg1_idx_label = format_labels['%s1_idx' % type]
                leg2_idx_label = format_labels['%s2_idx' % type]
                leg3_idx_label = format_labels['%s3_idx' % type]

                # Require first two leptons make the best Z
                output.analysis.selections.append(cms.PSet(
                    name=cms.string('Z12_Better_Z13'),
                    cut=cms.string(
                        'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                        (leg1_idx_label, leg2_idx_label, leg1_idx_label,
                         leg3_idx_label)
                    )
                ))

                output.analysis.selections.append(cms.PSet(
                    name=cms.string('Z12_Better_Z23'),
                    cut=cms.string(
                        'zCompatibility(%s, %s) < zCompatibility(%s, %s)' %
                        (leg1_idx_label, leg2_idx_label, leg2_idx_label,
                         leg3_idx_label)
                    )
                ))

                # Require first two leptons are ordered in PT
                output.analysis.selections.append(cms.PSet(
                    name=cms.string('%s_UniqueByPt' % type),
                    cut=cms.string('orderedInPt(%s, %s)' %
                                     (leg1_idx_label, leg2_idx_label))
                ))
            if count == 4:
                leg1_idx_label = format_labels['%s1_idx' % type]
                leg2_idx_label = format_labels['%s2_idx' % type]
                leg3_idx_label = format_labels['%s3_idx' % type]
                leg4_idx_label = format_labels['%s4_idx' % type]

                if isDblH:
                    output.analysis.selections.append(cms.PSet(
                        name=cms.string('hpp12_and_hmm34'),
                        cut=cms.string(
                            'hppCompatibility(%s, %s, 1) &&'
                            'hppCompatibility(%s, %s, -1)' %
                            (leg1_idx_label, leg2_idx_label, leg3_idx_label,
                             leg4_idx_label)
                        )
                    ))
                else:
                    if hzz:
                        cutstr = 'zCompatibilityFSR(%s, %s, "FSRCand") < zCompatibilityFSR(%s, %s, "FSRCand")'
                    else:
                        cutstr = 'zCompatibility(%s, %s) < zCompatibility(%s, %s)'

                    # Require first two leptons make the best Z

                    print cutstr%(leg1_idx_label, leg2_idx_label, leg1_idx_label,leg3_idx_label)

                    if not hzz: # HZZ wants all ZZ candidates to have their own row, so order the Zs but don't cut alternative pairings
                        output.analysis.selections.append(cms.PSet(
                            name=cms.string('Z12_Better_Z13'),
                            cut=cms.string(
                                cutstr %
                                (leg1_idx_label, leg2_idx_label, leg1_idx_label,
                                 leg3_idx_label)
                            )
                        ))
    
                        output.analysis.selections.append(cms.PSet(
                            name=cms.string('Z12_Better_Z23'),
                            cut=cms.string(
                                cutstr %
                                (leg1_idx_label, leg2_idx_label, leg2_idx_label,
                                 leg3_idx_label)
                            )
                        ))
    
                        output.analysis.selections.append(cms.PSet(
                            name=cms.string('Z12_Better_Z14'),
                            cut=cms.string(
                                cutstr %
                                (leg1_idx_label, leg2_idx_label, leg1_idx_label,
                                 leg4_idx_label)
                            )
                        ))
    
                        output.analysis.selections.append(cms.PSet(
                            name=cms.string('Z12_Better_Z24'),
                            cut=cms.string(
                                cutstr %
                                (leg1_idx_label, leg2_idx_label, leg2_idx_label,
                                 leg4_idx_label)
                            )
                        ))
                    #endif (everything past here happens for HZZ as well) 

                    output.analysis.selections.append(cms.PSet(
                        name=cms.string('Z12_Better_Z34'),
                        cut=cms.string(
                            cutstr %
                            (leg1_idx_label, leg2_idx_label, leg3_idx_label,
                             leg4_idx_label)
                        )
                    ))

                # Require first two leptons are ordered in PT
                output.analysis.selections.append(cms.PSet(
                    name=cms.string('%s_UniqueByPt12' % type),
                    cut=cms.string('orderedInPt(%s, %s)' %
                                   (leg1_idx_label, leg2_idx_label))
                ))
                # Require last two leptons are ordered in PT
                output.analysis.selections.append(cms.PSet(
                    name=cms.string('%s_UniqueByPt34' % type),
                    cut=cms.string('orderedInPt(%s, %s)' %
                                   (leg3_idx_label, leg4_idx_label))
                ))

    # Now apply our formatting operations
    format(output, **format_labels)
#    return LHEFilter*output

    return output

if __name__ == "__main__":
    # Some quick tests
    #print repr(make_ntuple(*'emmt'))
    print repr(make_ntuple(*'mmmm'))

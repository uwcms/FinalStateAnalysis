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

    # Triggers different for 25 and 50ns, no longer in common template
    # templates.trigger.singleLepton,
    # templates.trigger.doubleLepton,
    # templates.trigger.tripleLepton, # tiple e only, for some reason
    # Need to fill out photon triggers
    # templates.trigger.isomu,
    # templates.trigger.isomu24eta2p1,
    # templates.trigger.singlePho,
    # templates.trigger.doublePho,
    # templates.trigger.isoMuTau
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
    #templates.muons.trigger_25ns,
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
    #templates.electrons.trigger_25ns,
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



def add_ntuple(name, analyzer, process, schedule, event_view=False, filters=[]):
    ''' Add an ntuple to the process with given name and schedule it

    A path for the ntuple will be created.
    '''
    if hasattr(process, name):
        raise ValueError("An ntuple builder module named %s has already"
                         " been attached to the process!" % name)
    setattr(process, name, analyzer)
    analyzer.analysis.EventView = cms.bool(bool(event_view))
    # Make a path for this ntuple
    #p = cms.Path(analyzer)
    p = cms.Path()
    for f in filters:
        p *= f
    p *= analyzer
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
    postfix = kwargs.pop('postfix','')
    isShiftedMet = kwargs.pop('isShiftedMet',False)
    # Make sure we only use allowed leg types
    allowed = set(['m', 'e', 't', 'g','j'])
    assert(all(x in allowed for x in legs))
    # Make object labels
    object_labels = []
    format_labels = {
    }

    # Count how many objects of each type we put in
    counts = {
        't': 0,
        'm': 0,
        'e': 0,
        'g': 0,
	'j': 0,
    }

    hzz = kwargs.get('hzz',False)
    zh = kwargs.get('zh',False)

    runMVAMET = kwargs.get('runMVAMET', False)
    runNewMVAMET = kwargs.get('runNewMVAMET', False)
    fullJES = kwargs.get('fullJES', False)

    isMC = kwargs.get('isMC', False)

    ntuple_config = _common_template.clone()
    if fullJES:
        ntuple_config = PSet(
            ntuple_config,
            templates.topology.fullJES
        )

    if isShiftedMet :
        ntuple_config = PSet(
            ntuple_config,
            templates.event.shiftedMet
        )
        
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

    # Triggers we care about depend on run configuration
    leg_triggers = { 'e':PSet(), 'm':PSet(), 't':PSet(), 'j':PSet(), 'g':PSet() }
    if isMC:
        leg_triggers['e'] = templates.electrons.trigger_25ns_MC
        lep_triggers = templates.trigger.singleLepton_25ns_MC
    else:
        leg_triggers['e'] = templates.electrons.trigger_25ns
        lep_triggers = templates.trigger.singleLepton_25ns
    leg_triggers['m'] = templates.muons.trigger_25ns
    diLep_triggers = templates.trigger.doubleLepton_25ns
    triLep_triggers = templates.trigger.tripleLepton

    ntuple_config = PSet(
        ntuple_config,
        lep_triggers,
        diLep_triggers,
        triLep_triggers
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

    leg_branch_templates = {}
    for v in ['e','m','t','g','j']:
        leg_branch_templates[v] = PSet(
            _leg_templates[v],
            leg_triggers[v],
            custVariables[v],
            candidateVariables,
        )
        if isShiftedMet and v!='j':
            leg_branch_templates[v] = PSet(
                leg_branch_templates[v],
                templates.topology.shiftedMtToMET
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
        leg_branches = leg_branch_templates[leg].replace(object=label)

        # Add to the total config
        ntuple_config = PSet(
            ntuple_config,
            leg_branches,
        )


    # If basic jet information is desired for a non-jet final state, put it in
    extraJetVariables = kwargs.get('extraJetVariables', PSet())
    extra_jet_template = PSet(
        templates.topology.extraJet,
        extraJetVariables,
        )
    for i in range(kwargs.get("nExtraJets", 0)):
        label = "jet%i"%(i+1)
        format_labels[label] = 'evt.jets.at(%i)' % i
        format_labels[label + '_idx'] = '%i' % i
        
        ntuple_config = PSet(
            ntuple_config,
            extra_jet_template.replace(object=label)            
            )
    
    dicandidateVariables = kwargs.get('dicandidateVariables',PSet())
    dicandidate_template = PSet(
        templates.topology.pairs,
        dicandidateVariables
    )

    # Now we need to add all the information about the pairs
    for leg_a, leg_b in itertools.combinations(object_labels, 2):
        ntuple_config = PSet(
            ntuple_config,
            dicandidate_template.replace(object1=leg_a, object2=leg_b),
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
            _producer_translation[x] for x in legs ) + producer_suffix + postfix

    # Some feature are not included in miniAOD or are currently broken. 
    # Remove them from the ntuples to prevent crashes.
    #!!! Take items off of this list as we unbreak them. !!!#
    notInMiniAOD = [
        # candidates.py
        "t[1-9]?S?IP[23]D(Err)?",
        ]

    # get rid of MVA MET stuff if we're not computing it
    if not runMVAMET:
        notInMiniAOD.append("mvaMet((Et)|(Phi))")
        notInMiniAOD.append("mvaMetCov((00)|(01)|(10)|(11))")
        notInMiniAOD.append("[emtgj][1-9]?MtToMVAMET")
        notInMiniAOD.append("Mva((Met)|(MetPhi))")
        notInMiniAOD.append("MvaMetCovMatrix((00)|(01)|(10)|(11))")
        notInMiniAOD.append("NBTagPD((L)|(M))_idL_jVeto")
        notInMiniAOD.append("NBTagPD((L)|(M))_jVeto")
    if not fullJES:
        notInMiniAOD.append("JESTotal|JESClosure")

    allRemovals = re.compile("(" + ")|(".join(notInMiniAOD) + ")")
    
    ntuple_config = ntuple_config.remove(allRemovals)

    # Now build our analyzer EDFilter skeleton
    output = cms.EDFilter(
        "PATFinalStateAnalysisFilter",
        weights=cms.vstring(),
        # input final state collection.
        src=cms.InputTag( analyzerSrc ),
        evtSrc=cms.InputTag("patFinalStateEventProducer{0}".format(postfix)),
        # counter of events before any selections
        skimCounter=cms.InputTag("eventCount"),
        summedWeight=cms.InputTag("summedWeight"),
        analysis=cms.PSet(
            selections=cms.VPSet(),
            EventView=cms.bool(False),
            final=cms.PSet(
                sort=cms.string('daughter(0).pt'),  # Doesn't really matter
                take=cms.uint32(999), # max number of rows for an event
                plot=cms.PSet(
                    histos=cms.VPSet(),  # Don't make any final plots
                    # ntuple has all generated branches in it.
                    ntuple=ntuple_config.clone(),
                )
            ),
        )
    )

    # Apply minimal pt and eta cuts and "uniqueness requirements" 
    # to reduce final processing/storage.
    # See NtupleTools/python/uniqueness_cut_generator for details.
    noclean = kwargs.get('noclean', False)
    from FinalStateAnalysis.NtupleTools.uniqueness_cut_generator import uniqueness_cuts
    if not noclean:
        pt_cuts = kwargs.get('ptCuts',{'e':'0','m':'0','t':'0','g':'0','j':'0'})
        eta_cuts = kwargs.get('etaCuts',{'e':'10','m':'10','t':'10','g':'10','j':'10'})

        for name, cut in uniqueness_cuts(legs, pt_cuts, eta_cuts,
                                         skimCuts=kwargs.get('skimCuts', []),
                                         hzz=hzz, 
                                         zh=zh, 
                                         dblH=kwargs.get('dblhMode', False)).iteritems():
            output.analysis.selections.append(
                cms.PSet(
                    name=cms.string(name),
                    cut=cms.string(cut),
                    )
                )

    # Now apply our formatting operations
    format(output, **format_labels)
#    return LHEFilter*output

    return output

if __name__ == "__main__":
    # Some quick tests
    #print repr(make_ntuple(*'emmt'))
    print repr(make_ntuple(*'mmmm'))

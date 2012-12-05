import FWCore.ParameterSet.Config as cms

'''

Snippet to add trilepton ntuple production to the process

'''

from ntuple_builder import make_ntuple, add_ntuple

trilepton_final_states = [
    'emt',
    'mmt',
    'eet',
    'mmm',
    'emm',
    'eee',
    'eem'
]
photon_final_states = [
    'eeg',
    'egg',
    'mmg',
    'mgg',
    'emg',
]

def add_trilepton_ntuples(process, schedule,
                          do_trileptons = True,
                          do_photons    = False,
                          event_view    = False):
    final_states = []
    if do_trileptons:
        final_states.extend(trilepton_final_states)
    if do_photons:
        final_states.extend(photon_final_states)
    for final_state in final_states:
        print "Building %s final state" % final_state
        analyzer = make_ntuple(*final_state)
        add_ntuple(final_state, analyzer, process, schedule, event_view)

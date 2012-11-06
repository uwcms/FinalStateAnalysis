import FWCore.ParameterSet.Config as cms

'''

Snippet to add h2tau ntuple production to the process

'''

from ntuple_builder import make_ntuple, add_ntuple

final_states = [
    'et',
    'mt',
]

def add_h2tau_ntuples(process, schedule, noET=True):
    for final_state in final_states:
        if noET and final_state == 'et':
            print "Skipping ETau final state"
            continue
        print "Building %s final state" % final_state
        analyzer = make_ntuple(*final_state)
        add_ntuple(final_state, analyzer, process, schedule)

import FWCore.ParameterSet.Config as cms

'''

Snippet to add lepton+photon ntuple production to the process

'''

from ntuple_builder import make_ntuple, add_ntuple

ellpho_final_states = [ 
    'eg',
    'mg'
]

def add_leptonphoton_ntuples(process, schedule):
    final_states = []    
    final_states.extend(ellpho_final_states)
    
    for final_state in final_states:
        print "Building %s final state" % final_state
        analyzer = make_ntuple(*final_state)
        add_ntuple(final_state, analyzer, process, schedule)

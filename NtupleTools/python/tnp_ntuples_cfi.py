import FWCore.ParameterSet.Config as cms

'''

Snippet to add TNP dilepton ntuple production to the process

'''

from ntuple_builder import make_ntuple, add_ntuple

final_states = [
    'mm',
    'ee',
    'em',
]

def add_tnp_ntuples(process, schedule):
    for final_state in final_states:
        print "Building %s final state" % final_state
        analyzer = make_ntuple(*final_state, noclean=False)
        add_ntuple(final_state, analyzer, process, schedule)

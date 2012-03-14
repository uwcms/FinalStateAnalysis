import FWCore.ParameterSet.Config as cms

'''

Snippet to add quad ntuple production to the process

'''

from FinalStateAnalysis.Higgs.quad_ntuples import make_ntuple

final_states = [
    'eeem',
    'eeet',
    'eemm',
    'eemt',
    'eett',
    'emmm',
    'emmt',
    'mmmt',
    'mmtt',
]

def add_quad_ntuples(process, schedule):
    for final_state in final_states:
        print "Building %s final state" % final_state
        # build ntuplizer
        analyzer = make_ntuple(final_state[0], final_state[1], final_state[2],
                               final_state[3])
        # Add to process
        setattr(process, final_state, analyzer)
        # Make a path
        p = cms.Path(analyzer)
        setattr(process, final_state + 'path', p)
        schedule.append(p)

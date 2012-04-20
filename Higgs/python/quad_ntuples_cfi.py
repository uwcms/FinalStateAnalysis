import FWCore.ParameterSet.Config as cms

'''

Snippet to add quad ntuple production to the process

'''

from FinalStateAnalysis.Higgs.quad_ntuples import make_ntuple

zh_final_states = [
    'eeem',
    'eeet',
    'eemt',
    'eett',
    'emmm',
    'emmt',
    'mmmt',
    'mmtt',
]

zz_final_states = [
    'eeee',
    'eemm',
    'mmmm',
]

def add_quad_ntuples(process, schedule, do_zh=True, do_zz=False):
    final_states = []
    if do_zh:
        final_states.extend(zh_final_states)
    if do_zz:
        final_states.extend(zz_final_states)

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

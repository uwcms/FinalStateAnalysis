import FWCore.ParameterSet.Config as cms

'''

Snippet to add quad ntuple production to the process

'''

from ntuple_builder import make_ntuple, add_ntuple

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

zgg_final_states = [
    'eegg',
    'mmgg',
]

branches = {
    'rapidityGap': 'abs(subcand(0, 1).get.eta - subcand(2, 3).get.eta)',
}


def add_quad_ntuples(process, schedule,
                     do_zh=True, do_zz=False, do_zgg=False,
                     event_view=False):
    final_states = []
    if do_zh:
        final_states.extend(zh_final_states)
    if do_zz:
        final_states.extend(zz_final_states)
    if do_zgg:
        final_states.extend(zgg_final_states)

    for final_state in final_states:
        print "Building %s final state" % final_state
        analyzer = make_ntuple(*final_state, branches=branches)
        add_ntuple(final_state, analyzer, process, schedule, event_view)

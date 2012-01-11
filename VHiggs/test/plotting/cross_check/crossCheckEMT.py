import rootpy.io as io
import sys
sys.path.append('.')
from analysis_cfg import cfg

print "Run me from test/plotting"

file = io.open('../uw_old_emt_emu_vh.root')

tree = file.emt.final.Ntuple
print tree

events = [
    #(166163, 21535313),
    #(166380, 1570830562),
    #(167284, 482525686),
    #(167898, 1936669536),
    #(171156, 408963773),
    #(171315, 134426527),
    #(176841, 121308752),
    #(177074, 136387485),
    #(178854, 76038953),
    #(178920, 71077537),
    #(180241, 731156083),
    (172411, 237, 290309172),
    (166408, 485, 618658267),
    (166380, 1023, 1114594455),
    (172949, 1103, 1547599611),
    (177074, 496, 772810697),
    (177074, 159, 205460982),
    (177791, 157, 158096971),
    (177730, 137, 181708887),
    (180241, 412, 731156083),
    (179563, 55, 87859459),
]

all_cuts = cfg['emt']['baseline'] + \
        cfg['emt']['charge_categories']['emu']['object1']['pass'] +\
        cfg['emt']['charge_categories']['emu']['object2']['pass'] +\
        cfg['emt']['charge_categories']['emu']['object3']['pass'] +\
        cfg['emt']['charge_categories']['emu']['selections']['final']['cuts']


good_events = 0
for event_info in events:
    run, event, lumi = None, None, None
    if len(event_info) == 2:
        run, event = event_info
    elif len(event_info) == 3:
        run, lumi, event = event_info

    run_evt = [
        'run == %i' % run,
        'evt == %i' % event
    ]
    pass_topo = tree.GetEntries(' && '.join(run_evt))
    print "\nRUN: %i EVENT: %i" % (run, event)
    if not pass_topo:
        print "- has no loose e-mu-tau candidates!"
        continue
    else:
        print "- has %i loose e-mu-tau candidates:" % pass_topo
    for i in range(pass_topo):
        idx_cut = ['idx == %i' % i]
        bad_cuts = 0
        good_cands = 0
        for cut in all_cuts:
            if 'MuCharge' in cut:
                continue
            to_test = run_evt + idx_cut + [cut]
            to_test_str = ' && '.join(to_test)
            passes_cut = tree.GetEntries(to_test_str)
            if not passes_cut:
                print "-- [cand %i] fails cut: %s" % (i, cut)
                bad_cuts += 1
        if not bad_cuts:
            print "-- [cand %i] passes all cuts" % i
            good_cands += 1
    if good_cands:
        good_events += 1
    print "- has %i e-mu-tau candidates which pass all cuts" % good_cands

print "After all cuts %i/%i events remain" % (good_events, len(events))



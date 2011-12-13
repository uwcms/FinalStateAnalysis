import rootpy.io as io
import mmtAnalysis as mmt

file = io.open('../vhiggs.root')

tree = file.mmt.final.Ntuple
print tree

events = [
    (166438, 740, 832860130),
    (176201, 201, 295602695),
    (176697, 211, 290756462),
    (175990, 112, 120477532),
    (177074, 210, 287258412),
    (180250, 402, 735389588),
]

good_events = 0
for run, lumi, event in events:
    run_evt = [
        'run == %i' % run,
        'evt == %i' % event
    ]
    pass_topo = tree.GetEntries(' && '.join(run_evt))
    print "\nRUN: %i EVENT: %i" % (run, event)
    if not pass_topo:
        print "- has no loose mu-mu-tau candidates!"
        continue
    else:
        print "- has %i loose mu-mu-tau candidates:" % pass_topo
    for i in range(pass_topo):
        idx_cut = ['idx == %i' % i]
        bad_cuts = 0
        good_cands = 0
        for cut in mmt.all_cuts:
            if 'Charge' in cut:
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
    print "- has %i mu-mu-tau candidates which pass all cuts" % good_cands

print "After all cuts %i/%i events remain" % (good_events, len(events))



'''

Common definition of Zmumu selection used in ZH analysis

'''

from FinalStateAnalysis.TMegaSelector.megautil import And

def build_zmm_selection(meta_tree):
    ''' Build the Zmumu selection '''
    meta = meta_tree
    selection = And(
        # Trigger selection
        meta.doubleMuPass > 0.5,

        # Leading muon selection
        meta.m1_m2_SS < 0.5,
        meta.m1_m2_Mass < 120,
        meta.m1_m2_Mass > 60,

        meta.m1Pt > 20,
        meta.m2Pt > 10,

        meta.m1RelPFIsoDB < 0.25,
        meta.m2RelPFIsoDB < 0.25,

        meta.m1AbsEta < 2.4,
        meta.m2AbsEta < 2.4,
        meta.m1IsGlobal > 0.5,
        meta.m1IsTracker > 0.5,
        meta.m1GlbTrkHits > 10.5,
        meta.m2IsGlobal > 0.5,
        meta.m2IsTracker > 0.5,
        meta.m2GlbTrkHits > 10.5,
    )
    return selection

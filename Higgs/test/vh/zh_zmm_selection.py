'''

Common definition of Zmumu selection used in ZH analysis

'''

from FinalStateAnalysis.TMegaSelector.megautil import And

def build_selection(meta_tree):
    meta = meta_tree
    selection = And(
        # Trigger selection
        meta.doubleMuPass > 0.5,
        # Pick the best Z candidate in the first two positions
        meta.m1_m2_Zcompat < meta.m1_m3_Zcompat,
        meta.m1_m2_Zcompat < meta.m2_m3_Zcompat,

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
        # FIXME -> use VBTF ID
        meta.m1WWID > 0.5,
        meta.m2WWID > 0.5,

        # Order the leading Z muons by PT so we only have one candidate per event
        meta.m1Pt > meta.m2Pt,
    )

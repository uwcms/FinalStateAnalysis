'''

Implementation of ZH search in the mu-mu-mu-e channel

'''

from Analyzer import Analyzer
from FinalStateAnalysis.PlotTools.megautil import MetaTree, And, Or
from zh_zmm_selection import build_zmm_selection

meta = MetaTree()

unique = And(
    # Pick the best Z candidate in the first two positions
    meta.m1_m2_Zcompat < meta.m1_m3_Zcompat,
    meta.m1_m2_Zcompat < meta.m2_m3_Zcompat,
    meta.m1Pt > meta.m2Pt
)

base_selections = And(

    # Build the leading ZMM selection
    build_zmm_selection(meta),

    # Subleading muon selection
    meta.m3Pt > 10,
    meta.m3AbsEta < 2.4,

    meta.ePt > 10,
    meta.eAbsEta < 2.5,

    # Vetoes
    meta.muGlbIsoVetoPt10 < 1,
    meta.eVetoCicTightIso < 1,
    #meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # DZ cuts
    abs(meta.m1DZ - meta.m2DZ) < 0.1,
    abs(meta.m1DZ - meta.m3DZ) < 0.1,
    abs(meta.m1DZ - meta.eDZ) < 0.1,

    meta.eCiCTight.bit(1),
    meta.eMissingHits < 1.5,
    #meta.m3VBTFID > 0.5,
    meta.m3IsGlobal > 0.5,
    meta.m3IsTracker > 0.5,
    meta.m3GlbTrkHits > 10.5,
)

os = meta.e_m3_SS < 0.5

e_id = And(
    meta.eRelPFIsoDB < 0.25,
)

m3_id = And(
    meta.m3RelPFIsoDB < 0.25,
)

final = unique & os & base_selections & m3_id & e_id

l1_anti_iso = unique & os & base_selections & m3_id & ~e_id
l2_anti_iso = unique & os & base_selections & ~m3_id & e_id
both_anti_iso = unique & os & base_selections & ~m3_id & ~e_id

mt_cut = meta.m3MtToMET < 50

def pu_weight(x):
    return x.puWeightData2011AB

basic_histograms = [
    (lambda x: x.m1Pt, '', ('m1Pt', '#mu_{1} p_{T}', 20, 0, 200)),
    (lambda x: x.m1AbsEta, '', ('m1AbsEta', '#mu_{1} |#eta|', 10, 0, 2.5)),
    (lambda x: x.m1_m2_Mass, '', ('z1Mass', 'Z_{1} Mass', 20, 60, 120)),
    (lambda x: x.e_m3_Mass, '', ('z2Mass', 'Z_{2} Mass', 20, 30, 150)),
]

def build_histo_list(weight_function, name_suffix=""):
    # Function to take list of generic histograms and apply a weight function
    output = []
    for functor, location, ctor in basic_histograms:
        ctor_list = list(ctor)
        ctor_list[0] += name_suffix
        output.append(
            (functor, weight_function, location, tuple(ctor_list))
        )
    return output

class AnalyzeMMME(Analyzer):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeMMME, self).__init__(tree, output, **kwargs)

        l1_name, l1_id = 'mu', m3_id
        l2_name, l2_id = 'e', e_id

        # Our categories - all combos of OS/SS, and Z2 leptons pass/fail
        for sign_type, sign_cut in [ ('os', os), ('ss', ~os) ]:
            for l1_label, l1_cut in [('pass', l1_id), ('fail', ~l1_id)]:
                for l2_label, l2_cut in [('pass', l2_id), ('fail', ~l2_id)]:
                    self.define_region(
                        '_'.join(
                            [sign_type, l1_name, l1_label, l2_name, l2_label]),
                        unique & sign_cut & base_selections & l1_cut & l2_cut,
                        build_histo_list(pu_weight)
                    )

        self.disable_branch('*')
        for b in meta.active_branches():
            self.enable_branch(b)
        self.enable_branch('run')
        self.enable_branch('lumi')
        self.enable_branch('evt')
        self.enable_branch('e_m3_Mass')
        self.enable_branch('puWeightData2011AB')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        self.analyze(tree, entry)
        return True

    def finish(self):
        self.write_histos()

'''

Implementation of ZH search in the mu-mu-mu-e channel

'''

from Analyzer import Analyzer
from FinalStateAnalysis.TMegaSelector.megautil import MetaTree, And, Or
from zh_zee_selection import build_zee_selection

meta = MetaTree()

unique = And(
    # Pick the best Z candidate in the first two positions
    meta.e1_e2_Zcompat < meta.e1_e3_Zcompat,
    meta.e1_e2_Zcompat < meta.e2_e3_Zcompat,
    meta.e1Pt > meta.e2Pt
)

base_selections = And(

    # Build the leading zee selection
    build_zee_selection(meta),

    # Subleading muon selection
    meta.e3Pt > 10,
    meta.e3AbsEta < 2.5,

    meta.mPt > 10,
    meta.mAbsEta < 2.4,

    # Vetoes
    meta.muGlbIsoVetoPt10 < 1,
    meta.eVetoCicTightIso < 1,
    #meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # DZ cuts
    meta.e1DZ < 0.2,
    meta.e2DZ < 0.2,
    meta.e3DZ < 0.2,
    meta.mDZ < 0.2,
    meta.e3CiCTight.bit(1) > 0.5,
    meta.e3MissingHits < 1.5,
    #meta.mVBTFID > 0.5,
    meta.mIsGlobal > 0.5,
    meta.mIsTracker > 0.5,
    meta.mGlbTrkHits > 10.5,
)

os = meta.e3_m_SS < 0.5


m_id = And(
    meta.mRelPFIsoDB < 0.25,
)

e3_id = And(
    meta.e3RelPFIsoDB < 0.25,
)

final = unique & os & base_selections & e3_id & m_id

l1_anti_iso = unique & os & base_selections & ~m_id & e3_id

l2_anti_iso = unique & os & base_selections & m_id & ~e3_id

def pu_weight(x):
    return x.puWeightData2011AB

basic_histograms = [
    (lambda x: x.e1Pt, '', ('e1Pt', '#mu_{1} p_{T}', 20, 0, 200)),
    (lambda x: x.e1AbsEta, '', ('e1AbsEta', '#mu_{1} |#eta|', 10, 0, 2.5)),
    (lambda x: x.e1_e2_Mass, '', ('z1Mass', 'Z_{1} Mass', 20, 60, 120)),
    (lambda x: x.e3_m_Mass, '', ('z2Mass', 'Z_{2} Mass', 20, 30, 150)),
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

class AnalyzeEEEM(Analyzer):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeEEEM, self).__init__(tree, output, **kwargs)

        l1_name, l1_id = 'mu', m_id
        l2_name, l2_id = 'e', e3_id

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
        self.enable_branch('e3_m_Mass')
        self.enable_branch('puWeightData2011AB')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        self.analyze(tree, entry)
        return True

    def finish(self):
        self.write_histos()

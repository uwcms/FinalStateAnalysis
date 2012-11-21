'''

Implementation of ZH search in the mu-mu-tau-tau channel

'''

from Analyzer import Analyzer
from FinalStateAnalysis.PlotTools.megautil import MetaTree, And, Or
from zh_zmm_selection import build_zmm_selection

meta = MetaTree()

unique = And(
    meta.m1Pt > meta.m2Pt,
    meta.t1Pt > meta.t2Pt,
)

base_selections = And(
    # Build the leading ZMM selection
    build_zmm_selection(meta),

    # Subleading Z selection
    meta.t1Pt > 20,
    meta.t1AbsEta < 2.3,
    meta.t1DecayFinding > 0.5,

    meta.t2Pt > 20,
    meta.t2AbsEta < 2.3,
    meta.t2DecayFinding > 0.5,

    # Vetoes
    meta.muGlbIsoVetoPt10 < 1,
    meta.eVetoCicTightIso < 1,
    #meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # DZ cuts
    abs(meta.m1DZ - meta.m2DZ) < 0.1,
    abs(meta.m1DZ - meta.t1DZ) < 0.1,
    abs(meta.m1DZ - meta.t2DZ) < 0.1,

    # Tau cleaning
    meta.t1AntiElectronMedium > 0.5,
    meta.t1CiCTightElecOverlap < 0.5,
    #meta.t1ElecOverlap < 0.5,
    meta.t1AntiMuonLoose > 0.5,
    meta.t1MuOverlap < 0.5,

    meta.t2AntiElectronMedium > 0.5,
    meta.t2CiCTightElecOverlap < 0.5,
    #meta.t2ElecOverlap < 0.5,
    meta.t2AntiMuonLoose > 0.5,
    meta.t2MuOverlap < 0.5,
)

os = meta.t1_t2_SS < 0.5

t1_id = meta.t1MediumIso > 0.5

t2_id = meta.t2MediumIso > 0.5

final = unique & os & base_selections & t1_id & t2_id

l1_anti_iso = unique & os & base_selections & ~t1_id & t2_id
l2_anti_iso = unique & os & base_selections & t1_id & ~t2_id
both_anti_iso = unique & os & base_selections & ~t1_id & ~t2_id

def pu_weight(x):
    return x.puWeightData2011AB

basic_histograms = [
    (lambda x: x.m1Pt, '', ('m1Pt', '#mu_{1} p_{T}', 20, 0, 200)),
    (lambda x: x.m1AbsEta, '', ('m1AbsEta', '#mu_{1} |#eta|', 10, 0, 2.5)),
    (lambda x: x.m1_m2_Mass, '', ('z1Mass', 'Z_{1} Mass', 20, 60, 120)),
    (lambda x: x.t1_t2_Mass, '', ('z2Mass', 'Z_{2} Mass', 20, 30, 150)),
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

class AnalyzeMMTT(Analyzer):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeMMTT, self).__init__(tree, output, **kwargs)

        l1_name, l1_id = 't1', t1_id
        l2_name, l2_id = 't2', t2_id

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
        self.enable_branch('evt')
        self.enable_branch('t1_t2_Mass')
        self.enable_branch('puWeightData2011AB')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        self.analyze(tree, entry)
        return True

    def finish(self):
        self.write_histos()

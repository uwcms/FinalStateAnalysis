'''

Implementation of ZH search in the mu-mu-e-tau channel

'''
from Analyzer import Analyzer
from FinalStateAnalysis.TMegaSelector.megautil import MetaTree, And, Or
from zh_zmm_selection import build_zmm_selection

meta = MetaTree()

unique = meta.m1Pt > meta.m2Pt

base_selections = And(
    build_zmm_selection(meta),

    # Subleading muon selection
    meta.ePt > 10,
    meta.eAbsEta < 2.5,

    meta.tPt > 20,
    meta.tAbsEta < 2.3,
    meta.tDecayFinding > 0.5,

    # Vetoes
    meta.muGlbIsoVetoPt10 < 1,
    meta.eVetoCicTightIso < 1,
    #meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # DZ cuts
    meta.m1DZ < 0.2,
    meta.m2DZ < 0.2,
    meta.eDZ < 0.2,
    meta.tDZ < 0.2,

    # Tau cleaning
    meta.tAntiElectronMVA > 0.5,
    meta.tCiCTightElecOverlap < 0.5,
    meta.tAntiMuonTight > 0.5,
    meta.tMuOverlap < 0.5,
    meta.eCiCTight.bit(1),
    meta.eMissingHits < 0.5,
)

os = meta.e_t_SS < 0.5

hadronic_tau_id = meta.tLooseIso > 0.5

e_id = And(
    meta.eRelPFIsoDB < 0.10,
)

final = unique & os & base_selections & e_id & hadronic_tau_id

mt_cut = meta.eMtToMET < 50

def pu_weight(x):
    return x.puWeightData2011AB

basic_histograms = [
    (lambda x: x.m1Pt, '', ('m1Pt', '#mu_{1} p_{T}', 20, 0, 200)),
    (lambda x: x.m1AbsEta, '', ('m1AbsEta', '#mu_{1} |#eta|', 10, 0, 2.5)),
    (lambda x: x.m1_m2_Mass, '', ('z1Mass', 'Z_{1} Mass', 20, 60, 120)),
    (lambda x: x.e_t_Mass, '', ('z2Mass', 'Z_{2} Mass', 20, 30, 150)),
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

class AnalyzeMMET(Analyzer):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeMMET, self).__init__(tree, output, **kwargs)

        l1_name, l1_id = 'e', e_id
        l2_name, l2_id = 'tau', hadronic_tau_id

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
        self.enable_branch('puWeightData2011AB')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        self.analyze(tree, entry)
        return True

    def finish(self):
        self.write_histos()

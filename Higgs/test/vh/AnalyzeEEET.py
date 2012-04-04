'''

Implementation of ZH search in the e-e-e-tau channel

'''

from Analyzer import Analyzer
from FinalStateAnalysis.TMegaSelector.megautil import MetaTree, And, Or
from zh_zee_selection import build_zee_selection

meta = MetaTree()

# Selection to ensure there is only one candidate per final state
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
    meta.e3AbsEta < 2.4,

    meta.tPt > 20,
    meta.tAbsEta < 2.3,
    meta.tDecayFinding > 0.5,

    meta.e3_t_SS < 0.5,

    # Vetoes
    meta.muVetoPt5 < 1,
    meta.eVetoWP95Iso < 1,
    #meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # DZ cuts
    meta.e1DZ < 0.2,
    meta.e2DZ < 0.2,
    meta.e3DZ < 0.2,
    meta.tDZ < 0.2,

    # Tau cleaning
    meta.tAntiElectronMVA > 0.5,
    #meta.tElecOverlap < 0.5,
    meta.tAntiMuonTight > 0.5,
    #meta.tMuOverlap < 0.5,
)

hadronic_tau_id = meta.tLooseIso > 0.5

e3_id = And(
    meta.e3RelPFIsoDB < 0.10,
    meta.e3CiCTight.bit(1),
)

final = unique & base_selections & e3_id & hadronic_tau_id

mt_cut = meta.e3MtToMET < 50

def pu_weight(x):
    return x.puWeightData2011AB

basic_histograms = [
    (lambda x: x.e1Pt, '', ('e1Pt', '#e_{1} p_{T}', 20, 0, 200)),
    (lambda x: x.e1AbsEta, '', ('e1AbsEta', '#e_{1} |#eta|', 10, 0, 2.5)),
    (lambda x: x.e1_e2_Mass, '', ('z1Mass', 'Z_{1} Mass', 20, 60, 120)),
    (lambda x: x.e3_t_Mass, '', ('z2Mass', 'Z_{2} Mass', 20, 30, 150)),
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

class AnalyzeEEET(Analyzer):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeEEET, self).__init__(tree, output, **kwargs)

        self.define_region('unique',
                           unique,
                           build_histo_list(pu_weight)
                          )

        self.define_region('e_pass_tau_pass',
                           unique & base_selections & e3_id & hadronic_tau_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('e_fail_tau_pass',
                           unique & base_selections & ~e3_id & hadronic_tau_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('e_pass_tau_fail',
                           unique & base_selections & e3_id & ~hadronic_tau_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('e_fail_tau_fail',
                           unique & base_selections & ~e3_id & ~hadronic_tau_id,
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
        self.analyze(tree)
        return True

    def finish(self):
        self.write_histos()

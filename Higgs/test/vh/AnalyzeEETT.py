'''

Implementation of ZH search in the e-e-mu-tau channel

'''

from Analyzer import Analyzer
from FinalStateAnalysis.TMegaSelector.megautil import MetaTree, And, Or
from zh_zee_selection import build_zee_selection

meta = MetaTree()

unique = And(
    meta.e1Pt > meta.e2Pt,
    meta.t1Pt > meta.t2Pt,
)

base_selections = And(

    # Build the leading ZMM selection
    build_zee_selection(meta),

    meta.t1Pt > 20,
    meta.t1AbsEta < 2.3,
    meta.t1DecayFinding > 0.5,
    meta.t2Pt > 20,
    meta.t2AbsEta < 2.3,
    meta.t2DecayFinding > 0.5,

    meta.t1_t2_SS < 0.5,

    # Vetoes
    meta.muGlbIsoVetoPt10 < 1,
    meta.eVetoCicTightIso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # DZ cuts
    meta.e1DZ < 0.2,
    meta.e2DZ < 0.2,
    meta.t1DZ < 0.2,
    meta.t2DZ < 0.2,

    # Tau cleaning
    meta.t1AntiElectronMedium > 0.5,
    #meta.t1ElecOverlap < 0.5,
    meta.t1AntiMuonTight > 0.5,
    meta.t1MuOverlap < 0.5,
    meta.t2AntiElectronMedium > 0.5,
    #meta.t2ElecOverlap < 0.5,
    meta.t2AntiMuonTight > 0.5,
    meta.t2MuOverlap < 0.5,
)

hadronic_t1_id = meta.t1MediumIso > 0.5
hadronic_t2_id = meta.t2MediumIso > 0.5

final = unique & base_selections & hadronic_t1_id & hadronic_t2_id

#mt_cut = meta.t1MtToMET < 50

def pu_weight(x):
    return x.puWeightData2011AB

basic_histograms = [
    (lambda x: x.e1Pt, '', ('e1Pt', 'e_{1} p_{T}', 20, 0, 200)),
    (lambda x: x.e1AbsEta, '', ('e1AbsEta', 'e_{1} |#eta|', 10, 0, 2.5)),
    (lambda x: x.e1_e2_Mass, '', ('z1Mass', 'Z_{1} Mass', 20, 60, 120)),
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

class AnalyzeEETT(Analyzer):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeEETT, self).__init__(tree, output, **kwargs)

        self.define_region('tau1_pass_tau2_pass',
                           unique & base_selections & hadronic_t1_id & hadronic_t2_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('tau1_fail_tau2_pass',
                           unique & base_selections & ~hadronic_t1_id & hadronic_t2_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('tau1_pass_tau2_fail',
                           unique & base_selections & hadronic_t1_id & ~hadronic_t2_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('tau1_fail_tau2_fail',
                           unique & base_selections & ~hadronic_t1_id & ~hadronic_t2_id,
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

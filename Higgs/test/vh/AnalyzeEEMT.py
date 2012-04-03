'''

Implementation of ZH search in the e-e-mu-tau channel

'''

from Analyzer import Analyzer
from FinalStateAnalysis.TMegaSelector.megautil import MetaTree, And, Or
from zh_zee_selection import build_zee_selection

meta = MetaTree()

base_selections = And(

    # Build the leading ZMM selection
    build_zee_selection(meta),

    # Subleading muon selection
    meta.mPt > 10,
    meta.mAbsEta < 2.4,

    meta.tPt > 20,
    meta.tAbsEta < 2.3,
    meta.tDecayFinding > 0.5,

    meta.m_t_SS < 0.5,
    meta.m_t_Mass < 150,
    meta.m_t_Mass > 30,

    # Vetoes
    meta.muVetoPt5 < 1,
    meta.eVetoWP95Iso < 1,
    meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # DZ cuts
    meta.e1DZ < 0.2,
    meta.e2DZ < 0.2,
    meta.mDZ < 0.2,
    meta.tDZ < 0.2,

    # Tau cleaning
    meta.tAntiElectronLoose > 0.5,
    meta.tElecOverlap < 0.5,
    meta.tAntiMuonTight > 0.5,
    meta.tMuOverlap < 0.5,
)

hadronic_tau_id = meta.tLooseIso > 0.5

m_id = And(
    meta.mRelPFIsoDB < 0.15,
    meta.mVBTFID > 0.5,
)

mt_cut = meta.mMtToMET < 50

def pu_weight(x):
    return x.puWeightData2011AB

basic_histograms = [
    (lambda x: x.e1Pt, '', ('e1Pt', '#mu_{1} p_{T}', 20, 0, 200)),
    (lambda x: x.e1AbsEta, '', ('e1AbsEta', '#mu_{1} |#eta|', 10, 0, 2.5)),
    (lambda x: x.e1_e2_Mass, '', ('z1Mass', 'Z_{1} Mass', 20, 60, 120)),
    (lambda x: x.m_t_Mass, '', ('z2Mass', 'Z_{2} Mass', 20, 30, 150)),
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

class AnalyzeEEMT(Analyzer):

    def __init__(self, tree, output, **kwargs):
        super(AnalyzeEEMT, self).__init__(tree, output, **kwargs)

        self.define_region('mu_pass_tau_pass',
                           base_selections & m_id & hadronic_tau_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('mu_fail_tau_pass',
                           base_selections & ~m_id & hadronic_tau_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('mu_pass_tau_fail',
                           base_selections & m_id & ~hadronic_tau_id,
                           build_histo_list(pu_weight)
                          )

        self.define_region('mu_fail_tau_fail',
                           base_selections & ~m_id & ~hadronic_tau_id,
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

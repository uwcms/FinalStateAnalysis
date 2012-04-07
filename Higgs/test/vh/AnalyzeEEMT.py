'''

Implementation of ZH search in the e-e-mu-tau channel

'''

from Analyzer import Analyzer
from FinalStateAnalysis.TMegaSelector.megautil import MetaTree, And, Or
from zh_zee_selection import build_zee_selection

meta = MetaTree()

unique = meta.e1Pt > meta.e2Pt

base_selections = And(

    # Build the leading ZMM selection
    build_zee_selection(meta),

    # Subleading muon selection
    meta.mPt > 10,
    meta.mAbsEta < 2.4,

    meta.tPt > 20,
    meta.tAbsEta < 2.3,
    meta.tDecayFinding > 0.5,


    # Vetoes
    meta.muGlbIsoVetoPt10 < 1,
    meta.eVetoCicTightIso < 1,
    #meta.bjetVeto < 1,
    meta.tauVetoPt20 < 1,

    # DZ cuts
    meta.e1DZ < 0.2,
    meta.e2DZ < 0.2,
    meta.mDZ < 0.2,
    meta.tDZ < 0.2,

    # Tau cleaning
    meta.tAntiElectronLoose > 0.5,
    #meta.tElecOverlap < 0.5,
    meta.tAntiMuonTight > 0.5,
    meta.tMuOverlap < 0.5,
    #meta.mVBTFID > 0.5,
    meta.mIsGlobal > 0.5,
    meta.mIsTracker > 0.5,
    meta.mGlbTrkHits > 10.5,
)

os = meta.m_t_SS < 0.5

hadronic_tau_id = meta.tLooseIso > 0.5

m_id = And(
    meta.mRelPFIsoDB < 0.15,
)

final = unique & os & base_selections & m_id & hadronic_tau_id

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

        l1_name, l1_id = 'mu', m_id
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
        self.enable_branch('m_t_Mass')
        self.enable_branch('puWeightData2011AB')

    def process(self, entry):
        tree = self.tree
        read = tree.GetEntry(entry)
        self.analyze(tree, entry)
        return True

    def finish(self):
        self.write_histos()

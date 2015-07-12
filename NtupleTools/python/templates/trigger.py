'''

Ntuple branch template sets for trigger selections

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

IMPORTANT NOTE: If you want the logical OR of several paths, separate them 
by '|' rather than by ','. 
When the Smart Trigger gets a group of paths separated by commas, it uses 
the one with the lowest prescale (taking the first in case of a tie).

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

_trig_template = PSet(
    namePass = 'evt.hltResult("paths")',
    nameGroup = 'evt.hltGroup("paths")',
    namePrescale = 'evt.hltPrescale("paths")',
)

singleLepton_50ns_MC = PSet(
    _trig_template.replace(
        name='singleMu', 
        paths=r'HLT_Mu50_v\\d+'
        ),
    _trig_template.replace(
        name='singleE',
        paths=r'HLT_Ele27_eta2p1_WP75_Gsf_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg1', 
        paths=r'HLT_Mu17_TrkIsoVVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg2', 
        paths=r'HLT_Mu8_TrkIsoVVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg1_noiso', 
        paths=r'HLT_Mu17_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg2_noiso', 
        paths=r'HLT_Mu8_v\\d+'
        ),
    _trig_template.replace(
        name='singleE_leg1', 
        paths=r'HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleE_leg2', 
        paths=r'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    )

singleLepton_50ns = PSet(
    _trig_template.replace(
        name='singleMu', 
        paths=r'HLT_Mu40_v\\d+'
        ),
    _trig_template.replace(
        name='singleE',
        paths=r'HLT_Ele27_eta2p1_WPLoose_Gsf_v\\d+|HLT_Ele23_CaloIdL_TrackIdL_IsoVL_V\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg1', 
        paths=r'HLT_Mu17_TrkIsoVVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg2', 
        paths=r'HLT_Mu8_TrkIsoVVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg1_noiso', 
        paths=r'HLT_Mu17_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg2_noiso', 
        paths=r'HLT_Mu8_v\\d+'
        ),
    _trig_template.replace(
        name='singleE_leg1', 
        paths=r'HLT_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleE_leg2', 
        paths=r'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    )

singleLepton_25ns_MC = PSet(
    _trig_template.replace(
        name='singleMu', 
        paths=r'HLT_Mu50_v\\d+'
        ),
    _trig_template.replace(
        name='singleE',
        paths=r'HLT_Ele32_eta2p1_WP75_Gsf_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg1', 
        paths=r'HLT_Mu17_TrkIsoVVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg2', 
        paths=r'HLT_Mu8_TrkIsoVVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg1_noiso', 
        paths=r'HLT_Mu17_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg2_noiso', 
        paths=r'HLT_Mu8_v\\d+'
        ),
    _trig_template.replace(
        name='singleE_leg1', 
        paths=r'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleE_leg2', 
        paths=r'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    )

singleLepton_25ns = PSet(
    _trig_template.replace(
        name='singleMu', 
        paths=r'HLT_Mu50_v\\d+'
        ),
    _trig_template.replace(
        name='singleE',
        paths=r'HLT_Ele32_eta2p1_WPLoose_Gsf_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg1', 
        paths=r'HLT_Mu17_TrkIsoVVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg2', 
        paths=r'HLT_Mu8_TrkIsoVVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg1_noiso', 
        paths=r'HLT_Mu17_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu_leg2_noiso', 
        paths=r'HLT_Mu8_v\\d+'
        ),
    _trig_template.replace(
        name='singleE_leg1', 
        paths=r'HLT_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleE_leg2', 
        paths=r'HLT_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    )

doubleLepton_50ns = PSet(
    _trig_template.replace(
        name='doubleMu',
        paths=r'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\d+|HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+'
        ),
    _trig_template.replace(
        name='doubleE',
        paths=r'HLT_Ele17_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+'
        ),
    _trig_template.replace(
        name='singleESingleMu',
        paths=r'HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMuSingleE',
        paths=r'HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    )

doubleLepton_25ns = PSet(
    _trig_template.replace(
        name='doubleMu',
        paths=r'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\d+|HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+'
        ),
    _trig_template.replace(
        name='doubleE',
        paths=r'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+'
        ),
    _trig_template.replace(
        name='singleESingleMu',
        paths=r'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    _trig_template.replace(
        name='singleMuSingleE',
        paths=r'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v\\d+'
        ),
    )

tripleLepton = PSet(
    _trig_template.replace(
        name='tripleE',
        paths=r'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v\\d+'
        ),
    _trig_template.replace(
        name='doubleESingleMu',
        paths=r'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_v\\d+'
        ),
    _trig_template.replace(
        name='doubleMuSingleE',
        paths=r'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_v\\d+'
        ),
    _trig_template.replace(
        name='tripleMu',
        paths=r'HLT_TripleMu_12_10_5_v\\d+'
        ),
    )

# isomu = _trig_template.replace(name='isoMu',
#     paths=r'HLT_IsoMu17_v\\d+, HLT_IsoMu20_v\\d+, '
#           r'HLT_IsoMu24_v\\d+, HLT_IsoMu24_eta2p1_v\\d+, '
#           r'HLT_IsoMu30_v\\d+, HLT_IsoMu30_eta2p1_v\\d+'
# )
# 
# isomu24eta2p1 = _trig_template.replace(name='isoMu24eta2p1',
#     paths=r'HLT_IsoMu24_eta2p1_v\\d+')
# 
# doublemu = PSet(
#     _trig_template.replace(
#         name='doubleMu',
#         paths=r'HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+,HLT_Mu17_Mu8_v\\d+'),
#     _trig_template.replace(
#         name='doubleMuTrk',
#         paths=r'HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+,HLT_Mu17_TrkMu8_v\\d+'),
#      _trig_template.replace(
#         name='mu17mu8',
#         paths=r'HLT_Mu17_Mu8_v\\d+')
# )
# 
# singlee = PSet(
#     _trig_template.replace(
#     name='singleE',
#     paths=r'HLT_Ele27_WP80_v\\d+,HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v\\d+,HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v\\d+'
#     ),
#     _trig_template.replace(
#     name='singleEPFMT',
#     paths=r'HLT_Ele27_WP80_PFMET_MT50_v\\d+,HLT_Ele32_WP70_PFMT50_v\\d+'
#     )
# )
# 
# doublee = PSet(
#     _trig_template.replace(
#         name='doubleE',
#         paths=r'HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v\\d+,HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+',
#     ),
#     _trig_template.replace(
#         name='doubleEExtra',
#         paths=r'HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v\\d+,HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+,HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17_v5,HLT_Ele65_CaloIdVT_TrkIdT_v3,HLT_Ele100_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v2',
#     ),
#     _trig_template.replace(
#         name='doubleETight',
#         paths=r'HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+'
#     )
# )
# 
# tripee = PSet(
#     _trig_template.replace(
#         name='tripleE',
#         paths=r'HLT_Ele15_Ele8_Ele5_CaloIdL_TrkIdVL_v\\d+'
#         )
#     )
# 
# mueg = PSet(
#     # Mu17Ele8 paths
#     _trig_template.replace(
#         name='mu17ele8',
#         paths=r"HLT_Mu17_Ele8_CaloIdL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+"),
#     _trig_template.replace(
#         name='mu17ele8iso',
#         paths=r"HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+"),
#     # Mu8Ele17 paths
#     _trig_template.replace(
#         name='mu8ele17',
#         paths=r'HLT_Mu8_Ele17_CaloIdL_v\\d+,HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v\\d+'),
#     _trig_template.replace(
#         name='mu8ele17iso',
#         paths=r"HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+"),
# )
# 
# singlePho = _trig_template.replace( name='singlePho', paths='' )
# doublePho = _trig_template.replace(
#     name='doublePho',
#     paths=r'HLT_Photon26_CaloId10_Iso50_Photon18_CaloId10_Iso50_Mass60_v\\d+,HLT_Photon26_R9Id85_OR_CaloId10_Iso50_Photon18_R9Id85_OR_CaloId10_Iso50_Mass70_v\\d+,HLT_Photon36_R9Id85_OR_CaloId10_Iso50_Photon10_R9Id85_OR_CaloId10_Iso50_Mass80_v\\d+' )
# 
# 
# isoMuTau =PSet( 
#     _trig_template.replace(
#         name='isoMuTau',
# 	paths=r"HLT_IsoMu12_LooseIsoPFTau10_v\\d+,HLT_IsoMu15_LooseIsoPFTau15_v\\d+,HLT_IsoMu15_eta2p1_LooseIsoPFTau20_v\\d+,HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v\\d+,HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v\\d+"),
#     _trig_template.replace(
# 	name='muTau',
# 	paths=r"HLT_Mu18_eta2p1_LooseIsoPFTau20_v\\d+"),
#     _trig_template.replace(
#         name='muTauTest',
#         paths=r"HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v\\d+"),
# )
# 


'''

Ntuple branch template sets for trigger selections

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

_trig_template = PSet(
    namePass = 'evt.hltResult("paths")',
    nameGroup = 'evt.hltGroup("paths")',
    namePrescale = 'evt.hltPrescale("paths")',
)

singlemu = _trig_template.replace(
    name='singleMu', paths=r'HLT_Mu15_v\\d+, HLT_Mu24_v\\d+, HLT_Mu30_v\\d+')

isomu = _trig_template.replace(name='isoMu',
    paths=r'HLT_IsoMu17_v\\d+, HLT_IsoMu20_v\\d+, '
          r'HLT_IsoMu24_v\\d+, HLT_IsoMu24_eta2p1_v\\d+, '
          r'HLT_IsoMu30_v\\d+, HLT_IsoMu30_eta2p1_v\\d+'
)

isomu24eta2p1 = _trig_template.replace(name='isoMu24eta2p1',
    paths=r'HLT_IsoMu24_eta2p1_v\\d+')

doublemu = PSet(
    _trig_template.replace(
        name='doubleMu',
        paths=r'HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+,HLT_Mu17_Mu8_v\\d+'),
    _trig_template.replace(
        name='doubleMuTrk',
        paths=r'HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+,HLT_Mu17_TrkMu8_v\\d+'),
     _trig_template.replace(
        name='mu17mu8',
        paths=r'HLT_Mu17_Mu8_v\\d+')
)

singlee = PSet(
    _trig_template.replace(
    name='singleE',
    paths=r'HLT_Ele27_WP80_v\\d+,HLT_Ele27_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v\\d+,HLT_Ele32_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_v\\d+'
    ),
    _trig_template.replace(
    name='singleEPFMT',
    paths=r'HLT_Ele27_WP80_PFMET_MT50_v\\d+,HLT_Ele32_WP70_PFMT50_v\\d+'
    )
)

doublee = PSet(
    _trig_template.replace(
        name='doubleE',
        paths=r'HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v\\d+,HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+',
    ),
    _trig_template.replace(
        name='doubleEExtra',
        paths=r'HLT_Ele17_CaloIdL_CaloIsoVL_Ele8_CaloIdL_CaloIsoVL_v\\d+,HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+,HLT_Ele32_CaloIdT_CaloIsoT_TrkIdT_TrkIsoT_SC17_v5,HLT_Ele65_CaloIdVT_TrkIdT_v3,HLT_Ele100_CaloIdVL_CaloIsoVL_TrkIdVL_TrkIsoVL_v2',
    ),
    _trig_template.replace(
        name='doubleETight',
        paths=r'HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+'
    )

)

mueg = PSet(
    # Mu17Ele8 paths
    _trig_template.replace(
        name='mu17ele8',
        paths=r"HLT_Mu17_Ele8_CaloIdL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+"),
    _trig_template.replace(
        name='mu17ele8iso',
        paths=r"HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+"),
    # Mu8Ele17 paths
    _trig_template.replace(
        name='mu8ele17',
        paths=r'HLT_Mu8_Ele17_CaloIdL_v\\d+,HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v\\d+'),
    _trig_template.replace(
        name='mu8ele17iso',
        paths=r"HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v\\d+"),
)

singlePho = _trig_template.replace( name='singlePho', paths='' )
doublePho = _trig_template.replace(
    name='doublePho',
    paths=r'HLT_Photon26_CaloId10_Iso50_Photon18_CaloId10_Iso50_Mass60_v\\d+,HLT_Photon26_R9Id85_OR_CaloId10_Iso50_Photon18_R9Id85_OR_CaloId10_Iso50_Mass70_v\\d+,HLT_Photon36_R9Id85_OR_CaloId10_Iso50_Photon10_R9Id85_OR_CaloId10_Iso50_Mass80_v\\d+' )


isoMuTau =PSet( 
    _trig_template.replace(
        name='isoMuTau',
	paths=r"HLT_IsoMu12_LooseIsoPFTau10_v\\d+,HLT_IsoMu15_LooseIsoPFTau15_v\\d+,HLT_IsoMu15_eta2p1_LooseIsoPFTau20_v\\d+,HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v\\d+,HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v\\d+"),
    _trig_template.replace(
	name='muTau',
	paths=r"HLT_Mu18_eta2p1_LooseIsoPFTau20_v\\d+"),
    _trig_template.replace(
        name='muTauTest',
        paths=r"HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v\\d+"),
)



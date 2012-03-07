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
          r'HLT_IsoMu24_v\\d+, HLT_IsoMu24_eta2p1_v\\d+')

doublemu = _trig_template.replace(
    name='doubleMu',
    paths=r'HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+,HLT_Mu17_Mu8_v\\d+')

mueg = PSet(
    # Mu17Ele8 paths
    _trig_template.replace(
        name='mu17ele8',
        paths=r"HLT_Mu17_Ele8_CaloIdL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+"),
    # Mu8Ele17 paths
    _trig_template.replace(
        name='mu8ele17',
        paths=r'HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+,HLT_Mu17_Mu8_v\\d+')
)

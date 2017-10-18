'''

Ntuple branch template sets for trigger selections

Each string is transformed into an expression on a FinalStateEvent object.

Author: Evan K. Friis

IMPORTANT NOTE: If you want the logical OR of several paths, separate them 
by '|' rather than by ','. 
(When the Smart Trigger gets a group of paths separated by commas, it uses 
the one with the lowest prescale (taking the first in case of a tie).

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

_trig_template = PSet(
    namePass = 'evt.hltResult("paths")',
    nameGroup = 'evt.hltGroup("paths")',
    namePrescale = 'evt.hltPrescale("paths")',
)

singleLepton_25ns_MC = PSet(
    _trig_template.replace(
        name='singleIsoMu20',
        paths=r'HLT_IsoMu20_v\\d+'
        ),
    _trig_template.replace(
        name='singleIsoMu27',
        paths=r'HLT_IsoMu27_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu27',
        paths=r'HLT_Mu27_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu20',
        paths=r'HLT_Mu20_v\\d+'
        ),
    _trig_template.replace(
        name='singleIsoMu24',
        paths=r'HLT_IsoMu24_v\\d+'
        ),
    _trig_template.replace(
        name='singleIsoMu24eta2p1',
        paths=r'HLT_IsoMu24_eta2p1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu50',
        paths=r'HLT_Mu50_v\\d+'
        ),
    _trig_template.replace(
        name='singleE27Tight',
        paths=r'HLT_Ele27_WPTight_Gsf_v\\d+',
        ),
    _trig_template.replace(
        name='singleTau140',
        paths=r'HLT_VLooseIsoPFTau140_eta2p1_v\\d+'
        ),
    _trig_template.replace(
        name='singleTau140Trk50',
        paths=r'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v\\d+'
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
        )
    )

singleLepton_25ns = PSet(
        _trig_template.replace(
        name='singleIsoMu20',
        paths=r'HLT_IsoMu20_v\\d+'
        ),
    _trig_template.replace(
        name='singleIsoMu27',
        paths=r'HLT_IsoMu27_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu27',
        paths=r'HLT_Mu27_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu20',
        paths=r'HLT_Mu20_v\\d+'
        ),
    _trig_template.replace(
        name='singleIsoMu24',
        paths=r'HLT_IsoMu24_v\\d+'
        ),
    _trig_template.replace(
        name='singleIsoMu24eta2p1',
        paths=r'HLT_IsoMu24_eta2p1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu50',
        paths=r'HLT_Mu50_v\\d+'
        ),
    _trig_template.replace(
        name='singleE27Tight',
        paths=r'HLT_Ele27_WPTight_Gsf_v\\d+',
        ),
    _trig_template.replace(
        name='singleTau140',
        paths=r'HLT_VLooseIsoPFTau140_eta2p1_v\\d+'
        ),
    _trig_template.replace(
        name='singleTau140Trk50',
        paths=r'HLT_VLooseIsoPFTau140_Trk50_eta2p1_v\\d+'
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
        )
    )

doubleLepton_25ns = PSet(
    _trig_template.replace(
        name='doubleMu',
        paths=r'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_v\\d+|HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ_v\\d+'
        ),
    _trig_template.replace(
        name='doubleE_23_12',
        paths=r'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu23SingleE12DZ',
        paths=r'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu8SingleE23DZ',
        paths=r'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v\\d+'
        ),
    _trig_template.replace(
        name='doubleLooseIsoTau40',
        paths=r'HLT_DoubleLooseChargedIsoPFTau40_Trk1_eta2p1_Reg_v\\d+'
        ),
    _trig_template.replace(
        name='doubleTau35',
        paths=r'HLT_DoubleMediumChargedIsoPFTau35_Trk1_eta2p1_Reg_v\\d+'
        ),
    _trig_template.replace(
        name='doubleLooseIsoTau35',
        paths=r'HLT_DoubleLooseChargedIsoPFTau35_Trk1_eta2p1_Reg_v\\d+'
        ),
    _trig_template.replace(
        name='singleE24SingleLooseIsoTau30',
        paths=r'HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleE24SingleMediumIsoTau30',
        paths=r'HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTau30_eta2p1_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleE24SingleTightIsoTau30',
        paths=r'HLT_Ele24_eta2p1_WPTight_Gsf_TightChargedIsoPFTau30_eta2p1_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleE24SingleLooseIsoTau30TightID',
        paths=r'HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_TightID_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleE24SingleMediumIsoTau30TightID',
        paths=r'HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTau30_eta2p1_TightID_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleE24SingleTightIsoTau30TightID',
        paths=r'HLT_Ele24_eta2p1_WPTight_Gsf_TightChargedIsoPFTau30_eta2p1_TightID_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu20eta2p1LooseTau27eta2p1',
        paths=r'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu20eta2p1MediumTau27eta2p1',
        paths=r'HLT_IsoMu20_eta2p1_MediumChargedIsoPFTau27_eta2p1_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu20eta2p1TightTau27eta2p1',
        paths=r'HLT_IsoMu20_eta2p1_TightChargedIsoPFTau27_eta2p1_CrossL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu24eta2p1LooseTau20singleL1',
        paths=r'HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_SingleL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu24eta2p1MediumTau20singleL1',
        paths=r'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_SingleL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu24eta2p1TightTau20singleL1',
        paths=r'HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_SingleL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu24eta2p1LooseTau20TightIDsingleL1',
        paths=r'HLT_IsoMu24_eta2p1_LooseChargedIsoPFTau20_TightID_SingleL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu24eta2p1MediumTau20TightIDsingleL1',
        paths=r'HLT_IsoMu24_eta2p1_MediumChargedIsoPFTau20_TightID_SingleL1_v\\d+'
        ),
    _trig_template.replace(
        name='singleMu24eta2p1TightTau20TightIDsingleL1',
        paths=r'HLT_IsoMu24_eta2p1_TightChargedIsoPFTau20_TightID_SingleL1_v\\d+'
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


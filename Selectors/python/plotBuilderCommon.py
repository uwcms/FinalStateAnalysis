puWeights = [
    '3bx_S42011A',
    '3bx_S42011AB178078',
    '3bx_S42011B178078',
]

mu_triggers = [
    ('Mu15', 'Mu 15', r'HLT_Mu15_v\\d+'),
    ('Mu24', 'Mu 24', r'HLT_Mu24_v\\d+'),
    ('Mu30', 'Mu 30', r'HLT_Mu30_v\\d+'),
    ('SingleMus', 'SingleMu', r'HLT_Mu15_v\\d+, HLT_Mu24_v\\d+, HLT_Mu30_v\\d+'),

    ('IsoMu17', 'Iso Mu 17', r'HLT_IsoMu17_v\\d+'),
    ('IsoMu20', 'Iso Mu 20', r'HLT_IsoMu20_v\\d+'),
    ('IsoMu24', 'Iso Mu 24', r'HLT_IsoMu24_v\\d+'),
    ('IsoMu24eta2p1', 'Iso Mu 24 Eta2p1', r'HLT_IsoMu24_eta2p1_v\\d+'),
    ('IsoMus', 'Iso Mu Any', r'HLT_IsoMu17_v\\d+, HLT_IsoMu20_v\\d+, HLT_IsoMu24_v\\d+, HLT_IsoMu24_eta2p1_v\\d+'),
]

doublemu_triggers = [
    ('DoubleMu7', 'Double Mu 17', r'HLT_DoubleMu7_v\\d+'),
    ('Mu13Mu8', 'Mu (13) Mu (8)', r'HLT_Mu13_Mu8_v\\d+'),
    ('Mu17Mu8', 'Mu (17) Mu (8)', r'HLT_Mu17_Mu8_v\\d+'),
    ('DoubleMus', 'DoubleMuTriggers', r'HLT_DoubleMu7_v\\d+,HLT_Mu13_Mu8_v\\d+,HLT_Mu17_Mu8_v\\d+'),
]

emu_triggers = [
    ('Mu8Ele17CaloIDL', 'Mu (8) Ele (17)', r"HLT_Mu8_Ele17_CaloIdL_v\\d+"),
    ('Mu8Ele17CaloIDT', 'Mu (8) Ele (17)', r"HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v\\d+"),
    ('Mu8Ele17All', 'Mu (8) Ele (17)', r"HLT_Mu8_Ele17_CaloIdL_v\\d+,HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v\\d+"),

    ('Mu17Ele8CaloIDL', 'Mu (17) Ele (8)', r"HLT_Mu17_Ele8_CaloIdL_v\\d+"),
    ('Mu17Ele8CaloIDT', 'Mu (17) Ele (8)', r"HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+"),
    ('Mu17Ele8All', 'Mu (17) Ele (8)', r"HLT_Mu17_Ele8_CaloIdL_v\\d+,HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v\\d+"),
]

all_triggers = mu_triggers + doublemu_triggers + emu_triggers

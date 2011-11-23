import sys
import copy
import logging
# Get the data builder
import FinalStateAnalysis.PatTools.data as data

#skips = ['2011B', 'PromptReco_v6_1409']
skips = ['2011B', 'EM',  ]

data_sample, plotter = data.build_data(
    'Tau', '2011-10-28-v2-TauTNP', 'scratch_results', 1551, skips,
    count = '/mt/skimCounter', unweighted = False)

base_selections = [
    'TauJetPt > 20',
    'TauAbsEta < 2.3',
    'Tau_TauTNPPresel > 0.5',
    'MuonPt > 20',
    'MuonAbsEta < 2.1',
    'Muon_MuRelIso < 0.3',
    'HLTIsoMu17_HLT > 0.5',
    #'HLTMu15_HLT > 0.5',
    'NGlobalMuonsPt5_NGlbmuons < 0.5',
    'NBjetsPt20_Nbjets < 0.5',
    #'Tau_TauBtag < 2.0',
]

signal_region = [
    'Muon_MuRelIso < 0.1',
    'Muon_MtToMET < 40',
]

qcd_cr = [
    'Muon_MuRelIso > 0.1',
    'Muon_MtToMET < 40',
]

wjets_cr = [
    'Muon_MuRelIso < 0.1',
    'Muon_MtToMET > 60',
]

os = [
    'MuonCharge*TauCharge < 0'
]

ss = [
    'MuonCharge*TauCharge > 0'
]

passRegion = [
    'Tau_LooseHPS > 0.5',
]

failRegion = [
    '(Tau_LooseHPS < 0.5)',
]

realTau = [
    'Tau_GenDecayMode > -0.5'
]

fakeTau = [
    'Tau_GenDecayMode < -0.5'
]

highPu = [
    'FinalState_NVtx > 7.5'
]

lowPu = [
    'FinalState_NVtx < 7.5'
]

# Map histo names in template.py to the string needed to draw them
histoVarMap = {
    'Mvis' : ('muTauJetMass', (100, 0, 300)),
    'MT1' : ('Muon_MtToMET', (100, 0, 40)),
    'AbsTauEta' : ('TauAbsEta', (100, 0, 2.5)),
    'MuonCharge' : ('MuonCharge', (3, -1.5, 1.5)),
    'TauDecayMode' : ('Tau_DecayMode', (21, -0.5, 20.5)),
}

sampleMap = {
    'zjets' : 'Zjets',
    'wjets' : 'Wjets',
    'data' : 'data_SingleMu',
    'qcd' : 'QCDMu',
    'ttbar' : 'ttjets',
}

rebinning = {
    'Mvis' : 2,
}

registered = set([])

def get_th1(sample, region, histo, **kwargs):
    # Figure out what selections are applicable in this region
    selections = copy.copy(base_selections)
    if 'sig' in region:
        selections += signal_region
    elif 'qcd' in region:
        selections += qcd_cr
    elif 'wjets' in region:
        selections += wjets_cr

    if 'OS' in region:
        selections += os
    elif 'SS' in region:
        selections += ss

    if 'Pass' in region:
        selections += passRegion
    elif 'Fail' in region:
        selections += failRegion

    if 'realTau' in region:
        selections += realTau
    if 'fakeTau' in region:
        selections += fakeTau

    if 'lowPu' in region:
        selections += lowPu
    if 'highPu' in region:
        selections += highPu

    full_selection = ' && '.join(selections)

    region = region.replace('/', '')

    output_name = '_'.join([region, histo])

    key = (sample, output_name)

    if key not in registered:
        plotter.register_tree(
            output_name,
            '/mt/final/Ntuple',
            histoVarMap[histo][0],
            full_selection,
            w = 'puWeight_3bx_S42011A',
            binning = histoVarMap[histo][1],
            include = [sampleMap[sample]],
        )
        registered.add(key)

    rebin = 1
    if histo in rebinning:
        rebin = rebinning[histo]

    result = plotter.get_histogram(
        sampleMap[sample],
        '/mt/final/Ntuple:' + output_name, rebin = rebin)

    return result

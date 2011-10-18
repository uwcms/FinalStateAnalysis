import FinalStateAnalysis.Utilities.WeightedTFile as WeightedTFile
import FinalStateAnalysis.TagAndProbe.datadefs as datadefs
import os

data_sources = {}

data_name_map = {
    #'ztt' : 'Ztautau_pythia',
    'zjets' : 'Zjets_M50',
    'qcd' : 'PPmuXptGt20Mu15',
    'wjets' : 'WplusJets_madgraph',
    #'zll' : 'Zmumu_M20_pythia',
    'ttbar': 'TTplusJets_madgraph',
    'data': 'data',
}

for sample, sample_info in datadefs.datadefs.iteritems():
    if sample not in data_name_map.values():
        continue
    data_dict = {}
    data_sources[sample] = data_dict
    filename = os.path.join('..', 'data', sample + '.root')
    file = None
    if 'data' in sample:
        continue
    else:
        skim_eff = sample_info['skim']
        xsec = sample_info['x_sec']
        event_count = "ohyeah/eventCount"
        file = WeightedTFile.WeightedTFile(
            filename, 'READ',
            target_lumi = 1320,
            xsec = xsec,
            skim_eff = skim_eff,
            event_count = event_count,
            verbose = True
        )
    data_dict['file'] = file

# Add data
data_file = WeightedTFile.WeightedTFile(
    '../data/all_data.root', 'READ', weight=1.0)
data_sources['data'] = {
    'file' : data_file
}

#mc_yield = sum(info['file'].Get("ohyeah/sigPassOS/AbsTauEta").Integral()
                 #for sample, info in data_sources.iteritems()
                 #if 'data' not in sample)
#data_yield = data_sources['data']['file'].Get("ohyeah/sigPassOS/AbsTauEta").Integral()

#print mc_yield, data_yield

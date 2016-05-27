'''

Definitions of data samples used in analyses.

Picks either data7TeV or data8TeV according to the release.

For 8TeV data, if using a 53X release, 53X data samples are preferred.

Author: Evan K. Friis, Tapas Sarangi, UW Madison

'''

import copy
from FinalStateAnalysis.Utilities.version import \
        cmssw_major_version, cmssw_minor_version

data_name_map = None
datadefs = None

if cmssw_major_version() == 4:
    import data7TeV
    data_name_map = data7TeV.data_name_map
    datadefs = data7TeV.datadefs
elif cmssw_major_version() == 5 and cmssw_minor_version() == 2 :
    import data8TeV
    data_name_map = data8TeV.data_name_map
    datadefs = data8TeV.datadefs
elif cmssw_major_version() == 5 and cmssw_minor_version() >= 3 :
    import data8TeV
    import data8TeVNew
    data_name_map = copy.copy(data8TeV.data_name_map)
    datadefs = copy.copy(data8TeV.datadefs)
    # Always prefer the 53X version
    data_name_map.update(data8TeVNew.data_name_map)
    datadefs.update(data8TeVNew.datadefs)
elif cmssw_major_version() == 7:
    import data13TeV
    data_name_map = data13TeV.data_name_map
    datadefs = data13TeV.datadefs
elif cmssw_major_version() == 8:
    import data13TeV_LFV
    data_name_map = data13TeV_LFV.data_name_map
    datadefs = data13TeV_LFV.datadefs
else:
    raise ValueError("I can't figure out which release to use!")

#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
'''

Make a json file for each of the ZH events

'''


#!/usr/bin/env python

import json
import FinalStateAnalysis.MetaData.datatools as datatools
import os

# Pick the list of 2l2tau events from AN-11-402 (Table 11)

#μμeτ   161217        396   346679510
#eeeτ   163659        355   269046597
#μμeτ   171178         12    11119024
#μμμτ   172014         58    91568080
#eeeτ   172252         40    47105541
#μμμτ   172635        159   238215970
#μμeμ   177184         10    12646620
#eeeτ   177718        469   736335702
#eeττ   178100        335   455090581
#μμeτ   179497        224   298873305


events = [
    ("mmet",   161217,            396,   346679510),
    #("eeet",   163659,            355,   269046597), # 2l2tau only
    ("mmet",   171178,             12,    11119024),
    ("mmmt",   172014,             58,    91568080),
    ("eeet",   172252,             40,    47105541),
    ("mmmt",   172635,            159,   238215970),
    ("mmem",   177184,             10,    12646620),
    ("eeet",   177718,            469,   736335702),
    ("eett",   178100,            335,   455090581),
    ("mmet",   179497,            224,   298873305),
]

#mmet    &171178 &11119024       &85.33  &54.26  \\
#mmet    &161217 &346679510      &90.39  &70.57  \\
#mmmt    &172014 &91568080       &94.1   &63.23  \\
#mmmt    &177139 &226464086      &92.6   &190.8  \\      # dont have
#mmmt    &172635 &238215970      &92.38  &31.84  \\
#mmme    &177184 &12646620       &88.81  &66.43  \\
#mmme    &179889 &291267852      &60.59  &46.35  \\     # dont have
#eett    &178100 &455090581      &91.04  &62.87  \\
#eeet    &172252 &47105541       &92.32  &52.45  \\
#eeet    &177718 &736335702      &92.09  &58.13  \\

def get_pd(final_state):
    if final_state.count('m') > 1:
        return 'DoubleMu'
    if final_state.count('e') and final_state.count('m'):
        return 'MuEG'
    if final_state.count('e') > 1:
        return 'DoubleElectron'
    return 'ERROR'

# Group by channel
channels = {}

for fs, run, lumi, event in events:
    pd = get_pd(fs)
    # Get the dataname
    dataname = datatools.find_data_for_run(run, pd)

    channel_dict = channels.setdefault(fs, {})
    dataset_events = channel_dict.setdefault(dataname, [])
    dataset_events.append((run, lumi, event))

if not os.path.exists('event_lists'):
    os.makedirs('event_lists')

for channel, channel_info in channels.iteritems():
    with open('event_lists/2l2tau_%s_zh_events.json' % channel, 'w') as output:
        json.dump(channel_info, output, indent=2)


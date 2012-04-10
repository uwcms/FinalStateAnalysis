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
    ("mmet", 171178,12,11119024),
    ("mmet", 161217,396,346679510),
    ("mmmt", 172014,58,91568080),
    ("mmmt", 177139,143,226464086),
    ("mmmt", 172635,159,238215970),
    ("mmme", 179889,195,291267852),
    ("mmme", 177184,10,12646620),
    ("eett", 178871,535,721402028),
    ("eett", 178100,335,455090581),
    ("eeet", 172252,40,47105541),
    ("eeet", 177718,469,736335702),
    ("eeet", 163659,355,269046597),


    ("mmmt",171050,643,821417992),
    ("mmmt",179434,371,641824424),
    ("mmmt",179889,78,81028181),
    ("mmmt",179889,168,235516917),
    ("mmmt",175975,360,515584039),
    ("mmmt",176201,271,421507855),
    ("mmmt",176467,146,226304277),
    ("mmmt",177718,788,1263752726),
    ("mmmt",177730,189,264203514),
    ("mmmt",178098,32,42470279),
    ("mmmt",166512,1063,1231425135),
    ("mmmt",166841,62,66008312),
    ("mmmt",167281,272,346878062),
    ("mmmt",167786,107,126622509),

    # EEMT anti-iso events from abdollah
    ("eemt", 175886 , 5    , 1870597),
    ("eemt", 179563 , 55   , 87859459),
    ("eemt", 179563 , 177  , 287281642),
    ("eemt", 180076 , 160  , 291127256),
    ("eemt", 175975 , 118  , 124381600),
    ("eemt", 176286 , 453  , 667146038),
    ("eemt", 176807 , 70   , 103029014),
    ("eemt", 176886 , 107  , 167886668),
    ("eemt", 176933 , 158  , 258632028),
    ("eemt", 177139 , 450  , 730289557),
    ("eemt", 177183 , 55   , 83303116),
    ("eemt", 177201 , 538  , 778484323),
    ("eemt", 177718 , 451  , 707697062),
    ("eemt", 178365 , 797  , 1304368590),
    ("eemt", 178479 , 67   , 52217115),
    ("eemt", 161312 , 159  , 66046330),
    ("eemt", 163760 , 142  , 99809895),
    ("eemt", 165472 , 143  , 166392313),
    ("eemt", 165548 , 252  , 345446051),
    ("eemt", 165993 , 1447 , 1526558733),
    ("eemt", 166049 , 613  , 814346788),
    ("eemt", 166380 , 682  , 765067202),
    ("eemt", 166438 , 373  , 430705128),
    ("eemt", 166841 , 41   , 42157067),
    ("eemt", 167102 , 109  , 113554882),
    ("eemt", 167674 , 123  , 151560437),
    ("eemt", 172865 , 211  , 328047902),
    ("eemt", 172791 , 508  , 702201840),
]

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


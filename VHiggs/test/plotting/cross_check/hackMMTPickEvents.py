from FinalStateAnalysis.PatTools.datadefs import datadefs
import FinalStateAnalysis.PatTools.datatools as datatools
from subprocess import Popen, PIPE, STDOUT
import shlex
import re
import json

theirs_list = '''
event number = 832860130
run number = 166438
LumiSection = 740
mass H = 107.567
pt mu1 = 43.4273
pt mu2 = 30.5796
pt tau = 25.0878

event number = 295602695
run number = 176201
LumiSection = 201
mass H = 68.8899
pt mu1 = 22.7744
pt mu2 = 22.1396
pt tau = 44.5938

event number = 735389588
run number = 180250
LumiSection = 402
mass H = 14.472
pt mu1 = 52.4543
pt mu2 = 10.855
pt tau = 24.6317

event number = 290756462
run number = 176697
LumiSection = 211
mass H = 41.7268
pt mu1 = 48.4152
pt mu2 = 21.3887
pt tau = 34.5238

event number = 120477532
run number = 175990
LumiSection = 112
mass H = 68.2676
pt mu1 = 56.2604
pt mu2 = 25.8545
pt tau = 36.6988

event number = 287258412
run number = 177074
LumiSection = 210
mass H = 34.4705
pt mu1 = 27.289
pt mu2 = 26.9435
pt tau = 30.3022
'''

matcher = re.compile('''event number = (?P<evt>\d+)\s*
run number = (?P<run>\d+)\s*
LumiSection = (?P<lumi>\d+)\s*
''', re.MULTILINE)

output = {}

for match in matcher.finditer(theirs_list):
    run = int(match.group('run'))
    evt = int(match.group('evt'))
    lumi = int(match.group('lumi'))
    dataset = datatools.find_data_for_run(run, 'DoubleMu')
    print run, evt, lumi, dataset
    if dataset not in output:
        output[dataset] = [(run, lumi, evt)]
    else:
        output[dataset].append((run, lumi, evt))

print output

output_file = open('mmt_events_infn.json', 'w')
output_file.write(json.dumps(output, indent=4))

import glob
import os

from FinalStateAnalysis.TagAndProbe.datadefs import datadefs

anaCfg = 'fwliteTagAndProbe'
anaJobId = '2011-09-14-v1-TauIdAnalyze'

def get_dir(sample):
    dir_name = '-'.join([anaJobId, sample, anaCfg])
    base_dir = '/hdfs/store/user/efriis/'
    return base_dir + dir_name

def merge(outname, files):
    command = [
        'hadd', '-f',
        os.path.join('data', outname + '.root'),
    ]
    command.extend(files)
    return ' '.join(command)

def split_list(iterable, n=100):
    current = []
    for item in iterable:
        if len(current) == n:
            yield current
            current = []
        current.append(item)
    if current:
        yield current

output_commands = []
data_files = []

for sample, sample_info in datadefs.iteritems():
    dir = get_dir(sample)
    temp_files = []
    files = list(glob.glob(os.path.join(dir, '1', '*.root')))
    if len(files) < 200:
        output_commands.append(merge(sample, files))
    else:
        for i, sublist in enumerate(split_list(files)):
            output_commands.append(merge(sample + ('_%i' % i), sublist))
            temp_files.append('data/' + sample + '_%i.root' % i)
    if temp_files:
        output_commands.append(merge(sample, temp_files))

    if 'data' in sample:
        data_files.append('data/' + sample + '.root')

output_commands.append(merge('all_data', data_files))

for command in output_commands:
    print command


from FinalStateAnalysis.PatTools.datadefs import datadefs
import FinalStateAnalysis.PatTools.datatools as datatools
from subprocess import Popen, PIPE, STDOUT
import shlex

theirs_list = '''
run: 166163 event: 21535313
run: 166380  event: 1570830562
run: 167284  event: 482525686
run: 167898  event: 1936669536
run: 171156  event: 408963773
run: 171315  event: 134426527
run: 176841  event: 121308752
run: 177074  event: 136387485
run: 178854  event: 76038953
run: 178920  event: 71077537
run: 180241  event: 731156083
'''

theirs = set([])

for line in theirs_list.split('\n'):
    if not line:
        continue
    fields = line.split()
    theirs.add((int(fields[1]), int(fields[3])))

files = set([])

for run, evt in theirs:
    print "Adding run %i" % run
    dataset = datatools.map_data_to_dataset(datatools.find_data_for_run(run, 'MuEG'))
    command = 'das_client.py --limit=0 --query=\"file run=%i dataset=%s\"' % (run, dataset)
    command = shlex.split(command)
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    stdoutdata, stderrdata = p.communicate()
    for line in stdoutdata.split('\n'):
        if line.strip():
            files.add(line.strip())
    print "Now %i files" % len(files)

file_list = open('hackPickEvents_inputfiles.txt', 'w')
file_list.write('\n'.join(files))

events = ','.join('%i:%i' % (run, evt) for run, evt in theirs)

print '''

edmCopyPickMerge outputFile=hackEvents.root \
        eventsToProcess=%s \
        inputFiles_load=hackPickEvents_inputfiles.txt

''' % events

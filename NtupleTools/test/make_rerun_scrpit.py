#!/usr/bin/env cmsRun

# create a resubmit script for a FarmOut process

import sys

ifile = open(sys.argv[1], 'r')
ifileName = "%s" % sys.argv[1]
if str( ifileName[-2::] ) == 'sh':
	ifileCat = ifileName[:-3:]
	ofileName = "%s_re.sh" % ifileCat
elif str( ifileName[-2::] ) == 'ut':
	ifileCat = ifileName[:-4:]
	ofileName = "%s_re.out" % ifileCat
else:
	print "Please provide a '.sh' or '.out' file for conversion."
	ofileName = "poorly_named_file.out"

ofile = open(ofileName, "w")

dag = 'dags/dag"'
dagLen = len(dag)

for line in ifile:
  _line = line.strip()
  if _line[:4:] == 'farm':
    first = _line.find('"--output-dag')
    second = line.find('dags/dag"')
    _line2 = _line[:first:] + _line[(second+dagLen)::]
    newLine = "%s --resubmit-failed-jobs" % _line2
  else: newLine = _line
  ofile.write("%s\n" % newLine)

ifile.close()
ofile.close()

print "A resubmit file was just created for you called: %s" % ofileName

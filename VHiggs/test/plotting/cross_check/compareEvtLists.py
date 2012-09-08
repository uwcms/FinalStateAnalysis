ours_list = '''
166163 22 21535313
166380 1023 1114594455
166408 485 618658267
172411 237 290309172
172949 1103 1547599611
177074 159 205460982
177074 496 772810697
177730 137 181708887
177791 157 158096971
178479 402 645592922
179563 55 87859459
180241 412 731156083
'''

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

ours = set([])
theirs = set([])

for line in ours_list.split('\n'):
    if not line:
        continue
    fields = line.split()
    ours.add((fields[0], fields[2]))

for line in theirs_list.split('\n'):
    if not line:
        continue
    fields = line.split()
    theirs.add((fields[1], fields[3]))

print "UW has %i events" % len(ours)
print "INFN has %i events" % len(theirs)

common = ours & theirs
print "There are %i common events" % len(common)

ours_only = ours - theirs
print "UW has %i exclusive events" % len(ours_only)
theirs_only = theirs - ours
print "INFN have %i exclusive events" % len(theirs_only)

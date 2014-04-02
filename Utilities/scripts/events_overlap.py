#! /bin/env python

from RecoLuminosity.LumiDB import argparse
from pdb import set_trace
import itertools

def txt2tuple(line):
    return tuple([ int(i.strip()) for i in line.split(':') ])

def file2tlist(fname):
    ret = []
    with open(fname) as infile:
        for line in infile.readlines():
            if line.strip():
                toadd = txt2tuple(line)
                if len(toadd) == 3:
                    ret.append(toadd)
                else:
                    pass
                    #raise TypeError('cannot parse %s in file %s' % (line.strip(), fname))
    return set(ret) #set(txt2tuple(line) for line in open(fname).readlines() if line.strip())

def dump(fname, evts):
    with open(fname,'w') as out:
        out.write('\n'.join('%i:%i:%i' % i for i in evts))
        out.write('\n')

parser = argparse.ArgumentParser()
parser.add_argument('evtlists', nargs='+')
parser.add_argument('--dump-events', action='store_true', default=False, dest='dump')
args = parser.parse_args()

evt_lists = [ file2tlist(i) for i in args.evtlists ]
names     = [ i.split('.')[0].split('_')[-1] for i in args.evtlists ]
region    = '_'.join(args.evtlists[0].split('.')[0].split('_')[:-1])
evt_dict  = dict(i for i in zip(names, evt_lists))

intersect = lambda x,y: x.intersection(y)
difference = lambda x,y: x.difference(y)
full_intersection = reduce(intersect, evt_lists)
print 'Full intersection: %i' % len(full_intersection)
if args.dump:
    dump('full_intersection.txt', full_intersection)

intersections = {}
for ncomb in range(2, len(names) )[::-1]:
    for items in itertools.combinations(evt_dict.items(), ncomb):
        names = tuple([i[0] for i in items])
        inter = reduce(intersect, [i[1] for i in items])
        #remove double counting
        inter = inter.difference(full_intersection)
        inter_diff = reduce(lambda x,y: x.union(y), [value for key, value in intersections.iteritems() if all(name in key for name in names)], set()) 
        inter = inter.difference(inter_diff)
        #save region
        intersections[names] = inter
        if args.dump:
            dump(region+'_AND_'.join(names)+'.txt', inter)
        print ' & '.join(names)+': %i' % len(inter)

for name, evtset in evt_dict.iteritems():
    size = evtset.difference(full_intersection)
    inter_union = reduce(lambda x,y: x.union(y), [value for key, value in intersections.iteritems() if name in key], set())     
    size = size.difference( inter_union )
    print '%s only: %i' % (name, len(size))
    if args.dump:
        dump('%s_%s_only.txt' % (region, name), size)



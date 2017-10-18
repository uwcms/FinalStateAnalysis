#! /bin/env python

import os
import sys
import glob

BLUE  = lambda x: '\033[94m%s\033[0m' % x
GREEN = lambda x: '\033[92m%s\033[0m' % x
RED   = lambda x: '\033[91m%s\033[0m' % x

def get_stars(ratio, space):
    return '*'*int(ratio*space)

if len(sys.argv) == 1:
    print 'Usage: condor_summary.py jobid'

jobid = sys.argv[-1]
user  = os.environ['USER']
term_rows, term_columns = os.popen('stty size', 'r').read().split()
term_columns = int(term_columns)

status_files = glob.glob('/nfs_scratch/%s/%s/*/dags/*.status' % (user, jobid))
max_name_lenght = max([len(i.split('/')[4]) for i in status_files])
print_format = ('%'+str(max_name_lenght)+'s%10s%10s%10s%10s%10s|')
header       = print_format % ('sample', 'jobs', 'done', 'errors', 'submitted', 'other')
remaining_space = term_columns - len(header)
print header
for status in status_files:
    sample= status.split('/')[4]
    lines = [i for i in open(status).readlines() if 'NodeStatus =' in i]
    done  = len([i for i in lines if 'STATUS_DONE' in i])
    err   = len([i for i in lines if 'STATUS_ERROR' in i])
    sub   = len([i for i in lines if 'STATUS_SUBMITTED' in i])
    tot   = len(lines)
    #print lines
    ratio_done = float(done) / float(tot)
    ratio_err  = float(err) / float(tot)
    ratio_sub  = float(sub) / float(tot)
    ratio_oth  = float(tot - done - err - sub) / float(tot)

    print print_format % (sample, tot, done, err, sub, tot-done-err-sub) \
        +get_stars(ratio_oth,remaining_space) \
        +BLUE(get_stars(ratio_sub,remaining_space)) \
        +GREEN(get_stars(ratio_done,remaining_space)) \
        +RED(get_stars(ratio_err,remaining_space))


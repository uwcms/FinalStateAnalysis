#!/usr/bin/env python

'''

Find the right data set name given the PrimDS and run number

Usage:
    findDataset.py primds run

'''

import sys
import FinalStateAnalysis.MetaData.datatools as datatools


if __name__ == "__main__":
    primds = sys.argv[1]
    run = int(sys.argv[2])
    dataname = datatools.find_data_for_run(run,primds)
    dataset = datatools.map_data_to_dataset(dataname)
    sys.stdout.write('%s %s\n' % (dataname, dataset))

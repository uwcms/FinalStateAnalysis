'''

Wrapper around the ZZ PU weights.

See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4l2012Summer#PU_Reweighting

Figures out whether to use 2011 or 2012 by the $jobid environment variable.

'''

import os
import ROOT
ROOT.gSystem.Load('PUWeighting_C')

if '7TeV' in os.environ['jobid']:
    pu_function = ROOT.weightTrue2011
else:
    pu_function = ROOT.weightTrue2012

def pu_weight(row):
    nPU = row.nTruePU
    if nPU > 0:
        return pu_function(nPU)
    else:
        return 1.0


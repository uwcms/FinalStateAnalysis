#!/usr/bin/env python

'''

Python to the HCSaW tool to query theory errors.

'''


import ROOT
import re

ROOT.gSystem.AddIncludePath('-IHCSaW/Higgs_CS_and_Width/include')
ROOT.gROOT.ProcessLine('.L HCSaW/Higgs_CS_and_Width/src/HiggsCSandWidth.cc+')

# Define the lookup tables
_sm = ROOT.HiggsCSandWidth();

def get_pdf_err_str(mass):
    return "%0.3f/%0.3f" % (1 + _sm.HiggsCSpdfErrMinus(3, mass, 7),
            1 + _sm.HiggsCSpdfErrPlus(3, mass, 7))

def get_scale_err_str(mass):
    return "%0.3f/%0.3f" % (1 + _sm.HiggsCSscaleErrMinus(3, mass, 7),
            1 + _sm.HiggsCSscaleErrPlus(3, mass, 7))

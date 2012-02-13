#!/usr/bin/env python

'''

Add FF and SM4 models


'''

import ROOT

ROOT.gSystem.AddIncludePath('-IHCSaW/Higgs_CS_and_Width_Fermiophobic/include')
ROOT.gSystem.AddIncludePath('-IHCSaW/Higgs_CS_and_Width/include')
ROOT.gSystem.AddIncludePath('-IHCSaW/Higgs_CS_and_Width_SM4/include')

ROOT.gROOT.ProcessLine('.L HCSaW/Higgs_CS_and_Width_SM4/src/HiggsCSandWidthSM4.cc+')
ROOT.gROOT.ProcessLine('.L HCSaW/Higgs_CS_and_Width/src/HiggsCSandWidth.cc+')
ROOT.gROOT.ProcessLine('.L HCSaW/Higgs_CS_and_Width_Fermiophobic/src/HiggsCSandWidthFermi.cc+')

# Define the lookup tables
_sm = ROOT.HiggsCSandWidth();
_ff = ROOT.HiggsCSandWidthFermi()
_sm4 = ROOT.HiggsCSandWidthSM4()

print _sm.HiggsWidth(10, 160)/_sm.HiggsWidth(0, 160)

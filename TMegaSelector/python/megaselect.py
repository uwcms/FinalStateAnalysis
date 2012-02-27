'''

Python interface to the TMegaPySelector class

'''

import ROOT

# Load this library
ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/'
                  'libFinalStateAnalysisTMegaSelector.so')

# Make the MegaPySelectorClass visible

from ROOT import TMegaPySelector

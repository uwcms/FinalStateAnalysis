'''

Python interface to the TMegaPySelector class

'''

import ROOT

# Load this library
ROOT.gSystem.Load('$CMSSW_BASE/lib/$SCRAM_ARCH/'
                  'libFinalStateAnalysisTMegaSelector.so')

# Make the MegaPySelectorClass visible
from ROOT import TMegaPySelector

class MegaPySelector(TMegaPySelector):

    def __init__(self):
        self.added_cuts = set([])

    def Version(self):
        return 2

    def make_cut(self, selection, branch, op, value):
        if not self.chain:
            raise RuntimeError(
                "You can't call make_cut before Init(...),"
                " the chain is not yet available")
        key = (selection, branch, op, value)
        if key in self.added_cuts:
            raise KeyError("Multiple attempts to add: %s" % ' '.join(key))
        self.added_cuts.add(key)
        tbranch = self.chain.GetBranch(branch)
        # Make sure the branch exists
        if not tbranch:
            raise NameError("The branch %s does not exist in the tree" % branch)
        type = tbranch.GetTitle().split("/")
        if type == "I":
            self.MakeIntCut(selection, branch, op, value)
        elif type == "F":
            self.MakeFloatCut(selection, branch, op, value)
        elif type == "D":
            self.MakeDoubleCut(selection, branch, op, value)
        else:
            raise TypeError("I can't figure out the type of the branch!"
                            " The title is: " + tbranch.GetTitle())

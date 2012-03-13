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
        self.histograms = {}

    def Version(self):
        return 2

    def book(self, directory, name, *args, **kwargs):
        ''' Book a root object

        The "directory" must be a tuple of strings.
        We do this dumb thing as the TProofOutputFile seems fraught with peril.

        The object can be retrived with:
            self.histograms[(directories, name)]

        The name of the object will be:
            '__'.join(key)

        The object will constructed using:

            type(name, *args).

        Type can be specified using a kwarg['type'].  Default is TH1F.

        The title can be specified using kwarg['title'].

        '''

        the_type = kwargs.get('type', ROOT.TH1F)

        if not isinstance(directory, tuple):
            directory = (directory,)

        key = directory + (name,)
        name = '__'.join(key)
        object = the_type(name, *args)
        self.histograms[key] = object
        return None

    def make_cut(self, selection, branch, op, value):
        # Currently broken
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

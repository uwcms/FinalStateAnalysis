'''

Example Ntuple Analyzer
=======================

A simple analyzer to make histograms using the "mega" script.
This analyzes Zmumu events.

An analyzer script has three main requirements:

 1. there is a class with the same name as the file
 2. that class inherits from the MegaBase class
 3. the class has the following methods
    * __init__(self, tree, outputfile, **kwargs)
    * begin(self) - initializing/booking histograms
    * process(self) - loop over the tree and fill the histograms
    * finish(self) - cleanup (optional)
    * the class must define the 'path/to/the/Ntuple' as the class variable
      'tree'

Author: Evan K. Friis, UW Madison

'''

# import the MegaBase class
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase

# Import various other code used by this module
# We need this because of the "type = ROOT.TH2F" below
import ROOT


# define our analyzer class - it must be called MyAnalyzer, since that is
# the name of this file.  It inherits from MegaBase.
class MyAnalyzer(MegaBase):
    # We have to define the path that the target ntuple can be found.
    tree = 'mm/final/Ntuple'

    def __init__(self, tree, outputfile, **kwargs):
        '''
        The __init__ method must take the following arguments:

        tree:       a ROOT TTree that will be processed.
        outputfile: a ROOT TFile (already open) to write output into
        **kwargs:   optionally extra keyword args can be passed (advanced)
        '''
        self.tree = tree  # need to keep a reference to this for later
        self.outputfile = outputfile

    def begin(self):
        ''' Let's book some histograms.

        Let's pretend we have two regions in our analysis,
        "signal" and "sideband."  We'll organize our histograms into
        directories accordingly.

        The histograms are available via a dictionary called "histograms".

        The keys of the dictionary are the full paths to the histograms.

        '''

        # MegaBase includes some convenience methods for booking histograms.
        # This books a 200 bin TH1F called "MyHistoName" into the "signal"
        # folder.
        self.book('signal', 'MyPtHistoName', 'p_{T}', 200, 0, 100)

        # How to make a 2D histo
        self.book('signal', 'PtVsEta', 'p_{T} vs. #eta',
                  200, 0, 100, 100, -2.5, 2.5, type=ROOT.TH2F)

        # In our sideband
        self.book('sideband', 'MyPtHistoName', 'p_{T}', 200, 0, 100)

    def process(self):
        ''' Our analysis logic. '''
        # Loop over the tree
        for row in self.tree:
            # you get variables by simple attribute access
            leg1_pt = row.m1Pt

            # Apply some simple kinematic cuts
            if leg1_pt < 20 or row.m2Pt < 10:
                continue

            dimuon_mass = row.m1_m2_Mass

            # Figure out if we are in the peak or the sideband
            if 80 < dimuon_mass < 110:
                # yes, the above syntax is correct, python is awesome
                self.histograms['signal/MyPtHistoName'].Fill(leg1_pt)
                self.histograms['signal/PtVsEta'].Fill(leg1_pt, row.m1Eta)
            else:
                # sideband
                self.histograms['sideband/MyPtHistoName'].Fill(leg1_pt)

    def finish(self):
        ''' You could do something here, but we don't need to. '''
        pass  # this means 'do nothing' in python

'''

Look at real TTH -> mutau + X events and plot some quantities.

'''

import MuTauTree
from FinalStateAnalysis.PlotTools.MegaBase import MegaBase
import os

class AnalyzeTTHSignal(MegaBase):
    tree = 'mt/final/Ntuple'
    def __init__(self, tree, outfile, **kwargs):
        super(AnalyzeTTHSignal, self).__init__(tree, outfile, **kwargs)
        # Use the cython wrapper
        self.tree = MuTauTree.MuTauTree(tree)
        self.out = outfile
        # Histograms for each category
        self.histograms = {}

    def begin(self):
        # Book some histograms
        self.book('tth', 'muonPt', 'Muon Pt', 100, 0, 100)
        self.book('tth', 'nBjetJets20', 'Number TCHE b-jets > 20', 10, -0.5, 9.5)
        self.book('tth', 'nCSVBjetJets20', 'Number CSV b-jets > 20', 10, -0.5, 9.5)
        self.book('tth', 'nJets20', 'Number jets > 20', 10, -0.5, 9.5)
        self.book('tth', 'nJets40', 'Number jets > 40', 10, -0.5, 9.5)


    def process(self):
        # loop over events
        for event in self.tree:
            # Skip event if a cut fails
            # PT cut
            # Select only gg->ttH and qq->ttH processes
            if event.processID < 100:
                continue
            if event.mPt < 15:
                continue
            if event.tPt < 20:
                continue
            # Check if we pass some ID + Iso cuts
            if not event.mPFIDTight:
                continue
            if event.mRelPFIsoDB > 0.2:
                continue
            # Tau ID
            if not event.tLooseMVAIso:
                continue
            # Now plot some quantities
            self.histograms['tth/muonPt'].Fill(event.mPt)
            # How many jets are in the event
            self.histograms['tth/nJets20'].Fill(event.jetVeto20)
            self.histograms['tth/nJets40'].Fill(event.jetVeto40)
            self.histograms['tth/nBjetJets20'].Fill(event.bjetVeto)
            self.histograms['tth/nCSVBjetJets20'].Fill(event.bjetCSVVeto)


    def finish(self):
        self.write_histos()

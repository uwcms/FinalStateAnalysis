'''

Base class for analyzers.

Defines regions, a set of selections.  For each region, there is a set of
histograms.

'''

from FinalStateAnalysis.TMegaSelector.MegaBase import MegaBase
import os

class Analyzer(MegaBase):
    def __init__(self, tree, output, **kwargs):
        super(Analyzer, self).__init__(tree, output, **kwargs)
        self.regions = {}

    def define_region(self, region_name, selection, histograms):
        # Book the histograms
        booked_histograms = []
        for getter, weight, folder, ctor in histograms:
            # Book the histogram in region/desired/path/
            histo = self.book(os.path.normpath(region_name + '/' +  folder), *ctor)
            booked_histograms.append((getter, weight, histo))
        self.regions[region_name] = (selection, booked_histograms)

    def analyze(self, tree):
        for region, (selection, histograms) in self.regions.iteritems():
            # Check if it passes the selection
            if not selection(tree):
                continue
            # It passed, fill the histograms
            for histogram in histograms:
                # Unpack
                getter, weight, histo = histogram
                histo.Fill(getter(tree), weight(tree))

import ROOT
import os

class DataReader(object):
    allowed_regions = [
        'wjets', 'qcd', 'sigFail', 'sigPass'
    ]

    def __init__(self, name, filename, title):
        self.name = name
        self.filename = filename
        if filename:
            self.file = ROOT.TFile(filename, "READ")
        self.title = title
        self.owned = []
        self.local_copies = {}

    def th1(self, region, sign, variable_name, rebin=1):
        histo_name = os.path.join(
            'ohyeah', ''.join([region, sign]), variable_name)

        key = (histo_name, rebin)
        if key not in self.local_copies:
            histogram = self.file.Get(histo_name)
            if not histogram:
                raise ValueError("Couldn't get histogram: %s" % histo_name)
            owned_histo = histogram.Clone()
            owned_histo.Rebin(rebin)
            self.local_copies[key] = owned_histo
        return self.local_copies[key]

    def dataHist(self, region, sign, variable, rebin=1):
        histogram = self.th1(region, sign, variable.GetName(), rebin)
        datahist = ROOT.RooDataHist(
            self.name, " ".join([self.title, region, sign]),
            ROOT.RooArgList(variable), histogram)
        return datahist

    def histPdf(self, region, sign, variable, rebin=1):
        dataHist = self.dataHist(region, sign, variable, rebin)
        self.owned.append(dataHist)
        return ROOT.RooHistPdf(
            self.name, " ".join([self.title, region, sign]),
            ROOT.RooArgSet(variable), dataHist)

    def __hash__(self):
        return hash(self.name)

'''
TNPFitter
=========

Author: Evan K. Friis, UW Madison

A class which performs Tag and Probe fits by making selections on an input tree.

The constructor takes a TTree/Chain and list of RooRealVars.

A given region can be fitted using the [fit] method.

    def fit(self, xaxis, base_sel, pass_sel, fail_sel, pdfs,
            init_eff = 0.9, init_signal_fraction = 0.9):

The xaxis is the dependent variable (i.e. dimuon mass).  The base_sel is a list
TTree cuts ([ 'Mu1Pt > 10', 'Mu1Iso < 0.3' ] etc) which defines the denominator.
The [pass_sel] and [fail_sel] arguments are cuts applied on top of this to
select the passing and failing regions.  NB the pass and fail cuts be exclusive!

The [pdfs] parameter is a list of arguments to be passed to a RooWorkspace
factory.  They must define the following PDFs:

    signalPass, signalFail, backgroundPass, backgroundFail

Example:
    pdf = [
        "Voigtian::signalPass(finalStateVisP4Mass, mean[90,80,100], "
            "width[2.495], sigma[3,1,20])",
        "Voigtian::signalFail(finalStateVisP4Mass, mean, width, sigma)",
        "Exponential::backgroundPass(finalStateVisP4Mass, lp[0,-5,5])",
        "Exponential::backgroundFail(finalStateVisP4Mass, lf[0,-5,5])",
    ]


The [fit_trend] method automatically does fits in a set of binned regions of
another variable.

'''

import hashlib
import logging

import ROOT
from FinalStateAnalysis.Utilities.Histo import Histo

def importer(ws, obj):
    # Workaround to allow use of reserved word
    getattr(ws, 'import')(obj)

def _eff_and_errors(passing, failing):
    num = ROOT.TH1F("temp_num", "temp", 1, -0.5, 0.5)
    den = ROOT.TH1F("temp_den", "temp", 1, -0.5, 0.5)
    num.SetBinContent(1, passing)
    den.SetBinContent(1, passing + failing)
    tgraph = ROOT.TGraphAsymmErrors(num, den)
    return (tgraph.GetY()[0], tgraph.GetEYhigh()[0], tgraph.GetEYlow()[0])

def _total_weight(weight_dist):
    """ Get the total weight of the sample given the weight distribution """
    # Use our handy utility
    output = 0
    weight_histo = Histo(weight_dist)
    for bin in weight_histo.bins():
        weight = bin.center()
        entries = bin.value()
        output += weight * entries
    return output

class TNPFitter(object):
    log = logging.getLogger("TNPFitter")
    def __init__(self, tree, vars):
        print self.log
        self.vars = vars
        self.log.info("Constructing RooDataSet using vars: %s", vars)
        argset = ROOT.RooArgSet()
        for var in vars:
            argset.add(var)
        data = ROOT.RooDataSet("data", "TNP Data", tree, argset)
        self.ws = ROOT.RooWorkspace()
        self.log.info("Import dataset into persistent workspace")
        self.imp(data)

    def imp(self, object):
        getattr(self.ws, 'import')(object)

    def selection_key(self, selections):
        # Define a hash key for a set of selections
        md5 = hashlib.md5()
        for select in selections:
            md5.update(select)
        return md5.hexdigest()

    def reduce_data(self, selections):
        # TODO make this smarter
        key = self.selection_key(selections)
        self.log.info("Reducing data using %i selections. key: %s",
                      len(selections), key)
        # Try and get the reduced data
        cached = self.ws.data(key)
        if cached:
            return cached

        reduced = self.ws.data('data').reduce(' && '.join(selections))
        reduced.SetName(key)
        self.imp(reduced)
        return self.ws.data(key)

    def fit_trend(self, bin_var, bins, xaxis, base_sel, pass_sel,
                  fail_sel, pdfs, init_eff = 0.9,
                  init_signal_fraction = 0.9):
        results = []
        # Run over pairs of cuts
        for i, (start, end) in enumerate(zip(bins[:-1], bins[1:])):
            print start, end
            full_sel = base_sel + ['%s > %0.3f' % (bin_var, start),
                                   '%s <= %0.3f' % (bin_var, end)]
            ws, fit_result = self.fit(
                xaxis, full_sel, pass_sel, fail_sel, pdfs, init_eff,
                init_signal_fraction)
            efficiency = fit_result.floatParsFinal().find('efficiency')
            results.append((start, end, ws, fit_result, efficiency))
        return results

    def mc_trend(self, bin_var, bins, xaxis, weight,
                 truth_sel, base_sel, pass_sel, fail_sel):
        # Weight is a RooArgList of a single weight variable
        results = []
        # Run over pairs of cuts
        for i, (start, end) in enumerate(zip(bins[:-1], bins[1:])):
            print start, end
            full_sel = truth_sel + base_sel + [
                '%s > %0.3f' % (bin_var, start),
                '%s <= %0.3f' % (bin_var, end)
            ]
            # We need to compute the total number of passing/failing entries
            # with the PU weights
            pass_data = self.reduce_data(full_sel + pass_sel)
            fail_data = self.reduce_data(full_sel + fail_sel)
            pass_weighted = ROOT.TH1F("pass_weights", "pass_weights", 100, 0, 2)
            fail_weighted = ROOT.TH1F("fail_weights", "fail_weights", 100, 0, 2)

            pass_data.fillHistogram(pass_weighted, weight)
            passing_weighted = _total_weight(pass_weighted)
            fail_data.fillHistogram(fail_weighted, weight)
            failing_weighted = _total_weight(fail_weighted)

            class FakeEfficiency(object):
                def __init__(self, passing, failing):
                    self.eff, self.errUp, self.errDown = _eff_and_errors(
                        passing, failing)
                def getVal(self):
                    return self.eff
                def getErrorLo(self):
                    return self.errDown*-1
                def getErrorHi(self):
                    return self.errUp

            results.append((start, end, None, None,
                            FakeEfficiency(passing_weighted, failing_weighted)))
        return results

    @staticmethod
    def make_trend_graph(results):
        ''' Parse the results from fit_trend and make a TGraph.  '''
        output = ROOT.TGraphAsymmErrors(len(results))
        for i, (start, end, ws, fit_result, efficiency) in enumerate(results):
            bin_width = end-start
            middle =  bin_width*0.5 + start
            output.SetPoint(i, middle, efficiency.getVal())
            output.SetPointEXlow(i, 0.5*bin_width)
            output.SetPointEXhigh(i, 0.5*bin_width)
            output.SetPointEYhigh(i, efficiency.getErrorHi())
            output.SetPointEYlow(i, -1*efficiency.getErrorLo())
        return output

    @staticmethod
    def fit_trend_graph(graph):
        ''' Fit a trend to an error function '''
        fit_func = ROOT.TF1(
            "fit_func", "[0]*0.5*(1 + TMath::Erf([2]*(x - [1])))", 2)
        fit_func.SetParameter(0, graph.GetMaximum())
        fit_func.SetParLimits(0, 0, 1)
        # Find turnon
        before_turnon = graph.GetXaxis().GetXmin()
        after_turnon = graph.GetXaxis().GetXmax()
        # Find maximum
        graph_max = 0
        for i in xrange(graph.GetN()):
            x = graph.GetXaxis().GetBinCenter(i)
            y = graph.Eval(x)
            if y > graph_max:
                graph_max = y

        print before_turnon, after_turnon, graph_max
        for i in xrange(graph.GetN()):
            x = graph.GetXaxis().GetBinCenter(i)
            y = graph.Eval(x)
            print x, y, before_turnon, after_turnon, graph_max
            if y < 0.1*graph_max and x > before_turnon:
                before_turnon = x
            if y > 0.9*graph_max and x < after_turnon:
                after_turnon = x

        fit_func.SetParameter(
            1, 0.5*(after_turnon - before_turnon) + before_turnon)
        fit_func.SetParLimits(1, 0, 200)
        fit_func.SetParameter(2, 3)
        fit_func.SetParLimits(2, 0.01, 50)
        graph.Fit(fit_func)
        return fit_func

    def fit(self, xaxis, base_sel, pass_sel, fail_sel, pdfs,
            init_eff = 0.9, init_signal_fraction = 0.9):
        # you must define, signalPass, signalFail, backgroundPass,
        # backgroundFail PDF.
        pass_data = self.reduce_data(base_sel + pass_sel)
        fail_data = self.reduce_data(base_sel + fail_sel)
        n_passed = pass_data.numEntries()
        n_fail = fail_data.numEntries()
        # Make yield guesses
        n_all_signal = init_signal_fraction * (n_passed + n_fail)
        n_bkg_pass = n_passed*(1 - init_signal_fraction)
        n_bkg_fail = n_fail*(1-init_signal_fraction)

        # Bin the pass and fail samples
        pass_data_to_fit = ROOT.RooDataHist(
            "pass_binned", "pass_binned", ROOT.RooArgSet(xaxis), pass_data)
        fail_data_to_fit = ROOT.RooDataHist(
            "fail_binned", "fail_binned", ROOT.RooArgSet(xaxis), fail_data)
        #pass_data_to_fit = pass_data
        #fail_data_to_fit = fail_data

        temp_ws = ROOT.RooWorkspace()
        importer(temp_ws, xaxis)

        for pdf_command in pdfs:
            self.log.info("Running factory command %s", pdf_command)
            temp_ws.factory(pdf_command)

        # Define efficiency
        self.log.info("Defining efficiency @ %0.2f", init_eff)
        temp_ws.factory("efficiency[%0.3f, 0, 1]" % init_eff)
        self.log.info("Defining signal frac @ %0.2f", init_signal_fraction)
        self.log.info("Initial signal %i", n_all_signal)
        self.log.info("Initial bkg pass %i", n_bkg_pass)
        self.log.info("Initial bkg fail %i", n_bkg_fail)

        temp_ws.factory(
            "expr::numSignalPass('efficiency*numSignalAll',"
            "efficiency, numSignalAll[%i, 0.,1e10])" % n_all_signal);
        temp_ws.factory(
            "expr::numSignalFail('(1-efficiency)*numSignalAll',"
            "efficiency, numSignalAll)");

        temp_ws.factory(
            "SUM::pdfPass(numSignalPass*signalPass,"
            "numBackgroundPass[%i, 0, 1e10]*backgroundPass)" % n_bkg_pass)

        temp_ws.factory(
            "SUM::pdfFail(numSignalFail*signalFail,"
            "numBackgroundFail[%i, 0, 1e10]*backgroundFail)" % n_bkg_fail)

        importer(temp_ws, pass_data_to_fit)
        importer(temp_ws, fail_data_to_fit)

        pdf_pass = temp_ws.pdf('pdfPass')
        pdf_fail = temp_ws.pdf('pdfFail')
        #pdf_pass.Print('v')
        #pdf_fail.Print('v')
        options = ROOT.RooLinkedList()
        options.Add(ROOT.RooFit.Extended(True))
        nlls = []
        nlls.append(pdf_pass.createNLL(pass_data_to_fit, options))
        nlls.append(pdf_fail.createNLL(fail_data_to_fit, options))
        full_nll = ROOT.RooAddition("nll", "nll", ROOT.RooArgSet(*nlls))

        minuit = ROOT.RooMinuit(full_nll)
        minuit.setErrorLevel(1);
        minuit.setNoWarn();
        minuit.setPrintEvalErrors(0);
        minuit.setPrintLevel(0);
        minuit.setWarnLevel(3);
        minuit.migrad();
        minuit.hesse();
        minuit.hesse();
        result = minuit.save()
        #result.Print("v")
        return temp_ws, result


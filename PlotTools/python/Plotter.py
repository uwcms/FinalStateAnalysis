'''

Base class which makes nice plots.

Author: Evan K. Friis, UW

'''

import fnmatch
import os
import rootpy.plotting.views as views
import rootpy.plotting as plotting
from FinalStateAnalysis.MetaData.data_views import data_views
import ROOT

_original_draw = plotting.Legend.Draw
# Make legends not have crappy border
def _monkey_patch_legend_draw(self, *args, **kwargs):
    ''' Make a plotting.legend look nice '''
    self.SetBorderSize(0)
    _original_draw(self, *args, **kwargs)
plotting.Legend.Draw = _monkey_patch_legend_draw

class Plotter(object):
    def __init__(self, files, lumifiles, outputdir, blinder=None):
        ''' Initialize the Plotter object

        Files should be a list of SAMPLE_NAME.root files.
        Lumifiles should contain floats giving the effective luminosity of
        each of the files.

        If [blinder] is not None, it will be applied to the data view.
        '''
        self.outputdir = outputdir
        self.views = data_views(files, lumifiles)
        self.canvas = plotting.Canvas(name='adsf', title='asdf')
        self.canvas.cd()
        if blinder:
            # Keep the unblinded data around if desired.
            self.views['data']['unblinded_view'] = self.views['data']['view']
            # Apply a blinding function
            self.views['data']['view'] = blinder(self.views['data']['view'])
        self.data = self.views['data']['view']
        self.keep = []
        # List of MC sample names to use.  Can be overridden.
        self.mc_samples = [
            'Zjets_M50',
            'WplusJets_madgraph',
            'TTplusJets_madgraph',
            'WZJetsTo3LNu*',
            'ZZJetsTo4L*',
            'WW*',
        ]

    @staticmethod
    def rebin_view(x, rebin):
        ''' Make a view which rebins histograms '''
        rebinner = lambda x: x.Rebin(rebin)
        output = views.FunctorView(x, rebinner)
        return output

    def get_view(self, sample_pattern, key_name='view'):
        ''' Get a view which matches a pattern like "Zjets*"

        Generally key_name does not need to be modified, unless getting
        unblinded data via "unblinded_view"

        '''
        for sample, sample_info in self.views.iteritems():
            if fnmatch.fnmatch(sample, sample_pattern):
                return sample_info[key_name]
        raise KeyError("I can't find a view that matches %s, I have: %s" % (
            sample_pattern, " ".join(self.views.keys())))

    def make_stack(self, rebin=1):
        ''' Make a stack of the MC histograms '''
        all_mc_stack = views.StackView(
            *[self.rebin_view(self.get_view(x), rebin) for x in self.mc_samples]
        )
        return all_mc_stack

    def add_legend(self, samples, leftside=True, entries=None):
        ''' Build a legend using samples.

        If entries is None it will be taken from len(samples)

        '''
        nentries = entries if entries is not None else len(samples)
        legend = None
        if leftside:
            legend = plotting.Legend(nentries, leftmargin=0.03, topmargin=0.05, rightmargin=0.65)
        else:
            legend = plotting.Legend(nentries, rightmargin=0.07, topmargin=0.05, leftmargin=0.45)
        for sample in samples:
            legend.AddEntry(sample)
        legend.SetEntrySeparation(0.0)
        legend.SetMargin(0.35)
        legend.Draw()
        self.keep.append(legend)
        return legend

    def add_cms_blurb(self, sqrts, preliminary=True):
        ''' Add the CMS blurb '''
        latex = ROOT.TLatex()
        latex.SetNDC();
        latex.SetTextSize(0.04);
        latex.SetTextAlign(31);
        latex.SetTextAlign(11);
        label_text = "CMS"
        if preliminary:
            label_text += " Preliminary"
        label_text += " %i TeV" % sqrts
        label_text += " %0.1f fb^{-1}" % (self.views['data']['intlumi']/1000.)
        self.keep.append(latex.DrawLatex(0.18,0.96, label_text));

    def save(self, filename):
        ''' Save the current canvas contents to [filename] '''
        self.canvas.Update()
        if not os.path.exists(self.outputdir):
            os.makedirs(self.outputdir)
        self.canvas.SaveAs(os.path.join(self.outputdir, filename) + '.png')
        self.canvas.SaveAs(os.path.join(self.outputdir, filename) + '.pdf')
        # Reset keeps
        self.keep = []

    def plot(self, sample, path, drawopt='', rebin=None, styler=None, xaxis='', xrange=None):
        ''' Plot a single histogram from a single sample.

        Returns a reference to the histogram.

        '''
        view = self.views[sample]['view']
        if rebin:
            view = self.rebin_view(view, rebin)
        histo = view.Get(path)
        if xrange:
            histo.GetXaxis().SetRange(xrange[0], xrange[1])
        if styler:
            styler(histo)
        histo.Draw(drawopt)
        histo.GetXaxis().SetTitle(xaxis)
        self.keep.append(histo)
        return histo

    def compare_shapes(self, sample1, sample2, path, rebin=None):
        ''' Compare the spectra from two different samples '''
        view1 = views.NormalizeView(self.views[sample1]['view'])
        if rebin:
            view1 = self.rebin_view(view1, rebin)
        histo1 = view1.Get(path)
        view2 = views.NormalizeView(self.views[sample2]['view'])
        if rebin:
            view2 = self.rebin_view(view2, rebin)
        histo2 = view2.Get(path)
        histo1.Draw('pe')
        histo2.SetMarkerColor(ROOT.EColor.kRed)
        histo2.Draw('pe,same')
        histo1.SetMaximum(
            1.2*max(histo1.GetMaximum(), histo2.GetMaximum()))
        self.keep.append( (histo1, histo2) )

    def plot_mc_vs_data(self, folder, variable, rebin=1, xaxis='',
                        leftside=True, xrange=None):
        ''' Compare Monte Carlo to data '''
        path = os.path.join(folder, variable)
        mc_stack = self.make_stack(rebin).Get(path)
        mc_stack.Draw()
        mc_stack.GetHistogram().GetXaxis().SetTitle(xaxis)
        if xrange:
            mc_stack.GetXaxis().SetRange(xrange[0], xrange[1])
            mc_stack.Draw()
        self.keep.append(mc_stack)
        # Draw data
        data = self.rebin_view(self.data, rebin).Get(path)
        data.Draw('same')
        self.keep.append(data)
        # Make sure we can see everything
        if data.GetMaximum() > mc_stack.GetMaximum():
            mc_stack.SetMaximum(1.2*data.GetMaximum())
        # Add legend
        self.add_legend([data, mc_stack], leftside, entries=5)

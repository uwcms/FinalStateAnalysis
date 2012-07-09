'''

Base class to do WH plotting.

Author: Evan K. Friis, UW

Takes as input a set of ROOT [files] with analysis histgrams, and the corresponding
lumicalc.sum [lumifiles] that hve the effective lumi for each sample.

If [blind] is true, data in the p1p2p3 region will not be plotted.

'''

import fnmatch
import os
import rootpy.plotting.views as views
import rootpy.plotting as plotting
from FinalStateAnalysis.MetaData.data_views import data_views
from FinalStateAnalysis.MetaData.data_styles import data_styles
from FinalStateAnalysis.PlotTools.BlindView import BlindView
import ROOT

original_draw = plotting.Legend.Draw
# Make legends not have crappy border
def monkey_patch_legend_draw(self, *args, **kwargs):
    ''' Make a plotting.legend look nice '''
    self.SetBorderSize(0)
    original_draw(self, *args, **kwargs)
plotting.Legend.Draw = monkey_patch_legend_draw

def rebin_view(x, rebin):
    ''' Make a view which rebins histograms '''
    rebinner = lambda x: x.Rebin(rebin)
    output = views.FunctorView(x, rebinner)
    return output

class WHPlotterBase(object):
    def __init__(self, files, lumifiles, outputdir, blind=True):
        self.outputdir = outputdir
        self.views = data_views(files, lumifiles)
        self.canvas = plotting.Canvas(name='adsf', title='asdf')
        self.canvas.cd()
        if blind:
            # Don't look at the SS all pass region
            self.views['data']['view'] = BlindView(
                self.views['data']['view'], "ss/p1p2p3/.*")
        self.data = self.views['data']['view']
        self.keep = []

    def get_view(self, sample_pattern):
        for sample, sample_info in self.views.iteritems():
            if fnmatch.fnmatch(sample, sample_pattern):
                return sample_info['view']
        raise KeyError("I can't find a view that matches %s, I have: %s" % (
            sample_pattern, " ".join(self.views.keys())))

    def make_stack(self, rebin=1):
        ''' Make a stack of the MC histograms '''
        all_mc_stack = views.StackView(
            rebin_view(self.get_view('Zjets_M50'), rebin),
            rebin_view(self.get_view('WplusJets_madgraph'), rebin),
            rebin_view(self.get_view('TTplusJets_madgraph'), rebin),
            rebin_view(self.get_view('WZJetsTo3LNu*'), rebin),
            rebin_view(self.get_view('ZZJetsTo4L*'), rebin),
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

    def add_cms_blurb(self, sqrts, preliminary=True):
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
            view = rebin_view(view, rebin)
        histo = view.Get(path)
        if xrange:
            histo.GetXaxis().SetRange(xrange[0], xrange[1])
        if styler:
            styler(histo)
        histo.Draw(drawopt)
        histo.GetXaxis().SetTitle(xaxis)
        self.keep.append(histo)
        return histo

    def plot_mc_vs_data(self, folder, variable, rebin=1, xaxis='',
                        leftside=True, xrange=None):
        path = os.path.join(folder, variable)
        mc_stack = self.make_stack(rebin).Get(path)
        mc_stack.Draw()
        mc_stack.GetHistogram().GetXaxis().SetTitle(xaxis)
        if xrange:
            mc_stack.GetXaxis().SetRange(xrange[0], xrange[1])
            mc_stack.Draw()
        self.keep.append(mc_stack)
        # Draw data
        data = rebin_view(self.data, rebin).Get(path)
        data.Draw('same')
        self.keep.append(data)
        # Make sure we can see everything
        if data.GetMaximum() > mc_stack.GetHistogram().GetMaximum():
            mc_stack.SetMaximum(2*data.GetMaximum())
        # Add legend
        self.add_legend([data, mc_stack], leftside, entries=5)

    def make_signal_views(self, rebin):
        ''' Make signal views with FR background estimation '''

        vh120_view = views.SubdirectoryView(
            rebin_view(self.get_view('VH_*120'), rebin),
            'ss/p1p2p3/'
        )
        wz_view = views.SubdirectoryView(
            rebin_view(self.get_view('WZJetsTo3LNu*'), rebin),
            'ss/p1p2p3/'
        )
        zz_view = views.SubdirectoryView(
            rebin_view(self.get_view('ZZJetsTo4L*'), rebin),
            'ss/p1p2p3/'
        )
        all_data_view = rebin_view(self.get_view('data'), rebin)
        data_view = views.SubdirectoryView(all_data_view, 'ss/p1p2p3/')

        # View of weighted obj1-fails data
        obj1_view = views.SubdirectoryView(all_data_view, 'ss/f1p2p3/w1')
        # View of weighted obj2-fails data
        obj2_view = views.SubdirectoryView(all_data_view, 'ss/p1f2p3/w2')
        # View of weighted obj1&2-fails data
        obj12_view = views.SubdirectoryView(all_data_view, 'ss/f1f2p3/w12')

        subtract_obj12_view = views.ScaleView(obj12_view, -1)
        # Corrected fake view
        fakes_view = views.SumView(obj1_view, obj2_view, subtract_obj12_view)
        fakes_view = views.TitleView(
            views.StyleView(fakes_view, **data_styles['Zjets*']), 'Non-prompt bkg.')

        output = {
            'vh120' : vh120_view,
            'wz' : wz_view,
            'zz' : zz_view,
            'data' : data_view,
            'obj1' : obj1_view,
            'obj2' : obj2_view,
            'fakes' : fakes_view
        }

        return output

    def write_shapes(self, variable, rebin, outdir):
        ''' Write final shape histos for [variable] into a TDirectory [outputdir] '''
        sig_view = self.make_signal_views(rebin)
        outdir.cd()
        wz = sig_view['wz'].Get(variable)
        zz = sig_view['zz'].Get(variable)
        obs = sig_view['data'].Get(variable)
        fakes = sig_view['fakes'].Get(variable)
        vh120 = sig_view['vh120'].Get(variable)

        wz.SetName('wz')
        zz.SetName('zz')
        obs.SetName('data_obs')
        fakes.SetName('fakes')
        vh120.SetName('VH120')

        wz.Write()
        zz.Write()
        obs.Write()
        fakes.Write()
        vh120.Write()

    def plot_final(self, variable, rebin=1, xaxis='', maxy=10):
        ''' Plot the final output - with bkg. estimation '''
        sig_view = self.make_signal_views(rebin)
        vh_10x = views.TitleView(
            views.ScaleView(sig_view['vh120'], 5),
            "(5#times) m_{H} = 120"
        )

        stack = views.StackView(
            sig_view['wz'],
            sig_view['zz'],
            sig_view['fakes'],
            vh_10x,
        )
        histo = stack.Get(variable)
        histo.Draw()
        histo.GetHistogram().GetXaxis().SetTitle(xaxis)
        histo.SetMaximum(maxy)
        self.keep.append(histo)

        # Add legend
        self.add_legend(histo, leftside=False, entries=4)

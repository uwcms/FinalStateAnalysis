'''

Base class to do WH plotting.

Author: Evan K. Friis, UW

Takes as input a set of ROOT [files] with analysis histgrams, and the corresponding
lumicalc.sum [lumifiles] that hve the effective lumi for each sample.

If [blind] is true, data in the p1p2p3 region will not be plotted.

'''

import os
import rootpy.plotting.views as views
import rootpy.plotting as plotting
from FinalStateAnalysis.MetaData.data_views import data_views
from FinalStateAnalysis.MetaData.data_styles import data_styles
from FinalStateAnalysis.PlotTools.BlindView import BlindView


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

    def make_stack(self, rebin=1):
        ''' Make a stack of the MC histograms '''
        all_mc_stack = views.StackView(
            rebin_view(self.views['Zjets_M50']['view'], rebin),
            rebin_view(self.views['WplusJets_madgraph']['view'], rebin),
            rebin_view(self.views['TTplusJets_madgraph']['view'], rebin),
            rebin_view(self.views['WZJetsTo3LNu']['view'], rebin),
            rebin_view(self.views['ZZJetsTo4L_pythia']['view'], rebin),
        )
        return all_mc_stack


    def save(self, filename):
        self.canvas.SaveAs(os.path.join(self.outputdir, filename) + '.png')
        # Reset keeps
        self.keep = []

    # Plot a single sample
    def plot(self, sample, path, drawopt='', styler=None, xaxis=''):

        view = self.views[sample]['view']
        histo = view.Get(path)
        if styler:
            styler(histo)
        histo.Draw(drawopt)
        histo.GetXaxis().SetTitle(xaxis)
        self.keep.append(histo)
        return True

    def plot_mc_vs_data(self, folder, variable, rebin=1, xaxis=''):
        path = os.path.join(folder, variable)
        mc_stack = self.make_stack(rebin).Get(path)
        data = rebin_view(self.data, rebin).Get(path)
        mc_stack.Draw()
        mc_stack.GetXaxis().SetTitle(xaxis)
        self.keep.append(mc_stack)
        data.Draw('same')
        self.keep.append(data)

    def make_signal_views(self, rebin):
        ''' Make signal views with FR background estimation '''

        vh120_view = views.SubdirectoryView(
            rebin_view(self.views['VH_120']['view'], rebin),
            'ss/p1p2p3/'
        )
        wz_view = views.SubdirectoryView(
            rebin_view(self.views['WZJetsTo3LNu']['view'], rebin),
            'ss/p1p2p3/'
        )
        zz_view = views.SubdirectoryView(
            rebin_view(self.views['ZZJetsTo4L_pythia']['view'], rebin),
            'ss/p1p2p3/'
        )
        all_data_view = rebin_view(self.views['data']['view'], rebin)
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
            views.StyleView(fakes_view, **data_styles['Zjets*']), 'fakes')

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
        vh120.SetName('VH')

        wz.Write()
        zz.Write()
        obs.Write()
        fakes.Write()
        vh120.Write()

    def plot_final(self, variable, rebin=1, xaxis=''):
        sig_view = self.make_signal_views(rebin)
        stack = views.StackView(
            sig_view['wz'],
            sig_view['zz'],
            sig_view['fakes'],
        )
        histo = stack.Get(variable)
        histo.Draw()
        histo.GetXaxis().SetTitle(xaxis)
        self.keep.append(histo)

        sig_histo = sig_view['vh120'].Get(variable)
        sig_histo.Draw('same')
        self.keep.append(sig_histo)

        # Add legend
        legend = plotting.Legend(4, leftmargin=0.65)
        legend.AddEntry(histo)
        legend.AddEntry(sig_histo)
        legend.Draw()

        self.keep.append(legend)

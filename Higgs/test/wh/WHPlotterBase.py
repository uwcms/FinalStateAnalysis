'''

Base class to do WH plotting.

Author: Evan K. Friis, UW

Takes as input a set of ROOT [files] with analysis histgrams, and the corresponding
lumicalc.sum [lumifiles] that hve the effective lumi for each sample.

If [blind] is true, data in the p1p2p3 region will not be plotted.

'''

import rootpy.plotting.views as views
from FinalStateAnalysis.PlotTools.Plotter import Plotter
from FinalStateAnalysis.PlotTools.BlindView import BlindView
from FinalStateAnalysis.MetaData.data_styles import data_styles

class WHPlotterBase(Plotter):
    def __init__(self, files, lumifiles, outputdir, blind=True):
        blinder = None
        if blind:
            # Don't look at the SS all pass region
            blinder = lambda x: BlindView(x, "ss/p1p2p3/.*")
        super(WHPlotterBase, self).__init__(files, lumifiles, outputdir, blinder)

    def make_signal_views(self, rebin):
        ''' Make signal views with FR background estimation '''

        wz_view = views.SubdirectoryView(
            self.rebin_view(self.get_view('WZJetsTo3LNu*'), rebin),
            'ss/p1p2p3/'
        )
        zz_view = views.SubdirectoryView(
            self.rebin_view(self.get_view('ZZJetsTo4L*'), rebin),
            'ss/p1p2p3/'
        )
        all_data_view =self.rebin_view(self.get_view('data'), rebin)
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
            views.StyleView(fakes_view, **data_styles['Zjets*']), 'Non-prompt')

        charge_fakes = views.TitleView(
            views.StyleView(
                views.SubdirectoryView(all_data_view, 'os/p1p2p3/c1'),
                **data_styles['TT*']), 'Charge mis-id')

        output = {
            'wz' : wz_view,
            'zz' : zz_view,
            'data' : data_view,
            'obj1' : obj1_view,
            'obj2' : obj2_view,
            'fakes' : fakes_view,
            'charge_fakes' : charge_fakes,
        }

        # Add signal
        for mass in [110, 120, 130, 140]:
            vh_view = views.SubdirectoryView(
               self.rebin_view(self.get_view('VH_*%i' % mass), rebin),
                'ss/p1p2p3/'
            )
            output['vh%i' % mass] = vh_view

        return output

    def make_obj3_fail_cr_views(self, rebin):
        ''' Make views when obj3 fails, estimating the bkg in obj1 pass using
            f1p2f3 '''
        wz_view = views.SubdirectoryView(
           self.rebin_view(self.get_view('WZJetsTo3LNu*'), rebin),
            'ss/p1p2f3/'
        )
        zz_view = views.SubdirectoryView(
           self.rebin_view(self.get_view('ZZJetsTo4L*'), rebin),
            'ss/p1p2f3/'
        )
        all_data_view =self.rebin_view(self.get_view('data'), rebin)
        data_view = views.SubdirectoryView(all_data_view, 'ss/p1p2f3/')

        # View of weighted obj1-fails data
        obj1_view = views.SubdirectoryView(all_data_view, 'ss/f1p2f3/w1')
        # View of weighted obj2-fails data
        obj2_view = views.SubdirectoryView(all_data_view, 'ss/p1f2f3/w2')
        # View of weighted obj1&2-fails data
        obj12_view = views.SubdirectoryView(all_data_view, 'ss/f1f2f3/w12')

        subtract_obj12_view = views.ScaleView(obj12_view, -1)
        # Corrected fake view
        fakes_view = views.SumView(obj1_view, obj2_view, subtract_obj12_view)
        fakes_view = views.TitleView(
            views.StyleView(fakes_view, **data_styles['Zjets*']), 'Non-prompt')

        charge_fakes = views.TitleView(
            views.StyleView(
                views.SubdirectoryView(all_data_view, 'os/p1p2f3/c1'),
                **data_styles['TT*']), 'Charge mis-id')

        output = {
            'wz' : wz_view,
            'zz' : zz_view,
            'data' : data_view,
            'obj1' : obj1_view,
            'obj2' : obj2_view,
            'fakes' : fakes_view,
            'charge_fakes' : charge_fakes,
        }

        return output


    def make_wz_cr_views(self, rebin):
        ''' Make WZ control region views with FR background estimation '''

        wz_view = views.SubdirectoryView(
           self.rebin_view(self.get_view('WZJetsTo3LNu*'), rebin),
            'ss/p1p2p3_enhance_wz/'
        )
        zz_view = views.SubdirectoryView(
           self.rebin_view(self.get_view('ZZJetsTo4L*'), rebin),
            'ss/p1p2p3_enhance_wz/'
        )
        all_data_view =self.rebin_view(self.get_view('data'), rebin)
        data_view = views.SubdirectoryView(all_data_view, 'ss/p1p2p3_enhance_wz/')

        # View of weighted obj2-fails data
        fakes_view = views.SubdirectoryView(all_data_view, 'ss/p1f2p3_enhance_wz/w2')
        fakes_view = views.StyleView(fakes_view, **data_styles['Zjets*'])

        # Correct
        wz_in_fakes_view = views.SubdirectoryView(
           self.rebin_view(self.get_view('WZJetsTo3LNu*'), rebin),
            'ss/p1f2p3_enhance_wz/w2'
        )
        zz_in_fakes_view = views.SubdirectoryView(
           self.rebin_view(self.get_view('ZZJetsTo4L*'), rebin),
            'ss/p1f2p3_enhance_wz/w2'
        )

        diboson_view = views.SumView(wz_in_fakes_view, zz_in_fakes_view)
        inverted_diboson_view = views.ScaleView(diboson_view, -1)

        fakes_view = views.SumView(fakes_view, inverted_diboson_view)

        fakes_view = views.TitleView(fakes_view, 'Non-prompt')

        output = {
            'wz' : wz_view,
            'zz' : zz_view,
            'data' : data_view,
            'fakes' : fakes_view
        }

        # Add signal
        for mass in [110, 120, 130, 140]:
            vh_view = views.SubdirectoryView(
               self.rebin_view(self.get_view('VH_*%i' % mass), rebin),
                'ss/p1p2p3/'
            )
            output['vh%i' % mass] = vh_view

        return output

    def write_shapes(self, variable, rebin, outdir):
        ''' Write final shape histos for [variable] into a TDirectory [outputdir] '''
        sig_view = self.make_signal_views(rebin)
        outdir.cd()
        wz = sig_view['wz'].Get(variable)
        zz = sig_view['zz'].Get(variable)
        obs = sig_view['data'].Get(variable)
        fakes = sig_view['fakes'].Get(variable)

        wz.SetName('wz')
        zz.SetName('zz')
        obs.SetName('data_obs')
        fakes.SetName('fakes')

        for mass in [110, 120, 130, 140]:
            vh = sig_view['vh%i' % mass].Get(variable)
            vh.SetName('VH%i' % mass)
            vh.Write()

        wz.Write()
        zz.Write()
        obs.Write()
        fakes.Write()

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

    def plot_final_wz(self, variable, rebin=1, xaxis='', maxy=85):
        ''' Plot the final WZ control region - with bkg. estimation '''
        sig_view = self.make_wz_cr_views(rebin)

        stack = views.StackView(
            sig_view['fakes'],
            sig_view['wz'],
            sig_view['zz'],
        )
        histo = stack.Get(variable)
        histo.Draw()
        histo.GetHistogram().GetXaxis().SetTitle(xaxis)
        histo.SetMaximum(maxy)
        data = sig_view['data'].Get(variable)
        data.Draw('same')
        self.keep.append(data)
        self.keep.append(histo)

        # Add legend
        self.add_legend(histo, leftside=False, entries=4)

    def plot_final_f3(self, variable, rebin=1, xaxis='', maxy=None):
        ''' Plot the final F3 control region - with bkg. estimation '''
        sig_view = self.make_obj3_fail_cr_views(rebin)

        stack = views.StackView(
            sig_view['charge_fakes'],
            sig_view['fakes'],
            sig_view['wz'],
            sig_view['zz'],
        )
        histo = stack.Get(variable)
        histo.Draw()
        histo.GetHistogram().GetXaxis().SetTitle(xaxis)
        data = sig_view['data'].Get(variable)
        data.Draw('same')
        if maxy:
            histo.SetMaximum(maxy)
        else:
            histo.SetMaximum(
                1.2*max(histo.GetHistogram().GetMaximum(), data.GetMaximum()))
        self.keep.append(data)
        self.keep.append(histo)

        # Add legend
        self.add_legend(histo, leftside=False, entries=4)

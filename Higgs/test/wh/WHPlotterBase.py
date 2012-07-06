'''

Base class to do WH plotting.

'''

import os
import rootpy.plotting as plotting
from FinalStateAnalysis.MetaData.data_views import data_views

class WHPlotterBase(object):
    def __init__(self, files, lumifiles, outputdir):
        self.outputdir = outputdir
        self.views = data_views(files, lumifiles)
        self.canvas = plotting.Canvas(name='adsf', title='asdf')
        self.canvas.cd()
        self.all_mc_stack = plotting.views.StackView(
            self.views['Zjets_M50']['view'],
            self.views['WplusJets_madgraph']['view'],
            self.views['TTplusJets_madgraph']['view'],
            self.views['WZJetsTo3LNu']['view'],
            #self.views['ZZJetsTo4L_pythia']['view'],
        )
        self.data = self.views['data']['view']

    def save_plot(self, filename):
        self.canvas.SaveAs(os.path.join(self.outputdir, filename) + '.png')

    def plot_mc_vs_data(self, folder, variable, filename):
        path = os.path.join(folder, variable)
        mc_stack = self.all_mc_stack.Get(path)
        data = self.data.Get(path)
        print data.Integral()
        mc_stack.Draw()
        data.Draw('same')
        self.canvas.SaveAs(os.path.join(self.outputdir, filename) + '.png')
        #self.save_plot(filename)

    def make_plots(self):
        ''' Generic function to draw all plots '''
        pass
        #self.plot_mc_vs_data('

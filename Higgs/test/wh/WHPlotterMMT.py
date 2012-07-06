'''

Plot the MMT channel

'''

import glob
import logging
import WHPlotterBase
import sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class WHPlotterMMT(WHPlotterBase.WHPlotterBase):
    def __init__(self, files, lumifiles, outputdir):
        super(WHPlotterMMT, self).__init__(files, lumifiles, outputdir)

if __name__ == "__main__":
    jobid = '2012-07-04-7TeV-Higgs'
    samples = [
        'Zjets_M50', 'WplusJets_madgraph',
        'WZJetsTo3LNu',
        'TTplusJets_madgraph',
        "data_DoubleMu_Run2011A_05Aug2011_v1",
        "data_DoubleMu_Run2011A_May10ReReco_v1",
        "data_DoubleMu_Run2011A_PromptReco_v4",
        "data_DoubleMu_Run2011A_PromptReco_v6_1409"
    ]

    files = []
    lumifiles = []

    for x in samples:
        files.extend(glob.glob('results/%s/WHAnalyzeMMT/%s.root' % (jobid, x)))
        lumifiles.extend(glob.glob('inputs/%s/%s.lumicalc.sum' % (jobid, x)))

    plotter = WHPlotterMMT(files, lumifiles, 'results/plots/mmt')
    plotter.plot_mc_vs_data('os/p1p2f3', 'm1m2Mass')
    plotter.save('mcdata-os-p1p2f3-m1m2Mass')
    plotter.plot_mc_vs_data('os/p1p2f3/w3', 'm1m2Mass')
    plotter.save('mcdata-os-p1p2f3-w3-m1m2Mass')

    plotter.plot_mc_vs_data('os/p1f2p3', 'm1m2Mass')
    plotter.save('mcdata-os-p1f2p3-m1m2Mass')

    def make_styler(color):
        def unsuck(x):
            x.SetFillStyle(0)
            x.SetLineColor(color)
        return unsuck

    plotter.plot('data', 'os/p1p2f3/w3/m1m2Mass',  'hist', styler=make_styler(2))
    plotter.plot('data', 'os/p1p2p3/m1m2Mass', 'hist,same', styler=make_styler(1))
    plotter.save('zmm-os-fr-control')
    plotter.plot('Zjets_M50', 'os/p1p2f3/weight')
    plotter.save('zmm-mc-event-weights')

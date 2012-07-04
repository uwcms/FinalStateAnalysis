'''

Plot the MMT channel

'''

import WHPlotterBase

class WHPlotterMMT(WHPlotterBase.WHPlotterBase):
    def __init__(self, files, lumifiles, outputdir):
        super(WHPlotterMMT, self).__init__(files, lumifiles, outputdir)


if __name__ == "__main__":
    jobid = '2012-06-03-7TeV-Higgs'
    samples = [
        'Zjets_M50', 'WplusJets_madgraph',
        'WZJetsTo3LNu', 'TTplusJets_madgraph',
        "data_DoubleMu_Run2011A_05Aug2011_v1",
        "data_DoubleMu_Run2011A_May10ReReco_v1",
        "data_DoubleMu_Run2011A_PromptReco_v4",
        "data_DoubleMu_Run2011A_PromptReco_v6_1409"
    ]

    files = ['results/%s/WHAnalyzeMMT/%s.root' % (jobid, x) for x in samples]
    lumifiles = ['inputs/%s/%s.lumicalc.sum' % (jobid, x) for x in samples]

    plotter = WHPlotterMMT(files, lumifiles, 'plots/mmt')

    plotter.plot_mc_vs_data('os/p1f2p3', 'm1Pt', 'doot')

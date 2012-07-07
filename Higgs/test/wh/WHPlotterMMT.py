'''

Plot the MMT channel

Usage: python WHPlotterMMT.py

'''

import glob
import logging
import os
import ROOT
import sys
import WHPlotterBase

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

class WHPlotterMMT(WHPlotterBase.WHPlotterBase):
    def __init__(self, files, lumifiles, outputdir):
        super(WHPlotterMMT, self).__init__(files, lumifiles, outputdir)

if __name__ == "__main__":
    jobid = '2012-07-05-7TeV-Higgs'

    # Figure out if we are 7 or 8 TeV
    period = '7TeV' if '7TeV' in jobid else '8TeV'

    samples = [
        'Zjets_M50',
        'WplusJets_madgraph',
        'WZJetsTo3LNu',
        'ZZ*',
        'VH*',
        'TTplusJets_madgraph',
        "data_DoubleMu*",
    ]

    files = []
    lumifiles = []

    for x in samples:
        files.extend(glob.glob('results/%s/WHAnalyzeMMT/%s.root' % (jobid, x)))
        lumifiles.extend(glob.glob('inputs/%s/%s.lumicalc.sum' % (jobid, x)))

    outputdir = 'results/%s/plots/mmt' % jobid
    plotter = WHPlotterMMT(files, lumifiles, outputdir)

    ###########################################################################
    ##  Zmm control plots #####################################################
    ###########################################################################

    # Control Z->mumu + jet region
    plotter.plot_mc_vs_data('os/p1p2f3', 'm1m2Mass')
    plotter.save('mcdata-os-p1p2f3-m1m2Mass')

    plotter.plot_mc_vs_data('os/p1p2f3/w3', 'm1m2Mass')
    plotter.save('mcdata-os-p1p2f3-w3-m1m2Mass')

    plotter.plot_mc_vs_data('os/p1f2p3', 'm1m2Mass')
    plotter.save('mcdata-os-p1f2p3-m1m2Mass')

    # Check PU variables
    plotter.plot_mc_vs_data('os/p1p2f3', 'rho')
    plotter.save('mcdata-os-p1p2f3-rho')

    plotter.plot_mc_vs_data('os/p1p2f3', 'nvtx')
    plotter.save('mcdata-os-p1p2f3-nvtx')

    # Lower stat but closer to signal region
    plotter.plot_mc_vs_data('os/p1p2p3', 'rho')
    plotter.save('mcdata-os-p1p2p3-rho')

    plotter.plot_mc_vs_data('os/p1p2p3', 'nvtx')
    plotter.save('mcdata-os-p1p2p3-nvtx')

    # Make Z->mumu + tau jet control
    def make_styler(color, format=None):
        def unsuck(x):
            x.SetFillStyle(0)
            x.SetLineColor(color)
            if format:
                x.format = format
        return unsuck

    plotter.plot('data', 'os/p1p2f3/w3/m1m2Mass',  'hist', styler=make_styler(2, 'hist'))
    plotter.plot('data', 'os/p1p2p3/m1m2Mass', 'same', styler=make_styler(1))
    plotter.save('zmm-os-fr-control')

    plotter.plot('data', 'os/p1p2p3/prescale', styler=make_styler(1))
    plotter.save('zmm-os-prescale-check')

    plotter.plot('Zjets_M50', 'os/p1p2f3/weight')
    plotter.save('zmm-mc-event-weights')
    # Check MC weights
    plotter.plot('Zjets_M50', 'os/p1p2f3/weight_nopu')
    plotter.save('zmm-mc-event-weight_nopu')


    ###########################################################################
    ##  FR sideband MC-vs-Data ################################################
    ###########################################################################

    plotter.plot_mc_vs_data('ss/p1f2p3', 'm1Pt', 5, '#mu_{1} p_{T}')
    plotter.save('mcdata-ss-p1f2p3-m1Pt')

    plotter.plot_mc_vs_data('ss/p1f2p3/w2', 'm1Pt', 5, '#mu_{1} p_{T}')
    plotter.save('mcdata-ss-p1f2p3-w2-m1Pt')

    plotter.plot_mc_vs_data('ss/p1f2p3', 'm1Pt', 5, '#mu_{1} p_{T}')
    plotter.save('mcdata-ss-p1f2p3-m1Pt')

    plotter.plot_mc_vs_data('ss/p1f2p3/w2', 'm1Pt', 5, '#mu_{1} p_{T}')
    plotter.save('mcdata-ss-p1f2p3-w2-m1Pt')


    ###########################################################################
    ##  Signal region plots    ################################################
    ###########################################################################

    plotter.plot_final('m1Pt', 10)
    plotter.save('final-m1Pt')

    plotter.plot_final('m2Pt', 10)
    plotter.save('final-m2Pt')

    plotter.plot_final('subMass', 10)
    plotter.save('final-subMass')

    plotter.plot_final('m2Iso', 10)
    plotter.save('final-m2Iso')


    ###########################################################################
    ##  Making shape file     #################################################
    ###########################################################################

    shape_file = ROOT.TFile(
        os.path.join(outputdir, 'mmt_shapes_%s.root' % period), 'RECREATE')
    shape_dir = shape_file.mkdir('mmt')
    plotter.write_shapes('subMass', 10, shape_dir)
    shape_file.Close()



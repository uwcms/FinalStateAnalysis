'''

Plot the EMT channel

Usage: python WHPlotterEMT.py

'''

import glob
import logging
import os
import ROOT
import sys
import WHPlotterBase

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

class WHPlotterEMT(WHPlotterBase.WHPlotterBase):
    def __init__(self, files, lumifiles, outputdir):
        super(WHPlotterEMT, self).__init__(files, lumifiles, outputdir)

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
        "data_MuEG*",
    ]

    files = []
    lumifiles = []

    for x in samples:
        files.extend(glob.glob('results/%s/WHAnalyzeEMT/%s.root' % (jobid, x)))
        lumifiles.extend(glob.glob('inputs/%s/%s.lumicalc.sum' % (jobid, x)))

    outputdir = 'results/%s/plots/emt' % jobid
    plotter = WHPlotterEMT(files, lumifiles, outputdir)

    ###########################################################################
    ##  Zmm control plots #####################################################
    ###########################################################################

    # Control Z->tautau + jet region
    plotter.plot_mc_vs_data('os/p1p2f3', 'emMass')
    plotter.save('mcdata-os-p1p2f3-emMass')

    plotter.plot_mc_vs_data('os/p1p2f3/w3', 'emMass')
    plotter.save('mcdata-os-p1p2f3-w3-emMass')

    plotter.plot_mc_vs_data('os/p1f2p3', 'emMass')
    plotter.save('mcdata-os-p1f2p3-emMass')

    # Check PU variables
    #plotter.plot_mc_vs_data('os/p1p2f3', 'rho')
    #plotter.save('mcdata-os-p1p2f3-rho')

    #plotter.plot_mc_vs_data('os/p1p2f3', 'nvtx')
    #plotter.save('mcdata-os-p1p2f3-nvtx')

    # Lower stat but closer to signal region
    #plotter.plot_mc_vs_data('os/p1p2p3', 'rho')
    #plotter.save('mcdata-os-p1p2p3-rho')

    #plotter.plot_mc_vs_data('os/p1p2p3', 'nvtx')
    #plotter.save('mcdata-os-p1p2p3-nvtx')

    # Make Z->mumu + tau jet control
    def make_styler(color, format=None):
        def unsuck(x):
            x.SetFillStyle(0)
            x.SetLineColor(color)
            if format:
                x.format = format
        return unsuck

    plotter.plot('data', 'os/p1p2f3/w3/emMass',  'hist', styler=make_styler(2, 'hist'))
    plotter.plot('data', 'os/p1p2p3/emMass', 'same', styler=make_styler(1))
    plotter.save('ztt-os-fr-control')

    #plotter.plot('data', 'os/p1p2p3/prescale', styler=make_styler(1))
    #plotter.save('ztt-os-prescale-check')

    #plotter.plot('Zjets_M50', 'os/p1p2f3/weight')
    #plotter.save('ztt-mc-event-weights')
    ## Check MC weights
    #plotter.plot('Zjets_M50', 'os/p1p2f3/weight_nopu')
    #plotter.save('ztt-mc-event-weight_nopu')


    ###########################################################################
    ##  FR sideband MC-vs-Data ################################################
    ###########################################################################

    plotter.plot_mc_vs_data('ss/p1f2p3', 'mPt', 5, '#mu_{1} p_{T}')
    plotter.save('mcdata-ss-p1f2p3-mPt')

    plotter.plot_mc_vs_data('ss/p1f2p3/w2', 'mPt', 5, '#mu_{1} p_{T}')
    plotter.save('mcdata-ss-p1f2p3-w2-mPt')

    plotter.plot_mc_vs_data('ss/p1f2p3', 'ePt', 5, 'Electron p_{T}')
    plotter.save('mcdata-ss-p1f2p3-ePt')

    plotter.plot_mc_vs_data('ss/p1f2p3/w2', 'ePt', 5, 'Electron p_{T}')
    plotter.save('mcdata-ss-p1f2p3-w2-ePt')


    ###########################################################################
    ##  Signal region plots    ################################################
    ###########################################################################

    plotter.plot_final('mPt', 10)
    plotter.save('final-mPt')

    plotter.plot_final('ePt', 10)
    plotter.save('final-ePt')

    plotter.plot_final('subMass', 10)
    plotter.save('final-subMass')

    ###########################################################################
    ##  Making shape file     #################################################
    ###########################################################################

    shape_file = ROOT.TFile(
        os.path.join(outputdir, 'emt_shapes_%s.root' % period), 'RECREATE')
    shape_dir = shape_file.mkdir('emt')
    plotter.write_shapes('subMass', 10, shape_dir)
    shape_file.Close()



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
    jobid = os.environ['jobid']

    print "Plotting MMT for %s" % jobid

    # Figure out if we are 7 or 8 TeV
    period = '7TeV' if '7TeV' in jobid else '8TeV'
    sqrts = 7 if '7TeV' in jobid else 8

    samples = [
        'Zjets_M50',
        'WplusJets_madgraph',
        'WZJetsTo3LNu*',
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
    plotter.plot_mc_vs_data('os/p1p2f3', 'm1m2Mass', xaxis='m_{#mu#mu} (GeV)', xrange=(60, 120))
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-os-p1p2f3-m1m2Mass')

    plotter.plot_mc_vs_data('os/p1p2f3/w3', 'm1m2Mass')
    plotter.save('mcdata-os-p1p2f3-w3-m1m2Mass')

    plotter.plot_mc_vs_data('os/p1f2p3', 'm1m2Mass', xaxis='m_{#mu#mu} (GeV)', xrange=(60, 120))
    plotter.add_cms_blurb(sqrts)
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
            x.SetLineWidth(2)
            if format:
                x.format = format
        return unsuck

    zmm_weighted = plotter.plot('data', 'os/p1p2f3/w3/m1m2Mass',  'hist', styler=make_styler(2, 'hist'), xrange=(60, 120))
    zmm_weighted.SetTitle("Z#mu#mu + fake #tau_{h} est.")
    zmm_weighted.legendstyle='l'
    zmm_weighted.GetXaxis().SetTitle("m_{#mu#mu} (GeV)")

    zmm_unweighted = plotter.plot('data', 'os/p1p2p3/m1m2Mass', 'same', styler=make_styler(1), xrange=(60, 120))
    zmm_unweighted.SetTitle("Z#mu#mu observed")
    zmm_unweighted.SetTitle("Z#mu#mu + fake #tau_{h} obs.")
    zmm_unweighted.legendstyle='pe'

    plotter.add_legend([zmm_weighted, zmm_unweighted])
    plotter.add_cms_blurb(sqrts)
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

    plotter.plot_mc_vs_data('ss/p1f2p3', 'm1Pt', rebin=10, xaxis='#mu_{1} p_{T} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-p1f2p3-m1Pt')

    plotter.plot_mc_vs_data('ss/p1f2p3', 'subMass', rebin=10, xaxis='m_{#mu2#tau} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-p1f2p3-subMass')

    plotter.plot_mc_vs_data('ss/p1f2p3/w2', 'm1Pt', rebin=10, xaxis='#mu_{1} p_{T}', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-p1f2p3-w2-m1Pt')

    plotter.plot_mc_vs_data('ss/f1p2p3', 'subMass', rebin=20, xaxis='m_{#mu2#tau} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-f1p2p3-subMass')

    plotter.plot_mc_vs_data('ss/f1p2p3/w1', 'subMass', rebin=20, xaxis='m_{#mu2#tau} (GeV)', leftside=False)
    plotter.add_cms_blurb(sqrts)
    plotter.save('mcdata-ss-f1p2p3-w1-subMass')



    ###########################################################################
    ##  Signal region plots    ################################################
    ###########################################################################

    plotter.plot_final('m1Pt', 10)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-m1Pt')

    plotter.plot_final('m2Pt', 10)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-m2Pt')

    plotter.plot_final('subMass', 20, xaxis='m_{#mu_{2}#tau} (GeV)')
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-subMass')

    plotter.plot_final('m2Iso', 10)
    plotter.add_cms_blurb(sqrts)
    plotter.save('final-m2Iso')


    ###########################################################################
    ##  Making shape file     #################################################
    ###########################################################################

    shape_file = ROOT.TFile(
        os.path.join(outputdir, 'mmt_shapes_%s.root' % period), 'RECREATE')
    shape_dir = shape_file.mkdir('mmt')
    plotter.write_shapes('subMass', 20, shape_dir)
    shape_file.Close()



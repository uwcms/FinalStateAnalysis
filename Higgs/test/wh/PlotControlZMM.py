'''

Make inclusive Z->mumu control plots

'''

import os
import glob
from FinalStateAnalysis.PlotTools.Plotter import Plotter

jobid = os.environ['jobid']

output_dir = os.path.join('results', jobid, 'plots', 'zmm')

samples = [
    'Zjets_M50',
    'WZ*',
    'ZZ*',
    'WW*',
    'TT*',
    'WplusJets*',
    "data_DoubleMu*",
]

files = []
lumifiles = []

for x in samples:
    files.extend(glob.glob('results/%s/ControlZMM/%s.root' % (jobid, x)))
    lumifiles.extend(glob.glob('inputs/%s/%s.lumicalc.sum' % (jobid, x)))

plotter = Plotter(files, lumifiles, output_dir)

plotter.plot_mc_vs_data('zmm', 'm1m2Mass', rebin=4)
plotter.save('mass')

plotter.plot_mc_vs_data('zmm', 'm1Pt')
plotter.save('m1Pt')
plotter.plot_mc_vs_data('zmm', 'm2Pt')
plotter.save('m2Pt')

plotter.plot_mc_vs_data('zmm', 'm1AbsEta')
plotter.save('m1AbsEta')
plotter.plot_mc_vs_data('zmm', 'm2AbsEta')
plotter.save('m2AbsEta')

plotter.plot_mc_vs_data('zmm', 'nvtx')
plotter.save('nvtx')

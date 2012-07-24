'''

Make inclusive e-mu (Z + ttbar) control plots

'''

import os
import glob
from FinalStateAnalysis.PlotTools.Plotter import Plotter

jobid = os.environ['jobid']

output_dir = os.path.join('results', jobid, 'plots', 'em')

samples = [
    'Zjets_M50',
    'WZ*',
    'ZZ*',
    'TT*',
    'WplusJets*',
    "data_MuEG*",
]

files = []
lumifiles = []

for x in samples:
    files.extend(glob.glob('results/%s/ControlEM/%s.root' % (jobid, x)))
    lumifiles.extend(glob.glob('inputs/%s/%s.lumicalc.sum' % (jobid, x)))

plotter = Plotter(files, lumifiles, output_dir)

plotter.plot_mc_vs_data('em', 'emMass', rebin=4)
plotter.save('mass')

plotter.plot_mc_vs_data('em', 'mPt')
plotter.save('mPt')
plotter.plot_mc_vs_data('em', 'ePt')
plotter.save('ePt')

plotter.plot_mc_vs_data('em', 'mAbsEta')
plotter.save('mAbsEta')
plotter.plot_mc_vs_data('em', 'eAbsEta')
plotter.save('eAbsEta')

plotter.plot_mc_vs_data('em', 'nvtx')
plotter.save('nvtx')

plotter.plot_mc_vs_data('em', 'bjetCSVVeto')
plotter.save('bjetCSVVeto')

plotter.plot_mc_vs_data('em', 'bjetVeto')
plotter.save('bjetVeto')

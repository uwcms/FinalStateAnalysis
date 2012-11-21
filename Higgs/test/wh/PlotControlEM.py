'''

Make inclusive e-mu (Z + ttbar) control plots

'''

import os
import glob
from FinalStateAnalysis.PlotTools.Plotter import Plotter
from FinalStateAnalysis.MetaData.data_styles import data_styles

jobid = os.environ['jobid']

output_dir = os.path.join('results', jobid, 'plots', 'em')

samples = [
    'Zjets_M50',
    'WZ*',
    'WW*',
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

# Define how we estimate QCD - just take SS data.
import rootpy.plotting.views as views
def get_ss(x):
    return x.replace('em/', 'em/ss/')

mc_view = views.SumView(
    *[views.PathModifierView(plotter.get_view(x), get_ss) for x in [
        'WZJetsTo3LNu*',
        'ZZJetsTo4L*',
        'WW*',
        'WplusJets_madgraph',
        'TTplusJets_madgraph',
        'Zjets_M50',
    ]]
)

mc_inverted = views.ScaleView(mc_view, -1)

qcd_view = views.StyleView(
    views.TitleView(
        views.SumView(views.PathModifierView(plotter.data, get_ss), mc_inverted),
        'QCD'),
    **data_styles['QCD*'])

plotter.views['QCD'] = { 'view': qcd_view }

# Override ordering
plotter.mc_samples = [
    'WZJetsTo3LNu*',
    'ZZJetsTo4L*',
    'QCD',
    'WW*',
    'WplusJets_madgraph',
    'TTplusJets_madgraph',
    'Zjets_M50',
]

sqrts = 7 if '7TeV' in jobid else 8

plotter.plot_mc_vs_data('em', 'emMass', rebin=10, leftside=False,
                        xaxis='m_{e#mu} (GeV)')
plotter.add_cms_blurb(sqrts)
plotter.save('mass')

plotter.plot_mc_vs_data('em', 'mPt')
plotter.save('mPt')
plotter.plot_mc_vs_data('em', 'ePt', rebin=10)
plotter.save('ePt')

plotter.plot_mc_vs_data('em', 'mAbsEta')
plotter.save('mAbsEta')
plotter.plot_mc_vs_data('em', 'eAbsEta', rebin=5)
plotter.save('eAbsEta')

plotter.plot_mc_vs_data('em', 'nvtx')
plotter.save('nvtx')

plotter.plot_mc_vs_data('em', 'bjetCSVVeto')
plotter.save('bjetCSVVeto')

plotter.plot_mc_vs_data('em', 'bjetVeto')
plotter.save('bjetVeto')

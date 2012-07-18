'''

Make inclusive Z->mumu control plots

'''

import glob
import os
import rootpy.plotting.views as views
import rootpy.plotting as plotting
from FinalStateAnalysis.MetaData.data_views import data_views
from FinalStateAnalysis.MetaData.data_styles import data_styles

jobid = os.environ['jobid']

output_dir = os.path.join('results', jobid, 'plots', 'zmm')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

samples = [
    'Zjets_M50',
    "data_DoubleMu*",
]

files = []
lumifiles = []

for x in samples:
    files.extend(glob.glob('results/%s/ControlZMM/%s.root' % (jobid, x)))
    lumifiles.extend(glob.glob('inputs/%s/%s.lumicalc.sum' % (jobid, x)))

views = data_views(files, lumifiles)

canvas = plotting.Canvas(name='adsf', title='asdf')
canvas.cd()

mc = views['Zjets_M50']['view'].Get('zmm/m1m2Mass')
data = views['data']['view'].Get('zmm/m1m2Mass')

mc.Draw()
data.Draw('same')

canvas.SaveAs(os.path.join(output_dir, 'mass') + '.png')

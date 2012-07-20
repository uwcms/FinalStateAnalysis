'''

Make inclusive Z->mumu control plots

'''

import glob
import logging
import os
import rootpy.plotting.views as views
import rootpy.plotting as plotting
from FinalStateAnalysis.MetaData.data_views import data_views
from FinalStateAnalysis.MetaData.data_styles import data_styles
import sys
import ROOT

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

jobid = os.environ['jobid']

output_dir = os.path.join('results', jobid, 'plots', 'zmm')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

samples = [
    'Zjets_M50',
    "data_DoubleMu*",
    #"data_SingleMu*",
    'VH_120',
]

files = []
lumifiles = []

for x in samples:
    files.extend(glob.glob('results/%s/ControlZMM/%s.root' % (jobid, x)))
    lumifiles.extend(glob.glob('inputs/%s/%s.lumicalc.sum' % (jobid, x)))

data_views = data_views(files, lumifiles)

canvas = plotting.Canvas(name='adsf', title='asdf')
canvas.cd()

keep = []

def save(name):
    canvas.SetLogy(False)
    canvas.SaveAs(os.path.join(output_dir, name) + '.png')
    canvas.SetLogy(True)
    canvas.SaveAs(os.path.join(output_dir, name) + '.log.png')
    keep = []

def compare(path):
    mc = data_views['Zjets_M50']['view'].Get(path)
    data = data_views['data']['view'].Get(path)
    mc.Draw()
    data.Draw('same')
    keep.append( (mc, data) )

def veto_eff(histo):
    all = histo.Integral()
    vetoed = histo.Integral(2, histo.GetNbinsX()+2)
    return 1 - vetoed/all

def compare_shapes(path, xaxis=''):
    mc = views.TitleView(views.NormalizeView(data_views['Zjets_M50']['view']), 'MC Z#mu#mu').Get(path)
    data = views.TitleView(views.NormalizeView(data_views['data']['view']), 'Obs. Z#mu#mu').Get(path)
    wh = views.TitleView(views.SubdirectoryView(views.NormalizeView(data_views['VH_120']['view']), 'ss/p1p2p3'), 'WH120').Get(path.replace('zmm/', ''))
    mc.Draw()
    mc.GetXaxis().SetTitle(xaxis)
    mc_eff = veto_eff(mc)
    data_eff = veto_eff(data)
    wh_eff = veto_eff(wh)
    legend = plotting.Legend(2, rightmargin=0.07, topmargin=0.05, leftmargin=0.45)
    legend.SetBorderSize(0)
    data.Draw('same')
    wh.Draw('same, e')
    legend.AddEntry(wh)
    legend.AddEntry(mc)
    legend.AddEntry(data)
    legend.Draw()
    latex = ROOT.TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    keep.append(latex.DrawLatex(0.90,0.96,"Z-MC eff. %0.4f Z-DATA eff: %0.4f WH eff: %0.4f" % (mc_eff, data_eff, wh_eff)))
    keep.append( (mc, data, legend) )

def compare_shapes_good(path, xaxis=''):
    mc = views.NormalizeView(data_views['Zjets_M50']['view']).Get(path)
    data = views.NormalizeView(data_views['data']['view']).Get(path)
    mc.Draw()
    mc.GetXaxis().SetTitle(xaxis)
    mc_eff = veto_eff(mc)
    data_eff = veto_eff(data)
    legend = plotting.Legend(2, rightmargin=0.07, topmargin=0.05, leftmargin=0.45)
    legend.SetBorderSize(0)
    data.Draw('same')
    legend.AddEntry(mc)
    legend.AddEntry(data)
    legend.Draw()
    latex = ROOT.TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    keep.append(latex.DrawLatex(0.90,0.96,"MC eff. %0.3f DATA eff: %0.3f" % (mc_eff, data_eff)))
    keep.append( (mc, data, legend) )

compare('zmm/m1m2Mass')
save('mass')

compare('zmm/m1Pt')
save('m1Pt')
compare('zmm/m2Pt')
save('m2Pt')

compare('zmm/m1AbsEta')
save('m1AbsEta')
compare('zmm/m2AbsEta')
save('m2AbsEta')

compare('zmm/nvtx')
save('nvtx')

compare_shapes('zmm/bjetCSVVeto')
save('bjetCSVVeto')

compare_shapes('zmm/bjetVeto', xaxis='N. TCHE b-jets')
save('bjetVeto')

compare_shapes('zmm/muVetoPt5', xaxis='N. veto muons')
save('muVetoPt5')

compare_shapes('zmm/tauVetoPt20', xaxis='N. veto iso. #tau_{h}')
save('tauVetoPt20')

compare_shapes('zmm/eVetoCicTightIso', xaxis='N. veto CiC iso. e')
save('eVetoCicTightIso')

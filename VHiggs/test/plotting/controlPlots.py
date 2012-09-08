'''

Make control plots of PU vertex distributions in Zmumu events


'''

import ROOT
import os
import sys
import logging
import FinalStateAnalysis.PatTools.data as data_tool
from FinalStateAnalysis.Utilities.AnalysisPlotter import styling,samplestyles

#logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger("controlPlots")

ROOT.gROOT.SetBatch(True)
canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)


def saveplot(filename):
    # Save the current canvas
    filetype = '.pdf'
    #legend.Draw()
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'controlPlots', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join(
        "plots", 'controlPlots', filename + '_log' + filetype))

skips = ['EM', 'DoubleEl']
int_lumi = 4700

samples, plotter = data_tool.build_data(
    'VH', '2012-02-19-v1-WHAnalyze', 'scratch_results', int_lumi, skips,
    count = '/mmt/skimCounter', unweighted = False)


base_dimuon_selection = [
    #'(run < 5 && Muon1Pt > 13.5 || Muon1Pt > 13.365)',
    #'(run < 5 && Muon2Pt > 9 || Muon2Pt > 8.91)',
    'Muon1Pt > 20',
    'Muon2Pt > 10',
    'Muon1AbsEta < 1.44',
    'Muon2AbsEta < 1.44',
    'Muon1_MuRelIso < 0.1',
    'Muon2_MuRelIso < 0.1',
    'Muon1_MuID_WWID > 0.5',
    'Muon2_MuID_WWID > 0.5',
    'NIsoMuonsPt5_Nmuons < 0.5',
    'NBjetsPt20_Nbjets < 1', # Against ttbar
    'DoubleMus_HLT > 0.5 ',
    'Muon1Charge*Muon2Charge < 0',
    #'vtxNDOF > 0',
    #'vtxChi2/vtxNDOF < 10',
    #'METPt < 20',
    'Muon1_Muon2_Mass < 95',
    'Muon1_Muon2_Mass > 85',
]

plots = {
    'HLT_Group' : {
        'var' : 'DoubleMus_HLTGroup',
        'title' : 'N_{vtx}',
        'binning' : [5, -0.5, 4.5],
    },
    'NVtx' : {
        'var' : 'FinalState_NVtx',
        'title' : 'N_{vtx}',
        'binning' : [25, -0.5, 24.5],
    },
    'Rho' : {
        'var' : 'FinalState_Rho',
        'title' : '#rho',
        'binning' : [100, 0, 20],
    },
    'MET' : {
        'var' : 'METPt',
        'title' : 'MET',
        'binning' : [100, 0, 100],
    },
}

log.info("Plotting distribution of vertices w/o weighting")

for var, var_info in plots.iteritems():
    plotter.register_tree(
        'NoWeights' + var,
        '/mmt/final/Ntuple',
        var_info['var'],
        ' && '.join(base_dimuon_selection),
        w = '((0 < Mu15_HLTPrescale < 2)*0.985*0.982*0.995*0.994 + (Mu15_HLTPrescale > 2 || Mu15_HLTPrescale < 1)*1)',
        binning = var_info['binning'],
        include = ['*DoubleMu*', 'Zjets', 'VH120WW'],
    )

    plotter.register_tree(
        'Weights' + var,
        '/mmt/final/Ntuple',
        var_info['var'],
        ' && '.join(base_dimuon_selection),
        w = '((0 < Mu15_HLTPrescale < 2)*0.985*0.982*0.995*0.994 + (Mu15_HLTPrescale > 2 || Mu15_HLTPrescale < 1)*1)*(pu2011AB)',
        binning = var_info['binning'],
        include = ['*DoubleMu*', 'Zjets', 'VH120WW'],
    )

    data_noweight = plotter.get_histogram(
        'data_DoubleMu',
        '/mmt/final/Ntuple:NoWeights' + var,
        show_overflows = True
    )

    zjets_noweight = plotter.get_histogram(
        'Zjets',
        '/mmt/final/Ntuple:NoWeights' + var,
        show_overflows = True
    )

    #zjets_noweight = zjets_noweight*49000

    zjets_noweight.Draw('hist')
    data_noweight.Draw('pe, same')
    zjets_noweight.SetMaximum(
        1.5*max(zjets_noweight.GetMaximum(), data_noweight.GetMaximum()))
    zjets_noweight.GetXaxis().SetTitle(var_info['title'])

    legend = ROOT.TLegend(0.7, 0.65, 0.88, 0.9, "No correction", "brNDC")
    legend.SetFillStyle(0)
    legend.AddEntry(zjets_noweight.th1, "Fall11 Z+jets", "lf")
    legend.AddEntry(data_noweight.th1, "2011 Data", "pe")
    legend.Draw()

    saveplot('noweight_%s' % var)

    data_weight = plotter.get_histogram(
        'data_DoubleMu',
        '/mmt/final/Ntuple:Weights' + var,
        show_overflows = True
    )

    zjets_weight = plotter.get_histogram(
        'Zjets',
        '/mmt/final/Ntuple:Weights' + var,
        show_overflows = True
    )

    #zjets_weight = zjets_weight*49000

    zjets_weight.Draw('hist')
    data_weight.Draw('pe, same')
    zjets_weight.SetMaximum(
        1.5*max(zjets_weight.GetMaximum(), data_weight.GetMaximum()))
    zjets_weight.GetXaxis().SetTitle(var_info['title'])

    print zjets_noweight.Integral(), data_noweight.Integral()
    print zjets_weight.Integral(), data_weight.Integral()

    legend = ROOT.TLegend(0.7, 0.65, 0.88, 0.9, "3D Weights", "brNDC")
    legend.SetFillStyle(0)
    legend.AddEntry(zjets_weight.th1, "Fall11 Z+jets", "lf")
    legend.AddEntry(data_weight.th1, "2011 Data", "pe")
    legend.Draw()

    saveplot('weight_%s' % var)


'''

Combine fake rates from many channels

'''

import ROOT
from FinalStateAnalysis.Utilities.Histo import Histo

trilepton_fr_file = ROOT.TFile("results_fakeRates.root", "READ")
singlemu_fr_file = ROOT.TFile("results_singleMuFakeRates.root", "READ")

def get_histograms(file, data_set, fr_type):
    denom = file.Get("_".join([data_set, fr_type, 'data_denom']))
    num = file.Get("_".join([data_set, fr_type, 'data_num']))
    return Histo(num), Histo(denom)

scenarios = {
    'SingleMu_Wjets' : {
        'histos' : get_histograms(singlemu_fr_file, '2011AB', 'mu')
    },
    'SingleMu_QCD' : {
        'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muQCD')
    },
    #'TriLep_ZMM' : {
        #'histos' : get_histograms(trilepton_fr_file, '2011AB', 'mu')
    #},
    'Trilep_TT' : {
        'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muTTbar')
    },
    'Trilep_QCD' : {
        'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muQCD')
    },
}

combined_denom = None
combined_num = None

for type, type_info in scenarios.iteritems():
    num, denom = type_info['histos']
    efficiency = ROOT.TGraphAsymmErrors(num.th1, denom.th1)
    type_info['efficiency'] = efficiency
    if combined_denom is None:
        combined_denom = denom
    else:
        combined_denom = combined_denom + denom

    if combined_num is None:
        combined_num = num
    else:
        combined_num = combined_num + num
    print combined_num, combined_denom

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
canvas.SetLogy(True)

combined_eff = ROOT.TGraphAsymmErrors(combined_num.th1, combined_denom.th1)

data_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
data_fit_func.SetParameter(0, 0.02)
data_fit_func.SetParLimits(0, 0.0, 1)
data_fit_func.SetParameter(1, 1.87)
data_fit_func.SetParameter(2, -9.62806e-02)
data_fit_func.SetLineColor(ROOT.EColor.kBlack)
combined_eff.Fit(data_fit_func)

combined_eff.Draw("alp")
combined_eff.GetHistogram().SetMinimum(1e-3)
combined_eff.GetHistogram().SetMaximum(1.0)
data_fit_func.Draw("same")

canvas.SaveAs("plots/combineFakeRates/combined_eff.pdf")

for type, type_info in scenarios.iteritems():
    eff = type_info['efficiency']
    eff.Draw("alp")
    eff.GetHistogram().SetMinimum(1e-3)
    eff.GetHistogram().SetMaximum(1.0)
    data_fit_func.Draw("same")
    eff.GetHistogram().SetTitle("%f" % eff.Chisquare(data_fit_func))
    eff.GetHistogram().GetXaxis().SetTitle("%f" % eff.Chisquare(data_fit_func))
    canvas.SaveAs("plots/combineFakeRates/%s_eff.pdf" % type)

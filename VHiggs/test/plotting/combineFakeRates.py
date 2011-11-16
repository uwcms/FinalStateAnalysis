'''

Combine fake rates from many channels.

'''

import ROOT
from FinalStateAnalysis.Utilities.Histo import Histo

trilepton_fr_file = ROOT.TFile("results_fakeRates.root", "READ")
singlemu_fr_file = ROOT.TFile("results_singleMuFakeRates.root", "READ")

def get_histograms(file, data_set, fr_type):
    denom = file.Get("_".join([data_set, fr_type, 'data_denom']))
    num = file.Get("_".join([data_set, fr_type, 'data_num']))
    return Histo(num), Histo(denom)

# Muon fit function
muon_fit_func = ROOT.TF1("f1", "[0]*TMath::Landau(x,[1],[2],0)+[3]", 10, 200)
muon_fit_func.SetParameter(0, 0.5)
muon_fit_func.SetParLimits(0, 0.0, 10)
muon_fit_func.SetParameter(1, 15)
muon_fit_func.SetParameter(2, 1)
muon_fit_func.SetParameter(3, 5e-3)

elec_fit_func = ROOT.TF1("f1", "[0] + [1]*exp([2]*x)", 0, 200)
elec_fit_func.SetParameter(0, 0.02)
elec_fit_func.SetParLimits(0, 0.0, 1)
elec_fit_func.SetParameter(1, 1.87)
elec_fit_func.SetParameter(2, -9.62806e-02)

object_config = {
    'mu' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W+jet_{#mu} (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'mu')
            },
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muQCD')
            },
            'TriLep_ZMM' : {
                'title' : 'Z#mu #mu + jet_{#mu} (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'mu')
            },
            'TriLep_ZEE' : {
                'title' : 'Zee + jet_{#mu} (Double Elec)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muZEE')
            },
            'Trilep_TT' : {
                'title' : 'ttbar + jet_{#mu} (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muTTbar')
            },
            'Trilep_QCD' : {
                'title' : 'QCD (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muQCD')
            },
        },
        'function' : muon_fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'e' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W+jet_{#mu} (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'e')
            },
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'eQCD')
            },
            'TriLep_ZMM' : {
                'title' : 'Z#mu #mu + jet_{#mu} (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'e')
            },
        },
        'function' : muon_fit_func,
        'label' : 'Jet #rightarrow e fake rate',
    },
}

for object, object_info in object_config.iteritems():
    scenarios = object_info['scenarios']

    combined_denom = None
    combined_num = None

    for type, type_info in scenarios.iteritems():
        num, denom = type_info['histos']

        n_non_empty = len(list(bin.value() for bin in num.bins() if
                               bin.value() > 0))
        type_info['ndof'] = max(n_non_empty - 3, 1)

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

    frame = ROOT.TH1F("frame", "Fake rate", 100, 0, 100)
    frame.GetXaxis().SetTitle("Jet p_{T}")
    frame.SetMinimum(1e-3)
    frame.SetMaximum(1.0)

    combined_eff = ROOT.TGraphAsymmErrors(combined_num.th1, combined_denom.th1)

    data_fit_func = object_info['function']

    data_fit_func.SetLineColor(ROOT.EColor.kRed)

    combined_eff.Fit(data_fit_func)
    frame.Draw()
    combined_eff.Draw("p")
    combined_eff.GetHistogram().SetMinimum(1e-3)
    combined_eff.GetHistogram().SetMaximum(1.0)
    data_fit_func.Draw("same")

    label = ROOT.TPaveText(0.6, 0.6, 0.9, 0.87, "NDC")
    label.SetBorderSize(1)
    label.SetFillColor(ROOT.EColor.kWhite)
    label.AddText(object_info['label'])
    label.AddText("All channels")
    label.Draw()

    legend = ROOT.TLegend(0.6, 0.5, 0.9, 0.6, "", "NDC")
    legend.SetBorderSize(1)
    legend.SetFillColor(ROOT.EColor.kWhite)
    legend.AddEntry(data_fit_func, "Combined Fit", "l")
    legend.Draw()

    canvas.SetLogy(True)
    canvas.SaveAs("plots/combineFakeRates/%s_combined_eff.pdf" % object)
    canvas.SetLogy(False)
    canvas.SaveAs("plots/combineFakeRates/%s_combined_eff_lin.pdf" % object)

    for type, type_info in scenarios.iteritems():
        eff = type_info['efficiency']
        eff.Draw("ap")
        eff.GetHistogram().SetMinimum(1e-3)
        eff.GetHistogram().SetMaximum(1.0)
        data_fit_func.Draw("same")

        label = ROOT.TPaveText(0.6, 0.6, 0.9, 0.87, "NDC")
        label.SetBorderSize(1)
        label.SetFillColor(ROOT.EColor.kWhite)
        label.AddText(object_info['label'])
        label.AddText(type_info['title'])
        chi2 = eff.Chisquare(data_fit_func)
        chi2 /= type_info['ndof']
        label.AddText('#chi^{2}/NDF = %0.1f' % chi2)
        label.Draw()
        legend.Draw()

        eff.GetHistogram().GetXaxis().SetTitle("Jet p_{T}")
        canvas.SetLogy(True)
        canvas.SaveAs("plots/combineFakeRates/%s_%s_eff.pdf" % (object, type))
        canvas.SetLogy(False)
        canvas.SaveAs("plots/combineFakeRates/%s_%s_eff_lin.pdf" % (object, type))

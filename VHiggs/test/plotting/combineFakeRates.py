'''

Combine fake rates from many channels.

'''
import logging
log = logging.getLogger("combineFR")
ch = logging.StreamHandler()
log.setLevel(logging.INFO)
log.addHandler(ch)

import ROOT
ROOT.gStyle.SetOptFit(0)
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
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'mu'),
                'rebin' : 5,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muQCD'),
                'rebin' : 1,
            },
            'TriLep_ZMM' : {
                'title' : 'Z#mu #mu + jet_{#mu} (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'mu'),
                'rebin' : 5,
            },
            'TriLep_ZEE' : {
                'title' : 'Zee + jet_{#mu} (Double Elec)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muZEE'),
                'rebin' : 5,
            },
            'Trilep_TT' : {
                'title' : 'ttbar + jet_{#mu} (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muTTbar'),
                'rebin' : 5,
            },
            'Trilep_QCD' : {
                'title' : 'QCD (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muQCD'),
                'rebin' : 5,
            },
        },
        'rebin' : 1,
        'fit_label' : 'Combined Fit',
        'function' : muon_fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'muTight' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W+jet_{#mu} (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muTight'),
                'rebin' : 5,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muQCDTight'),
                'rebin' : 1,
            },
        },
        'rebin' : 1,
        'fit_label' : 'Combined Fit',
        'function' : muon_fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'e' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W+jet_{#mu} (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'e'),
                'rebin' : 5,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'eQCD'),
                'rebin' : 1,
                'exclude' : True,
            },
            'TriLep_ZMM' : {
                'title' : 'Z#mu #mu + jet_{#mu} (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'e'),
                'rebin' : 5,
                'exclude' : True,
            },
        },
        'rebin' : 5,
        'fit_label' : 'Wjets Fit',
        'function' : muon_fit_func,
        'label' : 'Jet #rightarrow e fake rate',
    },
    'eMIT' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W+jet_{#mu} (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'eMIT'),
                'rebin' : 5,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'eQCDMIT'),
                'rebin' : 1,
                'exclude' : True,
            },
        },
        'rebin' : 5,
        'fit_label' : 'Wjets Fit',
        'function' : muon_fit_func,
        'label' : 'Jet #rightarrow e fake rate',
    },
}

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
for object, object_info in object_config.iteritems():
    log.info("Computing fake rates for object: %s", object)
    scenarios = object_info['scenarios']

    combined_denom = None
    combined_num = None

    for type, type_info in scenarios.iteritems():
        log.info("Getting fake rates for object: %s type: %s", object, type)
        num, denom = type_info['histos']

        n_non_empty = len(list(bin.value() for bin in num.bins() if
                               bin.value() > 0))
        type_info['ndof'] = max(n_non_empty - 3, 1)

        if not type_info.get('exclude'):
            if combined_denom is None:
                combined_denom = denom
            else:
                combined_denom = combined_denom + denom

            if combined_num is None:
                combined_num = num
            else:
                combined_num = combined_num + num

        # Rebin
        num = Histo(num.th1, rebin=type_info['rebin'])
        denom = Histo(denom.th1, rebin=type_info['rebin'])

        efficiency = ROOT.TGraphAsymmErrors(num.th1, denom.th1)
        type_info['efficiency'] = efficiency



    canvas.SetLogy(True)

    frame = ROOT.TH1F("frame", "Fake rate", 100, 0, 100)
    frame.GetXaxis().SetTitle("Jet p_{T}")
    frame.SetMinimum(1e-3)
    frame.SetMaximum(1.0)

    combined_num = Histo(combined_num.th1, rebin=object_info['rebin'])
    combined_denom = Histo(combined_denom.th1, rebin=object_info['rebin'])

    combined_eff = ROOT.TGraphAsymmErrors(combined_num.th1, combined_denom.th1)

    data_fit_func = object_info['function']

    data_fit_func.SetLineColor(ROOT.EColor.kRed)

    combined_eff.Fit(data_fit_func)
    frame.Draw()
    combined_eff.Draw("p")
    combined_eff.GetHistogram().SetMinimum(1e-3)
    combined_eff.GetHistogram().SetMaximum(1.0)
    data_fit_func.Draw("same")

    label = ROOT.TPaveText(0.7, 0.7, 0.9, 0.87, "NDC")
    label.SetBorderSize(1)
    label.SetFillColor(ROOT.EColor.kWhite)
    label.AddText(object_info['label'])
    label.AddText("All channels")
    label.Draw()

    legend = ROOT.TLegend(0.7, 0.6, 0.9, 0.7, "", "NDC")
    legend.SetBorderSize(1)
    legend.SetFillColor(ROOT.EColor.kWhite)
    legend.AddEntry(data_fit_func, object_info['fit_label'], "l")
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

        #label = ROOT.TPaveText(0.6, 0.6, 0.9, 0.87, "NDC")
        label = ROOT.TPaveText(0.7, 0.7, 0.9, 0.87, "NDC")
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

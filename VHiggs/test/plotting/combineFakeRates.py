'''

Combine fake rates from many channels.

'''
import sys
import json
import logging
log = logging.getLogger("combineFR")
ch = logging.StreamHandler()
log.setLevel(logging.DEBUG)
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
roo_fit_func_str = "scale*TMath::Landau(jetPt,mu,sigma,0)+offset"
fit_func = ROOT.TF1("f1", "[0]*TMath::Landau(x,[1],[2],0)+[3]", 10, 200)

def setup_func_pars(func):
    ''' Refresh the fit parameters '''
    func.SetParameter(0, 3.5)
    func.SetParName(0, "scale")
    func.SetParLimits(0, 0.0, 10)
    func.SetParameter(1, 17)
    func.SetParName(1, "mu")
    func.SetParameter(2, 1.9)
    func.SetParName(2, "sigma")
    func.SetParameter(3, 10e-3)
    func.SetParName(3, "constant")

setup_func_pars(fit_func)

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
                'exclude' : True,
            },
            'TriLep_ZMM' : {
                'title' : 'Z#mu #mu + jet_{#mu} (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'mu'),
                'rebin' : 5,
            },
            #'TriLep_ZEE' : {
                #'title' : 'Zee + jet_{#mu} (Double Elec)',
                #'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muZEE'),
                #'rebin' : 5,
            #},
            ##'Trilep_TT' : {
                ##'title' : 'ttbar + jet_{#mu} (Double Mu)',
                ##'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muTTbar'),
                ##'rebin' : 5,
            ##},
            #'Trilep_QCD' : {
                #'title' : 'QCD (Double Mu)',
                #'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muQCD'),
                #'rebin' : 5,
                #'exclude' : True,
            #},
        },
        'rebin' : 2,
        'fit_label' : 'EWK Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'muQCD' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W+jet_{#mu} (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'mu'),
                'rebin' : 5,
                'exclude' : True,
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
                'exclude' : True,
            },
            'TriLep_ZEE' : {
                'title' : 'Zee + jet_{#mu} (Double Elec)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muZEE'),
                'exclude' : True,
                'rebin' : 5,
            },
            #'Trilep_TT' : {
                #'title' : 'ttbar + jet_{#mu} (Double Mu)',
                #'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muTTbar'),
                #'rebin' : 5,
                #'exclude' : True,
            #},
            'Trilep_QCD' : {
                'title' : 'QCD (Double Mu)',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'muQCD'),
                'rebin' : 5,
            },
        },
        'rebin' : 1,
        'fit_label' : 'QCD Fit',
        'function' : fit_func,
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
                'exclude' : True,
            },
        },
        'rebin' : 1,
        'fit_label' : 'EWK Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'muQCDTight' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W+jet_{#mu} (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muTight'),
                'rebin' : 5,
                'exclude' : True,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muQCDTight'),
                'rebin' : 1,
            },
        },
        'rebin' : 1,
        'fit_label' : 'QCD Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'muHighPt' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W+jet_{#mu} (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muHighPt'),
                'rebin' : 5,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muQCDHighPt'),
                'rebin' : 5,
                'exclude' : True,
            },
        },
        'rebin' : 5,
        'fit_label' : 'Combined Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'muHighPtQCDOnly' : {
        'scenarios' : {
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'muQCDHighPt'),
                'rebin' : 5,
                'exclude' : False,
            },
        },
        'rebin' : 5,
        'fit_label' : 'QCD Fit',
        'function' : fit_func,
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
        },
        'rebin' : 5,
        'fit_label' : 'Wjets Fit',
        'function' : fit_func,
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
            'TriLep_ZMM' : {
                'title' : 'Z#mu#mu + jet_{e}',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'eMuEG'),
                'rebin' : 10,
                'exclude' : False,
            },
        },
        'rebin' : 5,
        'fit_label' : 'Wjets Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow e fake rate',
    },
    'eMITQCD' : {
        'scenarios' : {
            'SingleMu_QCD' : {
                'title' : 'QCD (Single Mu)',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'eQCDMIT'),
                'rebin' : 1,
                'exclude' : False,
            },
        },
        'rebin' : 1,
        'fit_label' : 'QCD Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow e fake rate',
    },
    'tau' : {
        'scenarios' : {
            'TriLep_ZMM' : {
                'title' : 'Z#mu#mu + jet_{#tau}',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'tau'),
                'rebin' : 1,
                'exclude' : False,
            },
            'TriLep_AntiIsoMM' : {
                'title' : 'QCD + jet_{#tau}',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'tauQCD'),
                'rebin' : 2,
                'exclude' : True,
            },
            'SingleMu_Wjets' : {
                'title' : 'W #mu #nu + jet_{#tau}',
                'histos' : get_histograms(singlemu_fr_file, '2011AB', 'tau'),
                'rebin' : 2,
                'exclude' : True,
            },
        },
        'rebin' : 1,
        'fit_label' : 'Zjets Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #tau fake rate',
    },
    'tauQCD' : {
        'scenarios' : {
            'TriLep_AntiIsoMM' : {
                'title' : 'QCD + jet_{#tau}',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'tauQCD'),
                'rebin' : 1,
                'exclude' : False,
            },
            'TriLep_ZMM' : {
                'title' : 'Z#mu#mu + jet_{#tau}',
                'histos' : get_histograms(trilepton_fr_file, '2011AB', 'tau'),
                'rebin' : 1,
                'exclude' : True,
            },
        },
        'rebin' : 1,
        'fit_label' : 'QCD Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #tau fake rate',
    },
}

# Store the fit results so we can put them in a json at the end
fit_results = {}
canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
frame = ROOT.TH1F("frame", "Fake rate", 100, 0, 100)
frame.GetXaxis().SetTitle("Jet p_{T}")
frame.SetMinimum(1e-3)
frame.SetMaximum(1.0)

for object, object_info in object_config.iteritems():
    object_result = {}
    fit_results[object] = object_result
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
                combined_denom = Histo(denom.th1.Clone())
            else:
                combined_denom = combined_denom + denom
            if combined_num is None:
                combined_num = Histo(num.th1.Clone())
            else:
                combined_num = combined_num + num

        # Rebin
        num = Histo(num.th1, rebin=type_info['rebin'])
        denom = Histo(denom.th1, rebin=type_info['rebin'])

        log.debug("Numerator N=%i min=%f max=%f",
                  num.GetNbinsX(), num.GetXaxis().GetXmin(),
                  num.GetXaxis().GetXmax())
        log.debug("Denominator N=%i min=%f max=%f",
                  denom.GetNbinsX(), denom.GetXaxis().GetXmin(),
                  denom.GetXaxis().GetXmax())

        efficiency = ROOT.TGraphAsymmErrors(num.th1, denom.th1)
        type_info['efficiency'] = efficiency

    canvas.SetLogy(True)

    log.info("Computing combined efficiency")

    combined_num = Histo(combined_num.th1, rebin=object_info['rebin'])
    combined_denom = Histo(combined_denom.th1, rebin=object_info['rebin'])

    log.debug("Numerator N=%i min=%f max=%f",
              combined_num.GetNbinsX(), combined_num.GetXaxis().GetXmin(),
              combined_num.GetXaxis().GetXmax())
    log.debug("Denominator N=%i min=%f max=%f",
              combined_denom.GetNbinsX(), combined_denom.GetXaxis().GetXmin(),
              combined_denom.GetXaxis().GetXmax())

    combined_eff = ROOT.TGraphAsymmErrors(combined_num.th1, combined_denom.th1)

    log.debug("WTF")

    data_fit_func = object_info['function']
    setup_func_pars(data_fit_func)

    data_fit_func.SetLineColor(ROOT.EColor.kRed)
    data_fit_func.SetLineWidth(3)

    log.info("Fitting")

    ############################################################################
    ### Fit using regular ROOT  ################################################
    ############################################################################

    log.info("Fitting using ROOT")
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

    ############################################################################
    ### Fit using RooFit  ######################################################
    ############################################################################
    log.info("Fitting using RooFit")
    # following http://root.cern.ch/root/html/tutorials/roofit/rf701_efficiencyfit.C.html
    jet_pt = ROOT.RooRealVar("jetPt", "Jet Pt", 1, 0, 100, "GeV")
    # Fit function parameters
    scale = ROOT.RooRealVar("scale", "Landau Scale", 0.5, 0, 10)
    mu = ROOT.RooRealVar("mu", "Landau #mu", 10, 0, 100)
    sigma = ROOT.RooRealVar("sigma", "Landau #sigma", 1, 0, 10)
    constant = ROOT.RooRealVar("offset", "constant", 1.0e-2, 0, 1)

    roo_fit_func = ROOT.RooFormulaVar(
        "fake_rate", "Fake Rate", roo_fit_func_str,
        ROOT.RooArgList(scale, mu, sigma, constant, jet_pt))

    roo_cut = ROOT.RooCategory("cut", "cutr")
    roo_cut.defineType("accept", 1)
    roo_cut.defineType("reject", 0)

    roo_eff = ROOT.RooEfficiency("fake_rate_pdf", "Fake Rate",
                                 roo_fit_func, roo_cut, "accept")

    combined_fail = combined_denom - combined_num

    roo_pass = combined_num.makeRooDataHist(jet_pt)
    roo_fail = combined_fail.makeRooDataHist(jet_pt)

    roo_data = ROOT.RooDataHist(
        "data", "data",
        ROOT.RooArgList(jet_pt), ROOT.RooFit.Index(roo_cut),
        ROOT.RooFit.Import("accept", roo_pass),
        ROOT.RooFit.Import("reject", roo_fail),
    )

    fit_result = roo_eff.fitTo(
        roo_data, ROOT.RooFit.ConditionalObservables(ROOT.RooArgSet(jet_pt)),
        ROOT.RooFit.Save(True)
    )

    #fit_result.Print("v")


    roo_frame = jet_pt.frame(ROOT.RooFit.Title("Efficiency"))
    roo_data.plotOn(roo_frame, ROOT.RooFit.Efficiency(roo_cut))
    roo_fit_func.plotOn(roo_frame, ROOT.RooFit.LineColor(ROOT.EColor.kRed))

    fit_result_vars = fit_result.floatParsFinal()
    # Store the fit results for later
    object_result_vars = {}
    object_result['vars'] = object_result_vars
    object_result['raw_func'] = roo_fit_func_str
    fitted_fit_func = roo_fit_func_str.replace('jetPt', 'VAR')
    for var in ['scale', 'mu', 'sigma', 'offset']:
        value = fit_result_vars.find(var).getVal()
        object_result_vars[var] = value
        fitted_fit_func = fitted_fit_func.replace(var, '%0.4e' % value)
    object_result['fitted_func'] = fitted_fit_func

    keep = []

    for i in range(10):
        break
        log.info("Smearing parameters %i", i)
        smeared_pars = fit_result.randomizePars()
        # Create a non-owning list of arguments
        non_owned = ROOT.RooArgList(smeared_pars)
        non_owned.add(jet_pt)
        smeared_fit = ROOT.RooFormulaVar(
            "fake_rate_smeared_%i" % i, "Fake Rate", roo_fit_func_str,
            non_owned)
        smeared_fit.plotOn(roo_frame)
        keep.append((smeared_fit, smeared_pars))

    roo_frame.SetMinimum(1e-3)
    roo_frame.SetMaximum(1.0)

    roo_frame.Draw()

    canvas.Update()

    canvas.SetLogy(True)
    canvas.SaveAs("plots/combineFakeRates/%s_combined_eff_roofit.pdf" % object)

    ############################################################################
    ### Compare all regions to fitted fake rate  ###############################
    ############################################################################

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

# Save the files to an output json
with open('fake_rates.json', 'w') as json_file:
    json_file.write(json.dumps(fit_results, indent=4))

'''

Combine fake rates from many channels.

'''
import copy
import json
import logging
import sys

import ROOT
import FinalStateAnalysis.Utilities.styling as styling
from FinalStateAnalysis.Utilities.Histo import Histo

log = logging.getLogger("combineFR")
ch = logging.StreamHandler()
log.setLevel(logging.DEBUG)
log.addHandler(ch)

ROOT.gStyle.SetOptFit(0)

# Define the ROOT files that store the results
trilepton_fr_file = "results_fakeRates.root"
singlemu_fr_file = "results_singleMuFakeRates.root"

def get_histograms(file, data_set, fr_type):
    log.info("Getting %s:%s", data_set, fr_type)
    file = ROOT.TFile(file, "READ")
    denom = file.Get("_".join([data_set, fr_type, 'data_denom']))
    num = file.Get("_".join([data_set, fr_type, 'data_num']))
    log.info("Got numerator: %s", num.Integral())
    log.info("Got denominator: %s", denom.Integral())
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

#small_bins = range(0, 30, 2) + range(30, 60, 5) + range(60, 110, 10)
#med_bins = range(0, 30, 5) + range(30, 60, 10) + range(60, 120, 20)
#big_bins = range(0, 30, 5) + range(30, 40, 10) + range(40, 120, 20)
small_bins = 2
med_bins = 5
big_bins = 10

object_config = {
    'mu' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W',
                'file' : singlemu_fr_file,
                'histo' : 'mu',
                'rebin' : med_bins,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD',
                'file' : singlemu_fr_file,
                'histo' : 'muQCD',
                #'rebin' : 1,
                'rebin' : med_bins,
                'exclude' : True,
            },
            'TriLep_ZMM' : {
                'title' : 'Z',
                'file' : trilepton_fr_file,
                'histo' : 'mu',
                #'rebin' : 5,
                'rebin' : big_bins,
            },
            #'TriLep_ZEE' : {
                #'title' : 'Zee + jet_{#mu} (Double Elec)',
                #'histo' : 'muZEE',
                #'rebin' : 5,
            #},
            ##'Trilep_TT' : {
                ##'title' : 'ttbar + jet_{#mu} (Double Mu)',
                ##'histo' : 'muTTbar',
                ##'rebin' : 5,
            ##},
            #'Trilep_QCD' : {
                #'title' : 'QCD (Double Mu)',
                #'histo' : 'muQCD',
                #'rebin' : 5,
                #'exclude' : True,
            #},
        },
        #'rebin' : 2,
        'rebin' : med_bins,
        'comb_label' : 'W+Z',
        'fit_label' : 'EWK Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'muQCD' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W',
                'file' : singlemu_fr_file,
                'histo' : 'mu',
                'rebin' : 5,
                'exclude' : True,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD',
                'file' : singlemu_fr_file,
                'histo' : 'muQCD',
                'rebin' : med_bins,
            },
            'TriLep_ZMM' : {
                'title' : 'Z',
                'file' : trilepton_fr_file,
                'histo' : 'mu',
                'rebin' : 5,
                'exclude' : True,
            },
            'TriLep_ZEE' : {
                'title' : 'Zee',
                'file' : trilepton_fr_file,
                'histo' : 'muZEE',
                'exclude' : True,
                'rebin' : 5,
            },
            #'Trilep_TT' : {
                #'title' : 'ttbar + jet_{#mu} (Double Mu)',
                #'histo' : 'muTTbar',
                #'rebin' : 5,
                #'exclude' : True,
            #},
            'Trilep_QCD' : {
                'title' : 'QCD',
                'file' : trilepton_fr_file,
                'histo' : 'muQCD',
                'rebin' : 5,
            },
        },
        'rebin' : med_bins,
        'fit_label' : 'QCD Fit',
        'comb_label' : 'QCD',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'muHighPt' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W',
                'file' : singlemu_fr_file,
                'histo' : 'muHighPt',
                'rebin' : 5,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD',
                'file' : singlemu_fr_file,
                'histo' : 'muQCDHighPt',
                'rebin' : 5,
                'exclude' : True,
            },
        },
        'rebin' : 5,
        'comb_label' : 'W',
        'fit_label' : 'Combined Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'muHighPtQCDOnly' : {
        'scenarios' : {
            'SingleMu_QCD' : {
                'title' : 'QCD',
                'file' : singlemu_fr_file,
                'histo' : 'muQCDHighPt',
                'rebin' : 5,
                'exclude' : False,
            },
        },
        'rebin' : 5,
        'comb_label' : 'QCD',
        'fit_label' : 'QCD Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #mu fake rate',
    },
    'eMIT' : {
        'scenarios' : {
            'SingleMu_Wjets' : {
                'title' : 'W',
                'file' : singlemu_fr_file,
                'histo' : 'eMIT',
                'rebin' : 5,
            },
            'SingleMu_QCD' : {
                'title' : 'QCD',
                'file' : singlemu_fr_file,
                'histo' : 'eQCDMIT',
                'rebin' : 2,
                'exclude' : True,
            },
            'TriLep_ZMM' : {
                'title' : 'Z',
                'file' : trilepton_fr_file,
                'histo' : 'eMuEG',
                'rebin' : 10,
                'exclude' : False,
            },
        },
        'rebin' : 5,
        'comb_label' : 'W',
        'fit_label' : 'Wjets Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow e fake rate',
    },
    'eMITQCD' : {
        'scenarios' : {
            'SingleMu_QCD' : {
                'title' : 'QCD',
                'file' : singlemu_fr_file,
                'histo' : 'eQCDMIT',
                'rebin' : med_bins,
                'exclude' : False,
            },
        },
        'rebin' : med_bins,
        'comb_label' : 'QCD',
        'fit_label' : 'QCD Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow e fake rate',
    },
    'tau' : {
        'scenarios' : {
            'TriLep_ZMM' : {
                'title' : 'Z',
                'file' : trilepton_fr_file,
                'histo' : 'tau',
                'rebin' : 2,
                'exclude' : False,
            },
            'TriLep_AntiIsoMM' : {
                'title' : 'QCD',
                'file' : trilepton_fr_file,
                'histo' : 'tauQCD',
                'rebin' : 2,
                'exclude' : True,
            },
            'SingleMu_Wjets' : {
                'title' : 'W',
                'file' : singlemu_fr_file,
                'histo' : 'tau',
                'rebin' : 2,
                'exclude' : False,
            },
        },
        'rebin' : 2,
        'comb_label' : 'W+Z',
        'fit_label' : 'W+Z Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #tau fake rate',
    },
    'tauQCD' : {
        'scenarios' : {
            'TriLep_AntiIsoMM' : {
                'title' : 'QCD',
                'file' : trilepton_fr_file,
                'histo' : 'tauQCD',
                'rebin' : 2,
                'exclude' : False,
            },
            'TriLep_ZMM' : {
                'title' : 'Z',
                'file' : trilepton_fr_file,
                'histo' : 'tau',
                'rebin' : 2,
                'exclude' : True,
            },
        },
        'comb_label' : 'QCD',
        'rebin' : 2,
        'fit_label' : 'QCD Fit',
        'function' : fit_func,
        'label' : 'Jet #rightarrow #tau fake rate',
    },
}

# Hack to split by eta
for object in list(object_config.keys()):
    log.info("Modifying %s to split in eta", object)
    for type in ['barrel', 'endcap']:
        copy_object_info = copy.deepcopy(object_config[object])
        #copy_object_info['scenarios'] = copy_object_info['scenarios'].copy()
        scenarios = copy_object_info['scenarios']
        for scenario, scenario_info in scenarios.iteritems():
            scenario_info['histo'] = scenario_info['histo']  + '_' + type
        object_config[object + '_' + type] = copy_object_info
        log.info("Added %s", object + '_' + type)


# Store the fit results so we can put them in a json at the end
fit_results = {}
canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
frame = ROOT.TH1F("frame", "Fake rate", 100, 0, 100)
frame.GetXaxis().SetTitle("Jet p_{T}")
frame.SetMinimum(1e-3)
frame.SetMaximum(1.0)

# Fit function parameters
jet_pt = ROOT.RooRealVar("jetPt", "Jet Pt", 1, 0, 100, "GeV")

for object, object_info in object_config.iteritems():
    object_result = {}
    object_result['types'] = {}
    fit_results[object] = object_result
    log.info("Computing fake rates for object: %s", object)
    scenarios = object_info['scenarios']

    combined_denom = None
    combined_num = None

    for type, type_info in scenarios.iteritems():
        log.info("Getting fake rates for object: %s type: %s", object, type)
        num, denom = get_histograms(type_info['file'], '2011AB', type_info['histo'])
        object_result['types'][type] = {
            'num' : num.Integral(),
            'denom' : denom.Integral(),
        }

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
        fail = denom - num

        # Build the roo data hists
        roo_pass = num.makeRooDataHist(jet_pt)
        roo_fail = fail.makeRooDataHist(jet_pt)

        type_info['data_pass'] = roo_pass
        type_info['data_fail'] = roo_fail

    canvas.SetLogy(True)

    log.info("Computing combined efficiency")

    print combined_num.GetNbinsX()
    print combined_num.GetXaxis().GetXmin()
    print combined_num.GetXaxis().GetXmax()

    combined_num = Histo(combined_num.th1, rebin=object_info['rebin'])
    combined_denom = Histo(combined_denom.th1, rebin=object_info['rebin'])

    log.info("Fitting")


    ############################################################################
    ### Fit using RooFit  ######################################################
    ############################################################################
    log.info("Fitting using RooFit")
    # following http://root.cern.ch/root/html/tutorials/roofit/rf701_efficiencyfit.C.html

    scale = ROOT.RooRealVar("scale", "Landau Scale", 0.5, 0, 10)
    mu = ROOT.RooRealVar("mu", "Landau #mu", 10, 0, 100)
    sigma = ROOT.RooRealVar("sigma", "Landau #sigma", 1, 0.5, 10)
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
        ROOT.RooFit.Save(True),
        ROOT.RooFit.PrintLevel(-1)
    )

    fit_result_vars = fit_result.floatParsFinal()
    # Store the fit results for later
    object_result_vars = {}
    object_result['combined_denom'] = combined_denom.Integral()
    object_result['combined_num'] = combined_num.Integral()
    object_result['combined_eff'] = object_result['combined_num']/\
            object_result['combined_denom']

    object_result['vars'] = object_result_vars
    object_result['fit_status'] = fit_result.status()
    object_result['raw_func'] = roo_fit_func_str
    fitted_fit_func = roo_fit_func_str.replace('jetPt', 'VAR')
    for var in ['scale', 'mu', 'sigma', 'offset']:
        value = fit_result_vars.find(var).getVal()
        object_result_vars[var] = value
        fitted_fit_func = fitted_fit_func.replace(var, '%0.4e' % value)
    object_result['fitted_func'] = fitted_fit_func

    roo_frame = jet_pt.frame(ROOT.RooFit.Title("Efficiency"))

    def plot_func_on(frame, func, sigmas, scale_var_sys, plot_band=True):
        ''' A stupid function to do all the plotting for the function '''
        curves = {}
        if plot_band:
            func.plotOn(frame, ROOT.RooFit.LineColor(ROOT.EColor.kBlack),
                        ROOT.RooFit.VisualizeError(fit_result, sigmas),
                        ROOT.RooFit.FillColor(styling.colors['ewk_yellow'].code),
                       )
        curves['band'] = frame.findObject("fake_rate_Norm[jetPt]_errorband")
        func.plotOn(frame, ROOT.RooFit.LineColor(ROOT.EColor.kBlack))
        # Get the last added curve, which is the "plain" function.
        curves['nom'] = frame.findObject("fake_rate_Norm[jetPt]")

        # For multiplicative systematic
        scale_var_sys_up = 1 + scale_var_sys
        scale_var_sys_down = 1 - scale_var_sys

        scale.setVal(scale.getVal()*scale_var_sys_up)
        constant.setVal(constant.getVal()*scale_var_sys_up)

        roo_fit_func.plotOn(
            roo_frame,
            ROOT.RooFit.LineColor(styling.colors['ewk_purple'].code),
            ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed),
            #ROOT.RooFit.LineWidth(1),
        )
        curves['scale'] = frame.findObject("fake_rate_Norm[jetPt]")
        scale.setVal(scale.getVal()*scale_var_sys_down/scale_var_sys_up)
        constant.setVal(constant.getVal()*scale_var_sys_down/scale_var_sys_up)
        roo_fit_func.plotOn(
            roo_frame,
            ROOT.RooFit.LineColor(styling.colors['ewk_purple'].code),
            ROOT.RooFit.LineStyle(ROOT.RooFit.kDashed),
            #ROOT.RooFit.LineWidth(1),
        )
        # Restore state
        scale.setVal(scale.getVal()/scale_var_sys_down)
        constant.setVal(constant.getVal()/scale_var_sys_down)

        # Give good title
        frame.GetYaxis().SetTitle("Fake rate")
        frame.GetXaxis().SetTitle("Jet p_{T}")

        return curves

    scale_err = 30 # percent

    curves = plot_func_on(roo_frame, roo_fit_func, 1, scale_err/100.)

    roo_data.plotOn(roo_frame, ROOT.RooFit.Efficiency(roo_cut))
    curves['data'] = roo_frame.findObject('h_data_Eff[cut]')

    roo_frame.SetMinimum(3e-3)
    roo_frame.SetMaximum(1.0)
    roo_frame.Draw()

    left_edge = 0.60
    bottom_edge = 0.60
    divider = 0.88
    right_edge = 0.95
    top_edge = 0.95

    label_pos = [left_edge, divider, right_edge, top_edge, "NDC"]
    legend_pos = [left_edge, bottom_edge, right_edge, divider, "", "NDC"]

    label = ROOT.TPaveText(*label_pos)
    label.SetBorderSize(1)
    label.SetFillColor(ROOT.EColor.kWhite)
    label.AddText(object_info['label'])
    label.Draw()

    legend = ROOT.TLegend(*legend_pos)
    legend.SetBorderSize(1)
    legend.SetFillColor(ROOT.EColor.kWhite)
    legend.AddEntry(curves['data'], object_info['comb_label'] + " events", "p")
    legend.AddEntry(curves['nom'], object_info['comb_label'] + " fit", "l")
    legend.AddEntry(curves['band'], "1#sigma fit error", "f")
    legend.AddEntry(curves['scale'], "#pm %i%%" % scale_err, "l")
    legend.Draw()
    canvas.Update()
    canvas.SetLogy(True)
    canvas.SaveAs("plots/combineFakeRates/%s_combined_eff_roofit.pdf" % object)

    ############################################################################
    ### Compare all regions to fitted fake rate  ###############################
    ############################################################################

    for type, type_info in scenarios.iteritems():

        roo_frame = jet_pt.frame(ROOT.RooFit.Title("Efficiency"))
        roo_data = ROOT.RooDataHist(
            "data", "data",
            ROOT.RooArgList(jet_pt), ROOT.RooFit.Index(roo_cut),
            ROOT.RooFit.Import("accept", type_info['data_pass']),
            ROOT.RooFit.Import("reject", type_info['data_fail']),
        )
        plot_func_on(roo_frame, roo_fit_func, 1, scale_err/100., False)
        roo_data.plotOn(roo_frame, ROOT.RooFit.Efficiency(roo_cut))
        roo_frame.SetMinimum(3e-3)
        roo_frame.SetMaximum(1.0)
        roo_frame.Draw()

        label = ROOT.TPaveText(*label_pos)
        label.SetBorderSize(1)
        label.SetFillColor(ROOT.EColor.kWhite)
        label.AddText(object_info['label'])
        label.Draw()

        legend = ROOT.TLegend(*legend_pos)
        legend.SetBorderSize(1)
        legend.SetFillColor(ROOT.EColor.kWhite)
        legend.AddEntry(curves['data'], type_info['title'] + " events", "p")
        legend.AddEntry(curves['nom'], object_info['comb_label'] + " fit", "l")
        #legend.AddEntry(curves['band'], "1#sigma fit error", "f")
        legend.AddEntry(curves['scale'], "#pm %i%%" % scale_err, "l")
        legend.Draw()

        #eff.GetHistogram().GetXaxis().SetTitle("Jet p_{T}")
        canvas.SetLogy(True)
        canvas.SaveAs("plots/combineFakeRates/%s_%s_eff.pdf" % (object, type))
        canvas.SetLogy(False)
        canvas.SaveAs("plots/combineFakeRates/%s_%s_eff_lin.pdf" % (object, type))

# Save the files to an output json
with open('fake_rates.json', 'w') as json_file:
    json_file.write(json.dumps(fit_results, indent=4))

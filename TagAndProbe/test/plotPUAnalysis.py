import ROOT
import FinalStateAnalysis.Utilities.roottools as tools
import FinalStateAnalysis.Utilities.styling as styling
import os
import sys

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)

wjets_file = ROOT.TFile("pu_data/WplusJets_madgraph.root")
zjets_file = ROOT.TFile("pu_data/Zjets_M50.root")
data_file = ROOT.TFile("pu_data/all_data.root")

wjets_tree = wjets_file.Get("wjets/final/Ntuple")
zjets_tree = zjets_file.Get("ztt/final/Ntuple")
data_tree = data_file.Get("wjets/final/Ntuple")

# Get all the data runs
data_runs = {}

# Get our hacked version of lumiCalc
lumi_file = open(os.path.join(os.environ['CMSSW_BASE'],
                              'src', 'FinalStateAnalysis', 'Utilities',
                              'test', 'inst_lumis.txt'), 'r')
for line in lumi_file.readlines():
    line = line.replace(':', ',')
    run, inst, total = line.split(',')
    run = int(run)
    inst = float(inst)
    total = float(total)
    data_runs[run] = {
        'inst' : inst,
        'total' : total
    }
# Now add our data ntuples
for directory in tools.ls_by_type(data_file.Get("wjets/runs"), ROOT.TDirectory):
    run = int(directory.GetName())
    if run not in data_runs:
        print "WTF", run
        continue
    ntuple = directory.Get("final/Ntuple")
    assert(ntuple)
    data_runs[run]['ntuple'] = ntuple

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

# Make a histogram of the inst. lumi.
lumi_histo = ROOT.TH1F("LumiHisto", "Instantaneous Luminosity in 2011",
                       30, 0, 3000)

lumi_histo.GetXaxis().SetTitle("Instantaneous Luminosity (#mu b/s)")
lumi_histo.GetYaxis().SetTitle("Recorded Integrated Luminosity (pb)")
lumi_histo2011B = lumi_histo.Clone()
lumi_histo2011B.SetTitle("Instantaneous Luminosity in 2011B only")

for run, run_info in data_runs.iteritems():
    if 'ntuple' in run_info:
        lumi_histo.Fill(run_info['inst'], run_info['total']/1e6)
        if run > 176800:
            lumi_histo2011B.Fill(run_info['inst'], run_info['total']/1e6)

lumi_histo.Draw()
canvas.SaveAs("pu_plots/instLumi.pdf")

lumi_histo2011B.Draw()
canvas.SaveAs("pu_plots/instLumi2011B.pdf")

wjets_tree.Draw("rho>>htemp")
htemp = ROOT.gDirectory.Get("htemp")
htemp.SetTitle("#rho in W+jets MC")
htemp.GetXaxis().SetTitle("#rho")
htemp.Draw()
canvas.SaveAs("mc_w_rho.pdf")

data_tree.Draw("rho>>htemp")
htemp = ROOT.gDirectory.Get("htemp")
htemp.SetTitle("#rho in W+jets data")
htemp.GetXaxis().SetTitle("#rho")
htemp.Draw()
canvas.SaveAs("data_w_rho.pdf")

runs = sorted([key for key, value in data_runs.iteritems() if 'ntuple' in value])
print runs
lumi_history = ROOT.TH1F("LumiHistory", "Instantaneous Luminosity in 2011",
                       len(runs), 0, len(runs))
lumi_history.GetXaxis().SetTitle("Run")
lumi_history.GetYaxis().SetTitle("Instantaneous Luminosity")

for i, run in enumerate(runs):
    lumi_history.SetBinContent(i+1, data_runs[run]['inst'])
    if i % 10 == 0:
        lumi_history.GetXaxis().SetBinLabel(i+1, str(run))
    else:
        lumi_history.GetXaxis().SetBinLabel(i+1, '')

lumi_history.SetMarkerStyle(20)
lumi_history.Draw("lp")
canvas.SaveAs("pu_plots/instLumiHistor.pdf")

def make_efficiency(tree, numerator, denominator, cut, variable, binning):
    tree.Draw(variable + ">>htemp_den(%s)" % ",".join(binning),
              "(%s) && (%s)" % (denominator, cut))
    denom = ROOT.gDirectory.Get("htemp_den")
    tree.Draw(variable + ">>htemp_num(%s)" % ",".join(binning),
              "(%s) && (%s) && (%s)" % (numerator, denominator, cut))
    num = ROOT.gDirectory.Get("htemp_num")
    print num, denom
    assert(denom)
    assert(num)
    return ROOT.TGraphAsymmErrors(num, denom)

def make_efficiency_by_run_data(data_dict, min, max, numerator, denominator, cut, variable, binning):
    first = True
    for run, run_info in data_dict.iteritems():
        if 'ntuple' not in run_info:
            continue
        if run_info['inst'] < min or run_info['inst'] > max:
            continue

        tree = run_info['ntuple']

        if not first:
            tree.Draw(variable + ">>+htemp_den",
                      "(%s) && (%s)" % (denominator, cut))
            tree.Draw(variable + ">>+htemp_num",
                      "(%s) && (%s) && (%s)" % (numerator, denominator, cut))
        else:
            tree.Draw(variable + ">>htemp_den(%s)" % ",".join(binning),
                      "(%s) && (%s)" % (denominator, cut))
            tree.Draw(variable + ">>htemp_num(%s)" % ",".join(binning),
                      "(%s) && (%s) && (%s)" % (numerator, denominator, cut))


        first = False

    denom = ROOT.gDirectory.Get("htemp_den")
    num = ROOT.gDirectory.Get("htemp_num")
    print num, denom
    assert(denom)
    assert(num)
    return ROOT.TGraphAsymmErrors(num, denom)


# Make ZTT efficiencies
mc_puScenarios = {
    'low' : {
        'cut' : 'nSim < 5',
        'label' : '1 < N^{sim}_{vtx} < 5',
        'color' : styling.colors['ewk_orange'],
    },
    'med' : {
        'cut' : ' 5 <= nSim && nSim < 10',
        'label' : '5 < N^{sim}_{vtx} < 10',
        'color' : styling.colors['ewk_red'],
    },
    'high' : {
        'cut' : ' 10 < nSim',
        'label' : '10 < N^{sim}_{vtx}',
        'color' : styling.colors['ewk_purple'],
    },
}

data_puScenarios = {
    'low' : {
        'min' : 0,
        'max' : 1200,
        'label' : 'L < 1200 [#mub/s]',
        'color' : styling.colors['ewk_orange'],
    },
    'med' : {
        'min' : 1200,
        'max' : 1700,
        'label' : '1200 < L < 1700 [#mub/s]',
        'color' : styling.colors['ewk_red'],
    },
    'high' : {
        'min' : 1700,
        'max' : 1e9,
        'label' : '1700 < L [#mub/s]',
        'color' : styling.colors['ewk_purple'],
    },
}


either_puScenarios = {
    'low' : {
        'cut' : 'rho < 4',
        'label' : '#rho < 4',
        'color' : styling.colors['ewk_orange'],
    },
    'med' : {
        'cut' : ' 4 <= rho && rho < 8',
        'label' : '4 < #rho < 8',
        'color' : styling.colors['ewk_red'],
    },
    'high' : {
        'cut' : '8 < rho && rho < 10',
        'label' : '8 < #rho < 10',
        'color' : styling.colors['ewk_purple'],
    },
    'vhigh' : {
        'cut' : ' 10 < rho',
        'label' : '10 < #rho',
        'color' : styling.colors['ewk_light_purple'],
    },
}

ztt_denominator = 'genDecayMode > -1'
the_vars = [('pt', 'Reco. tau p_{T}', ['20', '0', '100']), ('abs(eta)', '|#eta|', ['25', '0', '2.5'])]
numerators = [
    'byVLooseCombinedIsolationDeltaBetaCorr',
    'byLooseCombinedIsolationDeltaBetaCorr',
    'byMediumCombinedIsolationDeltaBetaCorr',
    'byTightCombinedIsolationDeltaBetaCorr',
    'byVLooseIsolation',
    'byLooseIsolation',
    'byMediumIsolation',
    'byTightIsolation'
]

for var, var_name, binning in the_vars:
    continue
    for numerator in numerators:
        print 'ztt', var, numerator
        multigraph = ROOT.TMultiGraph("ztt_eff", "Z#tau#tau Efficiency")
        numerator_w_pt = numerator + '&& pt > 15'
        legend = ROOT.TLegend(0.6, 0.15, 0.85, 0.4, "", "brNDC")
        legend.SetFillStyle(0)
        for scenario, scenario_info in mc_puScenarios.iteritems():
            eff = make_efficiency(zjets_tree, numerator_w_pt, ztt_denominator,
                                  scenario_info['cut'], var, binning)
            eff.SetMarkerStyle(20)
            eff.SetMarkerColor(scenario_info['color'].code)
            legend.AddEntry(eff, scenario_info['label'])
            multigraph.Add(eff, "pe")
        canvas.Clear()
        multigraph.Draw('axis')
        multigraph.GetXaxis().SetTitle(var_name)
        legend.Draw()
        multigraph.SetMinimum(1e-4)
        multigraph.SetMaximum(1.0)
        canvas.SaveAs('pu_plots/' +  '_'.join(['ztt', numerator, var]) + '.pdf')

the_vars = [('jetpt', 'Reco. jet p_{T}', ['20', '0', '100']), ('abs(eta)', '|#eta|', ['25', '0', '2.5'])]
canvas.SetLogy(True)
wjets_denominator = 'jetpt > 20'
for var,var_name,  binning in the_vars:
    continue
    for numerator in numerators:
        multigraph = ROOT.TMultiGraph("wjets_eff", "W+jets Fake Rate")
        numerator_w_pt = numerator + '&& pt > 15'
        legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85, "", "brNDC")
        legend.SetFillStyle(0)
        for scenario, scenario_info in mc_puScenarios.iteritems():
            eff = make_efficiency(wjets_tree, numerator_w_pt, wjets_denominator,
                                  scenario_info['cut'], var, binning)
            eff.SetMarkerStyle(20)
            eff.SetMarkerColor(scenario_info['color'].code)
            legend.AddEntry(eff, scenario_info['label'])
            multigraph.Add(eff, "pe")
        canvas.Clear()
        multigraph.Draw('axis')
        multigraph.GetXaxis().SetTitle(var_name)
        legend.Draw()
        multigraph.SetMinimum(1e-3)
        multigraph.SetMaximum(5e-1)
        canvas.SaveAs('pu_plots/' +  '_'.join(['w_mc', numerator, var]) + '.pdf')


canvas.SetLogy(True)
wjets_denominator = 'jetpt > 20'
for var, var_name, binning in the_vars:
    continue
    for numerator in numerators:
        multigraph = ROOT.TMultiGraph("wjets_eff", "W+jets Fake Rate")
        numerator_w_pt = numerator + '&& pt > 15'
        legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85, "", "brNDC")
        legend.SetFillStyle(0)
        for scenario, scenario_info in data_puScenarios.iteritems():
            eff = make_efficiency_by_run_data(
                data_runs, scenario_info['min'], scenario_info['max'],
                numerator_w_pt, wjets_denominator, '1', var, binning)
            eff.SetMarkerStyle(20)
            eff.SetMarkerColor(scenario_info['color'].code)
            legend.AddEntry(eff, scenario_info['label'])
            multigraph.Add(eff, "pe")
        canvas.Clear()
        multigraph.Draw('axis')
        multigraph.GetXaxis().SetTitle(var_name)
        legend.Draw()
        multigraph.SetMinimum(1e-3)
        multigraph.SetMaximum(5e-1)
        canvas.SaveAs('pu_plots/' +  '_'.join(['w_data', numerator, var]) + '.pdf')

for (type, ntuple) in [('mc', wjets_tree), ('data', data_tree)]:
    continue
    for var, var_name, binning in the_vars:
        for numerator in numerators:
            multigraph = ROOT.TMultiGraph("wjets_eff", "W+jets Fake Rate")
            numerator_w_pt = numerator + '&& pt > 15'
            legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85, "", "brNDC")
            legend.SetFillStyle(0)
            for scenario, scenario_info in either_puScenarios.iteritems():
                eff = make_efficiency(ntuple, numerator_w_pt, wjets_denominator,
                                      scenario_info['cut'], var, binning)
                eff.SetMarkerStyle(20)
                eff.SetMarkerColor(scenario_info['color'].code)
                legend.AddEntry(eff, scenario_info['label'])
                multigraph.Add(eff, "pe")
                canvas.Clear()
                multigraph.Draw('axis')
                multigraph.GetXaxis().SetTitle(var_name)
                legend.Draw()
                multigraph.SetMinimum(1e-3)
                multigraph.SetMaximum(5e-1)
                canvas.SaveAs('pu_plots/' +  '_'.join(['w_vs_rho', type, numerator, var]) + '.pdf')

canvas.SetLogy(False)
for var, var_name, binning in the_vars:
    for numerator in numerators:
        multigraph = ROOT.TMultiGraph("wjets_eff", "Data-MC/Data")
        numerator_w_pt = numerator + '&& pt > 15'
        legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85, "", "brNDC")
        legend.SetFillStyle(0)
        for scenario, scenario_info in either_puScenarios.iteritems():
            mc_eff = make_efficiency(wjets_tree, numerator_w_pt, wjets_denominator,
                                     scenario_info['cut'], var, binning)
            data_eff = make_efficiency(data_tree, numerator_w_pt, wjets_denominator,
                                       scenario_info['cut'], var, binning)
            eff = ROOT.TGraph(mc_eff.GetN())
            for n in range(0, mc_eff.GetN()):
                x = mc_eff.GetXaxis().GetBinCenter(n+1)
                mc_val = mc_eff.Eval(x)
                data_val = data_eff.Eval(x)
                val = 0
                if data_val > 0:
                    val = (mc_val - data_val)/(data_val)
                eff.SetPoint(n, x, val)

            eff.SetMarkerStyle(20)
            eff.SetMarkerColor(scenario_info['color'].code)
            legend.AddEntry(eff, scenario_info['label'])
            multigraph.Add(eff, "p")
            canvas.Clear()
            multigraph.Draw('axis')
            multigraph.GetXaxis().SetTitle(var_name)
            multigraph.GetYaxis().SetTitle('DATA-MC/DATA')
            legend.Draw()
            multigraph.SetMinimum(-1.0)
            multigraph.SetMaximum(1.0)
            canvas.SaveAs('pu_plots/' +  '_'.join(['w_vs_rho_data_mc', type, numerator, var]) + '.pdf')

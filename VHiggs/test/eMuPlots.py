import ROOT
import os
import sys
import glob
import logging
import math
from FinalStateAnalysis.Utilities.AnalysisPlotter import styling,samplestyles
from FinalStateAnalysis.PatTools.datadefs import datadefs

logging.basicConfig(filename='example.log',level=logging.DEBUG)
log = logging.getLogger("plotting")
h1 = logging.StreamHandler(sys.stdout)
h1.level = logging.INFO
log.addHandler(h1)

logging.getLogger("AnalysisPlotter").addHandler(h1)

h2 = logging.StreamHandler(sys.stderr)
h2.level = logging.DEBUG
#logging.getLogger("ROOTCache").addHandler(h2)

ROOT.gROOT.SetBatch(True)
#ROOT.gROOT.SetStyle("Plain")
#ROOT.gStyle.SetOptFit(11111)
ROOT.SetMemoryPolicy( ROOT.kMemoryStrict )

from data import build_data

skips =[ 'EM', 'MuPt5', 'TauPlusX', '2011B', 'SingleMu', 'DoubleEl', 'MuHad']
samples, plotter = build_data('2011-10-17-v2-WHAnalyze', 'scratch_results', 2140, skips)

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)
def saveplot(filename):
    filename = filename.replace('/', '')
    filetype = '.pdf'
    canvas.SetLogy(False)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'eMu', filename + filetype))
    canvas.SetLogy(True)
    canvas.Update()
    canvas.Print(os.path.join("plots", 'eMu',
                               filename + '_log' + filetype))

selections = {
    'kine' :
    '((Mu17Ele8_HLT > 0.5 && ElecPt > 10 && MuPt > 20) || '
    '(Mu8Ele17_HLT > 0.5 && ElecPt > 20 && MuPt > 10)) && '
    ' MuAbsEta < 2.1 && ElecAbsEta < 2.5',

    'os_em' :
    'MuCharge*ElecCharge < 0',

    'ss_em' :
    'MuCharge*ElecCharge > 0',

    'mu_iso' :
    'Mu_MuRelIso < 0.3',

    'e_iso' :
    'Elec_ERelIso < 0.3',

    'hps_pass' :
    'Tau_LooseHPS > 0.5',

    'hps_fail' :
    'Tau_LooseHPS < 0.5',

    'ttbar_enriched' :
    'NBjetsPt20_Nbjets > 0',

    'mu_veto' :
    'NIsoMuonsPt5_Nmuons < 0.5',

    'b_veto' :
    'NBjetsPt20_Nbjets < 0.5',

    'ht_cut' :
    'FinalState_Ht > 80',
}

tauPt_fr_weight = '(((0.013318 + 0.185314*exp(-0.064584*TauPt)))/(1-(0.013318 + 0.185314*exp(-0.064584*TauPt))))'
fr_weight_cmd = '(%s && Tau_LooseHPS < 0.5)*(' + tauPt_fr_weight + ')'
jetPt_fr = '(0.009659 + 18.071184*exp(-0.125145*TauJetPt))'

regions = {
    'os_fr_region' : ['kine', 'os_em', 'mu_iso', 'e_iso'],
    'os_fr_region_ttbar' : ['kine', 'os_em', 'mu_iso', 'e_iso', 'ttbar_enriched'],
    'ss_fr_region' : ['kine', 'ss_em', 'mu_iso', 'e_iso'],
    'ss_fr_super_region' : ['kine', 'ss_em', 'mu_iso', 'e_iso', 'mu_veto', 'b_veto', 'ht_cut'],
    'os_final_region' : ['kine', 'os_em', 'mu_iso', 'e_iso', 'hps_pass'],
    'os_final_region_ttbar' : ['kine', 'os_em', 'mu_iso', 'e_iso', 'hps_pass', 'ttbar_enriched'],
    'ss_final_super_region' : ['kine', 'ss_em', 'mu_iso', 'e_iso', 'hps_pass', 'mu_veto', 'b_veto', 'ht_cut'],
}

variables = [
    ('NBjetsPt20_Nbjets', 'N_{b-jets}', [10, -0.5, 9.5]),
    ('Leg2Leg3_Mass', 'M_{#mu#tau}', [100, 0, 300]),
    ('Leg1Leg2_Mass', 'M_{e#tau}', [100, 0, 300]),
    ('Leg1_MtToMET', 'M_{T} e-MET', [100, 0, 300]),
    ('Leg2_MtToMET', 'M_{T} #mu-MET', [100, 0, 300]),
    ('TauJetPt', 'Tau Jet p_{t}', [100, 0, 200]),
    ('TauPt', 'Tau p_{t}', [100, 0, 200]),
    ('METPt',  'MET', [100, 0, 200]),
    ('vtxChi2/vtxNDOF', 'Vertex #chi^{2}/NDOF', [100, 0, 30]),
    ('NIsoMuonsPt5_Nmuons', 'N_{#mu}', [10, -0.5, 9.5]),
    ('NIsoElecPt5_Nelectrons', 'N_{e}', [10, -0.5, 9.5]),
    ('NjetsPt20_Njets', 'N_{jets}', [10, -0.5, 9.5]),
    #('MEtPt', 'MET', [100, 0, 200]),
    ('FinalState_Ht', 'H_{T}', [100, 0, 300])]


mc_legend = plotter.build_legend(
    '/mmt/final/SS/finalState/Leg1Leg2_Mass',
    include = ['*'],
    exclude = ['data*', 'VH*']
)

for variable, var_name, binning in variables:
    for region, selection_list in regions.iteritems():
        selection = " && ".join("(%s)" % selections[x] for x in selection_list)
        name = "_".join([region, variable])
        plotter.register_tree(
            name,
            '/emt/final/Ntuple',
            variable,
            selection,
            w = 'puWeight',
            binning = binning,
            #include = ['Zj*', '*DoubleMu*'],
            include = ['*'],
        )
        rebin = 10 if not variable.startswith('N') else 1
        stack = plotter.build_stack(
            '/emt/final/Ntuple:%s' % name,
            include = ['*'],
            exclude = ['*data*'],
            title = "",
            rebin = rebin,
            show_overflows=True,
        )
        data = plotter.get_histogram(
            'data_MuEG', '/emt/final/Ntuple:%s' % name,
            rebin = rebin,
            show_overflows=True,
        )
        stack.Draw()
        data.Draw("pe,same")
        stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.4)
        stack.GetXaxis().SetTitle(var_name)
        mc_legend.Draw()
        saveplot(name)

        if 'fr' in region:
            fr_name = name + 'FR'
            plotter.register_tree(
                name + 'FR',
                '/emt/final/Ntuple',
                variable,
                fr_weight_cmd % selection,
                w = 'puWeight',
                binning = binning,
                #include = ['Zj*', '*DoubleMu*'],
                include = ['*'],
            )


# Make the final plots corrected using FR method
for variable, var_name, binning in variables:
    for final_region in [x for x in regions if 'final' in x]:
        fr_region = final_region.replace('final', 'fr')
        # Get FR data
        final_name = '_'.join([final_region, variable])
        fr_name = '_'.join([fr_region, variable]) + 'FR'

        rebin = 10 if not variable.startswith('N') else 1

        data_fr = plotter.get_histogram(
            'data_MuEG', '/emt/final/Ntuple:%s' % fr_name,
            rebin = rebin,
            show_overflows=True,
        )
        data_final = plotter.get_histogram(
            'data_MuEG', '/emt/final/Ntuple:%s' % final_name,
            rebin = rebin,
            show_overflows=True,
        )

        wz_fr = plotter.get_histogram(
            'WZ', '/emt/final/Ntuple:%s' % fr_name,
            rebin = rebin,
            show_overflows=True,
        )
        wz_final = plotter.get_histogram(
            'WZ', '/emt/final/Ntuple:%s' % final_name,
            rebin = rebin,
            show_overflows=True,
        )
        wz_corrected = wz_final - wz_fr

        zz_fr = plotter.get_histogram(
            'ZZ', '/emt/final/Ntuple:%s' % fr_name,
            rebin = rebin,
            show_overflows=True,
        )
        zz_final = plotter.get_histogram(
            'ZZ', '/emt/final/Ntuple:%s' % final_name,
            rebin = rebin,
            show_overflows=True,
        )
        zz_corrected = zz_final - zz_fr

        stack = ROOT.THStack("FR_predictions", "Final e#mu#tau selections 2.1 fb^{-1}")
        stack.Add(zz_corrected.th1, 'hist')
        stack.Add(wz_corrected.th1, 'hist')
        styling.apply_style(data_fr, **samplestyles.SAMPLE_STYLES['ztt'])
        stack.Add(data_fr.th1, 'hist')

        signal = plotter.get_histogram(
            'VH115', '/emt/final/Ntuple:%s' % final_name,
            rebin = rebin,
            show_overflows=True,
        )
        signal = signal * 5
        #signal.SetFillColor(0)
        signal.SetLineWidth(2)
        stack.Add(signal.th1, 'hist')

        stack.Draw()
        #signal.Draw("same,hist")
        data_final.Draw('pe,same')
        stack.SetMaximum(max(stack.GetMaximum(), data.GetMaximum())*1.5)
        stack.GetXaxis().SetTitle(var_name)

        legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85, "", "brNDC")
        legend.AddEntry(zz_corrected.th1, "ZZ", 'lf')
        legend.AddEntry(wz_corrected.th1, "WZ", 'lf')
        legend.AddEntry(data_fr.th1, "Fakes", 'lf')
        legend.AddEntry(signal.th1, "VH(115) #times 5", 'lf')
        legend.SetFillStyle(0)
        legend.Draw()

        #data_fr.Draw('hist, same')
        saveplot(final_name + "fr_method")


# Compute tau fake rate in ttbar control region
tau_pt_denominator = plotter.get_histogram(
    'data_MuEG', '/emt/final/Ntuple:%s' % 'os_fr_region_ttbar_TauPt',
    rebin = 10,
            show_overflows=True,
)

tau_pt_numerator = plotter.get_histogram(
    'data_MuEG', '/emt/final/Ntuple:%s' % 'os_final_region_ttbar_TauPt',
    rebin = 10,
            show_overflows=True,
)

tau_pt_fake_rate = ROOT.TGraphAsymmErrors(
    tau_pt_numerator.th1, tau_pt_denominator.th1)
tau_pt_fake_rate.Draw("ape")
tau_pt_fake_rate.GetHistogram().GetXaxis().SetTitle("Tau p_{T}")
tau_pt_fake_rate.GetHistogram().SetTitle("Tau Isolation Fake Rate vs. tau p_{T} in ttbar")
tau_pt_fake_rate.GetHistogram().SetMaximum(0.2)
zmm_pt_fake_rate_func = ROOT.TF1('zmm_fr', "(0.013318 + 0.185314*exp(-0.064584*TauPt))".replace('TauPt', 'x'), 0, 200)
zmm_pt_fake_rate_func.SetLineColor(ROOT.EColor.kRed)
zmm_pt_fake_rate_func.Draw('same')
saveplot('ttbar_fakerate_tau_pt')


# Compute tau jet ptfake rate in ttbar control region
tau_jetpt_denominator = plotter.get_histogram(
    'data_MuEG', '/emt/final/Ntuple:%s' % 'os_fr_region_ttbar_TauJetPt',
    rebin = 10,
            show_overflows=True,
)

tau_jetpt_numerator = plotter.get_histogram(
    'data_MuEG', '/emt/final/Ntuple:%s' % 'os_final_region_ttbar_TauJetPt',
    rebin = 10,
            show_overflows=True,
)

tau_jetpt_fake_rate = ROOT.TGraphAsymmErrors(
    tau_jetpt_numerator.th1, tau_jetpt_denominator.th1)
tau_jetpt_fake_rate.Draw("ape")
tau_jetpt_fake_rate.GetHistogram().GetXaxis().SetTitle("Jet p_{T}")
tau_jetpt_fake_rate.GetHistogram().SetTitle("Tau Isolation Fake Rate vs. jet p_{T} in ttbar")
tau_jetpt_fake_rate.GetHistogram().SetMaximum(0.2)
zmm_jetpt_fake_rate_func = ROOT.TF1('zmm_jet_fr',jetPt_fr.replace('TauJetPt', 'x'), 0, 200)
zmm_jetpt_fake_rate_func.SetLineColor(ROOT.EColor.kRed)
zmm_jetpt_fake_rate_func.Draw('same')
saveplot('ttbar_fakerate_tau_jetpt')

#### BUILD DATA CARD
label = 'Leg2Leg3_Mass'
final_name = 'ss_final_super_region_%s' % label
fr_name = 'ss_fr_super_region_%sFR' % label
unweighted_name = 'ss_fr_super_region_%s' % label
rebin = 10

data_fr = plotter.get_histogram(
    'data_MuEG', '/emt/final/Ntuple:%s' % fr_name,
    rebin = rebin,
            show_overflows=True,
)
data_final = plotter.get_histogram(
    'data_MuEG', '/emt/final/Ntuple:%s' % final_name,
    rebin = rebin,
            show_overflows=True,
)
data_unweighted = plotter.get_histogram(
    'data_MuEG', '/emt/final/Ntuple:%s' % unweighted_name,
    rebin = rebin,
            show_overflows=True,
)

wz_fr = plotter.get_histogram(
    'WZ', '/emt/final/Ntuple:%s' % fr_name,
    rebin = rebin,
            show_overflows=True,
)
wz_final = plotter.get_histogram(
    'WZ', '/emt/final/Ntuple:%s' % final_name,
    rebin = rebin,
            show_overflows=True,
)
wz_corrected = wz_final - wz_fr

zz_fr = plotter.get_histogram(
    'ZZ', '/emt/final/Ntuple:%s' % fr_name,
    rebin = rebin,
            show_overflows=True,
)
zz_final = plotter.get_histogram(
    'ZZ', '/emt/final/Ntuple:%s' % final_name,
    rebin = rebin,
            show_overflows=True,
)
zz_corrected = zz_final - zz_fr


output = ROOT.TFile("emt_shapes.root", 'RECREATE')

for mass in [110, 115, 120, 125]:
    channel_dir = output.mkdir("emt_%i" % mass)
    channel_dir.cd()
    data_final.Write("data_obs")
    data_fr.Write("fakes")
    data_unweighted.Write("ext_data_unweighted")
    wz_corrected.Write("wz")
    zz_corrected.Write("zz")
    print "Getting signal for mass", mass
    signal = plotter.get_histogram(
        'VH%s' % mass, '/emt/final/Ntuple:%s' % final_name,
        rebin = rebin, show_overflows=True,
    )
    signal.Write("signal")

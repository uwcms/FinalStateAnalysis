import ROOT
import math
import sys

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)

import FinalStateAnalysis.TagAndProbe.fit.DataReader as DataReader
import FinalStateAnalysis.TagAndProbe.fit.plotting as plotting

ztt_data = DataReader.DataReader('ZTT',  "../data/Ztautau_pythia.root", 'Z#tau#tau')
qcd_data = DataReader.DataReader('QCD', "../data/PPmuXptGt20Mu15.root", "QCD")
wjets_data = DataReader.DataReader('Wjets', "../data/WplusJets_madgraph.root", "QCD")
data_data = DataReader.DataReader('data', "../data/all_data.root", "Data")

variable = "LogDCASig3D"
var_max = 4
x = ROOT.RooRealVar(variable, "log(DCA Significance)", 0, var_max)
eta = ROOT.RooRealVar("AbsTauEta", "AbsTauEta", 0, 0, 2.5)
pt = ROOT.RooRealVar("TauPt", "TauPt", 0, 0, 100)
pzeta = ROOT.RooRealVar("PZeta", "PZeta", 0, -20, 50)
mvis = ROOT.RooRealVar("Mvis", "Mvis", 50, 0, 200)

for fit_var, fit_var_name in [
    (x, variable),
    (eta, "TauEta"),
    (pzeta, "PZeta"),
    (pt, "TauPt"),
    (mvis, "Mvis"), ]:
    # Compare the shapes we are using to make sure it makes sense
    wjets_compare_shape, junk = plotting.compare_shapes(
        wjets_data, ("wjets", "SS"), ("sig", "OS"), fit_var)
    wjets_compare_shape.SetTitle("W+jets shape template comparison (%s)" %
                                fit_var_name)
    wjets_compare_shape.Draw()
    canvas.SaveAs("wjets_control_shape_extraction_%s.png" % fit_var_name)

    wjets_compare_shape, junk = plotting.compare_shapes(
        wjets_data, ("sigPass", "OS"), ("sigFail", "OS"), fit_var)
    wjets_compare_shape.SetTitle("W+jets shape template comparison (%s)" %
                                 fit_var_name)
    wjets_compare_shape.Draw()
    canvas.SaveAs("wjets_control_shape_sig_region_%s.png" % fit_var_name)

    qcd_compare_shape, junk = plotting.compare_shapes(
        qcd_data, ("sigFail", "SS"), ("sigFail", "OS"), fit_var, rebin=5)
    qcd_compare_shape.SetTitle("QCD shape template comparison (%s)" %
                               fit_var_name)
    qcd_compare_shape.Draw()
    canvas.SaveAs("qcd_control_shape_extraction_%s.png" % fit_var_name)

    qcd_compare_shape, junk = plotting.compare_shapes(
        qcd_data, ("sigPass", "OS"), ("sigFail", "OS"), fit_var, rebin=5)
    qcd_compare_shape.SetTitle("QCD shape template comparison (%s)" %
                              fit_var_name)
    qcd_compare_shape.Draw()
    canvas.SaveAs("qcd_control_shape_sig_region_%s.png" % fit_var_name)

    # Check getting pass and fail distributions for Wjets
    wjets_compare_shape, junk = plotting.compare_shapes(
        wjets_data, ("wjetsPass", "SS"), ("sigPass", "SS"), fit_var, rebin=5)
    wjets_compare_shape.SetTitle("W+jets shape template comparison (%s)" %
                                fit_var_name)
    wjets_compare_shape.Draw()
    canvas.SaveAs("wjets_control_shape_extraction_passOnly_%s.png" % fit_var_name)

    wjets_compare_shape, junk = plotting.compare_shapes(
        wjets_data, ("wjets", "SS"), ("sigFail", "OS"), fit_var, rebin=5)
    wjets_compare_shape.SetTitle("W+jets shape template comparison (%s)" %
                                fit_var_name)
    wjets_compare_shape.Draw()
    canvas.SaveAs("wjets_control_shape_extraction_failOnly_%s.png" % fit_var_name)

    # QCD extraction from Anti-Iso sideband
    qcd_compare_shape, junk = plotting.compare_shapes(
        qcd_data, ("qcdFail", "SS"), ("sigFail", "OS"), fit_var, rebin=10)
    qcd_compare_shape.SetTitle("QCD shape template comparison (%s)" %
                               fit_var_name)
    qcd_compare_shape.Draw()
    canvas.SaveAs("qcd_control_shape_extraction_failOnly_%s.png" % fit_var_name)

    qcd_compare_shape, junk = plotting.compare_shapes(
        qcd_data, ("qcdPass", "SS"), ("sigPass", "OS"), fit_var, rebin=10)
    qcd_compare_shape.SetTitle("QCD shape template comparison (%s)" %
                               fit_var_name)
    qcd_compare_shape.Draw()
    canvas.SaveAs("qcd_control_shape_extraction_passOnly_%s.png" % fit_var_name)

    ztt_compare_shape, junk = plotting.compare_shapes(
        ztt_data, ("sigPass", "OS"), ("sigFail", "OS"), fit_var, rebin=1)
    ztt_compare_shape.SetTitle("ztt shape template comparison (%s)" %
                              fit_var_name)
    ztt_compare_shape.Draw()
    canvas.SaveAs("ztt_control_shape_sig_region_%s.png" % fit_var_name)

    # Compare shapes between samples
    ztt_qcd_shape_compare, junk = plotting.compare_samples(
        ztt_data, qcd_data,
        ("sigPass", "OS"), ("sigPass", "OS"),
        fit_var, rebin = 5)
    ztt_qcd_shape_compare.SetTitle("ZTT/QCD passing shape template comparison %s" %
                                   fit_var_name)
    ztt_qcd_shape_compare.Draw()
    canvas.SaveAs("ztt_qcd_compare_shape_%s.png" % fit_var_name)

    ztt_wjets_shape_compare, junk = plotting.compare_samples(
        ztt_data, wjets_data,
        ("sigPass", "OS"), ("sigPass", "OS"),
        fit_var, rebin = 5)
    ztt_wjets_shape_compare.SetTitle("ZTT/Wjets passing shape template comparison %s" %
                                   fit_var_name)
    ztt_wjets_shape_compare.Draw()
    canvas.SaveAs("ztt_wjets_compare_shape_%s.png" % fit_var_name)

    ztt_qcd_shape_compare, junk = plotting.compare_samples(
        ztt_data, qcd_data,
        ("sigFail", "OS"), ("sigFail", "OS"),
        fit_var, rebin = 5)
    ztt_qcd_shape_compare.SetTitle("ZTT/QCD failing shape template comparison %s" %
                                   fit_var_name)
    ztt_qcd_shape_compare.Draw()
    canvas.SaveAs("ztt_qcd_compare_shape_fail_%s.png" % fit_var_name)

    ztt_wjets_shape_compare, junk = plotting.compare_samples(
        ztt_data, wjets_data,
        ("sigFail", "OS"), ("sigFail", "OS"),
        fit_var, rebin = 5)
    ztt_wjets_shape_compare.SetTitle("ZTT/Wjets failing shape template comparison %s" %
                                   fit_var_name)
    ztt_wjets_shape_compare.Draw()
    canvas.SaveAs("ztt_wjets_compare_shape_fail_%s.png" % fit_var_name)

    to_comp_samples = [ztt_data, qcd_data, wjets_data]

    pass_shape_compare, junk = plotting.compare_samples3(
        to_comp_samples, ("sigPass", "OS"), fit_var, rebin=5
    )
    pass_shape_compare.SetTitle("Shape comparison OS Passing (%s)" % fit_var_name)
    pass_shape_compare.Draw()
    canvas.SaveAs("pass_shape_compare_%s.png" % fit_var_name)

    fail_shape_compare, junk = plotting.compare_samples3(
        to_comp_samples, ("sigFail", "OS"), fit_var, rebin=5
    )
    fail_shape_compare.SetTitle("Shape comparison OS Failing (%s)" % fit_var_name)
    fail_shape_compare.Draw()
    canvas.SaveAs("fail_shape_compare_%s.png" % fit_var_name)


# Now let's do the QCD shape extraction
# Figure out how much data is in the PZeta
n_wjets_pzeta_ss = wjets_data.th1("wjets", "SS", x.GetName()).Integral()
n_wjets_sigfail_ss = wjets_data.th1("sigFail", "SS", x.GetName()).Integral()

wjets_extrapolation_factor = n_wjets_sigfail_ss/n_wjets_pzeta_ss
print "Wjets extrapolation:", wjets_extrapolation_factor

n_data_pzeta_ss = data_data.th1("wjets", "SS", x.GetName()).Integral()
print "Data in Pzeta SS sideband:", n_data_pzeta_ss
print "Expected W-jets contribution to SigFailed SS", \
        n_data_pzeta_ss*wjets_extrapolation_factor

#### Make QCD template

qcd_template = data_data.th1(
    "sigFail", "SS", x.GetName(), rebin=1).Clone()
print "Intial QCD template has %f entries" % qcd_template.Integral()
qcd_template.Draw()
current_max = qcd_template.GetMaximum()
canvas.SaveAs("initial_qcd_template.png")

wjets_side_band = data_data.th1(
    "wjets", "SS", x.GetName(), rebin=1).Clone()
wjets_side_band.Scale(-1*wjets_extrapolation_factor)
wjets_side_band.Draw()
canvas.SaveAs("wjets_correction.png")

qcd_template.Add(wjets_side_band)
qcd_template.Draw()
qcd_template.SetMaximum(current_max)
qcd_template.SetMinimum(0)
canvas.SaveAs("final_qcd_template.png")

class PseudoTFile(object):
    # Class that has the same Get(...) interface as a TFile
    def __init__(self):
        self.objects = {}
    def Get(self, item):
        return self.objects[item]

corr_qcd_data = DataReader.DataReader('CorrQCD', "", "Corrected QCD")
corr_qcd_tfile = PseudoTFile()
corr_qcd_tfile.objects['ohyeah/sigFailSS/%s' % x.GetName()] = qcd_template
corr_qcd_data.file = corr_qcd_tfile

#### OS - SS relationship for backgrounds
n_qcd_sig_os = qcd_data.th1("sig", "OS", x.GetName()).Integral()
n_qcd_sig_ss = qcd_data.th1("sig", "SS", x.GetName()).Integral()

n_qcd_qcd_os = qcd_data.th1("qcd", "OS", x.GetName()).Integral()
n_qcd_qcd_ss = qcd_data.th1("qcd", "SS", x.GetName()).Integral()

n_wjets_sig_os = wjets_data.th1("sig", "OS", x.GetName()).Integral()
n_wjets_sig_ss = wjets_data.th1("sig", "SS", x.GetName()).Integral()

n_wjets_wjets_os = wjets_data.th1("wjets", "OS", x.GetName()).Integral()
n_wjets_wjets_ss = wjets_data.th1("wjets", "SS", x.GetName()).Integral()

n_data_qcd_os = data_data.th1("qcd", "OS", x.GetName()).Integral()
n_data_qcd_ss = data_data.th1("qcd", "SS", x.GetName()).Integral()

n_data_wjets_os = data_data.th1("wjets", "OS", x.GetName()).Integral()
n_data_wjets_ss = data_data.th1("wjets", "SS", x.GetName()).Integral()

print "QCD Sig OS/SS =", n_qcd_sig_os/n_qcd_sig_ss
print "QCD Anti-Iso OS/SS =", n_qcd_qcd_os/n_qcd_qcd_ss
print "Data Anti-Iso OS/SS =", n_data_qcd_os/n_data_qcd_ss

print "WJets Sig OS/SS =", n_wjets_sig_os/n_wjets_sig_ss
print "WJets PZeta OS/SS =", n_wjets_wjets_os/n_wjets_wjets_ss
print "Data PZeta  OS/SS =", n_data_wjets_os/n_data_wjets_ss

n_data_sigPass_os = data_data.th1("sigPass", "OS", x.GetName()).Integral()
n_data_sigPass_ss = data_data.th1("sigPass", "SS", x.GetName()).Integral()
n_data_sigFail_os = data_data.th1("sigFail", "OS", x.GetName()).Integral()
n_data_sigFail_ss = data_data.th1("sigFail", "SS", x.GetName()).Integral()

#### Build PDFs

rebin_for_fit = 8

# Now build our templates
wjets_pdf = data_data.histPdf("wjets", "SS", x, rebin_for_fit)
qcd_pdf = corr_qcd_data.histPdf("sigFail", "SS", x, rebin_for_fit)
ztt_pass_pdf = ztt_data.histPdf("sigPass", "OS", x, rebin_for_fit)
ztt_fail_pdf = ztt_data.histPdf("sigFail", "OS", x, rebin_for_fit)

n_wjets_pass_os = ROOT.RooRealVar(
    "n_wjets_pass_os",
    "Number of Wjets in passing OS sample",
    n_data_sigPass_os*0.1, 1, n_data_sigPass_os)

n_qcd_pass_os = ROOT.RooRealVar(
    "n_qcd_pass_os",
    "Number of QCD in passing OS sample",
    n_data_sigPass_os*0.1, 1, n_data_sigPass_os)

n_wjets_fail_os = ROOT.RooRealVar(
    "n_wjets_fail_os",
    "Number of Wjets in failing OS sample",
    n_data_sigFail_os*0.1, 1, n_data_sigFail_os)

n_qcd_fail_os = ROOT.RooRealVar(
    "n_qcd_fail_os",
    "Number of QCD in failing OS sample",
    n_data_sigFail_os*0.6, 1, n_data_sigFail_os)

# Extrapolation into SS
n_wjets_pass_ss = ROOT.RooFormulaVar(
    "n_wjets_pass_ss",
    "Extrapolated # of Wjets in passing SS sample",
    "@0*%f" % (n_data_wjets_ss/n_data_wjets_os),
    ROOT.RooArgList(n_wjets_pass_os)
)

n_qcd_pass_ss = ROOT.RooFormulaVar(
    "n_qcd_pass_ss",
    "Extrapolated # of QCD in passing SS sample",
    #"[0]*%f" % (n_data_qcd_ss/n_data_qcd_os),
    "@0*%f" % (n_data_qcd_ss/n_data_qcd_os),
    ROOT.RooArgList(n_qcd_pass_os)
)

print n_qcd_pass_ss.getVal()

# Define the fit model for the signal
n_ztt_total = ROOT.RooRealVar(
    "n_ztt_total",
    "Total amount of all ZTT",
    n_data_sigPass_os, 1,
    n_data_sigPass_os + n_data_sigPass_ss + n_data_sigFail_os
)

ztt_efficiency = ROOT.RooRealVar(
    "ztt_efficiency",
    "Tau ID efficiency",
    0.6, 0, 1.0)

ztt_charge_misid = ROOT.RooRealVar(
    "ztt_charge_misid",
    "Tau Charge MisID",
    0.05, 0, 1.0)

n_ztt_pass_os = ROOT.RooFormulaVar(
    "n_ztt_pass_os",
    "Number of ZTT in the OS passed region",
    "@0*@1*(1-@2)",
    ROOT.RooArgList(n_ztt_total, ztt_efficiency, ztt_charge_misid)
)

n_ztt_pass_ss = ROOT.RooFormulaVar(
    "n_ztt_pass_ss",
    "Number of ZTT in the SS passed region",
    "@0*@1*@2",
    ROOT.RooArgList(n_ztt_total, ztt_efficiency, ztt_charge_misid)
)

n_ztt_fail_os = ROOT.RooFormulaVar(
    "n_ztt_pass_os",
    "Number of ZTT in the OS failed region",
    "@0*(1-@1)",
    ROOT.RooArgList(n_ztt_total, ztt_efficiency)
)

pdf_pass_os = ROOT.RooAddPdf(
    "pdf_pass_os",
    "OS Passing PDF",
    ROOT.RooArgList(ztt_pass_pdf, qcd_pdf, wjets_pdf),
    ROOT.RooArgList(n_ztt_pass_os, n_qcd_pass_os, n_wjets_pass_os),
)

pdf_fail_os = ROOT.RooAddPdf(
    "pdf_fail_os",
    "OS Failling PDF",
    ROOT.RooArgList(ztt_fail_pdf, qcd_pdf, wjets_pdf),
    ROOT.RooArgList(n_ztt_fail_os, n_qcd_fail_os, n_wjets_fail_os),
)

pdf_pass_ss = ROOT.RooAddPdf(
    "pdf_pass_ss",
    "SS Passing PDF",
    ROOT.RooArgList(ztt_pass_pdf, qcd_pdf, wjets_pdf),
    ROOT.RooArgList(n_ztt_pass_ss, n_qcd_pass_ss, n_wjets_pass_ss),
)

categories = ROOT.RooCategory("categories", "categories")
categories.defineType("pass_os")
categories.defineType("fail_os")
categories.defineType("pass_ss")

data_hist_pass_os = data_data.dataHist("sigPass", "OS", x, rebin_for_fit)
data_hist_pass_ss = data_data.dataHist("sigPass", "SS", x, rebin_for_fit)
data_hist_fail_os = data_data.dataHist("sigFail", "OS", x, rebin_for_fit)

combo_data = ROOT.RooDataHist(
    "comboData", "combined data",
    ROOT.RooArgList(x),
    ROOT.RooFit.Index(categories),
    ROOT.RooFit.Import("pass_os", data_hist_pass_os),
    ROOT.RooFit.Import("fail_os", data_hist_fail_os),
    ROOT.RooFit.Import("pass_ss", data_hist_pass_ss),
)

sim_pdf = ROOT.RooSimultaneous("sim_pdf", "simultaneous pdf", categories)
sim_pdf.addPdf(pdf_pass_os, "pass_os")
sim_pdf.addPdf(pdf_pass_ss, "pass_ss")
sim_pdf.addPdf(pdf_fail_os, "fail_os")

#sim_pdf.printCompactTree()
sim_pdf.fitTo(combo_data, ROOT.RooFit.Extended())

# Plot outputs
widescreen = ROOT.TCanvas("asdf", "asdf", 1200, 400)
widescreen.Divide(3)

legend = ROOT.TLegend(0.55, 0.55, 0.9, 0.9)
legend.SetFillStyle(0)

pass_os_frame = x.frame()
data_hist_pass_os.plotOn(pass_os_frame)
pdf_pass_os.plotOn(pass_os_frame)
pdf_pass_os.plotOn(
    pass_os_frame,
    ROOT.RooFit.LineColor(ROOT.EColor.kRed),
    ROOT.RooFit.FillColor(ROOT.EColor.kRed),
    ROOT.RooFit.FillStyle(2),

    ROOT.RooFit.Components(
        ",".join(x.GetName() for x in [qcd_pdf, wjets_pdf])
    )
)
legend.AddEntry(pass_os_frame.getObject(0), "Data", "p")
legend.AddEntry(pass_os_frame.getObject(1), "Z#tau#tau + Bkg", "l")
legend.AddEntry(pass_os_frame.getObject(2), "Bkg Only", "l")
widescreen.cd(1)
pass_os_frame.SetTitle("OS Passing Tau ID")
pass_os_frame.GetYaxis().SetTitle("")
pass_os_frame.Draw()
legend.Draw()

fail_os_frame = x.frame()
data_hist_fail_os.plotOn(fail_os_frame)
pdf_fail_os.plotOn(fail_os_frame)
pdf_fail_os.plotOn(
    fail_os_frame,
    ROOT.RooFit.LineColor(ROOT.EColor.kRed),
    ROOT.RooFit.Components(
        ",".join(x.GetName() for x in [qcd_pdf, wjets_pdf])
    )
)
fail_os_frame.SetTitle("OS Failing Tau ID")
fail_os_frame.GetYaxis().SetTitle("")
widescreen.cd(2)
fail_os_frame.Draw()

pass_ss_frame = x.frame()
data_hist_pass_ss.plotOn(pass_ss_frame)
pdf_pass_ss.plotOn(pass_ss_frame)
pdf_pass_ss.plotOn(
    pass_ss_frame,
    ROOT.RooFit.LineColor(ROOT.EColor.kRed),
    ROOT.RooFit.Components(
        ",".join(x.GetName() for x in [qcd_pdf, wjets_pdf])
    )
)
widescreen.cd(3)
pass_ss_frame.SetTitle("SS Failing Tau ID")
pass_ss_frame.GetYaxis().SetTitle("")
pass_ss_frame.Draw()

widescreen.SaveAs("fit_results.pdf")

z_data_sigPass_os = ztt_data.th1("sigPass", "OS", x.GetName()).Integral()
z_data_sigPass_ss = ztt_data.th1("sigPass", "SS", x.GetName()).Integral()

z_data_sigFail_os = ztt_data.th1("sigFail", "OS", x.GetName()).Integral()

print "True ID eff:", z_data_sigPass_os/(z_data_sigFail_os+z_data_sigPass_os)
print "True charge mis-ID:", z_data_sigPass_ss/(z_data_sigPass_ss + z_data_sigPass_os)

sys.exit(0)

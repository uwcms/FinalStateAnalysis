import ROOT
import math

ROOT.gROOT.SetStyle("Plain")

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)

samples = {
    'ZTT' : {
        'title' : 'Z#tau#tau',
        'file' : "Ztautau_pythia.root",
    },
    'QCD' : {
        'title' : 'QCD #mu Enriched',
        'file' : "PPmuXptGt20Mu15.root",
    },
    'Wjets' : {
        'title' : 'W+jets',
        'file' : "WplusJets_madgraph.root",
    },
    'data' : {
        'title' : 'Data',
        'file' : "all_data.root",
    },
}

variable = "LogDCASig3D"
var_max = 5

#variable = "Mvis"
#var_max = 200

x = ROOT.RooRealVar("x", "log(DCA Significance)", 0, var_max)

for sample, sample_info in samples.iteritems():
    sample_info['tfile'] = ROOT.TFile(sample_info['file'])

# Figure out W+jets scale factor (from pzeta sideband -> signal failed)

wjets_pzeta_ss = samples['Wjets']['tfile'].Get(
    "ohyeah/wjetsSS/%s" % variable)

wjets_signalfailed_ss = samples['Wjets']['tfile'].Get(
    "ohyeah/sigFailSS/%s" % variable)

wjets_scale_factor = wjets_signalfailed_ss.Integral()/wjets_pzeta_ss.Integral()
print "scale factor: ", wjets_scale_factor

# Now get the wjets template from data
data_pzeta_ss = samples['data']['tfile'].Get(
    "ohyeah/wjetsSS/%s" % variable)

# Now get the initial QCD template from data
data_signalfailed_ss = samples['data']['tfile'].Get(
    "ohyeah/sigFailSS/%s" % variable)

th1_qcd_template = data_signalfailed_ss.Clone()

# The two histograms to fit
data_signalfailed_os = samples['data']['tfile'].Get(
    "ohyeah/sigFailOS/%s" % variable)

data_signalpass_os = samples['data']['tfile'].Get(
    "ohyeah/sigPassOS/%s" % variable)

# The ZTT signal
ztt_signalfailed_os = samples['ZTT']['tfile'].Get(
    "ohyeah/sigFailOS/%s" % variable)

ztt_signalpass_os = samples['ZTT']['tfile'].Get(
    "ohyeah/sigPassOS/%s" % variable)

# Now we need to subtract the estimated W+jets in the QCD template
th1_qcd_template.Add(data_pzeta_ss, -1*wjets_scale_factor)

rebin_factor = 4

data_signalpass_os.Rebin(rebin_factor)
data_signalfailed_os.Rebin(rebin_factor)
data_pzeta_ss.Rebin(rebin_factor)

ztt_signalpass_os.Rebin(rebin_factor)
ztt_signalfailed_os.Rebin(rebin_factor)
th1_qcd_template.Rebin(rebin_factor)


# To be fitted
data_hist_failed = ROOT.RooDataHist("data", "Failed Tau ID",
                                    ROOT.RooArgList(x), data_signalfailed_os)

data_hist_passed = ROOT.RooDataHist("data", "Pass Tau ID",
                                    ROOT.RooArgList(x), data_signalpass_os)

qcd_template = ROOT.RooDataHist("QCDTemp", "QCD Template",
                                    ROOT.RooArgList(x), th1_qcd_template)

wjets_template = ROOT.RooDataHist("WJTemp", "W+jets Template",
                                  ROOT.RooArgList(x), data_pzeta_ss)

ztt_passed_template = ROOT.RooDataHist("ZTTPassTemp", "Z#tau#tau Passed",
                                  ROOT.RooArgList(x), ztt_signalpass_os)

ztt_failed_template = ROOT.RooDataHist("ZTTFailTemp", "Z#tau#tau Failed",
                                  ROOT.RooArgList(x), ztt_signalfailed_os)

model_test_frame = x.frame()
qcd_template.plotOn(model_test_frame)
model_test_frame.Draw()
canvas.SaveAs("qcd_template.pdf")

qcd_pdf = ROOT.RooHistPdf("QCDPDF", "QCD Template",
                          ROOT.RooArgSet(x), qcd_template)

wjets_pdf = ROOT.RooHistPdf("WJetsPdf", "W+jets Template",
                            ROOT.RooArgSet(x), wjets_template)

ztt_pass_pdf = ROOT.RooHistPdf("ZTTpassPdf", "ZTT Pass PDF",
                            ROOT.RooArgSet(x), ztt_passed_template)

ztt_fail_pdf = ROOT.RooHistPdf("ZTTfailPdf", "ZTT Fail PDF",
                            ROOT.RooArgSet(x), ztt_failed_template)

qcd_pass_norm = ROOT.RooRealVar(
    "nQCDPassed", "Number of QCD in passing sample", 0.1, 0, 1.0)

qcd_fail_norm = ROOT.RooRealVar(
    "nQCDFailed", "Number of QCD in failing sample", 0.6, 0, 1.0)

wjets_pass_norm = ROOT.RooRealVar(
    "nWjetsPassed", "Number of Wjets in passing sample", 0.1, 0, 1.0)
wjets_fail_norm = ROOT.RooRealVar(
    "nWjetsFailed", "Number of Wjets in failing sample", 0.3, 0, 1.0)

ztt_pass_norm = ROOT.RooRealVar(
    "nZTTPassed", "Number of ZTT in passing sample", 0.5, 0, 1.0)
ztt_fail_norm = ROOT.RooRealVar(
    "nZTTFailed", "Number of ZTT in failing sample", 0.5, 0, 1.0)


total_pass_pdf = ROOT.RooAddPdf(
    "PassPdf", "Total passing PDF",
    ROOT.RooArgList(ztt_pass_pdf, qcd_pdf, wjets_pdf),
    #ROOT.RooArgList(qcd_pass_norm, wjets_pass_norm, ztt_pass_norm),
    #ROOT.RooArgList(qcd_pass_norm, wjets_pass_norm),
    ROOT.RooArgList(ztt_pass_norm, qcd_pass_norm),
    True
)

total_fail_pdf = ROOT.RooAddPdf(
    "FailPdf", "Total failing PDF",
    ROOT.RooArgList(ztt_fail_pdf, qcd_pdf, wjets_pdf),
    #ROOT.RooArgList(qcd_fail_norm, wjets_fail_norm, ztt_fail_norm),
    ROOT.RooArgList(ztt_fail_norm, qcd_fail_norm),
    True
)


pass_frame = x.frame()
data_hist_passed.plotOn(pass_frame)
total_pass_pdf.fitTo(data_hist_passed)
total_pass_pdf.plotOn(pass_frame)
total_pass_pdf.plotOn(
    pass_frame,
    #ROOT.RooFit.Components(ROOT.RooArgSet(qcd_pdf, wjets_pdf)),
    ROOT.RooFit.Components("QCDPDF,WJetsPdf"),
    ROOT.RooFit.LineColor(ROOT.EColor.kRed)
)

total_pass_pdf.plotOn(
    pass_frame,
    #ROOT.RooFit.Components(ROOT.RooArgSet(qcd_pdf, wjets_pdf)),
    ROOT.RooFit.Components("WJetsPdf"),
    ROOT.RooFit.LineColor(ROOT.EColor.kGreen)
)
pass_frame.Draw()
canvas.SaveAs("pass.pdf")
canvas.SetLogy(True)
canvas.Update()
canvas.SaveAs("pass_log.pdf")

fail_frame = x.frame()
data_hist_failed.plotOn(fail_frame)
total_fail_pdf.fitTo(data_hist_failed)
total_fail_pdf.plotOn(fail_frame)
total_fail_pdf.plotOn(
    fail_frame,
    #ROOT.RooFit.Components(ROOT.RooArgSet(qcd_pdf, wjets_pdf)),
    ROOT.RooFit.Components("QCDPDF,WJetsPdf"),
    ROOT.RooFit.LineColor(ROOT.EColor.kRed)
)

total_fail_pdf.plotOn(
    fail_frame,
    #ROOT.RooFit.Components(ROOT.RooArgSet(qcd_pdf, wjets_pdf)),
    ROOT.RooFit.Components("WJetsPdf"),
    ROOT.RooFit.LineColor(ROOT.EColor.kGreen)
)
fail_frame.Draw()
canvas.SetLogy(False)
canvas.SaveAs("fail.pdf")
canvas.SetLogy(True)
canvas.Update()
canvas.SaveAs("fail_log.pdf")

n_fit_failed = ztt_fail_norm.getVal()*data_signalfailed_os.Integral()
n_fit_passed = ztt_pass_norm.getVal()*data_signalpass_os.Integral()

n_fit_failed_error = ztt_fail_norm.getError()*data_signalfailed_os.Integral()
n_fit_passed_error = ztt_pass_norm.getError()*data_signalpass_os.Integral()

def quad(*args):
    return math.sqrt(sum(x*x for x in args))

denom = n_fit_failed + n_fit_passed
denom_error = quad(n_fit_passed_error, n_fit_failed_error)

denom_rel_error = denom_error/denom
num_rel_error = n_fit_passed_error/n_fit_passed
total_rel_error = quad(denom_rel_error, num_rel_error)

n_true_failed = ztt_signalfailed_os.Integral()
n_true_passed = ztt_signalpass_os.Integral()

print "Fit efficiency: %0.1f%%" %  (100*n_fit_passed/denom)
print "Fit error: %0.1f%%" % (100*n_fit_passed*total_rel_error/denom)

print "True efficiency: %0.1f%%" % (100*n_true_passed/(n_true_passed + n_true_failed))

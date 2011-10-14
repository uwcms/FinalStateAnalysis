from templates import get_th1
import FinalStateAnalysis.Utilities.HistoEqualizer as he
from FinalStateAnalysis.Utilities.Histo import Histo
import ROOT

rebin = 1

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetHistLineWidth(2)
ROOT.gStyle.SetHistLineStyle(1)

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)

qcd_qcd_os_pass = get_th1('qcd', 'qcdPassOS', 'Mvis', rebin)
qcd_qcd_os_fail = get_th1('qcd', 'qcdFailOS', 'Mvis', rebin)

qcd_qcd_ss_pass = get_th1('qcd', 'qcdPassSS', 'Mvis', rebin)
qcd_qcd_ss_fail = get_th1('qcd', 'qcdFailSS', 'Mvis', rebin)

data_qcd_os_pass = get_th1('data', 'qcdPassOS', 'Mvis', rebin)
data_qcd_os_fail = get_th1('data', 'qcdFailOS', 'Mvis', rebin)

qcd_qcd_pass = qcd_qcd_os_pass + qcd_qcd_ss_pass
qcd_qcd_fail = qcd_qcd_os_fail + qcd_qcd_ss_fail
tr_func = he.HistoEqualizer(qcd_qcd_fail, qcd_qcd_pass)

qcd_qcd_pass_prime = qcd_qcd_fail.transform(tr_func)

qcd_qcd_pass.SetLineColor(ROOT.EColor.kBlue)
qcd_qcd_pass_prime.SetLineColor(ROOT.EColor.kViolet)
qcd_qcd_fail.SetLineColor(ROOT.EColor.kRed)
qcd_qcd_pass_prime.SetLineWidth(2)
qcd_qcd_pass.SetLineWidth(2)
qcd_qcd_fail.SetLineWidth(2)

qcd_qcd_pass.DrawNormalized()
qcd_qcd_pass_prime.DrawNormalized('same')
data_qcd_os_pass.DrawNormalized('same')
qcd_qcd_fail.DrawNormalized('same')

canvas.SaveAs("qcd_antiIso_mvis.png")


qcd_sig_os_pass = get_th1('qcd', 'sigPassOS', 'Mvis', rebin)
qcd_sig_os_fail = get_th1('qcd', 'sigFailOS', 'Mvis', rebin)

qcd_sig_ss_pass = get_th1('qcd', 'sigPassSS', 'Mvis', rebin)
qcd_sig_ss_fail = get_th1('qcd', 'sigFailSS', 'Mvis', rebin)

qcd_sig_pass = qcd_sig_os_pass + qcd_sig_ss_pass
qcd_sig_fail = qcd_sig_os_fail + qcd_sig_ss_fail

qcd_sig_pass_prime = qcd_sig_fail.transform(tr_func)

qcd_sig_pass.SetLineColor(ROOT.EColor.kBlue)
qcd_sig_pass_prime.SetLineColor(ROOT.EColor.kViolet)
qcd_sig_fail.SetLineColor(ROOT.EColor.kRed)

qcd_sig_pass.SetLineWidth(2)
qcd_sig_pass_prime.SetLineWidth(2)
qcd_sig_fail.SetLineWidth(2)

qcd_sig_pass.Rebin(10)
qcd_sig_pass_prime.Rebin(10)
qcd_sig_fail.Rebin(10)

qcd_sig_pass.DrawNormalized()
qcd_sig_pass_prime.DrawNormalized('same')
qcd_sig_fail.DrawNormalized('same')

canvas.SaveAs("qcd_sig_mvis.png")

a = get_th1('qcd', 'qcdPassSS', 'PZeta', rebin)
b = get_th1('qcd', 'sigPassSS', 'PZeta', rebin)

a.SetLineColor(ROOT.EColor.kRed)
b.SetLineColor(ROOT.EColor.kBlue)

a.DrawNormalized()
b.DrawNormalized('same')

canvas.SaveAs("quick_test.png")



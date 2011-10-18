import ROOT

import data_sources

import templates
import model
import FinalStateAnalysis.Utilities.styling as styling

ws = ROOT.RooWorkspace("workspace")

fit_ss_fail = False

templates.build_fit_vars(ws)
templates.build_templates(ws)
model.build_model(ws, templates.get_initial_sizes(), fit_ss_fail)

pzeta = ws.var('pzeta')

frame = pzeta.frame()

ztt_fail_pdf = ws.pdf('pdf_ztt_os_fail_pzeta')
qcd_fail_pdf = ws.pdf('pdf_qcd_os_fail_pzeta')

print frame
print ztt_fail_pdf

ztt_fail_pdf.plotOn(frame, ROOT.RooFit.LineColor(styling.colors['ewk_purple'].code))
qcd_fail_pdf.plotOn(frame, ROOT.RooFit.LineColor(styling.colors['ewk_red'].code))

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)
frame.Draw()
canvas.SaveAs("ztt_qcd_fail_shape_comp.pdf")

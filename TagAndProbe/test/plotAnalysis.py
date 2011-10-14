import ROOT

ROOT.gROOT.SetStyle("Plain")

samples = {
    'ZTT' : {
        'title' : 'Z#tau#tau',
        'file' : "ztt.root",
    },
    'QCD' : {
        'title' : 'QCD #mu Enriched',
        'file' : "qcd.root",
    },
    'Wjets' : {
        'title' : 'W+jets',
        'file' : "wjets.root",
    },
}

canvas = ROOT.TCanvas("as", "asdf", 800, 600)

stack = ROOT.THStack("stack", "stack")
legend = ROOT.TLegend(0.6, 0.6, 0.85, 0.85, "", "brNDC")
legend.SetBorderSize(0)
legend.SetFillStyle(0)

keep = []

color = 1

def get_overflow_bin(histo):
    overflow = histo.GetBinContent(histo.GetNbinsX()+1)
    current = histo.GetBinContent(histo.GetNbinsX())
    histo.SetBinContent(histo.GetNbinsX(), current + overflow)

for sample, sample_info in samples.iteritems():
    file = ROOT.TFile(sample_info['file'])
    sample_info['tfile'] = file

    #histo = file.Get("ohyeah/DCASig3D")
    histo = file.Get("ohyeah/DCASig23D")
    get_overflow_bin(histo)
    histo.Rebin(4)
    sample_info['histo'] = histo
    histo.GetXaxis().SetRangeUser(0.0, 20.0)
    histo.Scale(1.0/histo.Integral())
    histo.SetTitle(sample_info['title'])
    histo.GetXaxis().SetTitle("#mu-#tau track DCA significance")
    histo.GetXaxis().CenterTitle()
    histo.SetMinimum(1e-4)
    histo.SetMaximum(4e-1)
    canvas.SetLogy(False)
    histo.Draw()
    canvas.SaveAs(sample + ".pdf")
    canvas.SetLogy(True)
    canvas.SaveAs(sample + "_log.pdf")
    histo.SetLineColor(color)
    histo.SetLineWidth(2)
    stack.Add(histo, "hist")
    legend.AddEntry(histo, sample_info['title'], "l")
    keep.append(histo)
    color += 1
    if color == 3:
        color += 1

for histo in keep:
    print histo

canvas.Clear()
stack.Draw("nostack")
stack.GetXaxis().SetTitle("#mu-#tau track DCA significance")
stack.SetTitle('')
legend.Draw()

canvas.SetLogy(False)
canvas.SaveAs("summary.pdf")
canvas.SetLogy(True)
canvas.SaveAs("summary_log.pdf")


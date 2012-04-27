# Get the ROOT libraries
import ROOT
# For more information, look up "PyROOT"

# Always do this, it makes everything look less terrible.
ROOT.gROOT.SetStyle("Plain")

# Build TChains with all of the data for wjets
print "Making wjets chain"
wjets = ROOT.TChain('mmt/final/Ntuple') # mtt/.. is the path to the ntpule of interest
# Add all the data files

print wjets.Add('/hdfs/store/user/efriis/2012-04-23-Higgs/WplusJets_madgraph/1/*')

print "Making signal M(120) chain"
# Build the TChain for the signal
signal_120 = ROOT.TChain('mmt/final/Ntuple')
print signal_120.Add('/hdfs/store/user/efriis/2012-04-23-Higgs/VH_120/1/*')

# Make a histogram of leading tau PT
wjets_tau1_pt = ROOT.TH1F("wjets_tau1_pt", "p_{T} of #tau_{1} in W+jets",
                          100, 0, 100)
signal_tau1_pt = ROOT.TH1F("signal_tau1_pt", "p_{T} of #tau_{1} in W+jets",
                           100, 0, 100)

# Loop over Wjets events
print "looping over Wjets events"
for event_num, event in enumerate(wjets):
    if event_num % 1000 == 0:
        print "processing event %i" % event_num
    if event_num > 100000:
        # Don't process everything
        break
    wjets_tau1_pt.Fill(event.tPt)


print "looping over signal events"
for event_num, event in enumerate(signal_120):
    if event_num % 1000 == 0:
        print "processing event %i" % event_num
    if event_num > 100000:
        # Don't process everything
        break
    signal_tau1_pt.Fill(event.tPt)

# Plot the histograms
canvas = ROOT.TCanvas("the_name_doesnt_matter", "neither does the title", 800, 600)

# Normalize the shapes to 1
if wjets_tau1_pt.Integral():
	wjets_tau1_pt.Scale(1.0/wjets_tau1_pt.Integral())
if signal_tau1_pt.Integral():
	signal_tau1_pt.Scale(1.0/signal_tau1_pt.Integral())

wjets_tau1_pt.SetLineColor(ROOT.EColor.kBlue)
signal_tau1_pt.SetLineColor(ROOT.EColor.kRed)

# GOOD PLOTSPERSONSHIP
wjets_tau1_pt.GetXaxis().SetTitle("Leading #tau p_{T} (GeV)")
# Arbitrary units (since both are normalized to 1)
wjets_tau1_pt.GetYaxis().SetTitle("a.u.")
legend = ROOT.TLegend(0.6, 0.6, 0.95, 0.95, "", "brNDC")
legend.AddEntry(wjets_tau1_pt, "W+jets", "l")
legend.AddEntry(signal_tau1_pt, "WH(120)", "l")

# Compare the shapes
wjets_tau1_pt.Draw()
signal_tau1_pt.Draw('same')

legend.Draw()

canvas.SaveAs("tau_pt_comparison.jpg")

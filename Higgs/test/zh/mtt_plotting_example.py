# Get the ROOT libraries
import ROOT
# For more information, look up "PyROOT"

# Always do this, it makes everything look less terrible.
ROOT.gROOT.SetStyle("Plain")

zjets = ROOT.TChain('mtt/final/Ntuple')

print zjets.Add('/hdfs/store/user/efriis/2012-04-23-Higgs/Zjets_M50/2/*')

print "Making wjets chain"
wjets = ROOT.TChain('mtt/final/Ntuple') # mtt/.. is the path to the ntpule of interest
# Add all the data files

print wjets.Add('/hdfs/store/user/efriis/2012-04-23-Higgs/WplusJets_madgraph/1/*')

print "Making signal M(120) chain"
# Build the TChain for the signal
signal_120 = ROOT.TChain('mtt/final/Ntuple')
print signal_120.Add('/hdfs/store/user/efriis/2012-04-23-Higgs/VH_120/1/*')


# Make a histogram of leading tau PT
wjets_tau1_pt = ROOT.TH1F("wjets_tau1_pt", "Invariant #tau_{1} #tau_{2} Mass in W+jets",
                          20, 0, 200)
signal_tau1_pt = ROOT.TH1F("signal_tau1_pt", "Invariant #tau_{1} #tau_{2} Mass in W+jets",
                           20, 0, 200)
zjets_tau1_pt = ROOT.TH1F("zjets_tau1_pt", "Invariant #tau_{1} #tau_{2} Mass in W+jets",
                           20, 0, 200)


#wjets_tau1_pt = ROOT.TH2F("wjets_tau1_pt", "PZeta and PZetaVis",
 #                      25, -100, 100,25,0,100)
#signal_tau1_pt = ROOT.TH2F("signal_tau1_pt", "PZeta and PZetaVis",
 #                          25, -100, 100, 25, 0, 100)

#meta.m_t1_PZetaVis > 20
# Loop over Wjets events
print "looping over Wjets events"
for event_num, event in enumerate(wjets):
    if event_num % 1000 == 0:
        print "processing event %i" % event_num
   # if event_num > 100000:
        # Don't process everything
    #    break
    #wjets_tau1_pt.Fill(event.tPt)
    #wjets_tau1_pt.Fill(event.m2_t_PZeta,event.m2_t_PZetaVis)
    #wjets_tau1_pt.Fill(event.tLooseIso)
    if (event.t1Pt > 20 and  event.t2Pt>20 and event.mPt > 15 and event.t1LooseIso != 0 and event.t2LooseIso != 0 and event.t1DecayFinding > 0.5 and event.t2DecayFinding > 0.5 and event.t1_t2_SS < 0.5 and event.mRelPFIsoDB < 0.3 and event.t1_t2_SS < 0.5):

    	wjets_tau1_pt.Fill(event.t1_t2_Mass)

print "looping over signal events"
for event_num, event in enumerate(signal_120):
    if event_num % 1000 == 0:
        print "processing event %i" % event_num
#    if event_num > 100000:
        # Don't process everything
 #       break
    #signal_tau1_pt.Fill(event.tLooseIso)
  #  signal_tau1_pt.Fill(event.tPt)
  #  signal_tau1_pt.Fill(event.m2_t_PZeta,event.m2_t_PZetaVis)
    if (event.t1Pt > 20 and  event.t2Pt>20 and event.mPt > 15 and event.t1LooseIso != 0 and event.t2LooseIso != 0 and event.t1DecayFinding > 0.5 and event.t2DecayFinding > 0.5 and event.t1_t2_SS < 0.5 and event.mRelPFIsoDB < 0.3 and event.t1_t2_SS < 0.5):

	    signal_tau1_pt.Fill(event.t1_t2_Mass)


print "looping over zjet events"
for event_num, event in enumerate(zjets):
    if event_num % 1000 == 0:
        print "processing event %i" % event_num
    if (event.t1Pt > 20 and  event.t2Pt>20 and event.mPt > 15 and event.t1LooseIso != 0 and event.t2LooseIso != 0 and event.t1DecayFinding > 0.5 and event.t2DecayFinding > 0.5 and event.t1_t2_SS < 0.5 and event.mRelPFIsoDB < 0.3 and event.t1_t2_SS < 0.5):
        zjets_tau1_pt.Fill(event.t1_t2_Mass)


# Plot the histograms
canvas = ROOT.TCanvas("the_name_doesnt_matter", "neither does the title", 800, 600)

# Normalize the shapes to 1
if wjets_tau1_pt.Integral():
	wjets_tau1_pt.Scale(1.0/wjets_tau1_pt.Integral())
if zjets_tau1_pt.Integral():
        zjets_tau1_pt.Scale(1.0/zjets_tau1_pt.Integral())

if signal_tau1_pt.Integral():
	signal_tau1_pt.Scale(1.0/signal_tau1_pt.Integral())

wjets_tau1_pt.SetLineColor(ROOT.EColor.kBlue)
zjets_tau1_pt.SetLineColor(ROOT.EColor.kOrange)
signal_tau1_pt.SetLineColor(ROOT.EColor.kRed)

# GOOD PLOTSPERSONSHIP
#wjets_tau1_pt.GetXaxis().SetTitle("Leading #tau p_{T} (GeV)")
wjets_tau1_pt.GetXaxis().SetTitle(" #tau_{1} #tau_{2} Invariant Mass (GeV)")


# Arbitrary units (since both are normalized to 1)
wjets_tau1_pt.GetYaxis().SetTitle("a.u.")
legend = ROOT.TLegend(0.6, 0.6, 0.95, 0.95, "", "brNDC")
legend.AddEntry(wjets_tau1_pt, "W+jets", "l")
legend.AddEntry(zjets_tau1_pt, "Z+jets", "l")
legend.AddEntry(signal_tau1_pt, "WH(120)", "l")

# Compare the shapes
wjets_tau1_pt.Draw()
zjets_tau1_pt.Draw('same')
signal_tau1_pt.Draw('same')

legend.Draw()

canvas.SaveAs("zjets_tau1_tau2_Mass.png")

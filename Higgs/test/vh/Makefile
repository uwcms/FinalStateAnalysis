
# Job ID that produced the ntuples
trilepton_source=2012-03-14-Higgs

dilepton_ntuple_source=2012-03-14-Higgs

# Analyzer location
mega=$(fsa)/TMegaSelector/scripts/mega2

# Target to make EMT plots

emt_analysis: results/analysis/data_MuEG_Run2011B_PromptReco_v1.emt.root

################################################################################
## Define shortcuts for different samples ######################################
################################################################################

data_sample_templates=data_PRIMD_Run2011B_PromptReco_v1 \
		      data_PRIMD_Run2011A_PromptReco_v6_1409 \
		      data_PRIMD_Run2011A_05Aug2011_v1 \
		      data_PRIMD_Run2011A_PromptReco_v4 \
		      data_PRIMD_Run2011A_May10ReReco_v1

mueg_samples=$(subst PRIMD,MuEG, $(data_sample_templates))

doublemu_samples=$(subst PRIMD,DoubleMu, $(data_sample_templates))

doublee_samples=$(subst PRIMD,DoubleElectron, $(data_sample_templates))


#sm_backgrounds=Zjets_M50 QCD_20toInf_MuPt15 WplusJets_madgraph ttjets
sm_backgrounds=

dibosons=WWJetsTo2L2Nu_TuneZ2_7TeV WZJetsTo3LNu_pythia ZZJetsTo4L_pythia

# Run the EMT analysis
results/analysis/%.emt.root: AnalyzeEMT.py inputs/$(trilepton_source)/%.txt
	$(mega) $^ /emutau/final/Ntuple $@ 

################################################################################
## Fake rate targets & recipes  ################################################
################################################################################

fake_clean:
	rm results/fake_rates/*/*root

# Make num/denom for jet->mu fake rate in MMM events
results/fake_rates/mu/%.mmm.root: FakeRatesMMM.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /mumumu/final/Ntuple $@

# Make num/denom for jet->mu fake rate in MM events
results/fake_rates/mu/%.mm.root: FakeRatesMM.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /mumu/final/Ntuple $@

# How we combine all mu fake rate sources into a single file
results/fake_rates/mu/%.all.root: results/fake_rates/mu/%.mm.root \
  results/fake_rates/mu/%.mmm.root 
	hadd -f $@ $^

# Make num/denom for jet->e fake rate in MME events
results/fake_rates/e/%.emm.root: FakeRatesMME.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /emumu/final/Ntuple $@

# Make num/denom for jet->e fake rate in ME events
results/fake_rates/e/%.em.root: FakeRatesME.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /emu/final/Ntuple $@

# How we combine all e fake rate sources into a single file
results/fake_rates/e/%.all.root: results/fake_rates/e/%.em.root \
  results/fake_rates/e/%.emm.root 
	hadd -f $@ $^


################################################################################
## Define which samples are used for what ######################################
################################################################################

muon_fake_jobs=$(patsubst %, results/fake_rates/mu/%.all.root, \
	$(sm_backgrounds) $(doublemu_samples))

muon_fake_rates: $(muon_fake_jobs)

e_fake_jobs=$(patsubst %, results/fake_rates/e/%.all.root, \
	$(sm_backgrounds) $(mueg_samples))

electron_fake_rates: $(e_fake_jobs) 



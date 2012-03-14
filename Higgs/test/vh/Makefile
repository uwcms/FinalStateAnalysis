
# Job ID that produced the ntuples
trilepton_source=2012-03-14-Trileptons

dilepton_ntuple_source=2012-03-09-Test

mega=$(fsa)/TMegaSelector/scripts/mega2

# Target to make EMT plots

emt_analysis: results/analysis/data_MuEG_Run2011B_PromptReco_v1.emt.root

################################################################################
## Define rules to make make things ############################################
################################################################################

# Run the EMT analysis
results/analysis/%.emt.root: AnalyzeEMT.py inputs/$(trilepton_source)/%.txt
	$(mega) $^ /emutau/final/Ntuple $@ 

# Make num/denom for jet->mu fake rate in MMM events
results/fake_rates/mu/%.mmm.root: FakeRatesMMM.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /mumumu/final/Ntuple $@

# Make num/denom for jet->e fake rate in MME events
results/fake_rates/e/%.emm.root: FakeRatesMME.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /emumu/final/Ntuple $@

# Make num/denom for jet->e fake rate in ME events
results/fake_rates/e/%.em.root: FakeRatesME.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /emu/final/Ntuple $@

# Make num/denom for jet->mu fake rate in MM events
results/fake_rates/e/%.mm.root: FakeRatesMM.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /mumu/final/Ntuple $@


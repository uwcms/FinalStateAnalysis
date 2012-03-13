
# Job ID that produced the ntuples
ntuple_source=2012-03-09-Test

dilepton_ntuple_source=2012-03-09-Test

mega=$(fsa)/TMegaSelector/scripts/mega2

# Target to make EMT plots

emt_analysis: results/analysis/WZ.emt.root

################################################################################
## Define rules to make make things ############################################
################################################################################

# Run the EMT analysis
results/analysis/%.emt.root: AnalyzeEMT.py
	$(mega) AnalyzeEMT.py "$(ntuple_source)-$*" /emutau/final/Ntuple $@

# Make num/denom for jet->mu fake rate in MMM events
results/fake_rates/mu/%.mmm.root: FakeRatesMMM.py
	$(mega) FakeRatesMMM.py "$(ntuple_source)-$*" /mumumu/final/Ntuple $@

# Make num/denom for jet->e fake rate in MME events
results/fake_rates/e/%.emm.root: FakeRatesMME.py
	$(mega) FakeRatesMME.py "$(ntuple_source)-$*" /emumu/final/Ntuple $@

# Make num/denom for jet->e fake rate in ME events
results/fake_rates/e/%.em.root: FakeRatesME.py
	$(mega) FakeRatesME.py "$(dilepton_ntuple_source)-$*" /emu/final/Ntuple $@

# Make num/denom for jet->mu fake rate in MM events
results/fake_rates/e/%.mm.root: FakeRatesMM.py
	$(mega) FakeRatesMM.py "$(dilepton_ntuple_source)-$*" /mumu/final/Ntuple $@


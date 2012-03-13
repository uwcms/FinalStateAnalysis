

# Job ID that produced the ntuples
ntuple_source=2012-03-09-Test

mega=$(fsa)/TMegaSelector/scripts/mega2

# Target to make EMT plots

emt_analysis: results/analysis/WZ.emt.root

results/analysis/%.emt.root: AnalyzeEMT.py
	$(mega) AnalyzeEMT.py "$(ntuple_source)-$*" /emutau/final/Ntuple $@

results/fake_rates/mu/%.mmm.root: FakeRatesMMM.py
	$(mega) FakeRatesMMM.py "$(ntuple_source)-$*" /mumumu/final/Ntuple $@

results/fake_rates/e/%.emm.root: FakeRatesMME.py
	$(mega) FakeRatesMME.py "$(ntuple_source)-$*" /emumu/final/Ntuple $@

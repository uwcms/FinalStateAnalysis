

# Job ID that produced the ntuples
ntuple_source=2012-03-09-Test

mega=$(fsa)/TMegaSelector/scripts/mega

# Target to make EMT plots

emt_analysis: results/analysis/WZ.emt.root

results/analysis/%.emt.root: AnalyzeEMT.py
	$(mega) AnalyzeEMT.py "$(ntuple_source)-$*" /emutau/final/Ntuple $@


# Job ID that produced the ntuples
ntuple_id=2012-03-14-Higgs

# Analyzer location
mega=$(fsa)/TMegaSelector/scripts/mega2

.SECONDARY: %.root fake_rates.json

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

all_data_samples=$(mueg_samples) $(doublee_samples) $(doublemu_samples)

sm_backgrounds=Zjets_M50 QCD_20toInf_MuPt15 WplusJets_madgraph TTplusJets_madgraph
#sm_backgrounds=

dibosons=WZJetsTo3LNu_pythia ZZJetsTo4L_pythia

all_samples=$(all_data_samples) $(sm_backgrounds) $(dibosons)

################################################################################
## Recipes for analyzing data ##################################################
################################################################################

# Run the WH EMT analysis
results/analysis/%.emt.root: AnalyzeEMT.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so
	$(mega) AnalyzeEMT.py inputs/$(ntuple_id)/$*.txt \
	  /emutau/final/Ntuple $@ 

# Run the WH MMT analysis
results/analysis/%.mmt.root: AnalyzeMMT.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so
	$(mega) AnalyzeMMT.py inputs/$(ntuple_id)/$*.txt \
	  /mumutau/final/Ntuple $@ 

# Run the ZH MMT analysis
results/analysis/%.mmmt.root: AnalyzeMMMT.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so
	$(mega) AnalyzeMMMT.py inputs/$(ntuple_id)/$*.txt \
	  /mmmt/final/Ntuple $@ 

# Make num/denom for jet->mu fake rate in MMM events
results/fake_rates/mu/%.mmm.root: FakeRatesMMM.py inputs/$(ntuple_id)/%.txt
	$(mega) $^ /mumumu/final/Ntuple $@

# Make num/denom for jet->mu fake rate in MM events
results/fake_rates/mu/%.mm.root: FakeRatesMM.py inputs/$(ntuple_id)/%.txt
	$(mega) $^ /mumu/final/Ntuple $@

# How we combine all mu fake rate sources into a single file
results/fake_rates/mu/%.all.root: results/fake_rates/mu/%.mm.root \
  results/fake_rates/mu/%.mmm.root 
	hadd -f $@ $^

# Make num/denom for jet->e fake rate in MME events
results/fake_rates/e/%.emm.root: FakeRatesMME.py inputs/$(ntuple_id)/%.txt
	$(mega) $^ /emumu/final/Ntuple $@

# Make num/denom for jet->e fake rate in ME events
results/fake_rates/e/%.em.root: FakeRatesME.py inputs/$(ntuple_id)/%.txt
	$(mega) $^ /emu/final/Ntuple $@

# How we combine all e fake rate sources into a single file
results/fake_rates/e/%.all.root: results/fake_rates/e/%.em.root \
  results/fake_rates/e/%.emm.root 
	hadd -f $@ $^

# How to compile a .C file with ACLiC
%_C.so %_C.d: %.C
	./aclic_compile.sh $<
################################################################################
## Extracting meta information (number of events processed) ####################
################################################################################

inputs/$(ntuple_id)/data%.meta.json: inputs/$(ntuple_id)/data%.txt
	extract_meta_info.py $< /ee/metaInfo $@  --lumimask

inputs/$(ntuple_id)/%.meta.json: inputs/$(ntuple_id)/%.txt
	extract_meta_info.py $< /ee/metaInfo $@ 

# List of meta files for every sample
all_meta_info=$(patsubst %, inputs/$(ntuple_id)/%.meta.json, $(all_samples))

inputs/$(ntuple_id)/all_samples.json: $(all_meta_info)
	./merge_meta_info.py $@ $^

################################################################################
## Define which samples are used for what ######################################
################################################################################

# fake rate jobs
muon_fake_jobs=$(patsubst %, results/fake_rates/mu/%.all.root, \
	$(sm_backgrounds) $(doublemu_samples))


e_fake_jobs=$(patsubst %, results/fake_rates/e/%.all.root, \
	$(sm_backgrounds) $(mueg_samples))

# analysis jobs
emt_ana_jobs=$(patsubst %, results/analysis/%.emt.root, \
	$(sm_backgrounds) $(mueg_samples))

mmt_ana_jobs=$(patsubst %, results/analysis/%.mmt.root, \
	$(sm_backgrounds) $(doublemu_samples))

mmmt_ana_jobs=$(patsubst %, results/analysis/%.mmmt.root, \
	$(sm_backgrounds) $(doublemu_samples))

################################################################################
## MC to data correction functions  ############################################
################################################################################

################################################################################
## Fake rate functions #########################################################
################################################################################

# Script to build the file w/ the fake rate fit functions
fit_models.root: make_fit_models.py
	python make_fit_models.py

fake_rates.C: fake_rates.json make_fakerates.py
	python make_fakerates.py fake_rates.json

################################################################################
## Define analysis targets! ####################################################
################################################################################

muon_fake_rates: $(muon_fake_jobs)

electron_fake_rates: $(e_fake_jobs) 

fakerates: muon_fake_rates electron_fake_rates

emt_analysis: $(emt_ana_jobs)

mmt_analysis: $(mmt_ana_jobs)

mmmt_analysis: $(mmmt_ana_jobs)

analysis: emt_analysis mmt_analysis

################################################################################
## Cleanup #####################################################################
################################################################################

.PHONY: fake_clean inputs_clean fakerates muon_fake_rates electron_fake_rates

fake_clean:
	rm results/fake_rates/*/*root

inputs_clean:
	ls -d inputs/*/ | xargs rm -r 

meta_clean:
	rm inputs/*/*json



# Job ID that produced the ntuples
ntuple_id=2012-03-24-Higgs

# Analyzer location
mega=$(fsa)/TMegaSelector/scripts/mega2

.SECONDARY: %.root \
  results/fake_rates/mu/%.mmm.root \
  results/fake_rates/mu/%.mm.root \
  results/fake_rates/mu/%.mmmt.root \
  results/analysis/emt/%.root \
  results/analysis/mmt/%.root \
  results/analysis/mmmt/%.root \
  results/analysis/mmet/%.root \
  results/analysis/mmme/%.root 

.PRECIOUS: %.root \
  results/fake_rates/mu/%.mmm.root \
  results/fake_rates/mu/%.mm.root \
  results/fake_rates/mu/%.mmmt.root \
  results/analysis/emt/%.root \
  results/analysis/mmt/%.root \
  results/analysis/mmmt/%.root \
  results/analysis/mmet/%.root \
  results/analysis/mmme/%.root 

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
results/analysis/emt/%.root: AnalyzeEMT.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so inputs/$(ntuple_id)/%.lumi.sum
	$(mega) AnalyzeEMT.py inputs/$(ntuple_id)/$*.txt \
	  /emutau/final/Ntuple $@ 
	embed_label.py $@ dataset=$* intlumi=`cat inputs/$(ntuple_id)/$*.lumi.sum`

# Run the WH MMT analysis
results/analysis/mmt/%.root: AnalyzeMMT.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so inputs/$(ntuple_id)/%.lumi.sum
	$(mega) AnalyzeMMT.py inputs/$(ntuple_id)/$*.txt \
	  /mumutau/final/Ntuple $@ 
	embed_label.py $@ dataset=$* intlumi=`cat inputs/$(ntuple_id)/$*.lumi.sum`

# Run the ZMM analysis
results/analysis/zmumu/%.root: ZMuMuControl.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so inputs/$(ntuple_id)/%.lumi.sum
	$(mega) ZMuMuControl.py inputs/$(ntuple_id)/$*.txt \
	  /mumu/final/Ntuple $@ 
	embed_label.py $@ dataset=$*
	embed_label.py $@ dataset=$* intlumi=`cat inputs/$(ntuple_id)/$*.lumi.sum`

# Run the ZH MMMT analysis
results/analysis/mmmt/%.root: AnalyzeMMMT.py zh_zmm_selection.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so inputs/$(ntuple_id)/%.lumi.sum
	$(mega) AnalyzeMMMT.py inputs/$(ntuple_id)/$*.txt \
	  /mmmt/final/Ntuple $@ 
	embed_label.py $@ dataset=$* intlumi=`cat inputs/$(ntuple_id)/$*.lumi.sum`

# Run the ZH EEMT analysis
results/analysis/eemt/%.root: AnalyzeEEMT.py zh_zee_selection.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so inputs/$(ntuple_id)/%.lumi.sum
	$(mega) AnalyzeEEMT.py inputs/$(ntuple_id)/$*.txt \
	  /eemt/final/Ntuple $@ 
	embed_label.py $@ dataset=$* intlumi=`cat inputs/$(ntuple_id)/$*.lumi.sum`

# Run the ZH MMME analysis
results/analysis/mmme/%.root: AnalyzeMMME.py zh_zmm_selection.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so inputs/$(ntuple_id)/%.lumi.sum
	$(mega) AnalyzeMMME.py inputs/$(ntuple_id)/$*.txt \
	  /emmm/final/Ntuple $@ 
	embed_label.py $@ dataset=$* intlumi=`cat inputs/$(ntuple_id)/$*.lumi.sum`

# Run the ZH MMET analysis
results/analysis/mmet/%.root: AnalyzeMMET.py zh_zmm_selection.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so inputs/$(ntuple_id)/%.lumi.sum
	$(mega) AnalyzeMMET.py inputs/$(ntuple_id)/$*.txt \
	  /emmt/final/Ntuple $@ 
	embed_label.py $@ dataset=$* intlumi=`cat inputs/$(ntuple_id)/$*.lumi.sum`

# Run the ZH MMTT analysis
results/analysis/mmtt/%.root: AnalyzeMMTT.py zh_zmm_selection.py inputs/$(ntuple_id)/%.txt \
  corrections_C.so fake_rates_C.so inputs/$(ntuple_id)/%.lumi.sum
	$(mega) AnalyzeMMTT.py inputs/$(ntuple_id)/$*.txt \
	  /mmtt/final/Ntuple $@ 
	embed_label.py $@ dataset=$* intlumi=`cat inputs/$(ntuple_id)/$*.lumi.sum`

# Make num/denom for jet->mu fake rate in MMM events
results/fake_rates/mu/%.mmm.root: FakeRatesMMM.py inputs/$(ntuple_id)/%.txt \
	$(mega) $^ /mumumu/final/Ntuple $@

# Make num/denom for jet->mu fake rate in MM events
results/fake_rates/mu/%.mm.root: FakeRatesMM.py inputs/$(ntuple_id)/%.txt
	$(mega) $^ /mumu/final/Ntuple $@ 

# Make num/denom for jet->mu fake rate in MMMT events
results/fake_rates/mu/%.mmmt.root: FakeRatesMMMT.py inputs/$(ntuple_id)/%.txt
	$(mega) $^ /mmmt/final/Ntuple $@

# # FIXME we need to add the lumisum information to these some how!
# How we combine all mu fake rate sources into a single file
results/fake_rates/mu/%.all.root: results/fake_rates/mu/%.mm.root \
  results/fake_rates/mu/%.mmm.root results/fake_rates/mu/%.mmmt.root \
	hadd -f $@ $^
	embed_label.py $@ dataset=$*

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
	embed_label.py $@ dataset=$*

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

# For data, get the lumi mask from the file so we can run lumi calc on it.
inputs/$(ntuple_id)/data%.lumimask.json: inputs/$(ntuple_id)/data%.meta.json
	cat $< | dump_lumimask.py > $@

# Define which samples we need a data mask for
data_lumimask_files=$(patsubst %, inputs/$(ntuple_id)/%.lumimask.json, \
		    $(all_data_samples))

# Run lumi calc on the lumi masks from the above step.
inputs/$(ntuple_id)/%.lumicalc.csv: inputs/$(ntuple_id)/%.lumimask.json
	pixelLumiCalc.py overview -i $< -o $@

# For data, get the actual interesting stuff from the pixelLumiCalc output barf
inputs/$(ntuple_id)/data%.lumi.sum: inputs/$(ntuple_id)/data%.lumicalc.csv
	python $(fsa)/Utilities/python/lumicalc_parser.py $< > $@

# For MC, figure out what the effective int. lumi. is,
# using the number of processed events and the x-section.
inputs/$(ntuple_id)/%.lumi.sum: inputs/$(ntuple_id)/%.meta.json
	get_mc_lumi.py $* `cat $< | extract_json.py n_evts` > $@

data_lumimask_files=$(patsubst %, inputs/$(ntuple_id)/%.lumimask.json, \
		    $(all_data_samples))

data_lumicalc_files=$(patsubst %, inputs/$(ntuple_id)/%.lumicalc.csv, \
		    $(all_data_samples))

data_lumicalc_sums=$(patsubst %, inputs/$(ntuple_id)/%.lumi.sum, \
		    $(all_data_samples))

data_lumimasks: $(data_lumimask_files) $(data_lumicalc_files) \
  $(data_lumicalc_sums)


################################################################################
## Define which samples are used for what ######################################
################################################################################

muon_fake_samples=$(sm_backgrounds) $(doublemu_samples))
e_fake_samples=$(sm_backgrounds) $(mueg_samples))

# fake rate jobs
muon_fake_jobs=$(patsubst %, results/fake_rates/mu/%.all.root, \
	$(sm_backgrounds) $(doublemu_samples))

e_fake_jobs=$(patsubst %, results/fake_rates/e/%.all.root, \
	$(sm_backgrounds) $(mueg_samples))

# analysis jobs
emt_ana_jobs=$(patsubst %, results/analysis/emt/%.root, \
	$(sm_backgrounds) $(mueg_samples))

mmt_ana_jobs=$(patsubst %, results/analysis/mmt/%.root, \
	$(sm_backgrounds) $(doublemu_samples))

mmmt_ana_jobs=$(patsubst %, results/analysis/mmmt/%.root, \
	$(sm_backgrounds) $(doublemu_samples) $(dibosons))

eemt_ana_jobs=$(patsubst %, results/analysis/eemt/%.root, \
	$(sm_backgrounds) $(doublee_samples) $(dibosons))

mmme_ana_jobs=$(patsubst %, results/analysis/mmme/%.root, \
	$(sm_backgrounds) $(doublemu_samples) $(dibosons))

mmet_ana_jobs=$(patsubst %, results/analysis/mmet/%.root, \
	$(sm_backgrounds) $(doublemu_samples) $(dibosons))

mmtt_ana_jobs=$(patsubst %, results/analysis/mmtt/%.root, \
	$(sm_backgrounds) $(doublemu_samples) $(dibosons))

zh_ana_jobs=$(mmmt_ana_jobs) $(mmme_ana_jobs) $(mmet_ana_jobs) $(mmtt_ana_jobs) \
	    $(eemt_ana_jobs)

zmm_control_jobs=$(patsubst %, results/analysis/zmumu/%.root, \
	$(sm_backgrounds) $(doublemu_samples))

################################################################################
## MC to data correction functions  ############################################
################################################################################

################################################################################
## Define analysis targets! ####################################################
################################################################################

muon_fake_rates: $(muon_fake_jobs)

electron_fake_rates: $(e_fake_jobs) 

fakerates: muon_fake_rates electron_fake_rates

emt_analysis: $(emt_ana_jobs)

mmt_analysis: $(mmt_ana_jobs)

mmmt_analysis: $(mmmt_ana_jobs)

eemt_analysis: $(eemt_ana_jobs)

mmme_analysis: $(mmme_ana_jobs)

mmet_analysis: $(mmet_ana_jobs)

mmtt_analysis: $(mmtt_ana_jobs)

zh_analysis: mmmt_analysis mmme_analysis mmet_analysis mmtt_ana_jobs

zmm_analysis: $(zmm_control_jobs)

analysis: emt_analysis mmt_analysis zh_analysis zmm_analysis

################################################################################
## Fake rate functions #########################################################
################################################################################

# Script to build the file w/ the fake rate fit functions
results/fake_rates/fit_models.root: make_fit_models.py
	python make_fit_models.py $@

# Build the RooWorkspace with the fit results for the muon fake rates
results/fake_rates/muon_fr_fits.root: results/fake_rates/fit_models.root \
  fit_fake_rates.py muon_fr_cfg.py \
  inputs/$(ntuple_id)/all_samples.json $(muon_fake_jobs)
	./fit_fake_rates.py inputs/$(ntuple_id)/all_samples.json \
	  muon_fr_cfg.py  results/fake_rates/fit_models.root \
	  $@ results/fake_rates/mu/*.all.root

# Build the RooWorkspace with the fit results for the electron fake rates
results/fake_rates/electron_fr_fits.root: results/fake_rates/fit_models.root \
  fit_fake_rates.py electron_fr_cfg.py \
  inputs/$(ntuple_id)/all_samples.json  $(e_fake_jobs)
	./fit_fake_rates.py inputs/$(ntuple_id)/all_samples.json \
	  electron_fr_cfg.py  results/fake_rates/fit_models.root \
	  $@ results/fake_rates/e/*.all.root

fake_rates.C: fake_rates.json make_fakerates.py
	python make_fakerates.py fake_rates.json

################################################################################
## Making plots  ###############################################################
################################################################################

# See http://www.cmcrossroads.com/ask-mr-make/12908-rules-with-multiple-outputs-in-gnu-make
# for dealing w/ commands with multiple outputs 
plots/muon_fake_fits/plot_list.txt: results/fake_rates/muon_fr_fits.root render_fake_rates.py
	./render_fake_rates.py results/fake_rates/muon_fr_fits.root plots/muon_fake_fits/

plots/muon_fake_controls/plot_list.txt: inputs/$(ntuple_id)/all_samples.json \
  $(muon_fake_jobs) render_fake_rate_controls.py
	./render_fake_rate_controls.py inputs/$(ntuple_id)/all_samples.json \
	  data_DoubleMu plots/muon_fake_controls/ $(muon_fake_jobs)

plots/zmm_control/plot_list.txt: inputs/$(ntuple_id)/all_samples.json \
  zmm_analysis render_zmm_controls.py
	./render_zmm_controls.py inputs/$(ntuple_id)/all_samples.json \
	  plots/zmm_control/ $(zmm_control_jobs)

plots/zh/mmmt/plot_list.txt: $(mmmt_ana_jobs) render_zh_plots.py
	./render_zh_plots.py plots/zh/mmmt/ data_DoubleMu $(mmmt_ana_jobs) 

plots/zh/eemt/plot_list.txt: $(eemt_ana_jobs) render_zh_plots.py
	./render_zh_plots.py plots/zh/eemt/ data_DoubleElectron $(eemt_ana_jobs) 

plots/zh/mmet/plot_list.txt: $(mmet_ana_jobs) render_zh_plots.py
	./render_zh_plots.py plots/zh/mmet/ data_DoubleMu $(mmet_ana_jobs) 

plots/zh/mmtt/plot_list.txt: $(mmtt_ana_jobs) render_zh_plots.py
	./render_zh_plots.py plots/zh/mmtt/ data_DoubleMu $(mmtt_ana_jobs) 

plots/zh/mmme/plot_list.txt: $(mmme_ana_jobs) render_zh_plots.py
	./render_zh_plots.py plots/zh/mmme/ data_DoubleMu $(mmme_ana_jobs) 

zh_plots: \
  plots/zh/mmmt/plot_list.txt \
  plots/zh/mmme/plot_list.txt \
  plots/zh/mmtt/plot_list.txt \
  plots/zh/mmet/plot_list.txt 

plots: plots/zmm_control/plot_list.txt \
  plots/muon_fake_controls/plot_list.txt \
  plots/muon_fake_fits/plot_list.txt

################################################################################
## Packing things up ###########################################################
################################################################################

results.tgz: results/analysis/*/*.root results/fake_rates/*/*.root
	tar cvzf $@ results

################################################################################
## Cleanup #####################################################################
################################################################################

.PHONY: fake_clean inputs_clean fakerates muon_fake_rates electron_fake_rates \
  zmm_analysis

fake_clean:
	rm results/fake_rates/*/*root

inputs_clean:
	ls -d inputs/*/ | xargs rm -r 

meta_clean:
	rm inputs/*/*json


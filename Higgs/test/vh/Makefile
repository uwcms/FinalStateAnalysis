
# Job ID that produced the ntuples
trilepton_source=2012-03-14-Higgs

dilepton_ntuple_source=2012-03-14-Higgs

# Analyzer location
mega=$(fsa)/TMegaSelector/scripts/mega2

.SECONDARY: %.root

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


sm_backgrounds=Zjets_M50 QCD_20toInf_MuPt15 WplusJets_madgraph TTplusJets_madgraph
#sm_backgrounds=

dibosons=WWJetsTo2L2Nu_TuneZ2_7TeV WZJetsTo3LNu_pythia ZZJetsTo4L_pythia

################################################################################
## Recipes for analyzing data ##################################################
################################################################################

# Run the EMT analysis
results/analysis/%.emt.root: AnalyzeEMT.py inputs/$(trilepton_source)/%.txt
	$(mega) $^ /emutau/final/Ntuple $@ 

# Run the MMT analysis
results/analysis/%.mmt.root: AnalyzeMMT.py inputs/$(trilepton_source)/%.txt
	$(mega) $^ /mumutau/final/Ntuple $@ 

# Make num/denom for jet->mu fake rate in MMM events
results/fake_rates/mu/%.mmm.root: FakeRatesMMM.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /mumumu/final/Ntuple $@

# Make num/denom for jet->mu fake rate in MM events
results/fake_rates/mu/%.mm.root: FakeRatesMM.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /mumu/final/Ntuple $@

# How we combine all mu fake rate sources into a single file
results/fake_rates/mu/%.root: results/fake_rates/mu/%.mm.root \
  results/fake_rates/mu/%.mmm.root 
	hadd -f $@ $^

# Make num/denom for jet->e fake rate in MME events
results/fake_rates/e/%.emm.root: FakeRatesMME.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /emumu/final/Ntuple $@

# Make num/denom for jet->e fake rate in ME events
results/fake_rates/e/%.em.root: FakeRatesME.py inputs/$(dilepton_ntuple_source)/%.txt
	$(mega) $^ /emu/final/Ntuple $@

# How we combine all e fake rate sources into a single file
results/fake_rates/e/%.root: results/fake_rates/e/%.em.root \
  results/fake_rates/e/%.emm.root 
	hadd -f $@ $^

# How to compile a .C file with ACLiC
%_C.so %_C.d: %.C
	./aclic_compile.sh $<

################################################################################
## Define which samples are used for what ######################################
################################################################################

# fake rate jobs
muon_fake_jobs=$(patsubst %, results/fake_rates/mu/%.root, \
	$(sm_backgrounds) $(doublemu_samples))


e_fake_jobs=$(patsubst %, results/fake_rates/e/%.root, \
	$(sm_backgrounds) $(mueg_samples))

# analysis jobs
emt_ana_jobs=$(patsubst %, results/analysis/%.emt.root, \
	$(sm_backgrounds) $(mueg_samples))

mmt_ana_jobs=$(patsubst %, results/analysis/%.mmt.root, \
	$(sm_backgrounds) $(doublemu_samples))

################################################################################
## Define analysis targets! ####################################################
################################################################################

muon_fake_rates: $(muon_fake_jobs)

electron_fake_rates: $(e_fake_jobs) 

fakerates: muon_fake_rates electron_fake_rates

emt_analysis: $(emt_ana_jobs)

mmt_analysis: $(mmt_ana_jobs)

analysis: emt_analysis mmt_analysis

################################################################################
## Cleanup #####################################################################
################################################################################

.PHONY: fake_clean inputs_clean fakerates muon_fake_rates electron_fake_rates

fake_clean:
	rm results/fake_rates/*/*root

inputs_clean:
	ls -d inputs/*/ | xargs rm -r 


# Common definitions for Makefiles

# Which ntuple to use
ntuple_id=2012-04-06-Higgs

# Analyzer location
mega=$(fsa)/TMegaSelector/scripts/mega2
megaevents=$(fsa)/TMegaSelector/scripts/megaevents.py

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

all_mc_samples=$(sm_backgrounds) $(dibosons)

all_samples=$(all_data_samples) $(sm_backgrounds) $(dibosons)

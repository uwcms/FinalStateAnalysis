# Makefile to build the correct data cards
#
# Important targets:
#
# General analysis
# ================
#
#  fake_rates.C:	build the fake rate correction functions
#
# Limit Setting
# =============
#
#  analyze: 		run the analysis (maybe doing the fake rates to)
#
#  cards: 		build the ASCII and .root cards 
#  asymp: 		compute the asymptotic limits
#
#  cls_submits: 	builds the submit directories (in $scratch/cls_limits) 
#  			to submit condor jobs
#  grids: 		hadd add together the results from the condor jobs
#  			(requires condor jobs from cls_submits to be finished)
#  cls: 		compute the CLs limits 
#  			(requires condor jobs from cls_submits to be finished)

# The name of the un-stat-shaped root file - output of the analysis
no_stats_shape_file=wh_shapes_raw.root

################################################################################
##
##         ==============
##         Analysis Tasks 
##         ==============
##
################################################################################

################################################################################
## Computing the fake rates ####################################################
################################################################################

# How to build the single muon fake rate result file
results_singleMuFakeRates.root: singleMuFakeRates.py
	python singleMuFakeRates.py

results_fakeRates.root: fakeRates.py
	python fakeRates.py

# How to combine all the fake rate measurements
fake_rates.json: results_singleMuFakeRates.root results_fakeRates.root combineFakeRates.py
	python combineFakeRates.py

# How to turn it into a ROOT macro
fake_rates.C: fake_rates.json make_fakerates.py
	python make_fakerates.py

################################################################################
## Building the correction factors #############################################
################################################################################

# Measure the MuEG trigger efficiency
mueg_trig_correction_results.json: muEGTriggerMeasurement.py
	python muEGTriggerMeasurement.py

# Produce the corrections root macro
corrections.C: mueg_trig_correction_results.json make_corrections.py
	python make_corrections.py

################################################################################
## The main analysis job  ######################################################
################################################################################

# Define the files produced by the analysis
ana_output=$(no_stats_shape_file) #mmt_mumu_events.json emt_emu_events.json mmt_mumu_fakerate_summary.json emt_emu_fakerate_summary.json emt_emu_summary.json mmt_mumu_summary.json

$(ana_output): analysis.py analysis_cfg.py corrections.C fake_rates.C
	python analysis.py

analyze: $(ana_output)

################################################################################
##
##         =============
##         Limit Setting
##         =============
##
################################################################################

################################################################################
## Building "statistical" shape uncertainties ##################################
################################################################################

# The name of the shape root file
shape_file=wh_shapes.root
# Mass points to run limits on
masspoints=100 115 120 130 140 150 160
# Exclusion range to use when building CLs grid
min_cls="0.2"
max_cls="70"

# Define the cards we want to make
combined_txt_cards=$(patsubst %, cards/combined_%.txt,$(masspoints))
combined_root_cards=$(patsubst %, cards/combined_%.root,$(masspoints))
cls_submitters=$(patsubst %, $(scratch)/cls_limits/combined_%/submit,$(masspoints))

cards: $(shape_file) $(combined_txt_cards) $(combined_root_cards)

cls_submits: $(cls_submitters)

grids: $(patsubst %, $(scratch)/cls_limits/combined_%/grid.root,$(masspoints))

asymp: $(patsubst %, cards/combined_%.asymp.json,$(masspoints))

cls: $(patsubst %, cards/combined_%.cls.json,$(masspoints))

################################################################################
## Building "statistical" shape uncertainties ##################################
################################################################################

$(shape_file): $(no_stats_shape_file)
	cp $(no_stats_shape_file) $(shape_file)
	./addStatShapes.py $(shape_file)

################################################################################
## Building the data cards themselves  #########################################
################################################################################

# Rule to make a combined ASCII card
cards/combined_%.txt: $(shape_file) make_data_card.py
	python make_data_card.py -o $@ -m $* -f $(shape_file)

# Rule to make a RooWorkspace card from an ASCII one
cards/combined_%.root: cards/combined_%.txt
	text2workspace.py $< -o $@

################################################################################
## Computing the asymptotic limit ##############################################
################################################################################

# Rule to compute the asymptotic limit from a given card file
cards/combined_%.asymp.json: cards/combined_%.root
	combine $< -M Asymptotic -H ProfileLikelihood | limit2JSON.py > $@

################################################################################
## Tools for computing the full CLs limits  ####################################
################################################################################

# Rule to generate a submit directories
# The script to make the submit files is in StatTools/scripts
$(scratch)/cls_limits/combined_%/submit: cards/combined_%.root
	# Backup the previous submit directory
	#if [ -e $(scratch)/cls_limits ]; then
	   #mv $(scratch)/cls_limits  $(scratch)/cls_limits.`date +%m.%d.%H-%M`
	#fi
	make_grid_submission.py -submitdir `dirname $@` \
	  -i `readlink -f $<`  -mass $* \
	  -min $(min_cls) -max $(max_cls)

# Now define the combined grid result - will get updated as more files show up 
# This combines all the points into a "mass slice"
$(scratch)/cls_limits/combined_%/grid.root: $(scratch)/cls_limits/combined_%/point_*root
	hadd -f $@ $^ 

# Given the card file and the computed grid, compute the obs and exp CLs limits
cards/combined_%.cls.json: cards/combined_%.root $(scratch)/cls_limits/combined_%/grid.root 
	compute_cls.sh $^ $* > $@

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
#  For the limits, the channel can be selected by:
#  	make channel=XXX [target], where XXX is in [combined, emt, mmt]
#
#  analyze: 		run the analysis (maybe doing the fake rates to)
#
#  cards: 		build the ASCII and .root cards 
#  asymp: 		compute the asymptotic limits
#  asympplot: 		make the asymptotic limit plot
#  clsplot: 		make the CLs limit plot
#
#  cls_submits: 	builds the submit directories (in $scratch/cls_limits) 
#  			to submit condor jobs
#  grids: 		hadd add together the results from the condor jobs
#  			(requires condor jobs from cls_submits to be finished)
#  cls: 		compute the CLs limits 
#  			(requires condor jobs from cls_submits to be finished)
#
#  table: 		make a .tex table with the results

# The name of the un-stat-shaped root file - output of the analysis
raw_shape_file=wh_shapes_raw.root

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
ana_output=$(raw_shape_file) #mmt_mumu_events.json emt_emu_events.json mmt_mumu_fakerate_summary.json emt_emu_fakerate_summary.json emt_emu_summary.json mmt_mumu_summary.json

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

clean:
	rm -f cards/*

################################################################################
## Building "statistical" shape uncertainties ##################################
################################################################################

# The naem of the shape root file with interpolated histograms
interp_shape_file=wh_shapes_interp.root
# The naem of the shape root file with the FF and SM4 templates
extensions_shape_file=wh_shapes_sm4_ff.root
# The name of the shape root file
shape_file=wh_shapes.root
# Mass points to run limits on
masspoints=100 110 115 120 130 140 150 160 
# Exclusion range to use when building CLs grid
min_cls="0.2"
max_cls="70"
channel=combined
# Optionally change which final selection is used to make the limits
selection=final


# Define the cards we want to make
txt_cards=$(patsubst %, cards/$(channel)_%.txt,$(masspoints))
root_cards=$(patsubst %, cards/$(channel)_%.root,$(masspoints))
extra_txt_cards=$(patsubst %, cards/$(channel)_%FF.txt,$(masspoints)) $(patsubst %, cards/$(channel)_%SM4.txt,$(masspoints)) 
cls_submitters=$(patsubst %, $(scratch)/cls_limits/$(channel)_%/submit,$(masspoints))
asymp_results=$(patsubst %, cards/$(channel)_%.asymp.json,$(masspoints))
cls_results=$(patsubst %, cards/$(channel)_%.cls.json,$(masspoints))

cards: $(shape_file) $(txt_cards) $(root_cards)

extra_cards: $(extra_txt_cards)

cls_submits: $(cls_submitters)

grids: $(patsubst %, $(scratch)/cls_limits/$(channel)_%/grid.root,$(masspoints))

asymp: $(asymp_results)

asympplot: cards/$(channel).asymp.pdf

cls: $(cls_results)

clsplot: cards/$(channel).cls.pdf cards/$(channel).cls.tex

vh_cards.tgz: $(root_cards)
	tar -cvzf $@ $(root_cards)

vh_cards_txt.tgz: $(txt_cards)
	tar -cvzf $@ $(shape_file) $(txt_cards)

# Make the tex table for the note
table: final_yields.tex

final_yields.tex: $(shape_file) make_tex_tables.py
	./make_tex_tables.py -f $(shape_file) > $@

# Just show what mass points we are running
ls_mass_points: 
	echo $(masspoints)

################################################################################
## Building "statistical" shape uncertainties ##################################
################################################################################

# Add missing signal mass points
$(interp_shape_file): $(raw_shape_file) interpolateSignalHistograms.py
	cp $(raw_shape_file) $(interp_shape_file)
	./interpolateSignalHistograms.py $(interp_shape_file)

# Add Fermiphobic and SM4 corrected templates
$(extensions_shape_file): $(interp_shape_file) addSMExtensions.py
	cp $(interp_shape_file) $(extensions_shape_file)
	./addSMExtensions.py $(extensions_shape_file)

$(shape_file): $(extensions_shape_file) addStatShapes.py
	cp $(extensions_shape_file) $(shape_file)
	./addStatShapes.py $(shape_file)

################################################################################
## Building the data cards themselves  #########################################
################################################################################

# Rule to make a $(channel) ASCII card
cards/$(channel)_%.txt: $(shape_file) make_data_card.py
	python make_data_card.py -o $@ -m $* -f $(shape_file) \
	  --channels $(channel) --selection $(selection) \
	  --emt_shape ETauMass

# Rule to make a RooWorkspace card from an ASCII one
cards/$(channel)_%.root: cards/$(channel)_%.txt
	text2workspace.py $< -o $@

################################################################################
## Computing the asymptotic limit ##############################################
################################################################################

# Rule to compute the asymptotic limit from a given card file
cards/$(channel)_%.asymp.json: cards/$(channel)_%.root
	combine $< -M Asymptotic -H ProfileLikelihood \
	  -m `echo $* | sed "s|FF||" | sed "s|SM4||"` \
	  | limit2JSON.py --mass $* > $@
	rm higgsCombineTest.Asymptotic.mH`echo $* | sed "s|FF||" | sed "s|SM4||"`.root

################################################################################
## Tools for computing the full CLs limits  ####################################
################################################################################

# Rule to generate a submit directories
# The script to make the submit files is in StatTools/scripts
$(scratch)/cls_limits/$(channel)_%/submit: cards/$(channel)_%.root
	make_grid_submission.py -submitdir `dirname $@` \
	  -i `readlink -f $<`  -mass $* \
	  -min $(min_cls) -max $(max_cls)

# Now define the $(channel) grid result - will get updated as more files show up 
# This combines all the points into a "mass slice"
$(scratch)/cls_limits/$(channel)_%/grid.root: $(scratch)/cls_limits/$(channel)_%/point_*root
	hadd -f $@ $^ 

# Given the card file and the computed grid, compute the obs and exp CLs limits
cards/$(channel)_%.cls.json: cards/$(channel)_%.root $(scratch)/cls_limits/$(channel)_%/grid.root 
	compute_cls.sh $^ $* > $@

################################################################################
## Tools for plotting the limits ###############################################
################################################################################

# Rule to plot the CLs limits
cards/$(channel).cls.pdf: $(cls_results) legendpos.py
	python $(fsa)/StatTools/scripts/plotlimit.py \
	  --max-y 40 \
	  --method cls cards/$(channel)_*.cls.json -o $@ \
	  --legendpos `./legendpos.py $@`

cards/$(channel).cls.tex: $(cls_results)  
	python $(fsa)/StatTools/scripts/texlimit.py \
	  --method cls cards/$(channel)_*.cls.json > $@

cards/$(channel).asymp.tex: $(asymp_results)  
	python $(fsa)/StatTools/scripts/texlimit.py \
	  --method asymp cards/$(channel)_*.asymp.json > $@

# Rule to plot the asymptotic limits
cards/$(channel).asymp.pdf: $(asymp_results) legendpos.py
	python $(fsa)/StatTools/scripts/plotlimit.py \
	  --max-y 40 \
	  --method asymp cards/$(channel)_*.asymp.json -o $@ \
	  --legendpos `./legendpos.py $@`


################################################################################
## Tools for committing into combination SVN ###################################
################################################################################

combination=winter11
combination_mass_points=$(shell seq 115 145) 
combination_FF_mass_points=$(shell seq 120 145)

combination_cards: $(patsubst %, $(combination)/%/vhtt.root, $(combination_mass_points)) \
  $(patsubst %, $(combination)/%/FF_vhtt.root, $(combination_FF_mass_points)) \
  $(patsubst %, $(combination)/%/SM4_vhtt.root, $(combination_mass_points)) 

$(combination)/%/vhtt.root: cards/combined_%.root
	cp $< $@

$(combination)/%/FF_vhtt.root: cards/combined_%FF.root
	cp $< $@

$(combination)/%/SM4_vhtt.root: cards/combined_%SM4.root
	cp $< $@

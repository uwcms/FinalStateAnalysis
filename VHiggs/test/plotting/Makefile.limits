# Makefile to build the correct data cards
#
# Important targets:
#
# General analysis
# ================
#
#  fakes: 		build the fake rate correction functions
#
# Limit Setting
# =============
#
#  cards: 		build the ASCII and .root cards 
#  cls_submits: 	builds the submit directories (in $scratch/cls_limits) 
#  			to submit condor jobs
#  grids: 		hadd add together the results from the condor jobs
#  asymp: 		compute the asymptotic limits
#  cls: 		compute the CLs limits 
#  			(requires condor jobs from cls_submits to be finished)
#  

# The name of the un-stat-shaped root file - output of the analysis
no_stats_shape_file=wh_shapes_raw.root

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
max_cls="50"

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
	if [ -e $(scratch)/cls_limits ]; then
	   mv $(scratch)/cls_limits  $(scratch)/cls_limits.`date +%m.%d.%H-%M`
	fi
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

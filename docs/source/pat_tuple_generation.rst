Generating PAT Tuples
=====================

Setup a 4_2_8_patch7 and/or 5_2_5 area:

In each area run ``cmsenv``.

Get the code::

  git clone git@github.com:ekfriis/FinalStateAnalysis.git
  git checkout 2012-05-28-PatTuple

Add all the dependencies and compile them (takes forever)::

  cd FinalStateAnalysis/recipe
  ./recipe.sh
  cd ../..
  scram b -j 8 

Setup your environment variables::

  cd FinalStateAnalysis/
  source environment.sh

Build the crab submitters::

  cd PatTools/test
  python submit_tuplization_crab.py JOB_ID  --responsible YOUR_NAME

JOB_ID should be agreed upon before hand.  In general, it is formatted as 
YYYY-MM-DD-XTeV-PatTuple.

This will create a directory ``JOB_ID`` with a multicrab.cfg in it::

  source /cms/sw/glite3_2_5/etc/profile.d/grid_env.sh
  source /cms/sw/CRAB_2_8_1/crab.sh
  multicrab -create 
  multicrab -submit 

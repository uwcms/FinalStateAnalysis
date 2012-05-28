Generating PAT Tuples
=====================

Setup a 4_2_8_patch7 and/or 5_2_5 area:

First run ``cmsenv``.

JOB_ID should be agreed upon before hand, and a JOB_ID_TAG will be prepared.  In
general, the JOB_ID is formatted as "YYYY-MM-DD-XTeV-PatTuple".  NB that the
JOB_ID_TAG used for checkout omits the "XTeV" part.

Get the code::

  git clone git://github.com/ekfriis/FinalStateAnalysis.git
  cd FinalStateAnalysis
  git checkout JOB_ID_TAG

You can ignore messages about a "detached head."  Now add all the dependencies and compile (takes forever)::

  cd recipe
  ./recipe.sh
  cd ../..
  scram b -j 8 

Setup your environment variables::

  cd FinalStateAnalysis/
  source environment.sh

Build the crab submitters::

  cd PatTools/test
  python submit_tuplization_crab.py JOB_ID  --responsible YOUR_NAME

YOUR_NAME should be either "Maria", "Josh", "Ian", or "Evan"

This will create a directory ``JOB_ID`` with a multicrab.cfg in it.  Move it to
scratch, then symlink it back to AFS to prevent AFS quota issues.::

  mv JOB_ID /scratch/YOUR_NAME/JOB_ID
  ln -s /scratch/YOUR_NAME/JOB_ID JOB_ID

Now setup your grid stuff, submit the jobs, and say goodbye to your quota::

  source /cms/sw/glite3_2_5/etc/profile.d/grid_env.sh
  source /cms/sw/CRAB_2_8_1/crab.sh
  multicrab -create 
  multicrab -submit 


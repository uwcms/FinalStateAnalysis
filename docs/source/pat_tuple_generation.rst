Generating PAT Tuples
=====================

Setup a 4_2_8_patch7 and/or 5_2_5 area:

First run ``cmsenv``.

The JOB_ID label should be agreed upon before hand.  In
general, the JOB_ID is formatted as "YYYY-MM-DD-XTeV-PatTuple".  

Get the code::

  git clone git://github.com/uwcms/FinalStateAnalysis.git
  cd FinalStateAnalysis

Now add all the dependencies and compile (takes forever)::

  cd recipe
  ./recipe.sh
  cd ../..
  scram b -j 8 

Setup your environment variables::

  cd FinalStateAnalysis/
  source environment.sh

Build the crab submitters::

  cd PatTools/test
  python submit_tuplization_crab.py JOB_ID  

You can pass wildcards to --samples to submit only some samples.  The wildcard
matches the key name in MetaData/python/data{7,8}TeV.py

Example::

   python submit_tuplization_crab.py JOB_ID  --samples "Zjets*" "WplusJets*"

Will create submissions for Zjets and WplusJets only.

For UW group mega-submissions, add ``--responsible YOUR_NAME.`` YOUR_NAME should be either "Maria", "Josh", "Ian", or "Evan"

The submit_tuplization_crab.py script will create a directory ``JOB_ID`` with a multicrab.cfg in it.  

Now setup your grid stuff, submit the jobs, and say goodbye to your quota::

  source /cms/sw/glite3_2_5/etc/profile.d/grid_env.sh
  source /cms/sw/CRAB_2_8_1/crab.sh
  multicrab -create 
  multicrab -submit 

Note on JSON lumi masks
-----------------------

The JSON lumi masks are stored in RecoTools/data/masks.  To get the latest lumi
masks::

  cd $fsa/RecoTools/data/masks
  ./update.sh

this will copy all the new lumi masks from the official AFS area.  Now add and
commit the golden (excluding Muon physics) ones to the repository and commit::

  ls *txt | grep -v MuonPhys | xargs git add -f
  git commit -m "Adding new JSON lumimasks"

Computing the processed luminosity
----------------------------------

If using farmout
''''''''''''''''

Get the processed runs/lumis for a data sample::

  export PATH= /afs/hep.wisc.edu/cms/cmsprod/farmoutCmsJobs/:$PATH
  jobReportSummary.py /path/to/sample/submit/dir/*xml --json-out my_lumis.json

If using CRAB
'''''''''''''

Get the processed lumi JSON file via::

  crab -report

Query the lumi database
'''''''''''''''''''''''

Once you have the processed luminosity, check the recorded integrated luminosity of those run-lumis::

  lumiCalc2.py -i my_lumis.json recorded

See the LumiCalc twiki for more details. 

.. _LumiCalc: https://twiki.cern.ch/twiki/bin/viewauth/CMS/LumiCalc






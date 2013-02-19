Higgs Analysis Software
=======================

TTree Generation
----------------

The file ``higgs_ntuples_cfg.py`` generates TTrees for all Higgs final states of 
interest.  It can be tested in place by::

    cmsRun higgs_ntuples_cfg.py maxEvents=50 inputFiles=my_file.root

The jobs can be submitted to condor using the ``submit_job.py`` script.  Example
to submit jobs based on the 2012-03-05-EWKPatTuple::

   submit_job.py VH JOBID higgs_ntuples_cfg.py --input-dir=/hdfs/store/user/efriis/2012-03-05-EWKPatTuple/{sample}/ --input-files-per-job=5 > do_higgs.txt 
   # Submit the jobs
   bash < do_higgs.txt

The ``do_higgs.txt`` should be committed and tagged after each job submission (to keep track of what 
SW was used to produce the ntuples).


Higgs TTree Definitions
-----------------------

This directory contains the definitions of the Higgs ntuple content.
Each final state (e-mu = em, e-mu-tau = emt) of interest has a .py file
defining the content.

Common blocks of ntuples are grouped together into cfi files::

    h2tau_ntuples_cfi.py 
    trilepton_ntuples_cfi.py
    quad_ntuples_cfi.py
    tnp_ntuples_cfi.py


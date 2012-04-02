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

The ``do_higgs.txt`` should be committed and tagged after each job submission.


Analyses
--------

The VHiggs (ZH and WH) analyses implementations live in ``vh/``

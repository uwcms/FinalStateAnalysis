Higgs Analysis Software
=======================

The file ``make_ntuples_cfg.py`` generates TTrees for all Higgs final states of 
interest.  It can be tested in place by::

    cmsRun make_ntuples_cfg.py channels="em,mt" [options] inputFiles=file.root

There are some additional pre-defined groups of channels which are expanded
for your convenience::

    zh = eeem, eeet, eemt, eett, emmm, emmt, mmmt, mmtt,
    zz = eeee, eemm, mmmm,
    zgg = eegg, mmgg
    llt = emt, mmt, eet, mmm, emm
    zg = mmg,eeg
    zgxtra = mgg, emg, egg,


Ntuple Options
--------------

The available command line options (which are enabled/disabled by setting to
zero or one) are::

    skipEvents=0            - events to skip (for debugging)
    maxEvents=-1            - events to run on
    rerunMCMatch=0          - rerun MC matching
    eventView=0             - make a row in the ntuple correspond to an event
                              instead of a final state in an event.
    passThru=0              - turn off any preselection/skim
    rerunFSA=0              - regenerate PATFinalState dataformats
    verbose=0               - print out timing information
    noPhotons=0             - don't build things which depend on photons.

Batch submission
----------------

The jobs can be submitted to condor using the ``submit_job.py`` script, found in
the FinalStateAnalysis/Utilities/scripts folder.  Example to submit jobs based
on the 2012-03-05-EWKPatTuple::

   submit_job.py JOBID make_ntuples_cfg.py --input-dir=/hdfs/store/user/efriis/2012-03-05-EWKPatTuple/{sample}/ --input-files-per-job=5 > do_higgs.txt 
   # Submit the jobs
   bash < do_higgs.txt

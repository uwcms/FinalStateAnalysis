FSA Flat Ntuple Generation
==========================

The file ``make_ntuples_cfg.py`` generates TTrees for most final states of 
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
    verbose=0               - print out timing information
    noPhotons=0             - don't build things which depend on photons.
    isMC=0                  - run over monte carlo
    runDQM=0                - run on single objects instead of final states, plotting many quantities to make sure things work
    use25ns=1               - (with useMiniAOD=1) use conditions for 25ns PHYS14 miniAOD samples
    hzz=0                   - (with useMiniAOD=1) run the H->ZZ->4l group's FSR algorithm, don't clean
                              alternate Z pairings out of ntuples, several other small changes
    nExtraJets=0            - (for non-jet final states) add basic info about this many jets in addition to final state branches
    paramFile=''            - custom parameter file for ntuple production

Batch submission
----------------

The jobs can be submitted to condor using the ``submit_job.py`` script, found in
the FinalStateAnalysis/Utilities/scripts folder. Run submit_job.py -h to view the
list of possible command line options. submit_job.py creates text for a bash script 
to submit jobs via FarmoutAnalysisJobs.
(see http://www.hep.wisc.edu/cms/comp/faq.html#how-can-i-use-farmoutanalysisjobs...)
By default the output of this script is printed to stdout. You can also use the option
--output_file (-o) to create a script with this information. 

The following will run a bunch of PHYS14 miniAOD files. As new MiniAOD versions are released,
you only need to change the campaign-tag. This command uses a DAS lookup to find all available
datasets for a given campaign and pattern match to the DAS name desired. Careful selection of 
the campaign tag should avoid repeated datasets (since old datasets should be invalidated as
the new ones arrive: example, *-v1 should not appear if *-v2 has been released). Most other
things are now taken care of without special options (miniaod 25ns has been made default)::

   submit_job.py MiniAOD_Test make_ntuples_cfg.py channels="eeee,eeem,eemm,emmm,mmmm,eee,eem,emm,mmm" isMC=1 --campaign-tag="Phys14DR-PU20bx25_PHYS14_25_V*" --samples "ZZTo4L*" "WZJetsTo3LNu*" "WJetsToLNu_13TeV*" "T*_tW*" "T*ToLeptons_*" "TTW*" "TTZ*" "TTJets_MSDecaysCKM*" "DYJetsToLL_M-50_13TeV*" -o do_test.sh
   bash < do_test.sh

Alternatively, you can define a shorthand json to simplify the selection ntuple names (an example
can be found in MetData/tuples/MiniAOD-13TeV.json) by using the option --das-replace-tuple=file.json. 
The command would then use the shorthand names for lookup::


   submit_job.py MiniAOD_Test make_ntuples_cfg.py channels="eeee,eeem,eemm,emmm,mmmm,eee,eem,emm,mmm" isMC=1 --campaign-tag="Phys14DR-PU20bx25_PHYS14_25_V*" --das-replace-tuple=$fsa/MetaData/tuples/MiniAOD-13TeV.json --samples "ZZ*" "WZ*" "DY*" -o do_test.sh
   bash < do_test.sh
   
   
Note: It's a good idea to put your sample names with wildcards inside quotes, as otherwise the unix 
wildcard will be expanded before it is passed to the program (so a file named 'WZsubmit.sh' in your 
folder would cause the argument WZ* to become Wsubmit.sh, which you don't want)




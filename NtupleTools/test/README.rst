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
    svFit=0                 - run secondary vertex stuff
    runMVAMET=0             - compute MVA MET (defaults to 1 if svFit is enabled)
    runDQM=0                - run on single objects instead of final states, plotting many quantities to make sure things work
    hzz=0                   - run the H->ZZ->4l group's FSR algorithm, don't clean
                              alternate Z pairings out of ntuples, several other small changes
    nExtraJets=0            - (for non-jet final states) add basic info about this many jets in addition to final state branches
    paramFile=''            - analysis-specific parameter file defining cuts and extra 
                              ntuple variables. Note that when submitting to CONDOR from
                              UWLogin, the path should be specified starting with
                              'CMSSW_7_X_Y_pZ/src/...'. If you have renamed your CMSSW_BASE, 
                              you will need to find the default name in 'CMSSW_X_X_X formate. 
                              If the file cannot be found, a default is used and the job will not crash.
    keepPat=0               - Instead of creating flat ntuples, write out the high level
                              physics objects including the PATFinalState objects. If >= 2,
                              also keep the packedGenParticles. If >= 3, also keep the 
                              packedPFCandidates (will make output file much larger).

Batch submission
----------------

The jobs can be submitted to condor using the ``submit_job.py`` script, found in
the FinalStateAnalysis/Utilities/scripts folder. Run submit_job.py -h to view the
list of possible command line options. submit_job.py creates text for a bash script 
to submit jobs via FarmoutAnalysisJobs.
(see http://www.hep.wisc.edu/cms/comp/faq.html#how-can-i-use-farmoutanalysisjobs...)
By default the resulting script is printed to stdout. You can also use the option
--output_file (-o) to create put the script in a text file.

The following commands will run some jobs for RunII 25ns MC and data. As new MiniAOD versions are released,
you only need to change the campaign-tag. This command uses a DAS lookup to find all available
datasets for a given campaign and pattern match to the DAS name desired. Careful selection of 
the campaign tag should avoid repeated datasets (since old datasets should be invalidated as
the new ones arrive: example, *-v1 should not appear if *-v2 has been released). Most other
things are now taken care of without special options (miniaod 25ns has been made default)::

   submit_job.py MiniAOD_Test make_ntuples_cfg.py channels="eeee,eeem,eemm,emmm,mmmm,eee,eem,emm,mmm" isMC=1 --campaign-tag="RunIISpring15MiniAODv2-74X_mcRun2_asymptotic_v2-v*" --samples "ZZTo4L*" "WZJetsTo3LNu*" "WJetsToLNu_13TeV*" "T*_tW*" "T*ToLeptons_*" "TTW*" "TTZ*" "TTJets_MSDecaysCKM*" "DYJetsToLL_M-50_13TeV*" -o do_test.sh
   bash < do_test.sh

Alternatively, you can define a shorthand json to simplify the selection ntuple names (an example
can be found in MetData/tuples/MiniAOD-13TeV.json) by using the option --das-replace-tuple=file.json. 
The command would then use the shorthand names for lookup.

All the following commands work when submitting on CentOS7 machines (login01-05), not SLC6 (login06)! No need to increase the memory manually anymore as it is included in the farmout command automatically.

For MC 2016::

   submit_job.py SMHTT_2016 make_ntuples_cfg.py channels="em,mm,et,mt,tt" isMC=1 fullJES=1 metShift=1 isEmbedded=0 skipMET=1 htt=1 era="2016" isLFV=0 runMVAMET=0 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2016_SMHTT_MC.json --campaign-tag="RunIISummer16MiniAODv3-PUMoriond17_94X*" --samples "*" -o submit_mc_2016.sh

For MC 2017::

   submit_job.py SMHTT_2017 make_ntuples_cfg.py channels="em,mm,et,mt,tt" isMC=1 fullJES=1 metShift=1 isEmbedded=0 skipMET=1 htt=1 era="2017" isLFV=0 runMVAMET=0 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2017_SMHTT_MC.json --campaign-tag="RunIIFall17MiniAODv2-PU2017*v14*" --samples "*" -o submit_mc_2017.sh

For MC 2018::

   submit_job.py SMHTT_2018 make_ntuples_cfg.py channels="em,mm,et,mt,tt" isMC=1 fullJES=1 metShift=1 isEmbedded=0 skipMET=1 htt=1 era="2018" isLFV=0 runMVAMET=0 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2018_SMHTT_MC.json --campaign-tag="RunIIAutumn18MiniAOD-102X_upgrade2018*" --samples "*" -o submit_mc_2018.sh
   
   
Note: It's a good idea to put your sample names with wildcards inside quotes, as otherwise the unix 
wildcard will be expanded before it is passed to the program (so a file named 'WZsubmit.sh' in your 
folder would cause the argument WZ* to become Wsubmit.sh, which you don't want)

Note for LFV: Don't use isLFV=1 option because it is rerunning the electron calibration which is already performed elsewhere.


Data 2016::

   submit_job.py SMHTT_2016_data make_ntuples_cfg.py channels="mt,mm" isLFV=0 isMC=0 skipMET=1 fullJES=0 metShift=0 htt=1 era="2016" runMVAMET=0 isEmbedded=0 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2016_Data.json --apply-cmsRun-lumimask --samples "data_SingleMu*" -o submit_data_mt_2016.sh --data --lumimask-json Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt

Data 2017::

   submit_job.py SMHTT_2017_data make_ntuples_cfg.py channels="mt,mm" isLFV=0 isMC=0 skipMET=1 fullJES=0 metShift=0 htt=1 era="2017" runMVAMET=0 isEmbedded=0 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2017_Data.json --apply-cmsRun-lumimask --samples "data_SingleMu*" -o submit_data_mt_2017.sh --data --lumimask-json Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt

Data 2018 ABC::

   submit_job.py SMHTT_2018_data make_ntuples_cfg.py channels="mt,mm" isLFV=0 isMC=0 skipMET=1 fullJES=0 metShift=0 htt=1 era="2018" runMVAMET=0 isEmbedded=0 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2018_DataRereco.json --apply-cmsRun-lumimask --samples "data_SingleMu*" -o submit_dataMu_mt_2018.sh --data --lumimask-json Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt

Data 2018 D::

   submit_job.py SMHTT_2018_data make_ntuples_cfg.py channels="mt,mm" isLFV=0 isMC=0 skipMET=1 fullJES=0 metShift=0 htt=1 era="2018prompt" runMVAMET=0 isEmbedded=0 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2018_DataPrompt.json --apply-cmsRun-lumimask --samples "data_SingleMu*" -o submit_dataMu_mt_2018D.sh --data --lumimask-json Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt
   
Embedded 2016. In the sh file produced by submit_job.py you need to change --input-files-per-job=1 to --input-files-per-job=75::

   submit_job.py SMHTT_2016_embedded make_ntuples_cfg.py channels="mt" isLFV=0 isMC=0 skipMET=1 fullJES=0 metShift=0 htt=1 era="2016" runMVAMET=0 isEmbedded=1 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2016_Embedded.json --apply-cmsRun-lumimask --samples "*MuTau*" -o submit_embedded_2016.sh --embedded --instance prod/phys03 --lumimask-json Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt


Embedded 2017. In the sh file produced by submit_job.py you need to change --input-files-per-job=1 to --input-files-per-job=100::

   submit_job.py SMHTT_2017_embedded make_ntuples_cfg.py channels="mt" isLFV=0 isMC=0 skipMET=1 fullJES=0 metShift=0 htt=1 era="2017" runMVAMET=0 isEmbedded=1 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2017_Embedded.json --apply-cmsRun-lumimask --samples "*MuTau*" -o submit_embedded_2017.sh --embedded --instance prod/phys03 --lumimask-json Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt

Embedded 2018ABC. In the sh file produced by submit_job.py you need to change --input-files-per-job=1 to --input-files-per-job=100::

   submit_job.py SMHTT_2018_embedded make_ntuples_cfg.py channels="mt" isLFV=0 isMC=0 skipMET=1 fullJES=0 metShift=0 htt=1 era="2018" runMVAMET=0 isEmbedded=1 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2018ABC_Embedded.json --apply-cmsRun-lumimask --samples "*MuTau*" -o submit_embedded_2018ABC.sh --embedded --instance prod/phys03 --lumimask-json Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt

Embedded 2018D. In the sh file produced by submit_job.py you need to change --input-files-per-job=1 to --input-files-per-job=100::

   submit_job.py SMHTT_2018_embedded make_ntuples_cfg.py channels="mt" isLFV=0 isMC=0 skipMET=1 fullJES=0 metShift=0 htt=1 era="2018prompt" runMVAMET=0 isEmbedded=1 paramFile=CMSSW_10_2_16_UL/src/FinalStateAnalysis/NtupleTools/python/parameters/ztt.py --extra-usercode-files src/FinalStateAnalysis/NtupleTools/python/parameters --extra-usercode-files src/../cfipython/slc7_amd64_gcc700/RecoEgamma/EgammaTools --das-replace=../../MetaData/tuples/MiniAOD-2018D_Embedded.json --apply-cmsRun-lumimask --samples "*MuTau*" -o submit_embedded_2018D.sh --embedded --instance prod/phys03 --lumimask-json Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt




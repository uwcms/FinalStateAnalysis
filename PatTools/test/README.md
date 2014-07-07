PAT-TUPLE SUBMISSION
====================

The [submit_tuplization.py](https://github.com/uwcms/FinalStateAnalysis/blob/53X_SLC6_Dev/PatTools/test/submit_tuplization.py) takes care of creating the appropriate condor jobs.
You can access the help by simply

```
$ python submit_tuplization.py --help
usage: submit_tuplization.py [-h] [--samples SAMPLES [SAMPLES ...]]
                             [--dbsnames DBSNAMES [DBSNAMES ...]]
                             [--lumimask LUMIMASK] [--xrootd]
                             [--ignoreRunRange]
                             jobid

Build PAT Tuple CRAB submission

positional arguments:
  jobid                 Job ID identifier

optional arguments:
  -h, --help            show this help message and exit
  --samples SAMPLES [SAMPLES ...]
                        Filter samples using list of patterns (shell style)
  --dbsnames DBSNAMES [DBSNAMES ...]
                        use full DBS names
  --lumimask LUMIMASK   Optionally override the lumi mask used.
  --xrootd              fetch files from remote tiers using xrootd
  --ignoreRunRange      ignores the run range passed from datadefs
```

To submit a sample just run

```bash
python submit_tuplization.py $JOBID --xrootd --dbsnames=/SingleMu/Run2012A-22Jan2013-v1/AOD > to_submit.sh
bash < to_submit.sh
```

Once the jobs are done and checked please copy the json file that submit_tuplization.py produced at submission time:

```bash
cp *.json /afs/hep.wisc.edu/home/mverzett/public/uwdb_data/.
```

The information contaied into these file will be mirrored [here](http://www.hep.wisc.edu/~mverzett/cgi-bin/uwdb.cgi) allowing easy access and bookkeeping

MINI-AOD SUBMISSION
===================

The miniAOD submission is currently a work in progress. In the future, submit_tuplzation.py will be modified to allow the submission of miniAOD production locally using xrootd or using crab3. For now, the miniAOD_cfg.py file is just the output os a cmsDriver script for testing purposes only.

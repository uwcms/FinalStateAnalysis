Example mini-analysis
=====================

In this directory are a few files which illustrate using the tools in 
PlotTools to analyze flat ROOT ntuples into histogram files, and then to make
pretty plots from the histograms.

MyAnalyzer.py
-------------

The analysis logic lives here.  This file analyzes a sample (defined in inputs)
and produces a ROOT file with histograms. See the comments in that file for
more information on what it is doing.

Running MyAnalyzer.py
---------------------

The minimal way to run the analyzer is by directly using the "mega" command line
program.

```shell
mega MyAnalyzer.py inputs/JOBID/SAMPLE.txt outputfile.root
```

will process the files listed in SAMPLE.txt and create outptufile.root with the
histograms.   For a less tedious way of running the analysis, see the next
section.

Getting Fancy (a work in progress, not yet complete)
==================================

The inputs directory
--------------------

  The inputs directory stores meta information about the input data.  The
  format is inputs/JOBID/SAMPLE.extension

  The JOBID refers to label created when he ntuples batch jobs were run. SAMPLE
  refers to any old sample - like WplusJets\_madgraph or TTplusJets  In general,
  these correspond to the names of the keys in the datadefs dictionary found
  in MetaData/python/data8TeV.py and friends.

  The starting point is a SAMPLE.txt file, which contains a list of input
  data files.  The next step is to extract all the necessary info about the
  collection of files.  For data, this is the integrated luminosity, for MC
  the effective integrated luminosity.

```shell
  rake "getmeta[inputs/MyJobID, mm/ntuple/Final, 8]"
````

  Will build for each SAMPLE.txt in inputs/MyJobID a SAMPLE.lumicalc.sum
  which has the (effective) integrated lumi.  
  

Rakefile
--------

A rakefile is a Makefile written in the Ruby language.  It is used to define
and run analysis tasks.  A special directory structure is used to define
analysis tasks.

By running:

```shell
   export jobid=MYJOBID (just once)
   rake results/$jobid/MyAnalyzer/SAMPLE.root
```

rake will look at the desired output path and deduce that it should run
MyAnalyzer.py over the inputs in SAMPLE.txt and put the output in the path given
above.  It knows what files this operation depends on.  So if you run a second
time, it will see that nothing has changed and not re-run itself.  If you change
MyAnalyzer.py (or SAMPLE.txt) it will detect the change and know it needs to
re-analyze.


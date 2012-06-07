The WHtautau analysis lives here.

The varous analysis tasks are defined in the Rakefile.

Loading Ntuple Files
====================

Run::

   rake "getinputs[JOB_ID, SOURCE]"

where SOURCE is the location where to find the JOB_ID directory.  For example::

   rake "getinputs[2012-06-03-7TeV-Higgs, /scratch/efriis/data]"

The input .root files are stored in inputs/JOB_ID/sample1.txt,
inputs/JOB_ID/sample2.txt, etc

Analyzing Data
==============

Analysis tasks (things that make histograms) are defined in a .py file.
Each .py file acts on only one ntuple (i.e. e-mu-tau ntuple).
For example, FakeRatesMMT makes fake rate plots using mu-mu-tau events.
The analysis outputs are stored in::

  results/JOB_ID/Analyzer/sample.txt

where [Analyzer] is something like FakeRatesMMT and [sample] is something like
Zjets_M50.txt

You can run a job by::

  rake "analyze[JOB_ID, ANALYZER, sample]"

for example::
  
  rake "analyze[2012-06-03-7TeV-Higgs,FakeRatesMMT,Zjets_M50]"

Htautau Analysis
================

Quick start
-----------

You have to work on login06.  Run ONCE::

   ./setup.sh

which finds the ntuple files (in Evan's scratch directory) and figures out
the relevant integrated luminosities, etc.

To analyze the different samples in the e-mu channels, execute::

  ./run.sh

this will only run things if the output is out-of-date with respect to the 
analyzer.

To change cuts/make new histograms, edit the AnalyzeEM.py analyzer file.

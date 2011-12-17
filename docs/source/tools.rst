Tools
=====

These are various scripts that automate tedious tasks.

pickEvents.py
-------------

Location: PatTools/scripts/pickEvents.py

Given a json file which maps dataset names to lists of run/evt/lumis, create a
file which will call the appropriate copyPickMerge commands.

The json file should have the following format:

``{
    "DATASET_ALIAS" : [ [run1, lumi1, evt1], [run2, lumi2, evt] ],
    "ANOTHER_DATASET_ALIAS" : [ [run1, lumi1, evt1], [run2, lumi2, evt] ]
}``

The actual dataset corresponding to a dataset alias is mapped in
the datadefs dictionary in ``PatTools/datadefs.py``

Usage: 

  pickEvents.py json_file > pickers.sh

  bash < pickers.sh

printEvents.py
--------------

Location: PatTools/scripts/printEvents.py

Companion to pickEvents (above).  Prints out a nicely formatted list given the
run-lumi-evt json file.

deltaR.py
---------

This stupid thing just figures out the deltaR on the command line

Usage: 

  deltaR.py eta1,phi1 eta2,phi2

dropLumiInfo.py
---------------

If you merge a very tight skim together into one EDM root file, it still has the
lumi information from every skimmed lumisection/run.  This can take a lot of
space O(1GB).  This script just takes an input file and drops all the lumi and
run auxilliary information from it.

Usage:

  dropLumiInfo.py inputFiles=[input_file] outputFile=[output_file]


addSelectedHPSTaus.py
---------------------

Fireworks (cmsShow) works on a collection basis, so it doesn't work well w/ the
PFTau discriminator model.  This script just takes an input file, runs PFTau,
and adds a collection "hpsLooseTaus", which are taus which pass the decay mode
and loose combined iso discriminators. 

Usage:

  addSelectedHPSTaus.py inputFiles=[input_file] outputFile=[output_file]

trimJSON.py
-----------

Location: Utilities/scripts/trimJSON.py

Apply a run selection to a JSON file.

Usage:

  trimJSON.py -i json_in -o json_out [-firstRun X] [-lastRun Y]


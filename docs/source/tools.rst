pickEvents.py
=============

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

  pickEvents.py [json_file] > pickers.sh
  bash < pickers.sh

printEvents.py
=============

Location: PatTools/scripts/printEvents.py

Companion to pickEvents (above).  Prints out a nicely formatted list given the
run-lumi-evt json file.

deltaR.py
=========

This stupid thing just figures out the deltaR on the command line

Usage: 

  deltaR.py eta1,phi1 eta2,phi2

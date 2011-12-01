pickEvents.py
=============

Given a json file which maps dataset names to lists of run/evt/lumis, create a
file which will call the appropriate copyPickMerge commands.

Usage: 

pickEvents.py [json_file] > pickers.sh
bash < pickers.sh

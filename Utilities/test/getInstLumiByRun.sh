#!/usr/bin/env bash

# Get the instantaneous luminosity for all of the runs in a given JSON file

mkdir -p runs

JSON=$1

echo $JSON

echo "sadly brilcalc does not work here yet! find another way..."

#cat $1 | dumpRuns.py | xargs -t -n 1 -I % \
  lumiCalc2.py -r % -b stable lumibyls -norm pp7TeV -n 0.0429 -o runs/%.csv

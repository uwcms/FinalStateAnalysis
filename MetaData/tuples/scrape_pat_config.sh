#!/bin/bash

user=$1
for fsadir in `find /afs/hep.wisc.edu/cms/${user}/ -maxdepth 4 -type d -name FinalStateAnalysis`
do
  pat="${fsadir}/PatTools/test"
  if [ -d $pat ]
  then
    find $pat -name "*.json"
  fi
done

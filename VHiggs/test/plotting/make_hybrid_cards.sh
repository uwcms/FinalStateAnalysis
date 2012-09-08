#!/bin/bash

# Hack to make tautau/HWW work together

cd cards

for type in all mmt emt
do
  for i in 100 110 115 120 130 140
  do
    withHWW=${type}_channels_withHWW_$i.card
    dest=${type}_channels_hybrid_$i.card
    rm -f $dest
    if [ -e $withHWW ]
    then
      ln -s $withHWW $dest
    else
      ln -s ${type}_channels_noHWW_$i.card $dest
    fi
  done
done

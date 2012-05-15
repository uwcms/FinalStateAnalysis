#!/bin/bash

function interpolate {
   low=$1
   high=$2
   mass=$3
   mkdir -p $mass
   interpolate_card.py $low/vh3l_cut.txt $low $high/vh3l_cut.txt $high $mass "VHtt" "VHww" > $mass/vh3l_cut.txt
}

for mass in `seq 111 114`
do
  interpolate 110 115 $mass
done

for mass in `seq 116 119`
do
  interpolate 115 120 $mass
done

for mass in `seq 121 124`
do
  interpolate 120 125 $mass
done

for mass in `seq 126 129`
do
  interpolate 125 130 $mass
done

for mass in `seq 131 134`
do
  interpolate 130 135 $mass
done

for mass in `seq 136 139`
do
  interpolate 135 140 $mass
done

for mass in `seq 141 149`
do
  interpolate 140 150 $mass
done

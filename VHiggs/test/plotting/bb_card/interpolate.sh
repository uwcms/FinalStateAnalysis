#!/bin/bash

for mass in `seq 111 114`
do
  interpolate_card.py vhbb_DC_ALL_BDT.110.0.txt 110 vhbb_DC_ALL_BDT.115.0.txt \
    115 $mass "VH" > vhbb_DC_ALL_BDT.$mass.0.txt 
done

for mass in `seq 116 119`
do
  interpolate_card.py vhbb_DC_ALL_BDT.115.0.txt 115 vhbb_DC_ALL_BDT.120.0.txt 120 $mass "VH" > vhbb_DC_ALL_BDT.$mass.0.txt 
done

for mass in `seq 121 124`
do
  interpolate_card.py vhbb_DC_ALL_BDT.120.0.txt 120 vhbb_DC_ALL_BDT.125.0.txt 125 $mass "VH" > vhbb_DC_ALL_BDT.$mass.0.txt 
done

for mass in `seq 126 129`
do
  interpolate_card.py vhbb_DC_ALL_BDT.125.0.txt 125 vhbb_DC_ALL_BDT.130.0.txt 130 $mass "VH" > vhbb_DC_ALL_BDT.$mass.0.txt 
done

for mass in `seq 131 134`
do
  interpolate_card.py vhbb_DC_ALL_BDT.130.0.txt 130 vhbb_DC_ALL_BDT.135.0.txt 135 $mass "VH" > vhbb_DC_ALL_BDT.$mass.0.txt 
done

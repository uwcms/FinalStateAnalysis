#!/bin/bash

# Generate WH->WWW->3LNu for different mass points

for mass in `seq 110 5 160` 
do
  cat template.py | sed "s|HIGGSMASS|$mass|" > PYTHIA6_Tauola_SM_H_2W_2lnu_wh_mH${mass}_7TeV_cff.py
done

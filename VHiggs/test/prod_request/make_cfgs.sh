#!/bin/bash

# Generate WH->WWW->3LNu for different mass points

for mass in `seq 110 5 160` 
do
  cat template.py | sed "s|HIGGSMASS|$mass|" > PYTHIA6_Tauola_SM_H_2W_2lnu_wh_mH${mass}_7TeV_cff.py
done

for mass in `seq 110 5 160` 
do
  cat zh_tt_template.py | sed "s|HIGGSMASS|$mass|" > PYTHIA6_Tauola_SM_H_2Tau_zh_mH${mass}_7TeV_cff.py
done

for mass in `seq 110 5 160` 
do
  cat zh_ww_template.py | sed "s|HIGGSMASS|$mass|" > PYTHIA6_Tauola_SM_H_2W_2lnu_zh_mH${mass}_7TeV_cff.py
done

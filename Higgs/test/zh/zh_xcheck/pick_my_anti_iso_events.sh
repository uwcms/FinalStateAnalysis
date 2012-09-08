#!/bin/bash

# Checking EEMT channel

cat ../inputs/2012-04-08-Higgs/data_DoubleElec*txt > all_doubleel.txt

megaevents.py AnalyzeEEMT.py all_doubleel.txt /eemt/final/Ntuple my_eemt_l1_antiiso_events.json \
  l1_anti_iso

megaevents.py AnalyzeEEMT.py all_doubleel.txt /eemt/final/Ntuple my_eemt_l2_antiiso_events.json \
  l2_anti_iso

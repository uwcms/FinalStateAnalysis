#!/bin/bash 

hadd -f allData_2011A_pileupTruth_v2_finebin.root \
  Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.pileupTruth_v2_finebin.root \
  Cert_165088-167913_7TeV_PromptReco_JSON.pileupTruth_v2_finebin.root \
  Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v2.pileupTruth_v2_finebin.root \
  Cert_172620-173692_PromptReco_JSON.pileupTruth_v2_finebin.root

hadd -f allData_2011B_pileupTruth_v2_finebin.root \
  Cert_175832-177515_PromptReco_JSON.pileupTruth_v2_finebin.root \
  Cert_177718_178078_7TeV_PromptReco_Collisons11_JSON.pileupTruth_v2_finebin.root \
  Cert_177878-179431_7TeV_PromptReco_Collisions11_JSON.pileupTruth_v2_finebin.root \
  Cert_178098-180252_7TeV_PromptReco_Collisions11_JSON.pileupTruth_v2_finebin.root

 hadd -f allData_2011AB_pileupTruth_v2_finebin.root \
   allData_2011A_pileupTruth_v2_finebin.root \
   allData_2011B_pileupTruth_v2_finebin.root


hadd -f allData_2011A_pileupTruth_v2.root \
  Cert_160404-163869_7TeV_May10ReReco_Collisions11_JSON_v3.pileupTruth_v2.root \
  Cert_165088-167913_7TeV_PromptReco_JSON.pileupTruth_v2.root \
  Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v2.pileupTruth_v2.root \
  Cert_172620-173692_PromptReco_JSON.pileupTruth_v2.root

hadd -f allData_2011B_pileupTruth_v2.root \
  Cert_175832-177515_PromptReco_JSON.pileupTruth_v2.root \
  Cert_177718_178078_7TeV_PromptReco_Collisons11_JSON.pileupTruth_v2.root \
  Cert_178098-180252_7TeV_PromptReco_Collisions11_JSON.pileupTruth.root \

hadd -f allData_2011AB_pileupTruth_v2.root \
   allData_2011A_pileupTruth_v2.root \
   allData_2011B_pileupTruth_v2.root


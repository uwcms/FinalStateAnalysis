#!/bin/bash

# These updates are reflected in two commit messages that are not yet merged
# into working branches of CMSSW packages
# cov patch https://github.com/rfriese/cmssw/commit/0fbc53683807893b8230d84e4cfb9d8381ab97c7
# 76x patch https://github.com/rfriese/cmssw/commit/72cb039830ab9425b63eab4cb46b7d74674dce21

echo "Setting up MVA MET for 76x by copying updated files from Tyler's 76x repo"

for item in plugins/PFMETProducerMVA.cc plugins/PFMETProducerMVA.h python/mvaPFMET_cff.py src/PFMETAlgorithmMVA.cc test/mvaMETOnMiniAOD_cfg.py;
do
    echo "cp /afs/cern.ch/work/t/truggles/Z_to_tautau/ZTTJan14_7_6_3/src/RecoMET/METPUSubtraction/$item $CMSSW_BASE/src/RecoMET/METPUSubtraction/$item"
    cp /afs/cern.ch/work/t/truggles/Z_to_tautau/ZTTJan14_7_6_3/src/RecoMET/METPUSubtraction/$item $CMSSW_BASE/src/RecoMET/METPUSubtraction/$item
done

echo "If permissions don't work, let me know truggles at wisc dot edu or just hand copy from"
echo "The above commits."
echo "All done, scram b again"

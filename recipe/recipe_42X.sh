pushd $CMSSW_BASE/src

# For limit tool
cvs co -r V01-13-02 HiggsAnalysis/CombinedLimit
# For a fix to prevent segfaults on certain MC samples when using
# the GenParticlePrunder
cvs co -r V11-03-16 PhysicsTools/HepMCCandAlgos

# PAT RECIPE V08-06-55
addpkg DataFormats/PatCandidates  V06-04-19-04
addpkg PhysicsTools/PatAlgos      V08-06-55
addpkg PhysicsTools/PatUtils      V03-09-18
addpkg CommonTools/ParticleFlow   B4_2_X_V00-03-04
addpkg PhysicsTools/SelectorUtils V00-03-24
addpkg PhysicsTools/UtilAlgos     V08-02-14

echo "Checking out Tau POG recipe"
addpkg DataFormats/TauReco CMSSW_5_2_4 # yes, this is correct
addpkg RecoTauTag/TauTagTools CMSSW_5_2_4
cvs co -r V01-04-17 RecoTauTag/RecoTau
cvs co -r V01-04-01 RecoTauTag/Configuration
cvs co -r V00-04-01 CondFormats/EgammaObjects
cvs up -r 1.53 PhysicsTools/PatAlgos/python/tools/tauTools.py
# Apply an optimization - don't build taus w/ pt < 19
patch -N -p0 < FinalStateAnalysis/recipe/patches/speedupRecoTauCombBuilder.patch

# Add Marias patch for negative SSV 
patch -N -p0 < FinalStateAnalysis/recipe/marias_negativeSSV.patch

# Add MVA MET
# See https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet
rm -rf RecoMET/METProducers RecoMET/METAlgorithms/ DataFormats/METReco/
cvs co -r CMSSW_4_2_8_patch7 RecoMET/METAlgorithms
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METAlgorithms/interface/PFMETAlgorithmMVA.h
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METAlgorithms/interface/mvaMEtUtilities.h
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METAlgorithms/src/PFMETAlgorithmMVA.cc
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METAlgorithms/src/mvaMEtUtilities.cc
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METAlgorithms/BuildFile.xml
cvs co -r CMSSW_4_2_8_patch7 RecoMET/METProducers
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METProducers/interface/PFMETProducerMVA.h
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METProducers/src/PFMETProducerMVA.cc
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METProducers/src/SealModule.cc
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METProducers/python/mvaPFMET_cff.py
cvs up -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METProducers/BuildFile.xml
cvs up -r 1.6 RecoMET/METProducers/python/mvaPFMET_cff.py
pushd RecoMET/METProducers/src/
cp /afs/cern.ch/user/b/bianchi/public/SealModule.cc .
popd 

cvs co -r V00-04-01 CondFormats/EgammaObjects 
cvs co -r CMSSW_5_2_3_patch3 PhysicsTools/SelectorUtils
cvs up -r 1.22 PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h
# My modifications
echo "Adding packages from EK"
cvs co -r 1.1  RecoMET/METProducers/interface/PFMETProducerMVA2.h
cvs co -r 1.1  RecoMET/METProducers/interface/PFMETProducerMVAData.h
cvs co -r 1.1  RecoMET/METProducers/src/PFMETProducerMVA2.cc
cvs co -r 1.1  RecoMET/METProducers/src/PFMETProducerMVAData.cc
addpkg DataFormats/METReco
cvs co -r 1.1 DataFormats/METReco/interface/MVAMETData.h
cvs co -r 1.1 DataFormats/METReco/interface/MVAMETDataFwd.h
cvs co -r 1.1 DataFormats/METReco/src/MVAMETData.cc
patch -N -p0 < FinalStateAnalysis/recipe/patches/mvaMET_classesdef_42x.patch
patch -N -p0 < FinalStateAnalysis/recipe/patches/little_fix_for_MVAMETData.patch
cvs co -r 1.6 RecoMET/METAlgorithms/interface/mvaMEtUtilities.h
cvs co -r 1.7 RecoMET/METAlgorithms/src/mvaMEtUtilities.cc
cvs co -j 1.13 -j 1.14 RecoMET/METProducers/src/SealModule.cc

popd

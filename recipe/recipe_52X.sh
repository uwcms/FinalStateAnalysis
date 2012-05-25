# Tags for 52X

pushd $CMSSW_BASE/src

echo "Checking out PAT tags"
addpkg DataFormats/PatCandidates   V06-05-01
addpkg PhysicsTools/PatAlgos       V08-09-10
addpkg CommonTools/ParticleFlow    V00-03-11
addpkg JetMETCorrections/Type1MET  V04-06-05
addpkg PhysicsTools/PatUtils V03-09-22
addpkg CommonTools/RecoUtils V00-00-08

echo "Checking out Tau POG recipe"
cvs co -r V01-04-17 RecoTauTag/RecoTau #equivalent to 04-14
cvs co -r V01-04-03 RecoTauTag/Configuration
cvs co -r V00-04-01 CondFormats/EgammaObjects
cvs up -r 1.53 PhysicsTools/PatAlgos/python/tools/tauTools.py
cvs up -r 1.12 PhysicsTools/PatAlgos/python/producersLayer1/tauProducer_cff.py
cvs up -r 1.15 PhysicsTools/PatAlgos/python/recoLayer0/tauDiscriminators_cff.py

patch -N -p0 < FinalStateAnalysis/recipe/patches/PhysicsToolsPatAlgos_fix_btags_52X.patch

echo "Building MVA MET recipe"
rm -rf RecoMET/METAlgorithms
rm -rf RecoMET/METProducers
cvs co -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METAlgorithms 
cvs co -r b5_2_X_cvMEtCorr_2012May17 RecoMET/METProducers
cvs co -r V00-04-01 CondFormats/EgammaObjects 
cvs co -r CMSSW_5_2_3_patch3 PhysicsTools/SelectorUtils
cvs up -r 1.22 PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h
echo "Adding packages from EK"
cvs co -r 1.1  RecoMET/METProducers/interface/PFMETProducerMVA2.h
cvs co -r 1.1  RecoMET/METProducers/interface/PFMETProducerMVAData.h
cvs co -r 1.1  RecoMET/METProducers/src/PFMETProducerMVA2.cc
cvs co -r 1.1  RecoMET/METProducers/src/PFMETProducerMVAData.cc
cvs co -r 1.5  RecoMET/METProducers/python/mvaPFMET_cff.py
addpkg DataFormats/METReco
cvs co -r 1.1 DataFormats/METReco/interface/MVAMETData.h
cvs co -r 1.1 DataFormats/METReco/interface/MVAMETDataFwd.h
cvs co -r 1.1 DataFormats/METReco/src/MVAMETData.cc
cvs co -r 1.30 DataFormats/METReco/src/classes.h
cvs co -r 1.29 DataFormats/METReco/src/classes_def.xml
cvs up -r 1.6 RecoMET/METProducers/python/mvaPFMET_cff.py
# One forgotten fix from Christian
patch -N -p0 < FinalStateAnalysis/recipe/patches/little_fix_for_MVAMETData.patch
# Christian forgot to commit these
cvs co -r 1.6 RecoMET/METAlgorithms/interface/mvaMEtUtilities.h
cvs co -r 1.7 RecoMET/METAlgorithms/src/mvaMEtUtilities.cc
cvs co -r 1.14 RecoMET/METProducers/src/SealModule.cc

popd


# For updated lumi tools
cvs co -r V03-05-05 RecoLuminosity/LumiDB 
# For limit tool
cvs co -r V01-12-03 HiggsAnalysis/CombinedLimit
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

# Add Marias patch for negative SSV 
patch -p0 < FinalStateAnalysis/recipe/marias_negativeSSV.patch

# Add MVA MET
# See https://twiki.cern.ch/twiki/bin/view/CMS/MVAMet
cvs co -r V00-02 -d  pharris/MVAMet UserCode/pharris/MVAMet
# Evan's patches on the MVA MET (will hopefully be official soon)
tar xvzf /afs/cern.ch/user/f/friis/public/mvaMETRefactor.tgz 
cvs up -r 1.22 PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h


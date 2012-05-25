pushd $CMSSW_BASE/src

# Tags that work in any release

# Add and patch to way speed up trigger matching
echo "Applying pat trigger matching speedup"
patch -N -p0 < FinalStateAnalysis/recipe/patches/V06-04-16_DataFormats_PatCandidates_PassStrByRef.patch

echo "Adding 2D expression histogram feature"
addpkg -z CommonTools/Utils 
patch -N -p0 < FinalStateAnalysis/recipe/patches/V00-04-02_CommonTools_Utils_Add2DHistoFeature.patch

# Add support for PU Jet ID
# See https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID
cvs co -r V00-04-01 CondFormats/EgammaObjects
cvs co -r V00-02-05 -d CMGTools/External UserCode/CMG/CMGTools/External
cvs co -r V00-02 -d  pharris/MVAMet UserCode/pharris/MVAMet
cvs up -r 1.24 UserCode/CMG/CMGTools/External/src/PileupJetIdAlgo.cc

# Add Electron ID MVA
cvs co -r V00-00-08 -d EGamma/EGammaAnalysisTools UserCode/EGamma/EGammaAnalysisTools
# Get updated effective areas
cvs up -r 1.3 EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h
pushd EGamma/EGammaAnalysisTools/data
cat download.url | xargs wget
popd

# Get Electron ISO MVA weights
cvs co -r V00-00-00 UserCode/sixie/EGamma/EGammaAnalysisTools/data/

# Add muon MVA
cvs co -r V00-00-10 -d Muon/MuonAnalysisTools UserCode/sixie/Muon/MuonAnalysisTools 

# Get electron energy calibrations
# See https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaElectronEnergyScale
# :( no tag is provided on the twiki
cvs co -D "07/05/2012" -d EgammaCalibratedGsfElectrons UserCode/EGamma/EgammaCalibratedGsfElectrons

pushd $CMSSW_BASE/src/FinalStateAnalysis/recipe/
echo "Installing Higgs xsec lookup tables"
./install_HCSaW.sh
popd

popd

from ROOT import gROOT, gSystem

# Generate missing RooFit iterator dictionaries
#
# See: http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=11376

current_path = gROOT.GetMacroPath()
new_path = ':'.join([
    "$CMSSW_BASE/src/FinalStateAnalysis/Utilities/interface/",
    current_path,
])

gROOT.SetMacroPath(new_path)

gSystem.AddIncludePath("-I$ROOFITSYS/include")

gROOT.LoadMacro(
    "roofit_iterators.h+"
)

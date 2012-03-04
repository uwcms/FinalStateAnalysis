'''

Test PROOF dataset registration functionality

'''

import os
import sys
import ROOT
# This needs to be done so the libs get loaded.
from FinalStateAnalysis.TMegaSelector.megaselect import TMegaPySelector

files = ROOT.TFileCollection(
    'WZ_files_test', 'WZ ntuples',
    'wz_files.txt'
)

proof = ROOT.TProof.Open('workers=4')
proof.RegisterDataSet("WZ_files_test", files, "OV")

proof.SetParameter( "PROOF_UseTreeCache",  1 )
proof.Exec('gSystem->Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libFinalStateAnalysisTMegaSelector.so")')

cwd = os.path.abspath(os.getcwd())

path_ok = False
for path in os.environ.get('PYTHONPATH', '').split(':'):
    if not path:
        continue
    if os.path.samefile(cwd, path):
        path_ok = True

if not path_ok:
    print 'YOU MUST ADD $PWD TO THE PYTHONPATH'
    sys.exit(1)

print "Analyze dataset using TDSet"
proof.Process("WZ_files_test#/emt/final/Ntuple", "TMegaPySelector", "WZSelector")

results = proof.GetOutputList()

print results.FindObject("TauPt").GetMean()
print results.FindObject("MuPt").GetMean()
print results.FindObject("BytesRead").GetMean()

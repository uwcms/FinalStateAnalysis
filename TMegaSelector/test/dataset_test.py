'''

Test PROOF dataset registration functionality

'''

import os
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

cwd = os.getcwd()
if cwd not in os.environ.get('PYTHONPATH', ''):
    os.environ['PYTHONPATH'] = cwd + ':' + os.environ.get('PYTHONPATH', '')

print "Analyze dataset using TDSet"
proof.Process("WZ_files_test#/emt/final/Ntuple", "TMegaPySelector", "WZSelector")

results = proof.GetOutputList()

print results.FindObject("TauPt").GetMean()
print results.FindObject("MuPt").GetMean()
print results.FindObject("BytesRead").GetMean()

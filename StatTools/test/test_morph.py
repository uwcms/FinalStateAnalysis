'''

Stupid tests of the th1fmorph tool

'''

from FinalStateAnalysis.StatTools.morph import morph
from rootpy.io import open, DoesNotExist

file = open('$fsa/VHiggs/test/plotting/wh_shapes.root')

hist1 = file.get('mmt_mumu_final_140_MuTauMass/VH140')
hist2 = file.get('mmt_mumu_final_120_MuTauMass/VH120')
hist130true = file.get('mmt_mumu_final_130_MuTauMass/VH130')

print '140', hist1.Integral(), hist1.GetMean()
print '130 true', hist130true.Integral(), hist130true.GetMean()
print '120', hist2.Integral(), hist2.GetMean()

# Try to morph to 130

m130 = morph('130', '130', 130, hist1, 140, hist2, 120)
print m130.Integral(), m130.GetMean()

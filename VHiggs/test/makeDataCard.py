import ROOT
import math
import FinalStateAnalysis.Utilities.DataCard as dc
import FinalStateAnalysis.Utilities.Histo as Histo

shape_file = "all_shapes.root"

shapes = ROOT.TFile.Open(shape_file, "READ")

mmt = dc.DataCardChannel("mmt", shapes)
mmt.add_signal('signal')
mmt.add_background('fakes')
mmt.add_background('wz')
mmt.add_background('zz')

mmt.add_sys('lumi', 1.04, ['signal', 'wz', 'zz'])
mmt.add_sys('wz', 1.10, ['wz'])
mmt.add_sys('zz', 1.10, ['zz'])

mmt_fake_unweighted = Histo.Histo(shapes.Get('mmt/ext_data_unweighted'))
mmt_fake_error = 1 + math.sqrt(mmt_fake_unweighted.Integral())/mmt_fake_unweighted.Integral()
mmt.add_sys('mmt_fake_err', mmt_fake_error, ['fakes'])

emt = dc.DataCardChannel("emt", shapes)
emt.add_signal('signal')
emt.add_background('fakes')
emt.add_background('wz')
emt.add_background('zz')

emt.add_sys('lumi', 1.04, ['signal', 'wz', 'zz'])
emt.add_sys('wz', 1.10, ['wz'])
emt.add_sys('zz', 1.10, ['zz'])

emt_fake_unweighted = Histo.Histo(shapes.Get('emt/ext_data_unweighted'))
emt_fake_error = 1 + math.sqrt(emt_fake_unweighted.Integral())/emt_fake_unweighted.Integral()
emt.add_sys('emt_fake_err', emt_fake_error, ['fakes'])

output = open('all_channels.card', 'w')
card = dc.DataCard('VHtautau fit', '2.1 fb-1', [mmt, emt], shape_file)
card.write(output)

output = open('mmt_channels.card', 'w')
card = dc.DataCard('VHtautau fit', '2.1 fb-1', [mmt], shape_file)
card.write(output)

output = open('emt_channels.card', 'w')
card = dc.DataCard('VHtautau fit', '2.1 fb-1', [emt], shape_file)
card.write(output)

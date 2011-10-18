import ROOT
import math
import FinalStateAnalysis.Utilities.DataCard as dc
import FinalStateAnalysis.Utilities.Histo as Histo

def dump_table(file, folder):
    subdir = file.Get(folder)
    data = subdir.Get("data_obs").Integral()
    fakes = subdir.Get("fakes").Integral()
    n_denom = subdir.Get("ext_data_unweighted").Integral()
    fake_err = fakes*math.sqrt(n_denom)/n_denom
    wz = subdir.Get("wz").Integral()
    zz = subdir.Get("zz").Integral()
    signal = subdir.Get("signal").Integral()
    print " Sample & Yield \\\\"
    print " \hline"
    print " Fakes & $%0.1f \pm %0.1f$ \\\\" % (fakes, fake_err)
    print " WZ & %0.1f \\\\" % wz
    print " ZZ & %0.1f \\\\" % zz
    print " \hline"
    print " SM & $%0.1f \pm %0.1f$\\\\" % (wz + zz + fakes, fake_err)
    print " \hline"
    print " Data & $%i \pm %0.1f$ \\\\" % (int(data), math.sqrt(data))
    print "\hline"
    print " VH(115) & %0.1f \\\\" % signal

#shape_file = "all_shapes.root"
shape_file = "2x_shapes.root"

shapes = ROOT.TFile.Open(shape_file, "READ")

for folder in ['mmt_115', 'emt_115']:
    print "TEX TABLE FOR", folder
    print ""
    dump_table(shapes, folder)
    print ""

for mass in [115, 120, 125]:
    mmt = dc.DataCardChannel("mmt_%i" % mass, shapes)
    mmt.add_signal('signal')
    mmt.add_background('fakes')
    mmt.add_background('wz')
    mmt.add_background('zz')

    mmt.add_sys('lumi', 1.04, ['signal', 'wz', 'zz'])
    mmt.add_sys('wz', 1.10, ['wz'])
    mmt.add_sys('zz', 1.10, ['zz'])

    mmt_fake_unweighted = Histo.Histo(shapes.Get('mmt_115/ext_data_unweighted'))
    mmt_fake_error = 1 + math.sqrt(mmt_fake_unweighted.Integral())/mmt_fake_unweighted.Integral()
    mmt.add_sys('mmt_fake_err', mmt_fake_error, ['fakes'])

    emt = dc.DataCardChannel("emt_%i" % mass, shapes)
    emt.add_signal('signal')
    emt.add_background('fakes')
    emt.add_background('wz')
    emt.add_background('zz')

    emt.add_sys('lumi', 1.04, ['signal', 'wz', 'zz'])
    emt.add_sys('wz', 1.10, ['wz'])
    emt.add_sys('zz', 1.10, ['zz'])

    emt_fake_unweighted = Histo.Histo(shapes.Get('emt_115/ext_data_unweighted'))
    emt_fake_error = 1 + math.sqrt(emt_fake_unweighted.Integral())/emt_fake_unweighted.Integral()
    emt.add_sys('emt_fake_err', emt_fake_error, ['fakes'])

    output = open('all_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '2.1 fb-1', [mmt, emt], shape_file)
    card.write(output)

    output = open('mmt_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '2.1 fb-1', [mmt], shape_file)
    card.write(output)

    output = open('emt_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '2.1 fb-1', [emt], shape_file)
    card.write(output)

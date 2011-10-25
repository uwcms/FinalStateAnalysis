import ROOT
import math
import FinalStateAnalysis.Utilities.DataCard as dc
import FinalStateAnalysis.Utilities.Histo as Histo

wz_err = 0.166
zz_err = 0.40

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

def dump_table(file, folder, stream):
    subdir = file.Get(folder)
    data = subdir.Get("data_obs").Integral()
    fakes = subdir.Get("fakes").Integral()
    n_denom = subdir.Get("ext_data_unweighted").Integral()
    fake_err = fakes*math.sqrt(n_denom)/n_denom
    wz = subdir.Get("wz").Integral()
    zz = subdir.Get("zz").Integral()
    signal = subdir.Get("signal").Integral()
    stream.write(" Sample & Yield \\\\\n")
    stream.write(" \hline\n")
    stream.write(" Fakes & $%0.1f \pm %0.1f$ \\\\\n" % (fakes, fake_err))
    stream.write(" WZ & $%0.1f \pm %0.1f$ \\\\\n" % (wz, wz*wz_err))
    stream.write(" ZZ & $%0.1f \pm %0.1f$\\\\\n" % (zz, zz*zz_err))
    stream.write(" \hline\n")
    stream.write(" SM & $%0.1f \pm %0.1f$\\\\\n" % (wz + zz + fakes, quad(fake_err, wz*wz_err, zz*zz_err)))
    stream.write(" \hline")
    stream.write(" Data & $%i \pm %0.1f$ \\\\\n" % (int(data), math.sqrt(data)))
    stream.write("\hline\n")
    stream.write(" VH(115) & %0.1f \\\\\n" % signal)

shape_file = "all_shapes.root"
#shape_file = "2x_shapes.root"

shapes = ROOT.TFile.Open(shape_file, "READ")

for folder in ['mmt_115', 'emt_115']:
    file = open(folder + 'yields.tex', 'w')
    dump_table(shapes, folder, file)

for mass in [110, 115, 120, 125]:
    mmt = dc.DataCardChannel("mmt_%i" % mass, shapes)
    mmt.add_signal('signal')
    mmt.add_background('fakes')
    mmt.add_background('wz')
    mmt.add_background('zz')

    mmt.add_sys('lumi', 1.04, ['signal', 'wz', 'zz'])
    mmt.add_sys('wz', 1.0 + wz_err, ['wz'])
    mmt.add_sys('zz', 1.0 + zz_err, ['zz'])
    mmt.add_sys('tau_id', 1.06, ['wz', 'signal', 'zz'])
    mmt.add_sys('mu_id', 1.014, ['wz', 'signal', 'zz'])

    mmt_fake_unweighted = Histo.Histo(shapes.Get('mmt_115/ext_data_unweighted'))
    mmt_fake_error = 1 + math.sqrt(mmt_fake_unweighted.Integral())/mmt_fake_unweighted.Integral()
    mmt.add_sys('mmt_fake_err', mmt_fake_error, ['fakes'])

    emt = dc.DataCardChannel("emt_%i" % mass, shapes)
    emt.add_signal('signal')
    emt.add_background('fakes')
    emt.add_background('wz')
    emt.add_background('zz')

    emt.add_sys('lumi', 1.04, ['signal', 'wz', 'zz'])
    emt.add_sys('wz', 1.0 + wz_err, ['wz'])
    emt.add_sys('zz', 1.0 + zz_err, ['zz'])
    emt.add_sys('tau_id', 1.06, ['wz', 'signal', 'zz'])
    emt.add_sys('mu_id', 1.01, ['wz', 'signal', 'zz'])
    emt.add_sys('e_id', 1.02, ['wz', 'signal', 'zz'])

    emt_fake_unweighted = Histo.Histo(shapes.Get('emt_115/ext_data_unweighted'))
    emt_fake_error = 1 + math.sqrt(emt_fake_unweighted.Integral())/emt_fake_unweighted.Integral()
    emt.add_sys('emt_fake_err', emt_fake_error, ['fakes'])

    output = open('cards/all_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '2.1 fb-1', [mmt, emt], shape_file)
    card.write(output)

    output = open('cards/mmt_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '2.1 fb-1', [mmt], shape_file)
    card.write(output)

    output = open('cards/emt_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '2.1 fb-1', [emt], shape_file)
    card.write(output)

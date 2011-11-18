import ROOT
import math
import FinalStateAnalysis.Utilities.DataCard as dc
import FinalStateAnalysis.Utilities.Histo as Histo

wz_err = 0.166
zz_err = 0.40
lumi_err = 0.045
tau_err = 0.06
mu_id_err = 0.014
pdf_err = 0.03

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

shape_file = "wh_shapes.root"

shapes = ROOT.TFile.Open(shape_file, "READ")

for folder in ['mmt_115_final_MuTauMass', 'emt_115_final_ETauMass',
               'emm_115_final_MuElecMass', ]:
    file = open(folder + 'yields.tex', 'w')
    dump_table(shapes, folder, file)

for mass in [100, 110, 115, 120, 125, 135, 140, 145, 160]:
    mmt = dc.DataCardChannel("mmt_%i_final_MuTauMass" % mass, shapes)
    mmt.add_signal('signal')
    mmt.add_background('fakes')
    mmt.add_background('wz')
    mmt.add_background('zz')

    mmt.add_sys('lumi', 1 + lumi_err, ['signal', 'wz', 'zz'])
    mmt.add_sys('wz', 1.0 + wz_err, ['wz'])
    mmt.add_sys('zz', 1.0 + zz_err, ['zz'])
    mmt.add_sys('CMS_eff_t', 1+ tau_err, ['wz', 'signal', 'zz'])
    mmt.add_sys('CMS_eff_m', 1 + quad(mu_id_err, mu_id_err), ['wz', 'signal', 'zz'])
    mmt.add_sys('pdf_vh', 1 + pdf_err, ['signal'])

    mmt_fake_unweighted = Histo.Histo(shapes.Get('mmt_115_final_vtxChi2NODF/ext_data_unweighted'))
    mmt_fake_error = 1 + math.sqrt(mmt_fake_unweighted.Integral())/mmt_fake_unweighted.Integral()
    mmt.add_sys('mmt_fake_err', mmt_fake_error, ['fakes'])

    emt = dc.DataCardChannel("emt_%i_final_ETauMass" % mass, shapes)
    emt.add_signal('signal')
    emt.add_background('fakes')
    emt.add_background('wz')
    emt.add_background('zz')

    emt.add_sys('lumi', 1 + lumi_err, ['signal', 'wz', 'zz'])
    emt.add_sys('wz', 1.0 + wz_err, ['wz'])
    emt.add_sys('zz', 1.0 + zz_err, ['zz'])
    emt.add_sys('CMS_eff_t', 1 + tau_err, ['wz', 'signal', 'zz'])
    emt.add_sys('CMS_eff_m', 1 + mu_id_err, ['wz', 'signal', 'zz'])
    emt.add_sys('CMS_eff_e', 1.02, ['wz', 'signal', 'zz'])
    emt.add_sys('pdf_vh', 1 + pdf_err, ['signal'])

    emt_fake_unweighted = Histo.Histo(shapes.Get('emt_115_final_vtxChi2NODF/ext_data_unweighted'))
    emt_fake_error = 1 + math.sqrt(emt_fake_unweighted.Integral())/emt_fake_unweighted.Integral()
    emt.add_sys('emt_fake_err', emt_fake_error, ['fakes'])

    emm = dc.DataCardChannel("emm_%i_final_MuElecMass" % mass, shapes)
    emm.add_signal('signal')
    emm.add_background('fakes')
    emm.add_background('wz')
    emm.add_background('zz')

    emm.add_sys('lumi', 1 + lumi_err, ['signal', 'wz', 'zz'])
    emm.add_sys('wz', 1.0 + wz_err, ['wz'])
    emm.add_sys('zz', 1.0 + zz_err, ['zz'])
    emm.add_sys('CMS_eff_m', 1 + quad(mu_id_err, mu_id_err), ['wz', 'signal', 'zz'])
    emm.add_sys('CMS_eff_e', 1.02, ['wz', 'signal', 'zz'])
    emm.add_sys('pdf_vh', 1 + pdf_err, ['signal'])

    emm_fake_unweighted = Histo.Histo(shapes.Get('emm_115_final_MuElecMass/ext_data_unweighted'))
    emm_fake_error = 1 + math.sqrt(emm_fake_unweighted.Integral())/emm_fake_unweighted.Integral()
    emm.add_sys('emm_fake_err', emm_fake_error, ['fakes'])

    output = open('cards/all_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '4.6 fb-1', [mmt, emt, emm], shape_file)
    card.write(output)

    output = open('cards/mmt_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '4.6 fb-1', [mmt], shape_file)
    card.write(output)

    output = open('cards/emt_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '4.6 fb-1', [emt], shape_file)
    card.write(output)

    output = open('cards/emm_channels_%i.card' % mass, 'w')
    card = dc.DataCard('VHtautau fit', '4.6 fb-1', [emm], shape_file)
    card.write(output)

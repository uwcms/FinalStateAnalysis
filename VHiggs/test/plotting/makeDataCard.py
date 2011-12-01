import ROOT
import math
import re
import FinalStateAnalysis.Utilities.DataCard as dc
import FinalStateAnalysis.Utilities.Histo as Histo

import rootpy.io as io

wz_err = 0.166
zz_err = 0.40
lumi_err = 0.045
tau_err = 0.06
mu_id_err = 0.014
pdf_err = 0.04

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

shapes = io.open(shape_file, "READ")

for folder in ['mmt_115_final_MuTauMass', 'emt_115_final_ETauMass',
               'emm_115_final_MuElecMass', ]:
    break
    file = io.open(folder + 'yields.tex', 'w')
    dump_table(shapes, folder, file)

# Decide which shapes to use
mmt_shape = 'MuTauMass'
emt_shape = 'ETauMass'
emm_shape = 'MuElecMass'

# Counting experiment only
#mmt_shape = 'count'
#emt_shape = 'count'
#emm_shape = 'count'

# Add an arbitrary penalty factor to the fake rate error (for testing)
#fake_err_penalty = math.sqrt(3)
fake_err_penalty = 1

for mass in [100, 110, 115, 120, 125, 135, 140, 145, 160]:
    mmt_folder = "mmt_%i_final_%s" % (mass, mmt_shape)
    mmt = dc.DataCardChannel(mmt_folder, shapes)
    mmt.add_signal('signal')
    mmt.add_background('lead_fakes')
    mmt.add_background('sub_fakes')
    mmt.add_background('wz')
    mmt.add_background('zz')

    mmt.add_sys('lumi', 1 + lumi_err, ['signal', 'wz', 'zz'])
    mmt.add_sys('wz', 1.0 + wz_err, ['wz'])
    mmt.add_sys('zz', 1.0 + zz_err, ['zz'])
    mmt.add_sys('CMS_eff_t', 1+ tau_err, ['wz', 'signal', 'zz'])
    mmt.add_sys('CMS_eff_m', 1 + quad(mu_id_err, mu_id_err), ['wz', 'signal', 'zz'])
    mmt.add_sys('pdf_vh', 1 + pdf_err, ['signal'])

    for path, subdirs, histos in shapes.walk(mmt_folder, class_pattern="TH1*"):
        bin_index_finder = re.compile('.*_bin_(?P<index>[0-9]*)(Up|Down)')
        # Set of lead fake bins which have a systematic
        lead_fake_sys_bins = set([])
        sub_fake_sys_bins = set([])
        for histo in histos:
            if 'lead_fakes_' in histo:
                match = bin_index_finder.match(histo)
                assert(match)
                lead_fake_sys_bins.add(int(match.group('index')))
            if 'sub_fakes_' in histo:
                match = bin_index_finder.match(histo)
                assert(match)
                sub_fake_sys_bins.add(int(match.group('index')))
        for index in lead_fake_sys_bins:
            mmt.add_sys('lead_bin_%i' % index, 1.0, 'lead_fakes', type='shape')
        for index in sub_fake_sys_bins:
            mmt.add_sys('sub_bin_%i' % index, 1.0, 'sub_fakes', type='shape')

    emt_folder = "emt_%i_final_%s" % (mass, emt_shape)
    emt = dc.DataCardChannel(emt_folder, shapes)
    emt.add_signal('signal')
    emt.add_background('e_fakes')
    emt.add_background('mu_fakes')
    emt.add_background('wz')
    emt.add_background('zz')

    emt.add_sys('lumi', 1 + lumi_err, ['signal', 'wz', 'zz'])
    emt.add_sys('wz', 1.0 + wz_err, ['wz'])
    emt.add_sys('zz', 1.0 + zz_err, ['zz'])
    emt.add_sys('CMS_eff_t', 1 + tau_err, ['wz', 'signal', 'zz'])
    emt.add_sys('CMS_eff_m', 1 + mu_id_err, ['wz', 'signal', 'zz'])
    emt.add_sys('CMS_eff_e', 1.02, ['wz', 'signal', 'zz'])
    emt.add_sys('pdf_vh', 1 + pdf_err, ['signal'])

    for path, subdirs, histos in shapes.walk(emt_folder, class_pattern="TH1*"):
        bin_index_finder = re.compile('.*_bin_(?P<index>[0-9]*)(Up|Down)')
        # Set of lead fake bins which have a systematic
        mu_fake_sys_bins = set([])
        e_fake_sys_bins = set([])
        for histo in histos:
            if 'mu_fakes_' in histo:
                match = bin_index_finder.match(histo)
                assert(match)
                mu_fake_sys_bins.add(int(match.group('index')))
            if 'e_fakes_' in histo:
                match = bin_index_finder.match(histo)
                assert(match)
                e_fake_sys_bins.add(int(match.group('index')))
        for index in mu_fake_sys_bins:
            emt.add_sys('mu_bin_%i' % index, 1.0, 'mu_fakes', type='shape')
        for index in e_fake_sys_bins:
            emt.add_sys('e_bin_%i' % index, 1.0, 'e_fakes', type='shape')

    emm = dc.DataCardChannel("emm_%i_final_%s" % (mass, emm_shape), shapes)
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
    emm_fake_error = 1 + fake_err_penalty*math.sqrt(emm_fake_unweighted.Integral())/emm_fake_unweighted.Integral()
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

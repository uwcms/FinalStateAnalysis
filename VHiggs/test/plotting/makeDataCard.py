import math
import re
import FinalStateAnalysis.Utilities.DataCard as dc

import rootpy.io as io

wz_err = 0.166
zz_err = 0.40
lumi_err = 0.045
tau_err = 0.06
mu_id_err = 0.014
pdf_err = 0.04
chi2err = 0.05

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

def dump_table(file, folder, stream):
    subdir = file.Get(folder)
    data = subdir.Get("data_obs").Integral()
    fake_histo = subdir.Get("fakes")
    fakes = fake_histo.Integral()
    fake_error = 0
    # Add the errors from all bins in quadrature
    for bin in range(1, fake_histo.GetNbinsX() + 1):
        fake_error += fake_histo.GetBinError(bin)**2
    fake_error = math.sqrt(fake_error)

    wz = subdir.Get("wz").Integral()
    zz = subdir.Get("zz").Integral()
    signal = subdir.Get("signal").Integral()
    signalHWW = subdir.Get("signalHWW").Integral()
    stream.write(" Sample & Yield \\\\\n")
    stream.write(" \hline\n")
    stream.write(" Fakes & $%0.1f \pm %0.1f$ \\\\\n" % (fakes, fake_error))
    stream.write(" WZ & $%0.1f \pm %0.1f$ \\\\\n" % (wz, wz*wz_err))
    stream.write(" ZZ & $%0.1f \pm %0.1f$\\\\\n" % (zz, zz*zz_err))
    stream.write(" \hline\n")
    stream.write(" SM & $%0.1f \pm %0.1f$\\\\\n" % (
        wz + zz + fakes, quad(fake_error, wz*wz_err, zz*zz_err)))
    stream.write(" \hline")
    stream.write(" Data & $%i \pm %0.1f$ \\\\\n" % (int(data), math.sqrt(data)))
    stream.write("\hline\n")
    stream.write(" VH(120) & %0.1f \\\\\n" % (signal + signalHWW))

shape_file = "wh_shapes.root"

shapes = io.open(shape_file, "READ")

for label, folder in [('mmt_mumu', 'mmt_mumu_final_120_MuTauMass'),
                      ('emt_emu', 'emt_emu_final_120_ETauMass'),
                      #('emm_mumu', 'emm_mumu_final_120_MuElecMass')
                     ]:
    file = open(label + '_yields.tex', 'w')
    dump_table(shapes, folder, file)

# Decide which shapes to use
mmt_shape = 'MuTauMass'
emt_shape = 'ETauMass'
emm_shape = 'MuElecMass'

# Counting experiment only
#mmt_shape = 'count'
#emt_shape = 'count'
#emm_shape = 'count'

# Add a fake normalization error
e_fake_error = 0.0
mu_fake_error = 0.3
high_mu_fake_error = 0.0

#e_fake_error = -1
#mu_fake_error = -1
#high_mu_fake_error = -1

#for mass in [100, 110, 115, 120, 125, 135, 140, 145, 160]:
for with_HWW in [True, False]:
    for mass in [100, 110, 115, 120, 125, 130, 135, 140, 145]:

        signal_datasets = ['signal']

        if with_HWW:
            if mass in [120, 130, 140]:
                signal_datasets.append('signalHWW')
            else:
                continue

        mmt_folder = "mmt_mumu_final_%i_%s" % (mass, mmt_shape)
        mmt = dc.DataCardChannel(mmt_folder, shapes)
        for signal_dataset in signal_datasets:
            mmt.add_signal(signal_dataset)

        mmt.add_background('fakes')
        mmt.add_background('wz')
        mmt.add_background('zz')

        mmt.add_sys('lumi', 1 + lumi_err, signal_datasets + ['wz', 'zz'])
        mmt.add_sys('chi2Lt', 1 + chi2err, signal_datasets + ['wz', 'zz'])
        mmt.add_sys('wz', 1.0 + wz_err, ['wz'])
        mmt.add_sys('zz', 1.0 + zz_err, ['zz'])
        mmt.add_sys('CMS_eff_t', 1+ tau_err, signal_datasets + ['wz', 'zz'])
        mmt.add_sys('CMS_eff_m', 1 + quad(mu_id_err, mu_id_err), signal_datasets + ['wz', 'zz'])
        mmt.add_sys('pdf_vh', 1 + pdf_err, signal_datasets)
        if mu_fake_error > 0:
            mmt.add_sys('mu_fake_norm', 1 + mu_fake_error, 'fakes')
        if high_mu_fake_error > 0:
            mmt.add_sys('high_mu_fake_norm', 1 + high_mu_fake_error, 'fakes')

        bin_index_finder = re.compile('^fakes_(?P<fr_type>.*)_bin_(?P<index>[0-9]*)(Up|Down)')
        for path, subdirs, histos in shapes.walk(mmt_folder, class_pattern="TH1*"):
            # Set of lead fake bins which have a systematic
            fake_sys_bins = []
            for histo in histos:
                match = bin_index_finder.match(histo)
                if match:
                    fake_sys_bins.append(
                        '%s_bin_%s' % (match.group('fr_type'), match.group('index'))
                    )

            for fake_sys in fake_sys_bins:
                mmt.add_sys(fake_sys, 1.0, 'fakes', type='shape')

        emt_folder = "emt_emu_final_%i_%s" % (mass, emt_shape)
        emt = dc.DataCardChannel(emt_folder, shapes)
        for signal_dataset in signal_datasets:
            emt.add_signal(signal_dataset)
        emt.add_background('fakes')
        emt.add_background('wz')
        emt.add_background('zz')

        emt.add_sys('lumi', 1 + lumi_err, signal_datasets + ['wz', 'zz'])
        emt.add_sys('chi2Lt', 1 + chi2err, signal_datasets + ['wz', 'zz'])
        emt.add_sys('wz', 1.0 + wz_err, ['wz'])
        emt.add_sys('zz', 1.0 + zz_err, ['zz'])
        emt.add_sys('CMS_eff_t', 1+ tau_err, signal_datasets + ['wz', 'zz'])
        emt.add_sys('CMS_eff_m', 1 + mu_id_err, signal_datasets + ['wz', 'zz'])
        emt.add_sys('CMS_eff_e', 1.02, signal_datasets + ['wz', 'zz'])
        emt.add_sys('pdf_vh', 1 + pdf_err, signal_datasets)
        if e_fake_error > 0:
            emt.add_sys('e_fake_norm', 1 + e_fake_error, 'fakes')
        if mu_fake_error > 0:
            emt.add_sys('mu_fake_norm', 1 + mu_fake_error, 'fakes')

        for path, subdirs, histos in shapes.walk(emt_folder, class_pattern="TH1*"):
            # Set of lead fake bins which have a systematic
            fake_sys_bins = []
            for histo in histos:
                match = bin_index_finder.match(histo)
                if match:
                    fake_sys_bins.append(
                        '%s_bin_%s' % (match.group('fr_type'), match.group('index'))
                    )

            for fake_sys in fake_sys_bins:
                emt.add_sys(fake_sys, 1.0, 'fakes', type='shape')

        #emm_folder = "emm_mumu_final_%i_%s" % (mass, emm_shape)
        #emm = dc.DataCardChannel(emm_folder, shapes)
        #emm.add_signal('signal')
        #emm.add_background('fakes')
        #emm.add_background('wz')
        #emm.add_background('zz')

        #emm.add_sys('lumi', 1 + lumi_err, ['signal', 'wz', 'zz'])
        #emm.add_sys('wz', 1.0 + wz_err, ['wz'])
        #emm.add_sys('zz', 1.0 + zz_err, ['zz'])
        #emm.add_sys('CMS_eff_m', 1 + quad(mu_id_err, mu_id_err), ['wz', 'signal', 'zz'])
        #emm.add_sys('CMS_eff_e', 1.02, ['wz', 'signal', 'zz'])
        #emm.add_sys('pdf_vh', 1 + pdf_err, ['signal'])

        #for path, subdirs, histos in shapes.walk(emm_folder, class_pattern="TH1*"):
            ## Set of lead fake bins which have a systematic
            #fake_sys_bins = []
            #for histo in histos:
                #match = bin_index_finder.match(histo)
                #if match:
                    #fake_sys_bins.append(
                        #'%s_bin_%s' % (match.group('fr_type'), match.group('index'))
                    #)

            #for fake_sys in fake_sys_bins:
                #emm.add_sys(fake_sys, 1.0, 'fakes', type='shape')

        label = ''
        if with_HWW:
            label = '_withHWW'
        else:
            label = '_noHWW'


        output = open('cards/all_channels%s_%i.card' % (label, mass), 'w')
        #card = dc.DataCard('VHtautau fit', '4.6 fb-1', [mmt, emt, emm], shape_file)
        card = dc.DataCard('VHtautau fit', '4.6 fb-1', [mmt, emt], shape_file)
        card.write(output)

        output = open('cards/mmt_channels%s_%i.card' % (label, mass), 'w')
        card = dc.DataCard('VHtautau fit', '4.6 fb-1', [mmt], shape_file)
        card.write(output)

        output = open('cards/emt_channels%s_%i.card' % (label, mass), 'w')
        card = dc.DataCard('VHtautau fit', '4.6 fb-1', [emt], shape_file)
        card.write(output)

        #output = open('cards/emm_channels_%i.card' % mass, 'w')
        #card = dc.DataCard('VHtautau fit', '4.6 fb-1', [emm], shape_file)
        #card.write(output)

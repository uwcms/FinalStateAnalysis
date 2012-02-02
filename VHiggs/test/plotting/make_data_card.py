'''

Make the data card for a given mass point

'''

import math
from optparse import OptionParser
import re

import FinalStateAnalysis.StatTools.DataCard as dc

parser = OptionParser(usage="usage: %prog [options]")

parser.add_option("-o", "--out", dest="out", default="output_card.txt",
                  type="string", help="Output card file")

parser.add_option("-m", "--mass", dest="mass", default=120,
                  type=int, help="Higgs mass")

parser.add_option("-f", "--file", dest="file", default="wh_shapes.root",
                  type="string", help="Shape file")

parser.add_option("--mmt_shape", type="string", default="MuTauMass",
                  help="Shape to use for MMT channel")

parser.add_option("--emt_shape", type="string", default="ETauMass",
                  help="Shape to use for EMT channel")

parser.add_option("--wz_err", type="float", default=0.166,
                  help="WZ normalization error")

parser.add_option("--zz_err", type="float", default=0.40,
                  help="WZ normalization error")

parser.add_option("--lumi_err", type="float", default=0.045,
                  help="Lumi normalization error")

parser.add_option("--tau_err", type="float", default=0.06,
                  help="Tau ID error")

parser.add_option("--mu_err", type="float", default=0.014,
                  help="Mu ID error")

parser.add_option("--pdf_err", type="float", default=0.04,
                  help="VH PDF error")

parser.add_option("--topo_cut_err", type="float", default=0.05,
                  help="Topo cuts")

parser.add_option("--e_fake_err", type="float", default=0.00,
                  help="Error on electron fake rate")

parser.add_option("--mu_fake_err", type="float", default=0.3,
                  help="Error on muon fake rate")

parser.add_option("--high_mu_fake_err", type="float", default=0.00,
                  help="Error on high pt muon fake rate")

(options, args) = parser.parse_args()

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

# Import this after we parse the args
import rootpy.io as io
shapes = io.open(options.file, "READ")

wz_err = options.wz_err
zz_err = options.zz_err
lumi_err = options.lumi_err
tau_err = options.tau_err
mu_id_err = options.mu_err
pdf_err = options.pdf_err
chi2err = options.topo_cut_err

# Decide which shapes to use
mmt_shape = options.mmt_shape
emt_shape = options.emt_shape

# Add a fake normalization error
e_fake_error = options.e_fake_err
mu_fake_error = options.mu_fake_err
high_mu_fake_error = options.high_mu_fake_err

mass = options.mass

# Define which histograms are signal histograms
signal_datasets = ['signal', 'signalHWW']

#mmt_folder = "mmt_mumu_final_%s_%i" % (mmt_shape, mass)
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

#emt_folder = "emt_emu_final_%s_%i" % (emt_shape, mass)
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

output = open(options.out, 'w')
card = dc.DataCard('VHtautau fit', '4.6 fb-1', [mmt, emt], options.file)
card.write(output)

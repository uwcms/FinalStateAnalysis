'''

Make the data card for a given mass point

'''

import json
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

parser.add_option("--scale_file", type="string",
                  default="scale_systematics.json",
                  help="JSON file with scale sys information")

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

parser.add_option("--triboson_err", type="float", default=0.75,
                  help="Error on triboson cross section")

parser.add_option("--channels", type="choice", default="combined",
                  choices=["combined", "mmt", "emt"],
                  help="Which channels to use")

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

# Figure out what the scale systematics are
scale_systematics = {}
with open('scale_systematics.json') as scale_sys_file:
    scale_systematics = json.load(scale_sys_file)

# Define which histograms are signal histograms
signal_datasets = ['VH%i' % mass, 'VH%iWW' % mass]

#mmt_folder = "mmt_mumu_final_%s_%i" % (mmt_shape, mass)
mmt_folder = "mmt_mumu_final_%i_%s" % (mass, mmt_shape)
mmt = dc.DataCardChannel(mmt_folder, shapes)
for signal_dataset in signal_datasets:
    mmt.add_signal(signal_dataset)

mmt.add_background('fakes')
mmt.add_background('WZ')
mmt.add_background('ZZ')
mmt.add_background('tribosons')

mc_samples = ['WZ', 'ZZ', 'tribosons']
mc_samples = ['WZ', 'ZZ', ]

mmt.add_sys('lumi', 1 + lumi_err, signal_datasets + mc_samples)
mmt.add_sys('chi2Lt', 1 + chi2err, signal_datasets + mc_samples)
mmt.add_sys('wz_xsec', 1.0 + wz_err, ['WZ'])
mmt.add_sys('zz_xsec', 1.0 + zz_err, ['ZZ'])
mmt.add_sys('CMS_eff_t', 1+ tau_err, signal_datasets + mc_samples)
mmt.add_sys('CMS_eff_m', 1 + quad(mu_id_err, mu_id_err), signal_datasets + mc_samples)
mmt.add_sys('pdf_vh', 1 + pdf_err, signal_datasets)
if options.triboson_err > 0:
    mmt.add_sys('tribosons_xsec', 1.0 + options.triboson_err, ['tribosons'])

# Add the relevant scale systematics
for sample, sample_info in scale_systematics['mmt'].iteritems():
    # Check if this sample applies in this particular card
    if str(mass) in sample or sample=='WZ' or sample=='ZZ':
        if 'tau_up' in sample_info:
            avg_err = ((sample_info['tau_up'] - sample_info['tau_down'])/
                       (2*sample_info['nom']))
            mmt.add_sys('tau_scale', 1.0 + avg_err, [sample])
        if 'e_up' in sample_info:
            avg_err = ((sample_info['e_up'] - sample_info['e_down'])/
                       (2*sample_info['nom']))
            mmt.add_sys('e_scale', 1.0 + avg_err, [sample])


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
emt.add_background('WZ')
emt.add_background('ZZ')
emt.add_background('tribosons')

emt.add_sys('lumi', 1 + lumi_err, signal_datasets + mc_samples)
emt.add_sys('chi2Lt', 1 + chi2err, signal_datasets + mc_samples)
emt.add_sys('wz_xsec', 1.0 + wz_err, ['WZ'])
emt.add_sys('zz_xsec', 1.0 + zz_err, ['ZZ'])
emt.add_sys('CMS_eff_t', 1+ tau_err, signal_datasets + mc_samples)
emt.add_sys('CMS_eff_m', 1 + mu_id_err, signal_datasets + mc_samples)
emt.add_sys('CMS_eff_e', 1.02, signal_datasets + mc_samples)
emt.add_sys('pdf_vh', 1 + pdf_err, signal_datasets)
if e_fake_error > 0:
    emt.add_sys('e_fake_norm', 1 + e_fake_error, 'fakes')
if mu_fake_error > 0:
    emt.add_sys('mu_fake_norm', 1 + mu_fake_error, 'fakes')
if options.triboson_err > 0:
    emt.add_sys('tribosons_xsec', 1.0 + options.triboson_err, ['tribosons'])

for sample, sample_info in scale_systematics['emt'].iteritems():
    # Check if this sample applies in this particular card
    if str(mass) in sample or sample=='WZ' or sample=='ZZ':
        if 'tau_up' in sample_info:
            avg_err = ((sample_info['tau_up'] - sample_info['tau_down'])/
                       (2*sample_info['nom']))
            emt.add_sys('tau_scale', 1.0 + avg_err, [sample])
        if 'e_up' in sample_info:
            avg_err = ((sample_info['e_up'] - sample_info['e_down'])/
                       (2*sample_info['nom']))
            emt.add_sys('e_scale', 1.0 + avg_err, [sample])

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
channel_map = {
    'combined' : [mmt, emt],
    'emt' : [emt],
    'mmt' : [mmt],
}

card = dc.DataCard('VHtautau fit', '4.6 fb-1',
                   channel_map[options.channels], options.file)
card.write(output)

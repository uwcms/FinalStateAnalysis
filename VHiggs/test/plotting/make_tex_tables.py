#!/usr/bin/env python

'''

Make LaTeX tables with the final results.


'''


from optparse import OptionParser
import rootpy.io as io
import math
import sys

parser = OptionParser(usage="usage: %prog [options]")

parser.add_option("-f", "--file", dest="file", default="wh_shapes.root",
                  type="string", help="Shape file")

parser.add_option("-m", "--mass", dest="mass", default='120',
                  type="string", help="Higgs mass - can optionally append SM4 or FF")

parser.add_option("--wz_err", type="float", default=0.166,
                  help="WZ normalization error")

parser.add_option("--zz_err", type="float", default=0.40,
                  help="WZ normalization error")

parser.add_option("--triboson_err", type="float", default=1.00,
                  help="Error on triboson cross section")

parser.add_option("--mu_fake_err", type="float", default=0.3,
                  help="Error on muon fake rate")

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

if __name__ == "__main__":
    (options, args) = parser.parse_args()

    file = io.open(options.file, 'read')

    emt_folder = file.Get('emt_emu_final_count')
    mmt_folder = file.Get('mmt_mumu_final_count')

    results = {}

    mass = options.mass

    results['mass'] = mass
    results['emt_data'] = emt_folder.Get("data_obs").Integral()
    results['emt_wz'] = emt_folder.Get("WZ").Integral()
    results['emt_zz'] = emt_folder.Get("ZZ").Integral()
    results['emt_triboson'] = emt_folder.Get("tribosons").Integral()
    results['emt_fakes'] = emt_folder.Get("fakes").Integral()
    results['emt_fakes_err'] = emt_folder.Get("fakes").GetBinError(1)
    results['emt_vhtt'] = emt_folder.Get("VH%s" % mass).Integral()
    results['emt_vhww'] = emt_folder.Get("VH%sWW" % mass).Integral()

    results['mmt_data'] = mmt_folder.Get("data_obs").Integral()
    results['mmt_wz'] = mmt_folder.Get("WZ").Integral()
    results['mmt_zz'] = mmt_folder.Get("ZZ").Integral()
    results['mmt_triboson'] = mmt_folder.Get("tribosons").Integral()
    results['mmt_fakes'] = mmt_folder.Get("fakes").Integral()
    results['mmt_fakes_err'] = mmt_folder.Get("fakes").GetBinError(1)
    results['mmt_vhtt'] = mmt_folder.Get("VH%s" % mass).Integral()
    results['mmt_vhww'] = mmt_folder.Get("VH%sWW" % mass).Integral()

    for tag in ['emt', 'mmt']:
        results['%s_wz_err' % tag] = results['%s_wz' % tag]*options.wz_err
        results['%s_zz_err' % tag] = results['%s_zz' % tag]*options.zz_err
        results['%s_triboson_err' % tag] = results['%s_triboson' % tag]*options.triboson_err
        # Add additional norm uncertainty to fakes
        results['%s_fakes_err' % tag] = quad(
            results['%s_fakes_err' % tag],
            options.mu_fake_err*results['%s_fakes' % tag]
        )

        results['%s_bkg' % tag] = \
                results['%s_wz' % tag] \
                + results['%s_zz' % tag] \
                + results['%s_fakes' % tag] \
                + results['%s_triboson' % tag]

        results['%s_bkg_err' % tag] = quad(
                results['%s_wz_err' % tag],
                results['%s_zz_err' % tag],
                results['%s_fakes_err' % tag],
                results['%s_triboson_err' % tag]
        )

        results['%s_vh' % tag] = results['%s_vhtt' % tag] + results['%s_vhww' % tag]

    template =  '''
Channel  & \\mmt & \\emt \\\\
\hline
Fakes & ${mmt_fakes:0.2f} \\pm {mmt_fakes_err:0.2f}$ &  ${emt_fakes:0.2f} \\pm {emt_fakes_err:0.2f}$  \\\\
WZ & ${mmt_wz:0.2f} \\pm {mmt_wz_err:0.2f}$ &  ${emt_wz:0.2f} \\pm {emt_wz_err:0.2f}$  \\\\
ZZ & ${mmt_zz:0.2f} \\pm {mmt_zz_err:0.2f}$ &  ${emt_zz:0.2f} \\pm {emt_zz_err:0.2f}$  \\\\
Triboson & ${mmt_triboson:0.2f} \\pm {mmt_triboson_err:0.2f}$ &  ${emt_triboson:0.2f} \\pm {emt_triboson_err:0.2f}$  \\\\
\hline
Backgrounds & ${mmt_bkg:0.2f} \\pm {mmt_bkg_err:0.2f}$ & ${emt_bkg:0.2f} \\pm {emt_bkg_err:0.2f}$ \\\\
\hline
Observed & {mmt_data:0.0f} & {emt_data:0.0f} \\\\
\hline
VH({mass}) & {mmt_vh:0.2f} & {emt_vh:0.2f} \\\\
'''

    print template.format(**results)

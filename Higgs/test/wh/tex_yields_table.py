#!/usr/bin/env python

'''

Generate a tex table of the VHlep results.

Takes as inputs two JSON files with the yields for 7 and 8 TeV

'''

from RecoLuminosity.LumiDB import argparse
import json
import os
import sys
import uncertainties

header_template = r'''
\begin{tabular}{lccc|ccc}
Channel & Observed & VH $(120\GeV)$ & All bkg. & WZ & ZZ & Fakes \\
\hline
'''

def get_sample_yield_and_err(mapping, channel, sample):
    result = tuple(mapping[os.path.join(channel, sample)])
    return result

def render_entry(x):
    return '$%0.2f \pm %0.2f$' % (x.nominal_value, x.std_dev())


def get_row(channel_nicename, mapping, channel):
    fields = [channel_nicename]
    # Add data
    fields.append('%i' % int(round(get_sample_yield_and_err(mapping, channel, 'data_obs')[0])))
    fields.append('$%0.2f \pm %0.2f$' % get_sample_yield_and_err(mapping, channel, 'VH120'))

    wz = uncertainties.ufloat(get_sample_yield_and_err(mapping, channel, 'wz'))
    zz = uncertainties.ufloat(get_sample_yield_and_err(mapping, channel, 'zz'))
    fakes = uncertainties.ufloat(get_sample_yield_and_err(mapping, channel, 'fakes'))
    all_bkg = wz + zz + fakes

    results = {
        'data_obs': uncertainties.ufloat(get_sample_yield_and_err(mapping, channel, 'data_obs')),
        'VH120' : uncertainties.ufloat(get_sample_yield_and_err(mapping, channel, 'VH120')),
        'wz' : wz,
        'zz' : zz,
        'fakes' : zz,
        'all_bkg' : all_bkg,
    }

    for col in [all_bkg, wz, zz, fakes]:
        fields.append(render_entry(col))

    return results, ' & '.join(fields) + r' \\' + '\n'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('yields7TeV', help='7 TeV JSON yields')
    parser.add_argument('yields8TeV', help='8 TeV JSON yields')

    args = parser.parse_args()

    file7TeV = open(args.yields7TeV)
    json7TeV = json.load(file7TeV)

    file8TeV = open(args.yields8TeV)
    json8TeV = json.load(file8TeV)

    sys.stdout.write(header_template)

    totals = {}

    for mapping, label in [(json7TeV, '7\TeV '), (json8TeV, '8\TeV ')]:
        for channel, nicename in [
            ('eet', r'$ee\tau_h$'),
            ('emt', r'$e\mu\tau_h$'),
            ('mmt', r'$\mu\mu\tau_h$')]:
            subtotals, row = get_row(label + nicename, mapping, channel)
            sys.stdout.write(row)
            for sample, sample_yield in subtotals.iteritems():
                if sample not in totals:
                    totals[sample] = sample_yield
                else:
                    totals[sample] += sample_yield

    sys.stdout.write(r'\hline' + '\n')
    total_row = ['Total']
    total_row.append('%i' % int(round(totals['data_obs'].nominal_value)))
    for key in ['VH120', 'all_bkg', 'wz', 'zz', 'fakes']:
        total_row.append(render_entry(totals[key]))
    sys.stdout.write(' & '.join(total_row))
    sys.stdout.write(r' \\' + '\n')
    sys.stdout.write(r'\end{tabular}' + '\n')

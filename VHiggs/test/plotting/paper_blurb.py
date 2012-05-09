#!/usr/bin/env python

'''

Figure out what the blurb should be from the plot filename

'''

import sys

if __name__ == "__main__":
    output_pdf_file = sys.argv[1]
    blurbs = {
        'whtt' : 'e#mu#tau and #mu#mu#tau (W#tau#tau)',
        'whww' : 'Three light leptons (WWW)',
        'zh' : 'Four leptons (ZH)',
        'whgg' : 'V#gamma#gamma',
        'whbb' : 'Vbb',
        'leptons' : 'ZH + WWW + W#tau#tau',
        'with_gg' : 'ZH + WWW + W#tau#tau + #gamma #gamma',
        'with_all' : 'ZH + WWW + W#tau#tau + #gamma #gamma + bb',
    }

    for k, v in blurbs.items():
        if k in output_pdf_file:
            sys.stdout.write(v + '\n')

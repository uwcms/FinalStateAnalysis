#!/usr/bin/env python

'''

A stupid file to decide where the legend goes for each channel
in the final limit plots.

'''

import sys

if __name__ == "__main__":
    output_pdf_file = sys.argv[1]
    sys.stderr.write("Legend Pos: %s\n" % output_pdf_file)
    output = "ERROR"
    if 'mmt' in output_pdf_file or 'emt' in output_pdf_file:
        output = "0.75,0.15,0.95,0.35" + "\n"
    else:
        output = "0.50,0.60,0.75,0.90" + "\n"
    sys.stderr.write("Legend Pos result: %s\n" % output)
    sys.stdout.write(output)

#!/usr/bin/env python

'''

A stupid file to spit out the blurb text for each channel
in the final limit plots.

'''

import sys

if __name__ == "__main__":
    output_pdf_file = sys.argv[1]
    sys.stderr.write("Blurb text: %s\n" % output_pdf_file)
    output = "ERROR"
    if 'mmt' in output_pdf_file:
        output = "#mu #mu #tau channel"
    elif 'emt' in output_pdf_file:
        output = "e #mu #tau channel"
    elif 'combined' in output_pdf_file:
        #output = "Combined limit"
        output = ""

    sys.stderr.write("Blurb text result: %s\n" % output)
    sys.stdout.write(output)

#!/usr/bin/env python

'''

./addStatShapes.py [file]

This utility looks at all histograms in all folders of the given root file.

It adds a [histo]_bin_i(Up/Down) extra shape templates in each directory
corresponding to the statistical error of the unweighted fake rate histogram.

'''

import os
import sys
import re
import logging
import math
import ROOT
log = logging.getLogger("statshapes")
logging.basicConfig(level=logging.INFO)

from rootpy.io import open, DoesNotExist

fake_finder = re.compile('fakes')

def update_file(f):
    path_regex = re.compile(
      '(?P<channel>[^_]+)_(?P<charge>[^_]+)_final_(?P<mass>\d+)_(?P<var>[^_]+)')

    for thing in f.walk(class_pattern='TH1*'):
        path, subdirs, histos = thing
        log.info("==> examining directory %s", path)
        if not histos:
          continue

        path_match = path_regex.match(path)
        if not path_match:
            log.info("==> skipping!")
            continue

        # Get a unique label for this channel to use for the fake rate bin
        # systematics.
        type = '%s_%s' % (
            path_match.group('channel'), path_match.group('charge'))

        directory = f.get(path)
        directory.cd()

        for histo in histos:
            match = fake_finder.match(histo)
            if match:
                log.info("Found fake histogram: %s", histo)

                final_h = f.get(os.path.join(path, histo))

                systematics = []

                min_threshold = 0.02

                for i, bin in enumerate(final_h):
                    # Skip empty bins
                    if bin == 0:
                        continue
                    bin_error = final_h.getBinError(i+1)/bin
                    if bin_error < min_threshold:
                        continue

                    shift_up = final_h.Clone(final_h.getName() + "_%s_bin_%iUp" % (type, i))
                    shift_down = final_h.Clone(final_h.getName() + "_%s_bin_%iDown" % (type, i))

                    shift_up[i] = shift_up[i]*(1 + bin_error)
                    shift_down[i] = shift_down[i]*(1 - bin_error)

                    shift_up.Write(shift_up.GetName(), ROOT.TObject.kOverwrite)
                    shift_down.Write(shift_down.GetName(), ROOT.TObject.kOverwrite)

if __name__ == "__main__":
    filename = sys.argv[1]
    log.info("Updating file: %s", filename)
    f = open(filename, 'update')
    update_file(f)

#!/usr/bin/env python

'''

Embed a TText label in a ROOT file.

Author: Evan K. Friis, UW Madison

Usage:
    embed_label.py doot.root a=b c=d

In doot.root there is a TText with name "a", title "b",
and a TText with name "c" title "d".



'''

from RecoLuminosity.LumiDB import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("rootfile", help="ROOT file to embed label in")
    parser.add_argument("labels", metavar='label', nargs="+",
                        help="Label(s) to embed.  Format: key=value")

    args = parser.parse_args()

    for label in args.labels:
        if '=' not in label:
            print "Can't parse %s, you need to specify labels as key=val pars" \
                    % label
            sys.exit(1)

    # Don't import this until we know we need it
    from rootpy import io
    from ROOT import TText

    file = io.open(args.rootfile, 'UPDATE')
    file.cd()

    keep = []
    for label in args.labels:
        key, val = tuple(label.split('='))
        the_label = TText(0, 0, val)
        the_label.SetName(key)
        the_label.Write()
        keep.append(the_label)
    file.Write()

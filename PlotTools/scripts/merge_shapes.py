#! /bin/env python

import ROOT
from optparse import OptionParser
import sys
import os
import logging
from pdb import set_trace

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

def parse_cgs(cgs_filename):
    ret = {}
    groups = {}
    with open(cgs_filename) as infile:
        for line in infile.readlines():
            #skip comments and empty lines
            try:
                if not line.strip() or line.strip().startswith('#'): 
                    continue
                if line.startswith('$ GROUP'):
                    objects = [i.strip() for i in line.split()]
                    groupname = objects[2]
                    #gets rid of spurious whitespaces and then split by coma
                    groupobjs = (''.join(objects[3:])).split(',')
                    groups[groupname] = groupobjs
                else: #not a group
                    keyword, value = tuple( i.strip() for i in line.split(':') )
                    values = [i.strip() for i in value.split(',')]
                    sub_values = []
                    for val in values:
                        newval = [val] if val not in groups else groups[val]
                        sub_values.extend(newval)
                    ret[keyword] = sub_values
            except:
                raise ValueError('cannot parse line: %s \nIn file %s' % (line, cgs_filename))
    return ret

def normalize(hist):
    for i in range(0, hist.GetNbinsX()+2): #scale underflow/overflow too                                                                                                                              
        content = hist.GetBinContent(i)
        error   = hist.GetBinError(i)
        width   = hist.GetBinWidth(i)
        hist.SetBinContent(i, content / width)
        hist.SetBinError(i, error / width)
        
    return hist


if __name__ == '__main__':
    usage = "usage: %prog [options] rootfiles cgsfiles"
    parser = OptionParser(usage=usage) #'Merges shape files plots',
    parser.add_option("-o", "--output-file", dest="ofile_name",
                      help="output file name", default='merge.root')
    parser.add_option("-m", "--mass", dest="mass",
                      help="signal mass point", default='125')
    parser.add_option("-q", "--quiet",
                  action="store_true", dest="quiet", default=False,
                  help="less printout")
    parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="more printout")

    (args, options) = parser.parse_args()

    #if args.quiet:
    #    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    #if args.verbose:
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)

    root_names = [i for i in options if '.root' in i]
    cgs_files  = [i for i in options if 'cgs' in   i]
    mass_point = args.mass # '125'

    parsed_cgs = []
    for i in cgs_files:
        logging.info('parsing %s' % i)
        parsed_cgs.append( parse_cgs(i) )
    
    h_signal = None
    h_data   = None
    h_bkg    = None

    root_files = []
    for i in root_names:
        logging.info('opening %s' % i)
        root_files.append( ROOT.TFile.Open(i) )

    ofile      = ROOT.TFile(args.ofile_name, 'recreate')

    for cgs in parsed_cgs:
        for category in cgs['categories']:
            #fill background
            for bkg in cgs['backgrounds']:
                path = os.path.join(category, bkg)
                for tfile in root_files:
                    tmp_h = tfile.Get(path)
                    logging.info( 'getting %s' % path )
                    if tmp_h:
                        if not h_bkg:
                            h_bkg = tmp_h.Clone('Ztt')
                            #h_bkg.SetTitle('Ztt')
                        else:
                            h_bkg.Add(tmp_h)
                    else:
                        logging.warning( 'skipping %s' % path )

            #fill signal
            for sig in cgs['signals']:
                path = os.path.join(category, sig)+mass_point
                for tfile in root_files:
                    tmp_h = tfile.Get(path)
                    logging.info( 'getting %s' % path )
                    if tmp_h:
                        if not h_signal:
                            h_signal = tmp_h.Clone('ggH')
                            #h_signal.SetTitle('ggH')
                        else:
                            h_signal.Add(tmp_h)
                    else:
                        logging.warning( 'skipping %s' % path )

            for dat in cgs['data']:
                path = os.path.join(category, dat) 
                for tfile in root_files:
                    tmp_h = tfile.Get(path)
                    logging.info( 'getting %s' % path )
                    if tmp_h:
                        if not h_data:
                            h_data = tmp_h.Clone('data_obs')
                        else:
                            h_data.Add(tmp_h)
                    else:
                        logging.warning( 'skipping %s' % path )

    #signal is signal + bkg
    h_signal.Add(h_bkg)

    h_signal = normalize(h_signal)
    h_data   = normalize(h_data  )
    h_bkg    = normalize(h_bkg   )

    error = h_bkg.Clone('errorBand')
    
    #Writing
    ofile.cd()
    h_signal.Write()
    h_data.Write()
    h_bkg.Write()
    error.Write()
    ofile.Close()
    
    for i in root_files:
        i.Close()

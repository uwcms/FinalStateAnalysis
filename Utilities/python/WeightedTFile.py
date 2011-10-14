import ROOT
import os
import logging

'''

Wrapper about a ROOT TFile which scales histograms that are requested

Author: Evan K. Friis

'''

class WeightedTFile(object):
    ''' Wrapper around a TFile which automatically scales histograms
    '''
    @staticmethod
    def comp_weight(target_lumi, xsec, event_count, skim_eff=1.0):
        ''' Compute a sample weight given the desired luminosity and xsec

        Example: 2 nanobarn process, w/ 1 pb^-1 of data. In the final file
        we have 350 events.

        >>> WeightedTFile.comp_weight(1.0, 2000, 350, 1.0) == 2000/350
        >>> True
        '''
        target_event_count =  target_lumi*xsec*skim_eff
        return target_event_count/event_count

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger("WeightedTFile")
        # Build a regular TFile
        if isinstance(args[0], basestring):
            self.log.info("Loading file from path %s", args[0])
            self.filename = args[0]
            if not os.path.exists(self.filename):
                raise IOError(
                    "<WeightedTFile> Cannot open: %s" % self.filename)
            self.file = ROOT.TFile(args)
        else:
            self.log.info("Loading existing file %s", args[0])
            # Use an existing file--like object
            assert(len(args) == 1)
            self.file = args[0]


        self.weight = 1.0
        self.weighted_copies = {}
        self.verbose = kwargs.get('verbose', False)

        # Check if we want to do any weighting at all
        if 'weight' in kwargs:
            self.weight = kwargs['weight']
        elif 'target_lumi' in kwargs:
            self.target_lumi = kwargs['target_lumi']
            self.log.info("Normalizing to int. lumi: %s", self.target_lumi)
            self.xsec = kwargs['xsec']
            self.log.info("Using xsec: %s", self.xsec)
            # Can either specify event count explicitly or take it from
            # the integral of a histogram
            self.event_count = kwargs['event_count']
            if isinstance(self.event_count, str):
                count_histo = self.file.Get(self.event_count)
                if not count_histo:
                    raise IOError("<WeightedTFile> Could not load event count "
                                  "histo %s from file %s" % (self.event_count,
                                                             self.file))
                assert(count_histo)
                self.event_count = count_histo.Integral()
                self.log.info("Got event cout %i", self.event_count)

            # Can get the skim efficiency explicitly for from the ratio of two
            # histograms.
            self.skim_eff = 1.0
            if 'skim_eff' in kwargs:
                skim_eff_arg = kwargs['skim_eff']
                if isinstance(skim_eff_arg, tuple):
                    num_histo = self.file.Get(skim_eff_arg[0])
                    den_histo = self.file.Get(skim_eff_arg[1])
                    assert(num_histo)
                    assert(den_histo)
                    self.skim_eff = num_histo.Integral()/den_histo.Integral()
                else:
                    self.skim_eff = skim_eff_arg
            self.weight = self.comp_weight(
                self.target_lumi, self.xsec, self.event_count, self.skim_eff)

        self.log.info("Computed weight: %f" % self.weight)
        #if self.verbose:
            #print self

    def get_unweighted(self, path):
        return self.file.Get(path)

    def get_weighted(self, path):
        if path in self.weighted_copies:
            return self.weighted_copies[path]
        else:
            unweighted = self.get_unweighted(path)
            if not unweighted:
                raise ReferenceError("Could not get histogram %s from file %s" %
                                     (path, self.file))
            object = unweighted.Clone()
            object.Scale(self.weight)
            self.weighted_copies[path] = object
            return object

    def Get(self, path):
        # Override default behavior
        return self.get_weighted(path)

    def __repr__(self):
        return "<WeightedTFile(%s, w=%f)>" % (self.file, self.weight)

'''

Base class with convenience functions for TMega python selectors.

'''

import os
import multiprocessing
import ROOT

class MegaBase(object):
    log = multiprocessing.get_logger()
    def __init__(self, tree, output, **kwargs):
        self.tree = tree
        self.output = output
        self.opts = kwargs
        self.histograms = {}

    def book(self, location, name, *args, **kwargs):
        ''' Book an object at location

        The object is built using::

            the_type(name, *args)

        The type can be specified using the 'type' kwarg.  The default is
        ROOT.TH1F

        '''
        self.log.info("booking %s at %s", name, location)

        directory = self.output.Get(location)
        if not directory:
            directory = self.output.mkdir(location)
        directory.cd()
        the_type = kwargs.get('type', ROOT.TH1F)
        object = the_type(name, *args)
        directory.Append(object)
        self.histograms[os.path.join(location, name)] = object
        return object

    def enable_branch(self, branch):
        ''' Set the branch to read on TTree::GetEntry '''
        self.tree.SetBranchStatus(branch, 1)

    def disable_branch(self, branch):
        ''' Set the branch to NOT be read on TTree::GetEntry '''
        self.tree.SetBranchStatus(branch, 0)

    def write_histos(self):
        ''' Write all histograms to the file. '''
        self.output.Write()
        #for histo in self.histograms.values():
            #histo.Write()

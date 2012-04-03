'''

Base class with convenience functions for TMega python selectors.

'''

import json
import os
import multiprocessing
import ROOT

def make_dirs(base_dir, subdirs):
    ''' Make the directory structure.  Subdirs is a list. '''
    if not subdirs:
        return base_dir
    next_folder = subdirs.pop(0)
    if base_dir.Get(next_folder):
        return make_dirs(base_dir.Get(next_folder), subdirs)
    else:
        new_dir = base_dir.mkdir(next_folder)
        return make_dirs(new_dir, subdirs)

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
        self.log.debug("booking %s at %s", name, location)

        directory = make_dirs(self.output, os.path.normpath(location).split('/'))

        if not directory:
            raise IOError("Couldn't create directory %s in file %s" %
                          (location, self.output))

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

    def save_json(self, name, pyobject):
        ''' Serialize pyobject into a TObjString in the output file using JSON '''
        json_str = json.dumps(pyobject)
        text = ROOT.TObjString(json_str)
        self.output.WriteTObject(text, name)

    def write_histos(self):
        ''' Write all histograms to the file. '''
        self.output.Write()

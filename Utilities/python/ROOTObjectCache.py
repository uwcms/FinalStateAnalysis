import ROOT
import os
import logging


class ROOTObjectCache(object):
    open_files = {}
    def __init__(self, file, reset = False):
        # Instrument for testing
        self.log = logging.getLogger("ROOTObjectCache")
        self.get_counter = 0
        self.put_counter = 0
        self.keep = []
        if isinstance(file, basestring):
            if file in self.open_files:
                self.cache_file = self.open_files[file]
            elif not reset and os.path.exists(file):
                self.log.info("Using existing cache file at path: %s", file)
                self.cache_file = ROOT.TFile(file, "UPDATE")
            else:
                self.log.info("Creating new cache file at path: %s", file)
                self.cache_file = ROOT.TFile(file, "RECREATE")
            self.open_files[file] = self.cache_file
        else:
            self.cache_file = file

    def write(self):
        self.log.info("...writing %s", self.cache_file.GetFile().GetPath())
        self.cache_file.Write()

    def get(self, key):
        self.get_counter += 1
        self.log.debug("ObjectCache: getting %s", key)
        #self.cache_file.ReadAll()
        object = self.cache_file.Get(key + ";1")
        #object.GetDirectory()
        return object

    def put(self, key, object):
        self.log.debug("PUT")
        self.put_counter += 1
        self.log.debug("ObjectCache: (1) # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        # Save state
        working_dir = ROOT.gDirectory
        self.log.debug("ObjectCache: (2) # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        self.cache_file.cd()
        self.log.debug("ObjectCache: (3) # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        object.SetName(key)
        clone = object.Clone()
        clone.Write()
        self.log.debug("ObjectCache: (4) # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        result = self.cache_file.Get(key)
        #result.SetDirectory(ROOT.gDirectory)
        self.log.debug("ObjectCache: (5) # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        assert(result)
        # Restore state
        working_dir.cd()
        self.log.debug("ObjectCache: (8) # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        assert(result)
        # IS THIS OK
        self.keep.append(result)
        return result
        #return result.Clone()

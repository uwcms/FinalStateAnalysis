import ROOT

import glob
import os
import hashlib
import tempfile
import logging

import FinalStateAnalysis.Utilities.ROOTObjectCache as ROOTObjectCache
import FinalStateAnalysis.Utilities.CachingTTree as CachingTTree

'''

Wrapper around a set of TFiles which lazily merges all of the objects.

The merging is cached in a ROOTObjectCache so the expensive summing should only
be done once.

'''

class TFileCollection(ROOTObjectCache.ROOTObjectCache):
    @staticmethod
    def file_key(files):
        # Compute a unique key for a list of files
        m = hashlib.md5()
        for file in sorted(os.path.abspath(file) for file in files):
            m.update(file)
            mtime = os.path.getmtime(file)
            m.update("%s" % int(mtime))
        return m.hexdigest()

    @staticmethod
    def histo_key(histo_path):
        m = hashlib.md5()
        m.update(histo_path)
        return m.hexdigest()

    def __init__(self, *globs, **kwargs):
        self.files = []
        for aglob in globs:
            for file in glob.glob(aglob):
                self.files.append(file)
        if not self.files:
            raise IOError("No input files found in %s" % globs)
        self.key = self.file_key(self.files)
        reset = False
        if 'reset' in kwargs:
            reset = kwargs['reset']
        # Initialize the local cache file
        cache_filepath = os.path.join(tempfile.gettempdir(), self.key + ".root")
        super(TFileCollection, self).__init__(cache_filepath, reset = reset)
        # Get a proto file so we can deduce the structure
        self.proto_file = ROOT.TFile.Open(self.files[0], "READ")
        self.log = logging.getLogger("TFileCollection")
        self.cache_log = logging.getLogger('ROOTCache')
        common_prefix = os.path.commonprefix(self.files)
        self.log.info("Created a TFileCollection wrapping %i files from %s",
                      len(self.files), common_prefix)


    def __repr__(self):
        return "TFileCollection(%s)[%i]" % (self.key[0:5], len(self.files))

    def get_histo(self, path):
        self.log.info(self.__repr__() + "::get(%s)", path)
        key = self.histo_key(path)
        cached = self.get(key)
        if cached:
            self.log.info("--> is cached!")
            return cached
        self.log.info("computing...")
        # Otherwise add the histos and cache them
        output = None
        self.cache_log.info(
            "%s::Merging histogram %s...", self.__repr__(), path)
        current_dir = ROOT.gDirectory
        for file in self.files:
            tfile = ROOT.TFile.Open(file, "READ")
            if output is None:
                output = tfile.Get(path).Clone()
                output.SetDirectory(0) # Memory resident
            else:
                output.Add(tfile.Get(path))
            tfile.Close()
        current_dir.cd()
        self.cache_log.info(
            "%s::Finished merging histogram %s.", self.__repr__(), path)
        return self.put(key, output)

    def get_tree(self, path):
        #self.log.debug("TFileCollection: (1) # of open files %i",
                       #ROOT.gROOT.GetListOfFiles().GetEntries())
        #self.log.debug("TFileCollection: open files: %s",
                       #", ".join(str(file) for file in ROOT.gROOT.GetListOfFiles()))
        # Try and get the TChain
        chain_key = self.histo_key(path)
        cached_chain = self.get(chain_key)
        #self.log.debug("TFileCollection: (1a) # of open files %i",
                       #ROOT.gROOT.GetListOfFiles().GetEntries())
        #self.log.debug("TFileCollection: open files: %s",
                       #", ".join(str(file) for file in ROOT.gROOT.GetListOfFiles()))
        #self.log.debug("GetTree: cached_chain is %s", str(cached_chain))
        #self.log.debug("TFileCollection: (1aa) # of open files %i",
                       #ROOT.gROOT.GetListOfFiles().GetEntries())
        if not cached_chain:
            chain = ROOT.TChain(path)
            for file in self.files:
                chain.AddFile(file)
            # ? chain.CanDeleteRefs(True)
            cached_chain = self.put(chain_key, chain)
        #self.log.debug("TFileCollection: (1b) # of open files %i",
                       #ROOT.gROOT.GetListOfFiles().GetEntries())
        assert(cached_chain)
        #self.log.debug("TFileCollection: (2) # of open files %i",
                       #ROOT.gROOT.GetListOfFiles().GetEntries())
        # WARNING - if this command is executed, the thing won't work? why
        #self.log.debug("GetTree: cached_chain dir is %s", str(cached_chain))
        #self.log.debug("TFileCollection: (3) # of open files %i",
                       #ROOT.gROOT.GetListOfFiles().GetEntries())
        #self.log.debug(str(cached_chain.GetDirectory()))
        # Now we got the chain, build the caching ttree using the same
        # cache file as the TFileCollection
        base_path = os.path.dirname(path)
        return CachingTTree.CachingTTree(cached_chain, base_path, self.cache_file)

    def Get(self, path):
        proto_obj = self.proto_file.Get(path)
        if isinstance(proto_obj, ROOT.TTree):
            return self.get_tree(path)
        elif isinstance(proto_obj, ROOT.TH1):
            return self.get_histo(path)

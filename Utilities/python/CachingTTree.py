import ROOT
import hashlib
import logging
import FinalStateAnalysis.Utilities.ROOTObjectCache as ROOTObjectCache

'''

TTree wrapper which caches "Draw" results in a persistent TFile.

All normal TTree functions are passed transparently to the owned tree.

The function

    draw(self, variable, selection, binning=None)

returns a TH1F of the given variable, suing the selection and binning.

Author: Evan K. Friis, UW Madison

'''

class CachingTTree(ROOTObjectCache.ROOTObjectCache):
    @staticmethod
    def get_key(path, variable, selection, binning):
        ''' Get a unique key for a TTree '''
        m = hashlib.md5()
        m.update(path)
        m.update(variable)
        m.update(selection)
        if binning:
            for bin in binning:
                m.update(str(bin))
        return path.replace('/', '') + m.hexdigest()

    def __init__(self, tree, path, cache_file):
        self.log = logging.getLogger(__name__)
        self.cache_log = logging.getLogger('ROOTCache')
        self.cache = cache_file
        self.log.info("CachingTTree(%s) in cache file: %s", tree.GetName(),
                      cache_file)
        super(CachingTTree, self).__init__(cache_file)
        self.tree = tree
        assert(isinstance(self.tree, ROOT.TTree))
        #assert(tree.GetDirectory())
        #self.log.info("CachingTTree(%s) has directory %s", tree.GetName(),
                      #tree.GetDirectory())
        #self.path = tree.GetDirectory().GetPath().split(':')[-1]
        self.path = path

    def key(self, variable, selection, binning=None):
        return self.get_key(self.path, variable, selection, binning)

    def draw(self, variable, selection, binning=None):
        key = self.key(variable, selection, binning)
        self.log.debug("CachingTTree::draw # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        # Try and get object from the cache
        cached = self.get(key)
        if cached:
            return cached
        self.cache_log.info(
            "Drawing %s::(%s) from %i files",
            variable, selection, self.tree.GetListOfFiles().GetEntries())
        # TODO FIXME somewhere in here a new file is opened
        # Otherwise do the computation and store the result
        destination_str = key # store in histogram w/ same name as key
        if binning:
            destination_str += "(%s)" % ", ".join(str(x) for x in binning)
        var_string = "%s>>%s" % (variable, destination_str)
        self.log.info("Drawing %s : %s into key %s", variable, selection, key)
        self.log.debug("CachingTTree::preDraw # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        self.tree.Draw(var_string, selection, "goff")
        self.log.debug("CachingTTree::postDraw # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        result = ROOT.gDirectory.Get(key)
        self.log.debug("CachingTTree::postDrawGet # of open files %i",
                       ROOT.gROOT.GetListOfFiles().GetEntries())
        self.cache_log.info("Done drawing")
        #return self.put(key, result)
        self.put(key, result)
        output = self.get(key)
        #ROOT.SetOwnership(output, False)
        output.SetDirectory(0) # Set as memory resident
        return output

    def __getattr__(self, attr):
        return getattr(self.tree, attr)

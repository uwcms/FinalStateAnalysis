import ROOT
import fnmatch
import logging
import hashlib

import samplestyles
import styling
import Histo


'''

Wrapper which takes a set of files containing histograms and makes nice stacks.

'''

class AnalysisSample(object):
    log = logging.getLogger("AnalysisPlotter")
    def __init__(self, file, name, **kwargs):
        self.file = file
        self.name = name
        self.log.info("AnalysisSample(%s)", name)
        self.style_dict = {}
        # Take defaults, if they are defined
        for style_name, style_def in samplestyles.SAMPLE_STYLES.iteritems():
            if fnmatch.fnmatch(name, style_name):
                self.log.info(
                    "AnalysisSample(%s) using style: %s", name, style_name)
                self.style_dict.update(style_def)
                break

        if not self.style_dict:
            self.log.warning("AnalysisSample(%s) - no default style found!",
                             name)
        # Now take any extra parameters from the kwargs
        self.style_dict.update(kwargs)
        self.owned = {}
        self.computed_hists = {}

    def get(self, path, **kwargs):
        self.check_hists('gethisto')
        owned_key = (path, tuple(kwargs.keys()))
        if owned_key not in self.owned:
            self.log.debug("AnalysisSample(%s) retrieving %s", self.name, path)
            th1 = None
            #self.log.debug("AnalysisSample(%s) computed: %s",
                           #self.name, self.computed_hists.keys())
            if path in self.computed_hists:
                self.check_hists('gothisto')
                th1 = self.computed_hists[path]
                self.log.debug("AnalysisSample(%s) got: %s = %s",
                               self.name, path, th1)
                self.check_hists('afterget')
            else:
                th1 = self.file.Get(path)
            if not th1:
                raise ValueError(
                    "AnalysisSample::%s Could not get object %s from file %s" %
                    (self.name, path, self.file))
            self.owned[owned_key] = Histo.Histo(th1, **kwargs)
        object = self.owned[owned_key]
        # Update style
        styling.apply_style(object, **self.style_dict)
        return object

    def norm(self, path):
        object = self.get(path)
        return object.Integral()

    def title(self, path):
        object = self.get(path)
        return object.GetTitle()

    def add_to_stack(self, path, stack, drawopt=None, **kwargs):
        object = self.get(path, **kwargs)
        if drawopt is None:
            drawopt = self.style_dict.get('draw_opt', '')
        stack.Add(object.th1, drawopt)

    def add_to_legend(self, path, legend, drawopt=None):
        object = self.get(path)
        if drawopt is None:
            drawopt = self.style_dict.get('draw_opt', 'lf')
        nicename = self.style_dict.get('nicename', self.name)
        legend.AddEntry(object.th1, nicename, drawopt)

    def register_tree(self, name, tree, var, selection, w=None, binning=None):
        #print self.name
        #print self.file
        key = ":".join([tree, name])
        if key in self.computed_hists:
            raise ValueError("The histogram with key %s has"
                             " already been registered!" % key)

        ttree = self.file.get_unweighted(tree)
        name = key.replace(':', '')
        self.check_hists('begin')

        weight = 1.0
        if hasattr(self.file, 'weight'):
            weight = self.file.weight
        if not selection:
            selection = "%f" % weight
        else:
            selection = "(%s)*%f" % (selection, weight)
        if w:
            selection = "(%s)*(%s)" % (selection, w)

        histo = ttree.draw(var, selection, binning)
        assert(histo)
        histo = histo.Clone()
        histo.SetDirectory(0)
        ROOT.SetOwnership(histo, 0)
        self.computed_hists[key] = histo
        self.log.debug(
            "AnalysisSample(%s) registered computed hist %s = %s, int = %s",
            self.name, key, self.computed_hists[key], histo.Integral())
        self.check_hists('end')
        #self.log.debug("AnalysisSample(%s) all registered computed hist %s",
                       #self.name, self.computed_hists.keys())

    def check_hists(self, label):
        for key, value in self.computed_hists.iteritems():
            if not value:
                self.log.warning(
                    "AnalysisSample(%s) @ %s computed hist: %s has become %s!"
                    " %s (is none = %s)",
                    self.name, label, key, str(value), repr(value), value is None)


class AnalysisMultiSample(AnalysisSample):
    def __init__(self, name, *subsamples, **kwargs):
        self.subsamples = subsamples
        super(AnalysisMultiSample, self).__init__(None, name, **kwargs)

    def get(self, path, **kwargs):
        owned_key = (path, tuple(kwargs.keys()))
        if owned_key not in self.owned:
            merged_histo = None
            for subsample in self.subsamples:
                subhisto = subsample.get(path, **kwargs)
                if not merged_histo:
                    merged_histo = subhisto
                else:
                    merged_histo = merged_histo + subhisto
            self.owned[owned_key] = merged_histo
        object = self.owned[owned_key]
        styling.apply_style(object, **self.style_dict)
        return object

    def register_tree(self, name, tree, var, selection, w=None, binning=None):
        for subsample in self.subsamples:
            subsample.register_tree( name, tree, var, selection, w, binning)

class AnalysisPlotter(object):
    log = logging.getLogger("AnalysisPlotter")
    def __init__(self, *samples):
        self.samples = samples
        self.sample_dict = dict(
            (sample.name, sample) for sample in self.samples)
    @staticmethod
    def match_sample(name, includes, excludes):
        ''' Wildcard match a set of objects
        >>> AnalysisPlotter.match_sample('ztt', 'z*', 'data')
        True
        >>> AnalysisPlotter.match_sample('wjets', 'z*', 'data')
        False
        >>> AnalysisPlotter.match_sample('wjets', '*', 'data')
        True
        >>> AnalysisPlotter.match_sample('data', '*', 'data')
        False
        >>> # You can use multiple matches or excludes
        >>> AnalysisPlotter.match_sample('ztt', ['z*', 'wjets'], 'data')
        True
        >>> AnalysisPlotter.match_sample('wjets', ['z*', 'wjets'], 'data')
        True
        '''
        # Listify the include/excludes
        if isinstance(includes, basestring) and includes:
            includes = [includes]
        if isinstance(excludes, basestring) and excludes:
            excludes = [excludes]
        matches = False
        if includes:
            for include in includes:
                if fnmatch.fnmatch(name, include):
                    matches = True
                    break
        if excludes:
            for exclude in excludes:
                if fnmatch.fnmatch(name, exclude):
                    matches = False
                    break
        AnalysisPlotter.log.debug(
            "Testing %s against includes: %s and excludes: %s = %s",
            name, includes, excludes, matches)
        return matches

    def register_tree(self, name, tree, var, selection, binning=None, w = None,
                      include='*', exclude=None):
        for subsample in self.samples:
            if self.match_sample(subsample.name, include, exclude):
                subsample.register_tree(name, tree, var, selection, w, binning)

    def build_stack(self, path, include='*', exclude=None,
                    title=None, **kwargs):
        ''' Build a stack of histograms given the include and exclude
        patterns
        '''
        h = hashlib.md5()
        h.update(path)
        good_samples = []
        for sample in self.samples:
            if self.match_sample(sample.name, include, exclude):
                good_samples.append(sample)
                h.update(sample.name)
        samples_copy = sorted(good_samples, key=lambda x: x.norm(path))
        title = samples_copy[0].title(path) if title is None else title
        name = h.hexdigest()
        output = ROOT.THStack(name, title)
        for sample in samples_copy:
            sample.add_to_stack(path, output, **kwargs)
        return output

    def build_legend(self, path, include='*', exclude=None,
                     #xlow=0.15, ylow=0.6, xhigh=0.4, yhigh=0.89):
                     xlow=0.65, ylow=0.6, xhigh=0.89, yhigh=0.89, drawopt=None):
        output = ROOT.TLegend(xlow, ylow, xhigh, yhigh, "", "brNDC")
        output.SetFillStyle(0)
        output.SetBorderSize(0)
        for sample in self.samples:
            if self.match_sample(sample.name, include, exclude):
                sample.add_to_legend(path, output, drawopt=drawopt)
        return output

    def get_histogram(self, sample, path, **kwargs):
        histo = self.sample_dict[sample].get(path, **kwargs)
        drawopt = self.sample_dict[sample].style_dict.get('draw_opt', '')
        histo.SetOption(drawopt)
        return histo


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

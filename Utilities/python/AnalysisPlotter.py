import ROOT
import fnmatch
import itertools
import re
import logging
import hashlib
import tempfile

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

    def get_weight(self):
        return self.file.weight

    def get_event_count(self):
        return self.file.event_count

    def get_skim_eff(self):
        return self.file.skim_eff

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
            drawopt = self.style_dict.get('draw_opt', 'hist')
        stack.Add(object.th1, drawopt)

    def add_to_legend(self, path, legend, drawopt=None):
        object = self.get(path)
        if drawopt is None:
            drawopt = self.style_dict.get('draw_opt', 'hist')
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

    def scan_to_file(self, filename, tree, var, selection):
        ttree = self.file.get_unweighted(tree)
        outputname = "_".join([filename, self.name, "scanlog"])
        ttree.GetPlayer().SetScanRedirect(True)
        ttree.GetPlayer().SetScanFileName(outputname)
        ttree.Scan(var, selection, 'precision=30')
        return outputname

    def query(self, tree, vars, selection):
        ttree = self.file.get_unweighted(tree)
        print ttree
        result = ttree.Query(vars, selection)
        # Initialize output lists
        output = {}
        for i in range(result.GetFieldCount()):
            output[result.GetFieldName(i)] =  []
        row = result.Next()
        while row:
            for i in range(result.GetFieldCount()):
                print i,result.GetFieldName(i)
                #value = str(row.GetField(i))
                value = row[i]
                print value
                output[result.GetFieldName(i)] = value
            row = result.Next()
        return output

    def get_run_lumi_evt_broken(self, tree, selection):
        # We have to split the event field, because otherwise stupid root will
        # round it.
        result = self.query(tree, "run:lumi:evt%10000:evt/10000", selection)
        # This is broken in current pyroot version??  Works on laptop.
        output = []
        for run, lumi, evt_lsbs, evt_msbs in itertools.izip(
            result['run'], result['lumi'], result['evt%10000'],
            result['evt/10000']):
            run = int(run)
            lumi = int(lumi)
            evt = int(evt_msbs)*10000 + int(evt_lsbs)
            output.append( (run, lumi, evt) )
        return output

    def get_run_lumi_evt(self, tree, selection):
        # Workaround using scan_to_file
        self.log.info("Temporary run-lumi-evt workaround")
        tempfilename = tempfile.mktemp()
        self.log.info("Temporary run-lumi-evt file: %s", tempfilename)
        final_file = self.scan_to_file(
            tempfilename, tree,
            "run:lumi:evt%10000:TMath::Floor(evt/10000)", selection)
        matcher = re.compile(r'\*\s+(?P<row>\d+) \*\s+(?P<run>\d+) \*\s+(?P<lumi>\d+) \*\s+(?P<evt_lsb>\d+) \*\s+(?P<evt_msb>\d+) \*')
        output = []
        with open(final_file) as f:
            for line in f:
                match = matcher.match(line.strip())
                if match:
                    run = int(match.group('run'))
                    lumi = int(match.group('lumi'))
                    evt = int(match.group('evt_msb'))*10000 + \
                            int(match.group('evt_lsb'))
                    output.append( (run, lumi, evt) )
        return output


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

    def get_weight(self):
        return [x.get_weight() for x in self.subsamples]

    def get_event_count(self):
        return [x.get_event_count() for x in self.subsamples]

    def get_skim_eff(self):
        return [x.get_skim_eff() for x in self.subsamples]

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

    def scan_to_file(self, filename, tree, var, selection):
        for subsample in self.subsamples:
            subsample.scan_to_file(filename, tree, var, selection)

    def get_run_lumi_evt(self, tree, selection):
        output = {}
        for subsample in self.subsamples:
            output[subsample.name] = subsample.get_run_lumi_evt(tree, selection)
        return output

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

    def scan_to_file(self, filename, tree, var, selection,
                     include='*', exclude=None):
        for subsample in self.samples:
            if self.match_sample(subsample.name, include, exclude):
                subsample.scan_to_file(filename, tree, var, selection)

    def get_run_lumi_evt(self, tree, selection, include='*', exclude=None):
        output = {}
        for subsample in self.samples:
            if self.match_sample(subsample.name, include, exclude):
                output.update(subsample.get_run_lumi_evt(tree, selection))
        return output

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
        if sample not in self.sample_dict:
            raise KeyError(
                "I don't know anything about sample %s - only these: %s" % (
                    sample, ", ".join(self.sample_dict.keys())))
        histo = self.sample_dict[sample].get(path, **kwargs)
        drawopt = self.sample_dict[sample].style_dict.get('draw_opt', '')
        histo.SetOption(drawopt)
        return histo

    def get_weight(self, sample):
        ''' Get the weight normalization for a sample '''
        if sample not in self.sample_dict:
            raise KeyError(
                "I don't know anything about sample %s - only these: %s" % (
                    sample, ", ".join(self.sample_dict.keys())))
        return self.sample_dict[sample].get_weight()

    def get_skim_eff(self, sample):
        ''' Get the skim eff for a sample '''
        if sample not in self.sample_dict:
            raise KeyError(
                "I don't know anything about sample %s - only these: %s" % (
                    sample, ", ".join(self.sample_dict.keys())))
        return self.sample_dict[sample].get_skim_eff()

    def get_event_count(self, sample):
        ''' Get the event count for a sample '''
        if sample not in self.sample_dict:
            raise KeyError(
                "I don't know anything about sample %s - only these: %s" % (
                    sample, ", ".join(self.sample_dict.keys())))
        return self.sample_dict[sample].get_event_count()


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)

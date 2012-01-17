import ROOT
import random
import array

'''

Wrapper around a TH1F

'''

class Histo(object):
    ''' Histo

    An extension of ROOT.TH1

    >>> import ROOT
    >>> example = Histo(ROOT.TH1F("test", "test", 22, -0.5, 21.5))
    >>> example.Fill(7.0) # returns bin filled into
    8
    >>> # Normal TH1 commands still work
    >>> example.GetMean()
    7.0
    >>> example2 = Histo(ROOT.TH1F("test2", "test2", 22, -0.5, 21.5))
    >>> example2.Fill(10)
    11
    >>> # Overloaded operators
    >>> example3 = example + example2
    >>> example3.Integral()
    2.0
    >>> example3.GetMean()
    8.5
    >>> example4 = example3 * 5.0 # normalization
    >>> example4.Integral()
    10.0
    >>> hist = ROOT.TH1F("t", "t", 22, -0.5, 21.5)
    >>> # Conversion to RooFitStuff
    >>> rooVar = ROOT.RooRealVar("x", "x", 0, 0, 20)
    >>> type(example.makeRooDataHist(rooVar))
    <class 'ROOT.RooDataHist'>
    >>> # Rebinning
    >>> rebinned = Histo(hist, rebin = 2)
    >>> rebinned.GetNbinsX()
    11
    >>> # The original histogram doesn't change
    >>> hist.GetNbinsX()
    22
    >>> # Bins are objects too
    >>> bin_objects = Histo(hist)
    >>> bin_objects.Fill(-1)
    -1
    >>> bin_objects.Fill(5)
    6
    >>> # Looping over bins - lets count nonzero bins
    >>> len([bin for bin in bin_objects.bins() if bin.value()])
    1
    >>> underflow = bin_objects.bin(0)
    >>> float(underflow)
    1.0
    >>> # Making the CDF function
    >>> hist = ROOT.TH1F("t2", "t2", 22, -0.5, 21.5)
    >>> bin = hist.Fill(5)
    >>> bin = hist.Fill(10)
    >>> bin = hist.Fill(-1) # underflow
    >>> bin = hist.Fill(-1) # underflow
    >>> histo = Histo(hist)
    >>> cdf = histo.cdf()
    >>> cdf(1.0)
    0.0
    >>> cdf(9.0)
    0.5
    >>> cdf(12.0)
    1.0
    >>> cdf, cdf_inv = histo.cdf(include_overflows=True, include_inverse=True, \
                                 smooth=True)
    >>> cdf_inv(0.5)
    -0.5
    >>> cdf_inv((1.0-0.75)/2 + 0.75) - ((10.5 - 5.5)/2 + 5.5)
    0.0
    >>> # Transforming a histogram
    >>> hist = ROOT.TH1F("t3", "t3", 22, -0.5, 21.5)
    >>> bin = hist.Fill(5)
    >>> histo = Histo(hist)
    >>> histo(5), histo(10.0)
    (1.0, 0.0)
    >>> transformed = histo.transform(lambda x: x+5)
    >>> transformed(5), round(transformed(10.0), 3)
    (0.0, 1.0)
    >>> # Non-equal rebinning
    >>> hist = Histo(ROOT.TH1F("t4", "t4", 10, 0, 10))
    >>> bin = hist.Fill(0.5)
    >>> bin = hist.Fill(6)
    >>> bin = hist.Fill(8)
    >>> rebinned = hist.cloneAndRebin([0, 1, 2, 3, 10])
    >>> rebinned(0.5)
    1.0
    >>> rebinned(7.5)
    2.0
    >>> rebinned.GetNbinsX()
    4
    '''
    def __init__(self, th1, **kwargs):
        self.th1 = th1.Clone()
        self.th1.SetDirectory(0)
        ROOT.SetOwnership(self.th1, 0)
        # Check if we want to rebin the histogram
        if 'rebin' in kwargs:
            clone = self.th1.Clone()
            clone.Rebin(kwargs['rebin'])
            self.th1 = clone

        if kwargs.get('show_overflows', False):
            underflow = self.bin(0)
            first_bin = self.bin(1)
            first_bin += underflow
            last_bin = self.bin(self.GetNbinsX())
            overflow = self.bin(self.GetNbinsX()+1)
            last_bin += overflow

        # Stuff we need to prevent being eaten by the GC
        self.owned = []

    def __getattr__(self, attr):
        return getattr(self.th1, attr)

    def cloneAndRebin(self, binning):
        # Returns a rebinned histogram
        bin_array = array.array('d', binning)
        rebinned = self.th1.Rebin(len(binning)-1, self.GetName() + 'rebinned',
                                  bin_array)
        return Histo(rebinned)

    def makeRooDataHist(self, *variables):
        output =  ROOT.RooDataHist(
            self.GetName(), self.GetTitle(), ROOT.RooArgList(*variables),
            self.th1)
        return output

    def makeRooHistPdf(self, *variables):
        # Build a root data hist and a roohist pdf
        data_hist = self.makeRooDataHist(*variables)
        output = ROOT.RooHistPdf(
            self.GetName(), self.GetTitle(),
            ROOT.RooArgSet(*variables), data_hist)
        return data_hist, output

    def __add__(self, other):
        clone = self.th1.Clone()
        clone.Add(other.th1)
        return Histo(clone)

    def __sub__(self, other):
        clone = self.th1.Clone()
        clone.Add(other.th1, -1.0)
        return Histo(clone)

    def __mul__(self, number):
        clone = self.th1.Clone()
        clone.Scale(number)
        return Histo(clone)

    def __call__(self, x):
        return self.th1.GetBinContent(self.FindBin(x))

    def __nonzero__(self):
        if self.th1:
            return True
        else:
            return False

    def bin(self, bin_index):
        return HistoBin(self.th1, bin_index)

    def bins(self, include_overflows=False):
        low_end = 0
        if not include_overflows:
            low_end = 1
        high_end = self.th1.GetNbinsX()
        if include_overflows:
            high_end += 1
        for i in xrange(low_end, high_end+1):
            yield self.bin(i)

    def cdf(self, include_overflows=False, include_inverse=False, smooth=False):
        ''' Build the cumulative distribution function of the histogram '''
        xy_points = []
        total = 0.0
        for bin in self.bins(include_overflows):
            total += bin.value()
            xy_points.append((bin.upper_edge(), total))

        def smoother(iterable):
            last_y = None
            for x, y in iterable:
                if last_y is None or y != last_y:
                    yield (x,y)
                    last_y = y
        if smooth:
            xy_points[:] = [xy_points[0]] + \
                    list(smoother(xy_points[1:-1])) + [xy_points[-1]]

        output_graph = ROOT.TGraph(len(xy_points))
        output_inverted_graph = ROOT.TGraph(len(xy_points))
        for i, (x,y) in enumerate(xy_points):
            output_graph.SetPoint(i, x, y/total)
            output_inverted_graph.SetPoint(i, y/total, x)
        # Closure function
        def cdf_function(x):
            return output_graph.Eval(x)
        def cdf_inverted_function(x):
            return output_inverted_graph.Eval(x)
        if include_inverse:
            return cdf_function, cdf_inverted_function
        else:
            return cdf_function

    def sample(self, n):
        ''' Generate n samples from this histogram '''
        cdf, cdf_inverse = self.cdf(False, True, True)
        for i in xrange(n):
            return cdf_inverse(random.random())

    def zeroOutNegativeBins(self):
        for bin in self.bins():
            if bin.value() < 0:
                bin.set(0)

    def transform(self, function, steps_per_bin=1e4):
        output = self.th1.Clone()
        output.Reset("ICES")
        for bin in self.bins():
            if not bin.value():
                continue
            step_size = bin.width()/steps_per_bin
            step_start = bin.low_edge()
            step_content = bin.value()/steps_per_bin
            for step in xrange(int(steps_per_bin)):
                x = step_start + step*step_size
                x_prime = function(x)
                output.Fill(x_prime, step_content)
        return Histo(output)

class HistoBin(object):
    def __init__(self, th1, bin_index):
        self.th1 = th1
        self.bin_index = bin_index
    def center(self):
        return self.th1.GetBinCenter(self.bin_index)
    def width(self):
        return self.th1.GetBinWidth(self.bin_index)
    def low_edge(self):
        return self.th1.GetBinLowEdge(self.bin_index)
    def upper_edge(self):
        return self.low_edge() + self.width()
    def value(self):
        return self.th1.GetBinContent(self.bin_index)
    def set(self, value):
        return self.th1.SetBinContent(self.bin_index, value)
    def __float__(self):
        return self.value()
    def __iadd__(self, to_add):
        self.set(self.value() + float(to_add))

if __name__ == "__main__":
    import doctest
    doctest.testmod()

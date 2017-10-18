'''

A rootpy histogram "view" which blinds out histos whose path matches a regex.

One can optionally pass a "blinding" function which applies some operation
(i.e. zeroing some bins) to the histogram to blind it.  If it isn't specified,
the entire histogram will be Reset() to zero.

You can use "blind_in_range" to blind only a subset.

Author: Evan K. Friis, UW Madison

'''

from rootpy.plotting import views
import re

def blind_in_range(start, end):
    ''' Make a functor to blind a TH1 between start and end '''
    def blind(histo):
        startbin = histo.FindBin(start)
        endbin = histo.FindBin(end)
        for i in range(startbin, endbin+1):
            histo.SetBinContent(i, 0)
            histo.SetBinError(i, 0)
        return histo
    return blind

def set_to_zero(histo):
    histo.Reset()
    return histo

class BlindView(views._FolderView):
    def __init__(self, directory, regex, blinding=None):
        super(BlindView, self).__init__(directory)
        self.regex = re.compile(regex)
        if blinding is not None:
            self.blind = blinding
        else:
            self.blind = set_to_zero

    def apply_view(self, thingy):
        # Set in base class
        path = self.getting
        if self.regex.match(path):
            # We need to blind
            clone = thingy.Clone()
            return self.blind(clone)
        # Not blinded
        return thingy

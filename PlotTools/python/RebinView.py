'''

View to rebin a histogram.

Author: Evan K. Friis, UW Madison

'''

import array
import rootpy.plotting.views as views

class RebinView(views._FolderView):
    ''' Rebin a histogram.

    The original histogram is unmodified, a rebinned clone is returned.

    '''
    def __init__(self, dir, binning):
        self.binning = binning
        super(RebinView, self).__init__(dir)

    @staticmethod
    def rebin(histogram, binning):
        ''' Rebin a histogram

        [binning] can be either an integer, or a list/tuple for variable bin
        sizes.

        '''
        # Just merging bins
        if isinstance(binning, int):
            histogram.Rebin(binning)
            return histogram
        # Fancy variable size bins
        bin_array = array.array('d', binning)
        new_histo = histogram.Rebin(len(binning)-1, histogram.GetName() + 'rebin', bin_array)

	print new_histo.GetTitle()
        return new_histo
        #import pdb; pdb.set_trace()

    def apply_view(self, object):
        object = object.Clone()
        return self.rebin(object, self.binning)

'''

View to rebin a histogram.

Author: Evan K. Friis, UW Madison

'''

import rootpy.plotting.views as views

class RebinView(views._FolderView):
    ''' Rebin a histogram.

    The original histogram is unmodified, a rebinned clone is returned.

    '''
    def __init__(self, dir, binning):
        self.binning = binning
        super(RebinView, self).__init__(dir)

    def apply_view(self, object):
        object = object.Clone()
        object.Rebin(self.binning)
        return object

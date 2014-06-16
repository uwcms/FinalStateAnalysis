'''

View to scale a histogram content by the bin view

Author: Mauro Verzetti, Uni. Zurich

'''

import rootpy.plotting.views as views
try:
    from rootpy.utils import asrootpy
except ImportError:
    from rootpy import asrootpy
import ROOT
import os

class DifferentialView(views._FolderView):
    ''' Scales a histogram content by the bin width.

    The original histogram is unmodified, a clone is returned.

    '''
    def __init__(self, dir):
        super(DifferentialView, self).__init__(dir)

    def apply_view(self, object):
        object = object.Clone()
        for i in range(0, object.GetNbinsX()+2): #scale underflow/overflow too
            content = object.GetBinContent(i)
            error   = object.GetBinError(i)
            width   = object.GetBinWidth(i)  
            object.SetBinContent(i, content / width)
            object.SetBinError(i, error / width)  

        return object

import rootpy.plotting.views as views
from THBin import zipBins

class InflateErrorView(views._FolderView):
    ''' 
    Inflates the errors in a histograms, useful for introducing systematics
    '''
    def __init__(self, dir, inflation):
        self.inflation = 1+inflation
        super(InflateErrorView, self).__init__(dir)

    def apply_view(self, object):
        object = object.Clone()
        for hbin in zipBins(object):
            hbin.error *= self.inflation 
        return object

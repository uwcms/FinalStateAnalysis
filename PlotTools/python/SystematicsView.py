import rootpy.plotting.views as views
from FinalStateAnalysis.StatTools.quad     import quad
from THBin import zipBins

class SystematicsView(views._FolderView):
    ''' 
    Adds a yield systematics
    '''
    def __init__(self, input_view, sys_error):
        self.sys_error = sys_error
        super(SystematicsView, self).__init__(input_view)

    @staticmethod
    def add_error(histo, sys_error):
        clone = histo.Clone()
        for hbin in zipBins(clone):
            hbin.error = quad(
                hbin.error, 
                hbin.content * sys_error
            ) 
        return clone

    def apply_view(self, hist):
        return SystematicsView.add_error(hist, self.sys_error)


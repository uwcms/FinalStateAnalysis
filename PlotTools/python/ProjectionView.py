import ROOT
try:
    from rootpy.utils import asrootpy
except ImportError:
    from rootpy import asrootpy

class ProjectionView(object):
    def __init__(self, input_view, axis, proj_range):
        self.input = input_view
        self.axis  = axis
        self.range = proj_range

    def Get(self, path):
        hist = self.input.Get(path) 
        if not isinstance(hist, (ROOT.TH2, ROOT.TH3)):
            return hist #nothin to do

        projection_axis = 'X' if self.axis.upper() == 'Y' else 'Y'
        axis = getattr(hist, 'Get%saxis' % projection_axis)()
        min_bin = axis.FindFixBin(self.range[0])
        max_bin = axis.FindFixBin(self.range[1])
        if axis.GetBinLowEdge(max_bin) == self.range[1]:
            max_bin -= 1

        output = getattr(hist, 'Projection%s' % self.axis.upper())(hist.GetName() + '_projection', min_bin, max_bin)
        output = asrootpy( output )
        #print "ProjectionView: path %s, minimum:%.2f --> %i, maximum:%.2f --> %i, integral: %.3f entries: %i" % (path, self.range[0], min_bin, self.range[1], max_bin, output.Integral(), output.GetEntries()) 
        output.decorate( **hist.decorators )
        output.SetTitle( hist.GetTitle() )
        #print hist.GetTitle(), output.GetTitle()
        return output

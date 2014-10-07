'''

A rootpy histogram "view" which converts an integer histogram to a
TGraphAsymmErrors with correct, asymmetric Poissonian errors.

Optionally, you can suppress empty (zero) bins.

Author: Evan K. Friis, UW Madison

'''

from rootpy.plotting import views
try:
    from rootpy.utils import asrootpy
except ImportError:
    from rootpy import asrootpy
import FinalStateAnalysis.StatTools.poisson as poisson

class PoissonView(views._FolderView):
    def __init__(self, dir, x_err=True, set_zero_bins=None, marker_size=1, is_scaled=False):
        super(PoissonView, self).__init__(dir)
        self.x_err = x_err
        self.set_zero_bins = set_zero_bins
        self.marker_size = marker_size
        self.is_scaled = is_scaled

    def apply_view(self, histo):
        graph = poisson.convert(histo, self.x_err, self.set_zero_bins, self.is_scaled)
        graph.SetMarkerSize(self.marker_size)
        return asrootpy(graph)

'''

Implements the same as a rootpy.plotting.views.SumView
but subtracting instead.

The views in positions 2-N are subtracted from view at argument 1
in the constructor.

Optionally, one can require that the returned values be non-negative.
Negative bins are set to zero.

Author: Evan K. Friis, UW Madison

'''

from rootpy.plotting import views

class PositiveView(views._FolderView):
    ''' Restrict a histogram to non-negative entries

    Negative bins are set to zero.

    '''
    def __init__(self, dir):
        super(PositiveView, self).__init__(dir)

    @staticmethod
    def positivize(histogram):
        output = histogram.Clone()
        for i in range(output.GetSize()):
            if output.GetArray()[i] < 0:
                output.AddAt(0, i)
        return output

    def apply_view(self, histogram):
        return self.positivize(histogram)

class SubtractionView(views.SumView):
    '''

    Subtract the histograms in the views <to_subtract> from the histogram
    in the <main_view>.

    If 'restrict_positive' is set to true in kwargs, zero out any
    negative bins.

    '''
    def __init__(self, main_view, *to_subtract, **kwargs):
        # Make all the subtracted ones negative
        negated = [views.ScaleView(x, -1) for x in to_subtract]
        # Now make this a sum of the main view + the negated subtractors
        # Remember, the base class is a SumView.
        super(SubtractionView, self).__init__(main_view, *negated)
        self.restrict_positive = kwargs.get('restrict_positive', False)

    def merge_views(self, *histograms):
        output = super(SubtractionView, self).merge_views(*histograms)
        if self.restrict_positive:
            # Steal PositiveView's positive-izer
            output = PositiveView.positivize(output)
        return output

'''

Implements the same as a rootpy.plotting.views.SumView
but subtracting instead.

The views in positions 2-N are subtracted from view at argument 1
in the constructor.

Author: Evan K. Friis, UW Madison

'''

from rootpy.plotting import views

class SubtractionView(views.SumView):
    def __init__(self, main_view, *to_subtract):
        # Make all the subtracted ones negative
        negated = [views.ScaleView(x, -1) for x in to_subtract]
        # Now make this a sum of the main view + the negated subtractors
        # Remember, the base class is a SumView.
        super(SubtractionView, self).__init__(main_view, *negated)

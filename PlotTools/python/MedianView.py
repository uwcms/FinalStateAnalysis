import rootpy.plotting.views as views
import math
def quad(*xs):
    return math.sqrt(sum(x * x for x in xs))

class MedianView(object):
    ''' Takes high and low, returns median assigning half the diff as error. '''
    def __init__(self, highv=None, lowv=None, centv=None, **kwargs):
        self.highv = highv
        self.lowv  = lowv
        self.centv = views.ScaleView( views.SumView(lowv, self.highv) , 0.5) if not centv else centv
        self.get_defaults = kwargs

    def Get(self, path, **kwargs):
        central_hist = self.centv.Get(path)
        high_hist    = self.highv.Get(path) if self.highv else None
        low_hist     = self.lowv.Get(path)  if self.lowv  else None
        defaults     = self.get_defaults #gets the getting defaults

        #Deal with special cases
        defaults.update(kwargs) #adds/overrride with the provided ones
        ret_hist = central_hist.Clone()
        if 'sys2stat' in defaults and not defaults['sys2stat']:
            #we don't want that the systematic shift is added to the statistical error.
            #simply return central_hist
            return ret_hist
        if 'shift' in defaults:
            #we want the histogram shifted one sigma up/down
            if defaults['shift'] == 'up':
                #we want the shift up, return it if we have it, otherwise return the central+(central-shift_down)
                return high_hist if high_hist else central_hist*2 + low_hist
            elif defaults['shift'] == 'down':
                #we want the shift up, return it if we have it, otherwise return the central-(shift_up-central)
                return low_hist if low_hist else central_hist*2 - high_hist
            else:
                raise KeyError("Shift keyword argument can only be 'up' or 'down'")            
        
        for bin in range(1, high_hist.GetNbinsX() + 1):
            error = quad(
                central_hist.GetBinError(bin),
                (high_hist.GetBinContent(bin) - central_hist.GetBinContent(bin))
            ) if high_hist else \
            quad(
                central_hist.GetBinError(bin),
                (central_hist.GetBinContent(bin) - low_hist.GetBinContent(bin))
            ) 
            
            ret_hist.SetBinError(bin, error)
        return ret_hist

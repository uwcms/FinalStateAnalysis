'''

View to rebin a histogram.

Author: Evan K. Friis, UW Madison

'''

import array
import rootpy.plotting.views as views
import rootpy.plotting as plotting
try:
    from rootpy.utils import asrootpy
except ImportError:
    from rootpy import asrootpy
import ROOT
import os

class RebinView(views._FolderView):
    ''' Rebin a histogram.

    The original histogram is unmodified, a rebinned clone is returned.

    '''
    def __init__(self, dir, binning):
        self.binning = binning
        super(RebinView, self).__init__(dir)

    @staticmethod
    def newRebin2D(histogram, bin_arrayx, bin_arrayy):
        'Rebin 2D histo with irregular bin size'
        
        #create a clone with proper binning
        # from pdb import set_trace; set_trace()
        new_histo = plotting.Hist2D(
            bin_arrayx,
            bin_arrayy,
            #name = histogram.name,
            title = histogram.title,
            **histogram.decorators
        )

        #check that new bins don't overlap on old edges
        oldbinx = [float(histogram.GetXaxis().GetBinLowEdge(1))]
        oldbiny = [float(histogram.GetYaxis().GetBinLowEdge(1))]
        oldbinx.extend(float(histogram.GetXaxis().GetBinUpEdge(x)) for x in xrange(1, histogram.GetNbinsX()+1))
        oldbiny.extend(float(histogram.GetYaxis().GetBinUpEdge(y)) for y in xrange(1, histogram.GetNbinsY()+1))
        for x in bin_arrayx:
            if x==0:
                if not any( abs((oldx)) < 10**-8 for oldx in oldbinx ):
                    raise Exception('New bin edge in x axis %s does not match any old bin edge, operation not permitted' % x)
            else:
                if not any( abs((oldx / x)-1.) < 10**-8 for oldx in oldbinx ):
                    raise Exception('New bin edge in x axis %s does not match any old bin edge, operation not permitted' % x)
        for y in bin_arrayy:
            if y ==0:
                if not any( abs((oldy) )< 10**-8 for oldy in oldbiny ):
                    raise Exception('New bin edge in y axis %s does not match any old bin edge, operation not permitted' % y)
            else:
                if not any( abs((oldy / y)-1.) < 10**-8 for oldy in oldbiny ):
                    raise Exception('New bin edge in y axis %s does not match any old bin edge, operation not permitted' % y)
        
        #fill the new histogram
        for x in xrange(1, histogram.GetNbinsX()+1 ):
            for y in xrange(1, histogram.GetNbinsY()+1 ):
                new_histo.Fill(histogram.GetXaxis().GetBinCenter(x), histogram.GetYaxis().GetBinCenter(y), histogram.GetBinContent(x,y))

        new_histo.SetEntries( histogram.GetEntries() )
        return new_histo
                              
    def rebin(self, histogram, binning):
        ''' Rebin a histogram

        [binning] can be either an integer, or a list/tuple for variable bin
        sizes.

        '''
        # Just merging bins
        if isinstance(binning, int):
            if binning == 1 or isinstance(histogram, ROOT.TH2):
                return histogram
            histogram.Rebin(binning)
            return histogram
        # Fancy variable size bins
        if isinstance(histogram, ROOT.TH2):
            if not isinstance(binning[0], (list, tuple)):
                return histogram
            #print binning[0], ' ' , binning[1] 
            bin_arrayx = binning[0] #array.array('d',binning[0])
            bin_arrayy = binning[1] #array.array('d',binning[1])
            if len(binning[0]) ==1 and len(binning[1])==1 :                
                return  histogram.Rebin2D(int(binning[0][0]),int(binning[1][0]), histogram.GetName() + 'rebin')
            else:
                return self.newRebin2D(histogram, bin_arrayx, bin_arrayy)
        elif isinstance(histogram, ROOT.TH1):
            if isinstance(binning[0], (list, tuple)):
                return histogram
            bin_array = array.array('d', binning)
            ret = asrootpy( histogram.Rebin(len(binning)-1, histogram.GetName() + 'rebin', bin_array) )
            if hasattr(histogram, 'decorators'):
                ret.decorate( **histogram.decorators )
            return ret 
        else:
            print 'ERROR in RebinView: not a TH1 or TH2 histo. Rebin not done'
            
            return histogram
        #import pdb; pdb.set_trace()

    def apply_view(self, object):
        object = object.Clone()
        return self.rebin(object, self.binning)

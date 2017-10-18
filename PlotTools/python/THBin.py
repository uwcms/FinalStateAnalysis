from ROOT import TH1

class TH1Bin(object):
    def __init__(self,th1,binNum):
        '''Initializes the TH1Bin, a helper class to make easier dealing with single bins ROOT, supposed to work in a for loop!'''
        self._th1     = th1
        self._binNum  = binNum
        self.center   = th1.GetBinCenter(binNum)   
        self.content  = th1.GetBinContent(binNum)  
        self.error    = th1.GetBinError(binNum)    
        self.lowEdge  = th1.GetBinLowEdge(binNum)  
        self.width    = th1.GetBinWidth(binNum)
        
    def flush(self):
        '''flushes the content of the bin into the histogram from which it was taken'''
        #print 'called flush'
        self._th1.SetBinContent( self._binNum, self.content )  
        self._th1.SetBinError(   self._binNum, self.error )    
        
    def __del__(self):
        '''flushes before deleting!'''
        #print 'called del'
        self.flush()

    ## def __repr__:
    ##     return 'TH1Bin: bin# %s, content'

def zipBins(*args,**kwargs):
    '''zipBins(h1,...[start=1,end=-1]) ==> iterator of tuples of bins
    This functions takes an arbitrary number of histograms and return an iterator of tuples of TH1Bin.
    Basically it make the histogram behave like a list of TH1Bin.
    If start keyword argument is set the lists will start from that value (default is one, so no underflow)
    If end keyword argument is set the lists will end at that value (default is -1, meaning that the lenght if the iterator will be the minimum bin size of the histograms passed, overflow excluded)
    If end is larger than a binning None is returned instead the Bin instance'''
    start = kwargs['start'] if 'start' in kwargs else 1
    end   = kwargs['end'] if 'end' in kwargs else min( map(lambda x: x.GetNbinsX(), args ) )
    for i in range(start, end+1):
        if len(args) == 1:
            yield TH1Bin(args[0],i)
        else:
            yield tuple([TH1Bin(h1,i) for h1 in args])







import ROOT

'''

Wrapper about TLegend

'''

class Legend(ROOT.TLegend):
    def __init__(self, **kwargs):
        self.xlow = 0.6
        self.ylow = 0.5
        self.xhigh = 0.89
        self.yhigh = 0.89
        self.align = 'left'

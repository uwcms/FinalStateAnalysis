from rootpy.io import root_open
import ROOT
import sys
from math import pow, sqrt

class GraphReader(object):
    """Loads a graph with trigger efficiency from data"""
    def __init__(self, filename):
        self.table = {} 
        #dict is fine for small number of bins, 
        #for larger ones use sorted list and binary search
        input_file= root_open(filename)
        if  not input_file:
               sys.stderr.write("Can't open file: %s\n" % filename)
        gr1 = input_file.Get("ZMassEtaLt1p48_Data")
        gr2 = input_file.Get("ZMassEta1p48to2p1_Data")
        gr3 = input_file.Get("ZMassEtaGt2p1_Data")
        
        npoint1=gr1.GetN()
        eff1 = []
        eta_thrs = 0.0, 1.48
        for n in range(0, npoint1):
            xval = ROOT.Double(0)
            yval = ROOT.Double(0)
            gr1.GetPoint(n, xval, yval)
            xevalp = gr1.GetErrorXhigh(n)
            xevalm = gr1.GetErrorXlow(n)
            yeval = gr1.GetErrorY(n)
            pt_thrs = xval-xevalm, xval+xevalp
            if pt_thrs not in self.table:
                self.table[pt_thrs] = {}
            self.table[pt_thrs][eta_thrs] = yval, yval-yeval

        eta_thrs = 1.48, 2.1
        npoint2=gr2.GetN()
        eff2 = []
        for n in range(0, npoint2):
            xval = ROOT.Double(0)
            yval = ROOT.Double(0)
            gr2.GetPoint(n, xval, yval)
            xevalp = gr2.GetErrorXhigh(n)
            xevalm = gr2.GetErrorXlow(n)
            yeval= gr2.GetErrorY(n)
            pt_thrs = xval-xevalm, xval+xevalp
            if pt_thrs not in self.table:
                self.table[pt_thrs] = {}
            self.table[pt_thrs][eta_thrs] = yval, yval-yeval


        eta_thrs =  2.1, 3.0
        npoint3=gr3.GetN()
        eff3 = []
        for n in range(0, npoint3):
            xval = ROOT.Double(0)
            yval = ROOT.Double(0)
            gr3.GetPoint(n, xval, yval)
            xevalp = gr3.GetErrorXhigh(n)
            xevalm = gr3.GetErrorXlow(n)
            yeval = gr3.GetErrorY(n)
            if pt_thrs not in self.table:
                self.table[pt_thrs] = {}
            self.table[pt_thrs][eta_thrs] = yval, yval-yeval
  
    
    def __call__(self, pt, abseta):
        """Return correction given pt and eta, 
        raise error if out of boundaries"""
        for pt_thrs, pt_vals in self.table.iteritems():
            ptmin, ptmax = pt_thrs
            if ptmin <= pt < ptmax:
                for eta_thrs, correction in pt_vals.iteritems():
                    etamin, etamax = eta_thrs
                    if etamin <= abseta < etamax:
                        return correction
        raise ValueError("pt or eta out of boundaries for correction range: %s %s" %(pt, abseta))
                    
class GraphReaderSF(object):
    """Loads a graph with trigger efficiency from data"""
    def __init__(self, filename):
        self.table = {} 
        #dict is fine for small number of bins, 
        #for larger ones use sorted list and binary search
        input_file= root_open(filename)
        if  not input_file:
               sys.stderr.write("Can't open file: %s\n" % filename)
        gr1 = input_file.Get("ZMassEtaLt1p48_Data")
        gr2 = input_file.Get("ZMassEta1p48to2p1_Data")
        gr3 = input_file.Get("ZMassEtaGt2p1_Data")
        grMC1 = input_file.Get("ZMassEtaLt1p48_MC")
        grMC2 = input_file.Get("ZMassEta1p48to2p1_MC")
        grMC3 = input_file.Get("ZMassEtaGt2p1_MC")
        
        npoint1=gr1.GetN()
        eff1 = []
        eta_thrs = 0.0, 1.48
        for n in range(0, npoint1):
            xval = ROOT.Double(0)
            yval = ROOT.Double(0)
            gr1.GetPoint(n, xval, yval)
            xvalMC = ROOT.Double(0)
            yvalMC = ROOT.Double(0)
            grMC1.GetPoint(n, xvalMC, yvalMC)
            xevalp = gr1.GetErrorXhigh(n)
            xevalm = gr1.GetErrorXlow(n)
            yeval = gr1.GetErrorY(n)
            yevalMC = grMC1.GetErrorY(n)
            
            pt_thrs = xval-xevalm, xval+xevalp
            if pt_thrs not in self.table:
                self.table[pt_thrs] = {}
            err2=yeval*yeval/(yvalMC*yvalMC)+yevalMC*yevalMC*yval*yval/pow(yvalMC,4)
            self.table[pt_thrs][eta_thrs] = yval/yvalMC, sqrt(err2)

        eta_thrs = 1.48, 2.1
        npoint2=gr2.GetN()
        eff2 = []
        for n in range(0, npoint2):
            xval = ROOT.Double(0)
            yval = ROOT.Double(0)
            gr2.GetPoint(n, xval, yval)
            xvalMC = ROOT.Double(0)
            yvalMC = ROOT.Double(0)
            grMC2.GetPoint(n, xvalMC, yvalMC)
            xevalp = gr2.GetErrorXhigh(n)
            xevalm = gr2.GetErrorXlow(n)
            yeval= gr2.GetErrorY(n)
            yevalMC = grMC2.GetErrorY(n)
            pt_thrs = xval-xevalm, xval+xevalp
            if pt_thrs not in self.table:
                self.table[pt_thrs] = {}
            err2=yeval*yeval/(yvalMC*yvalMC)+yevalMC*yevalMC*yval*yval/pow(yvalMC,4)
            self.table[pt_thrs][eta_thrs] = yval/yvalMC, sqrt(err2)


        eta_thrs =  2.1, 3.0
        npoint3=gr3.GetN()
        eff3 = []
        for n in range(0, npoint3):
            xval = ROOT.Double(0)
            yval = ROOT.Double(0)
            gr3.GetPoint(n, xval, yval)
            xvalMC = ROOT.Double(0)
            yvalMC = ROOT.Double(0)
            grMC3.GetPoint(n, xvalMC, yvalMC)
            xevalp = gr3.GetErrorXhigh(n)
            xevalm = gr3.GetErrorXlow(n)
            yeval = gr3.GetErrorY(n)
            yevalMC = grMC3.GetErrorY(n)
            pt_thrs = xval-xevalm, xval+xevalp
            if pt_thrs not in self.table:
                self.table[pt_thrs] = {}
            err2=yeval*yeval/(yvalMC*yvalMC)+yevalMC*yevalMC*yval*yval/pow(yvalMC,4)
            self.table[pt_thrs][eta_thrs] = yval/yvalMC,  sqrt(err2)
  

    def __call__(self, pt, abseta):
        """Return correction given pt and eta, 
        raise error if out of boundaries"""
        for pt_thrs, pt_vals in self.table.iteritems():
            ptmin, ptmax = pt_thrs
            if ptmin <= pt < ptmax:
                for eta_thrs, correction in pt_vals.iteritems():
                    etamin, etamax = eta_thrs
                    if etamin <= abseta < etamax:
                        return correction
        raise ValueError("pt or eta out of boundaries for correction range: %s %s" %(pt, abseta))


class GraphReaderTrackingEta(object):
    """Loads a graph with trigger efficiency from data"""
    def __init__(self, filename):
        self.table = {} 
        #dict is fine for small number of bins, 
        #for larger ones use sorted list and binary search
        input_file= root_open(filename)
        if  not input_file:
               sys.stderr.write("Can't open file: %s\n" % filename)
        gr1 = input_file.Get("ratio_eta")
        npoint1=gr1.GetN()
        eff1 = []
        for n in range(0, npoint1):
            xval = ROOT.Double(0)
            yval = ROOT.Double(0)
            gr1.GetPoint(n, xval, yval)
            xevalp = gr1.GetErrorXhigh(n)
            xevalm = gr1.GetErrorXlow(n)
            yevalp = gr1.GetErrorYhigh(n)
            yevalm = gr1.GetErrorYlow(n)
            
            eta_thrs = xval-xevalm, xval+xevalp
            if eta_thrs not in self.table:
                self.table[eta_thrs] = {}
            self.table[eta_thrs] = yval, max(yevalp, yevalm)

     
    
    def __call__(self, eta):
        """Return correction given pt and eta, 
        raise error if out of boundaries"""
        if eta < -2.4 : eta = -2.39
        if eta > 2.4 : eta = 2.39
        for eta_thrs, eta_vals in self.table.iteritems():
            etamin, etamax = eta_thrs
            if etamin <= eta < etamax:
                return eta_vals
        raise ValueError("pt or eta out of boundaries for correction range: %s %s" %(pt, abseta))
                    

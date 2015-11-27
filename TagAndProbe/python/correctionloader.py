

class CorrectionLoader(object):
    """Loads a txt file with data to MC corrections"""
    def __init__(self, filename):
        """Creates object given input filename path 
        
        txt file format, tab separated table, no header
        columns: ptmin, ptmax, eta min, eta max, correction
        uncertainty"""
        self.table = {} 
        #dict is fine for small number of bins, 
        #for larger ones use sorted list and binary search
        with open(filename) as input_file:
            for line in input_file:
                str_vals = [i.strip() for i in line.split() if i.strip()]
                vals = [float(i) for i in str_vals]
                pt_thrs  = vals[0], vals[1]
                eta_thrs = vals[2], vals[3]
                if pt_thrs not in self.table:
                    self.table[pt_thrs] = {}
                self.table[pt_thrs][eta_thrs] = vals[4], vals[5]

    def __call__(self, pt, eta):
        """Return correction given pt and eta, 
        raise error if out of boundaries"""
        for pt_thrs, pt_vals in self.table.iteritems():
            ptmin, ptmax = pt_thrs
            if ptmin <= pt < ptmax:
                for eta_thrs, correction in pt_vals.iteritems():
                    etamin, etamax = eta_thrs
                    if etamin <= eta < etamax:
                        return correction
        raise ValueError("pt or eta out of boundaries for correction range: %s %s" %(pt, eta))
                    

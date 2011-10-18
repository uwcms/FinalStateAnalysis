from templates import get_th1
from templates import data_name_map
import math


regions = ['sig', 'qcd', 'wjets']
types = ['Pass', 'Fail']

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

def ass_error(x, y):
    return math.sqrt(x)*(2*y)/((x + y)*(x+y))


for sample in data_name_map.keys():
    print ""
    print "==================="
    print sample
    print "==================="
    for type in types:
        for region in regions:
            extras = ['']
            if 'zjets' in sample and 'sig' in region:
                extras = ['/realTau', '/fakeTau']
            for extra in extras:
                for sign in ['OS', 'SS']:
                    muon = get_th1(sample, region + type + sign + extra, 'MuonCharge')
                    positive = muon(1)
                    negative = muon(-1)
                    pos_error = math.sqrt(positive)/positive
                    neg_error = math.sqrt(negative)/negative
                    total_error = quad(pos_error, neg_error)
                    ratio = positive/negative
                    error = ratio*total_error

                    assymetry = (positive - negative)/(positive + negative)
                    assymetry_err = quad(ass_error(positive, negative),
                                         ass_error(negative, positive))
                    print " & ".join([
                        type + extra,
                        region.upper(),
                        #sample,
                        sign,
                        #"$%0.2f \pm %0.2f$" % (ratio, error),
                        "$%0.1f \pm %0.1f$" % (100*assymetry, 100*assymetry_err),

                    ]) + " \\\\"


# Make latex table

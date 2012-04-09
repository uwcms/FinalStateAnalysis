'''

Interface to use TEfficiency to compute efficiency intervals

'''

import ROOT


def efficiency(passed, total, conf=0.682689492137):
    ''' Use Clopper-Pearson to compute confidence interval

    '''

    eff = 0
    if total:
       eff = passed*1./total

    total = ROOT.TMath.Nint(total)
    passed = ROOT.TMath.Nint(passed)

    up = ROOT.TEfficiency.ClopperPearson(total, passed, conf, True)
    down = ROOT.TEfficiency.ClopperPearson(total, passed, conf, False)

    return (eff, eff - down, up - eff)

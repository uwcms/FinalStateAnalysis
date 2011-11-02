import math
from data import get_th1

print "Checking QCD template extraction"

def quad(*xs):
    return math.sqrt(sum(x*x for x in xs))

def get_ratio(sample, region, quiet=False):
    os_th1 = get_th1(sample, region.replace('Pass', 'PassOS'), 'AbsTauEta')
    ss_th1 = get_th1(sample, region.replace('Pass', 'PassSS'), 'AbsTauEta')
    os = os_th1.Integral()
    ss = ss_th1.Integral()

    os_error = math.sqrt(os_th1.GetEntries())/os_th1.GetEntries()
    ss_error = math.sqrt(ss_th1.GetEntries())/ss_th1.GetEntries()

    total_err = quad(os_error + ss_error)

    if not quiet:
        print "OS/SS in sample %s, region %s: %0.0f/%0.0f = %0.2f +- %0.2f (rel)" % (
        (sample, region, os, ss, os/ss, total_err))

    return os, ss, os_error, ss_error

def get_ratio_corrected(sample, region, correctFor):
    os, ss, os_error, ss_error = get_ratio(sample, region)

    os_abs_errors = [os*os_error]
    ss_abs_errors = [ss*ss_error]

    for corrSample in correctFor:
        corr_os, corr_ss, corr_os_err, corr_ss_err = get_ratio(
            corrSample, region, True)
        os -= corr_os
        ss -= corr_ss
        os_abs_errors.append(corr_os*corr_os_err)
        ss_abs_errors.append(corr_ss*corr_ss_err)

    os_abs_error = quad(*os_abs_errors)
    ss_abs_error = quad(*ss_abs_errors)

    os_rel_error = os_abs_error/os
    ss_rel_error = ss_abs_error/ss
    total_rel_error = quad(os_rel_error, ss_rel_error)

    print "Corrected OS/SS for %s - %s, %0.0f/%0.0f = %0.2f +- %0.2f (rel)" % (
        sample, region, os, ss, os/ss, total_rel_error)



get_ratio('qcd', 'qcdPass')
get_ratio('qcd', 'sigPass')

get_ratio('data', 'qcdPass')

get_ratio('wjets', 'wjetsPass')
get_ratio('wjets', 'sigPass')

get_ratio('data', 'wjetsPass')

get_ratio('zjets', 'qcdPass/realTau')
get_ratio('wjets', 'qcdPass')

get_ratio('zjets', 'sigPass/realTau')
get_ratio('zjets', 'sigPass/fakeTau')
get_ratio('ttbar', 'sigPass')

get_ratio_corrected('data', 'qcdPass', ['zjets', 'ttbar', 'wjets'])

def muon_charge_ass(sample, region):
    os_th1 = get_th1(sample, region.replace('Pass', 'PassOS'), 'MuonCharge')
    ss_th1 = get_th1(sample, region.replace('Pass', 'PassSS'), 'MuonCharge')
    print "  ".join("%s" % x for x in [
        sample, region, os_th1.GetEntries(), os_th1.GetMean(), ss_th1.GetEntries(), ss_th1.GetMean()])

muon_charge_ass('qcd', 'qcdPass')
muon_charge_ass('qcd', 'sigPass')
muon_charge_ass('wjets', 'wjetsPass')
muon_charge_ass('data', 'wjetsPass')
muon_charge_ass('wjets', 'sigPass')
muon_charge_ass('zjets', 'sigPass/realTau')
muon_charge_ass('zjets', 'sigPass/fakeTau')

# Check W extrapolation error

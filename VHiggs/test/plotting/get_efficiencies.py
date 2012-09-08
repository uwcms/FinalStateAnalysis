'''

Print out signal efficiencies.

'''

import logging
import math
from rootpy import io
from uncertainties import ufloat
import sys
import ROOT

ROOT.gSystem.AddIncludePath('-IHCSaW/Higgs_CS_and_Width/include')
ROOT.gROOT.ProcessLine('.L HCSaW/Higgs_CS_and_Width/src/HiggsCSandWidth.cc++')

results_file = io.open('vhtt_shapes.root')

logging.basicConfig(stream=sys.stderr,level=logging.INFO)
log = logging.getLogger("my_efficiencies")
log.setLevel(logging.DEBUG)

from get_stat_errors import get_stat_error

def get_vhtt_yield(mass):
    log.warning("Get VHTT yield %s", mass)
    mmt_yield = results_file.Get('mmt_mumu_final_count/VH%i' % mass).Integral()
    emt_yield = results_file.Get('emt_emu_final_count/VH%i' % mass).Integral()

    _, (mmt_passed, mmt_total) = get_stat_error('VH%i' % mass, mmt_yield)
    _, (emt_passed, emt_total) = get_stat_error('VH%i' % mass, emt_yield)

    assert(mmt_total == emt_total)

    mmt_passed = ufloat( (mmt_passed, math.sqrt(mmt_passed) ))
    emt_passed = ufloat( (emt_passed, math.sqrt(emt_passed) ))
    total = ufloat( (mmt_total, math.sqrt(mmt_total) ))

    all_passed = mmt_passed + emt_passed

    log.warning("total %s", total)
    log.warning("all %s", all_passed)

    #multply by fraction of ZH_WH_ttH that is WH
    wh_xsec = ROOT.HiggsCSandWidth().HiggsCS(3, mass, 7)
    zh_xsec = ROOT.HiggsCSandWidth().HiggsCS(4, mass, 7)
    tth_xsec = ROOT.HiggsCSandWidth().HiggsCS(5, mass, 7)

    wh_fraction = wh_xsec/(wh_xsec + zh_xsec + tth_xsec)

    log.warning("wh_frac %s", wh_fraction)

    br_bonus = 1.0/(0.1075+0.1057+0.1125)

    log.warning("br_bonus %s", br_bonus)

    return 100*br_bonus*(all_passed/total)/wh_fraction

def get_vhww_yield(mass):
    mmt_yield = results_file.Get('mmt_mumu_final_count/VH%iWW' % mass).Integral()
    emt_yield = results_file.Get('emt_emu_final_count/VH%iWW' % mass).Integral()

    _, (mmt_passed, mmt_total) = get_stat_error('VH%iWW' % mass, mmt_yield)
    _, (emt_passed, emt_total) = get_stat_error('VH%iWW' % mass, emt_yield)

    assert(mmt_total == emt_total)

    mmt_passed = ufloat( (mmt_passed, math.sqrt(mmt_passed) ))
    emt_passed = ufloat( (emt_passed, math.sqrt(emt_passed) ))
    total = ufloat( (mmt_total, math.sqrt(mmt_total) ))

    all_passed = mmt_passed + emt_passed

    return 100*all_passed/total

guillelmo_data = '''
110   0.0798+/-0.0014  0.0344+/-0.0078
115   0.0925+/-0.0014  0.0478+/-0.0085
120   0.1046+/-0.0015  0.0504+/-0.0027
125   0.1173+/-0.0016  0.0442+/-0.0079
130   0.1285+/-0.0017  0.0568+/-0.0069
135   0.1348+/-0.0018  0.0415+/-0.0078
140   0.1457+/-0.0017  0.0525+/-0.0082
150   0.1619+/-0.0019  0.0637+/-0.0071
160   0.1922+/-0.0021  0.0592+/-0.0096
170   0.1866+/-0.0129  0.0000+/-0.0000
180   0.1738+/-0.0123  0.0000+/-0.0000
190   0.1611+/-0.0119  0.0000+/-0.0000
200   0.1429+/-0.0113  0.0000+/-0.0000
'''

zh_data = '''
110 0.149+-0.008 0.0+-0
120 0.153+-0.004 0.017+-0.003
130 0.173+-0.009 0.024+-0.003
140 0.178+-0.009 0.025+-0.004
150 0.179+-0.009 0.029+-0.004
160 0.202+-0.010 0.040+-0.004
'''

def parse_data(data, mass):
    for line in data.split('\n'):
        line = line.strip()
        if not line:
            continue
        fields = line.split()
        the_mass = int(fields[0])
        if the_mass == mass:
            return 100*ufloat(fields[1]), 100*ufloat(fields[2])
    return None

def guillelmos_efficiencies(mass):
    return parse_data(guillelmo_data, mass)

def zh_efficiency(mass):
    wh_xsec = ROOT.HiggsCSandWidth().HiggsCS(3, mass, 7)
    zh_xsec = ROOT.HiggsCSandWidth().HiggsCS(4, mass, 7)
    tth_xsec = ROOT.HiggsCSandWidth().HiggsCS(5, mass, 7)

    zh_fraction = zh_xsec/(wh_xsec + zh_xsec + tth_xsec)

    br_ztoll = 1/(0.1096)

    return br_ztoll*parse_data(zh_data, mass)/zh_fraction

for mass in [110, 120, 130, 140, 150, 160]:
    ek_vhtt_eff = get_vhtt_yield(mass)
    ek_vhww_eff = get_vhww_yield(mass)

    gu_vhww_eff, gu_vhtt_eff = guillelmos_efficiencies(mass)

    zh_vhtt_eff, zh_vhww_eff = guillelmos_efficiencies(mass)

    def render_tex(number):
        return '$%0.2f\\%% \pm %0.2f\\%%$' % (number.nominal_value, number.std_dev())

    print ' & '.join([
        '%i GeV' % mass,
        render_tex(gu_vhtt_eff),
        render_tex(gu_vhww_eff),
        render_tex(ek_vhtt_eff),
        render_tex(ek_vhww_eff),
        render_tex(zh_vhtt_eff),
        render_tex(zh_vhww_eff),
    ]) + '\\\\'


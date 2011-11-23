'''

Check the PU dependency of the charge MisID rate for Michele.

'''

import data
import math

def get_charge(pass_ss, pass_os):
    mc_charge_eff = (pass_ss/(pass_os + pass_ss))
    mc_charge_eff_error = math.sqrt(pass_ss*(1 - mc_charge_eff))/(pass_os + pass_ss)
    return mc_charge_eff, mc_charge_eff_error

low_pass_os =  data.get_th1('zjets', 'sigPassOSlowPu/realTau', 'AbsTauEta').Integral()
low_pass_ss =  data.get_th1('zjets', 'sigPassSSlowPu/realTau', 'AbsTauEta').Integral()

high_pass_os =  data.get_th1('zjets', 'sigPassOShighPu/realTau', 'AbsTauEta').Integral()
high_pass_ss =  data.get_th1('zjets', 'sigPassSShighPu/realTau', 'AbsTauEta').Integral()

print "NVtx <= 7 MC charge mis-ID %0.3f +- %0.3f" % get_charge(low_pass_ss, low_pass_os)
print "NVtx >= 7 PU charge mis-ID %0.3f +- %0.3f" % get_charge(high_pass_ss, high_pass_os)

#!/usr/bin/env python

import pdb
from FinalStateAnalysis.StatTools.cardreader import read_card
from FinalStateAnalysis.MetaData.higgs_tables import cross_section, branching_ratio
from uncertainties import ufloat

lumi = 5000

w_to_any_lepton = 0.1075+0.1057+0.1125
z_to_any_lepton = 0.10096

def cube(x):
    return x*x*x

def square(x):
    return x*x

def get_exp_with_error(card, bin, process, my_systs):
    expected = card.exp[bin][process]
    total_relative_error = 1
    for syst in card.systs:
        error_object = my_systs[syst[0]]
        error = syst[4][bin][process]
        if error and error != 1:
            if isinstance(error, list): # up/down format
                error = error[1]
            percent_error = error - 1
            multiplier = 1 + percent_error*error_object
            total_relative_error = total_relative_error*multiplier
    return expected, (total_relative_error)

for mass in range(110, 165, 10):
    card = read_card("combo/comb_leptonic_%i.txt" % mass)

    wh_yield = lumi*cross_section('WH', mass, 7)
    zh_yield = lumi*cross_section('ZH', mass, 7)

    wh_www_yield = wh_yield * branching_ratio('WW', mass)

    wh_wtt_yield = wh_yield * branching_ratio('tautau', mass)

    zh_ztt_yield = zh_yield * branching_ratio('tautau', mass)

    zh_zww_yield = zh_yield * branching_ratio('WW', mass)



    wh_www_yield_leptons = wh_www_yield*cube(w_to_any_lepton)
    wh_wtt_yield_leptons = wh_wtt_yield*w_to_any_lepton
    zh_zww_yield_leptons = zh_zww_yield*square(w_to_any_lepton)*z_to_any_lepton
    zh_ztt_yield_leptons = zh_ztt_yield*z_to_any_lepton

    #print "Mass: ", mass
    #print "WH->WWW->leptons 5fb event yield: %0.2f" % wh_www_yield_leptons
    #print "WH->Wtt->leptons 5fb event yield: %0.2f" % wh_wtt_yield_leptons
    #print "ZH->ZWW->leptons 5fb event yield: %0.2f" % zh_zww_yield_leptons
    #print "ZH->Ztt->leptons 5fb event yield: %0.2f" % zh_ztt_yield_leptons

    # Build list of systematics
    all_systematics = {}
    for syst in card.systs:
        all_systematics[syst[0]] = ufloat((0, 1), syst[0])

    # Get WWW yield from card
    www_www_exp = get_exp_with_error(card, 'ch2', 'VHww', all_systematics)
    www_wtt_exp = get_exp_with_error(card, 'ch2', 'VHtt', all_systematics)

    wtt_wtt_mmt_exp = get_exp_with_error(
        card, 'ch1_ch1_mmt_mumu_final_MuTauMass', 'VH%i' % mass, all_systematics)
    wtt_wtt_emt_exp = get_exp_with_error(
        card, 'ch1_ch1_emt_emu_final_SubleadingMass', 'VH%i' % mass, all_systematics)
    wtt_wtt_exp = (
        (wtt_wtt_mmt_exp[0] + wtt_wtt_emt_exp[0]), # yields
        (wtt_wtt_mmt_exp[0]*wtt_wtt_mmt_exp[1] + wtt_wtt_emt_exp[0]*wtt_wtt_emt_exp[1]), # errors
    )

    wtt_www_mmt_exp = get_exp_with_error(
        card, 'ch1_ch1_mmt_mumu_final_MuTauMass', 'VH%iWW' % mass, all_systematics)
    wtt_www_emt_exp = get_exp_with_error(
        card, 'ch1_ch1_emt_emu_final_SubleadingMass', 'VH%iWW' % mass, all_systematics)
    wtt_www_exp = (
        wtt_www_mmt_exp[0] + wtt_www_emt_exp[0], # yields
        (wtt_www_mmt_exp[0]*wtt_www_mmt_exp[1] + wtt_www_emt_exp[0]*wtt_www_emt_exp[1]), # errors
    )

    zh_zww_exp = [0, 0]
    zh_ztt_exp = [0, 0]


    for zh_bin in ['ch3_ch1_mmem', 'ch3_ch1_mmet', 'ch3_ch1_mmmt', 'ch3_ch1_mmtt', 'ch3_ch1_eeem', 'ch3_ch1_eeet', 'ch3_ch1_eemt', 'ch3_ch1_eett']:
        zh_zww_exp_bin = get_exp_with_error(
            card, zh_bin, 'zh_ww%i' % mass, all_systematics)
        zh_zww_exp[0] += zh_zww_exp_bin[0]
        zh_zww_exp[1] += zh_zww_exp_bin[0]*zh_zww_exp_bin[1]
        zh_ztt_exp_bin = get_exp_with_error(
            card, zh_bin, 'zh_tt%i' % mass, all_systematics)
        zh_ztt_exp[0] += zh_ztt_exp_bin[0]
        zh_ztt_exp[1] += zh_ztt_exp_bin[0]*zh_ztt_exp_bin[1]


    template = ' & '.join([
        '{mass:0.0f} \\GeV',
        '{www_wtt:0.1f}%%\\pm{www_wtt_err:0.1f}%%',
        '{www_www:0.1f}%%\\pm{www_www_err:0.1f}%%',
        '{wtt_wtt:0.1f}%%\\pm{wtt_wtt_err:0.1f}%%',
        '{wtt_www:0.1f}%%\\pm{wtt_wtt_err:0.1f}%%',
        '{zh_ztt:0.1f}%%\\pm{zh_ztt_err:0.1f}%%',
        '{zh_zww:0.1f}%%\\pm{zh_zww_err:0.1f}%%',
    ]) + '\\\\\n'

    # Convert to percent
    # WWW is the only one where we don't convert the error to absolute already
    www_www = 100*www_www_exp[0]*www_www_exp[1]/wh_www_yield_leptons
    www_wtt = 100*www_wtt_exp[0]*www_wtt_exp[1]/wh_wtt_yield_leptons

    wtt_www = 100*wtt_www_exp[1]/wh_www_yield_leptons
    wtt_wtt = 100*wtt_wtt_exp[1]/wh_wtt_yield_leptons

    #print zh_ztt_yield_leptons, zh_zww_yield_leptons, zh_zww_exp, zh_ztt_exp

    zh_zww = 100*zh_zww_exp[1]/zh_zww_yield_leptons
    zh_ztt = 100*zh_ztt_exp[1]/zh_ztt_yield_leptons

    template_dict = {
        'mass' : mass,
        'www_wtt' : www_wtt.nominal_value,
        'www_wtt_err' : www_wtt.std_dev(),
        'www_www' : www_www.nominal_value,
        'www_www_err' : www_www.std_dev(),

        'wtt_wtt' : wtt_wtt.nominal_value,
        'wtt_wtt_err' : wtt_wtt.std_dev(),
        'wtt_www' : wtt_www.nominal_value,
        'wtt_www_err' : wtt_www.std_dev(),

        'zh_ztt' : zh_ztt.nominal_value,
        'zh_ztt_err' : zh_ztt.std_dev(),
        'zh_zww' : zh_zww.nominal_value,
        'zh_zww_err' : zh_zww.std_dev(),
    }
    print template.format(**template_dict)



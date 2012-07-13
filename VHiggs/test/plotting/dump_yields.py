import pprint
import uncertainties
import FinalStateAnalysis.StatTools.cardreader as cardreader

card = cardreader.read_card("combo/comb_leptonic_120.txt")
systs = cardreader.create_uncertainties(card)

analyses = {
    'TT' : {
        'channels' : [
            'ch1_ch1_' + x for x in [
                'mmt_mumu_final_MuTauMass',
                'emt_emu_final_SubleadingMass',
            ]
        ],
        'names' : {
            'tt_signal' : 'VH120',
            'ww_signal' : 'VH120WW',
            'WZ' : 'WZ',
            'ZZ' : 'ZZ',
            'fakes' : 'fakes',
        },
    },
    'WW' : {
        'channels' : [
            'ch2'
        ],
        'names' : {
            'tt_signal' : 'VHtt',
            'ww_signal' : 'VHww',
            'WZ' : 'WZ',
            'ZZ' : 'ZZ',
            'fakes' : 'Wjets',
        },
    },
    'ZH' : {
        'channels' : [
            'ch3_ch1_' + x for x in [
                'mmem',
                'mmet',
                'mmmt',
                'mmtt',
                'eeem',
                'eeet',
                'eemt',
                'eett',
            ]
        ],
        'names' : {
            'tt_signal' : 'zh_tt120',
            'ww_signal' : 'zh_ww120',
            'WZ' : None,
            'ZZ' : 'ZZ',
            'fakes' : 'Zjets',
        },
    }
}

#pprint.pprint(dc.systs)

mega_bkg = 0

for analysis, ana_info in analyses.iteritems():
    print '===================='
    print analysis
    print '===================='
    all_bkg = 0
    for process, real_process_name in ana_info['names'].iteritems():
        if real_process_name is None:
            continue
        print process
        process_total = 0.0
        for channel in ana_info['channels']:
            exp, total_err = cardreader.get_exp_with_error(
                card, channel, real_process_name, systs,
                exclude=['pdf_qqbar', 'QCDscale_VH'],
            )
            exp_with_err = exp*total_err
            #print channel, exp_with_err
            process_total += exp_with_err
        print "%0.2f +- %0.2f" % (process_total.nominal_value,
                                  process_total.std_dev())
        for (var, error) in process_total.error_components().items():
            break
            print "%s: %f" % (var.tag, error)

        if process in ['WZ', 'ZZ', 'fakes']:
            all_bkg += process_total
    print "all bkg: "
    print "%0.2f +- %0.2f" % (all_bkg.nominal_value,
                              all_bkg.std_dev())
    mega_bkg += all_bkg

print "mega bkg"
print "%0.2f +- %0.2f" % (mega_bkg.nominal_value,
                          mega_bkg.std_dev())

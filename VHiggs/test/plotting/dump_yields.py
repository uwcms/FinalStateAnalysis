from optparse import OptionParser
import pprint
import uncertainties
from HiggsAnalysis.CombinedLimit.DatacardParser import parseCard, addDatacardParserOptions


parser = OptionParser(usage="usage: %prog [options] datacard.txt -o output \nrun with --help to get list of options")

addDatacardParserOptions(parser)

(options, args) = parser.parse_args()

dc =  parseCard(open('trilepton_cards/combined_120.txt'), options)

analyses = {
    'TT' : {
        'channels' : [
            'TT_mmt_mumu_final_MuTauMass',
            'TT_emt_emu_final_SubleadingMass',
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
            'WWW'
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
            'ZH_mmem',
            'ZH_mmet',
            'ZH_mmmt',
            'ZH_mmtt',
            'ZH_eeem',
            'ZH_eeet',
            'ZH_eemt',
            'ZH_eett',
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

for analysis, ana_info in analyses.iteritems():
    print '===================='
    print analysis
    print '===================='
    for subchannel in ana_info['channels']:


    for process, real_process_name in ana_info['names'].iteritems():
        process_total = 0.0
        for channel in ana_info['channels']:
            process_total


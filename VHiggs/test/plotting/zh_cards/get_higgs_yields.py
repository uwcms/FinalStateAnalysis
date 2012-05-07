'''

Stupid script to get the Higgs TT and WW yields from the ZH data cards.

'''

from optparse import OptionParser
import pprint
import uncertainties
from HiggsAnalysis.CombinedLimit.DatacardParser import parseCard, addDatacardParserOptions


parser = OptionParser(usage="usage: %prog [options] datacard.txt -o output \nrun with --help to get list of options")

addDatacardParserOptions(parser)

(options, args) = parser.parse_args()

dc =  parseCard(open('hzz2l2t_120.txt'), options)

print dc.exp

total_htt = 0
total_hww = 0

for bin in dc.bins:
    total_htt += dc.exp[bin]['zh_tt120']
    total_hww += dc.exp[bin]['zh_ww120']

print total_htt, total_hww

from optparse import OptionParser
import pprint
import uncertainties
from HiggsAnalysis.CombinedLimit.DatacardParser import parseCard, addDatacardParserOptions


parser = OptionParser(usage="usage: %prog [options] datacard.txt -o output \nrun with --help to get list of options")

addDatacardParserOptions(parser)

(options, args) = parser.parse_args()

dc =  parseCard(open('combo/leptons_120.txt'), options)

def filter_dict(input):
    output = {}
    for k, v in input.iteritems():
        if v:
            output[k] = v
    return output

for syst in dc.systs:
    name, _, _, _, channel_dict = syst

    relevant_channels = [ (k, filter_dict(v)) for k, v in channel_dict.iteritems()
                         if any(v.values()) ]

    print "%s: %s" % (name, relevant_channels)

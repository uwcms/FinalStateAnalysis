'''

Reads a .txt file and returns the output from

HiggsAnalysis.CombinedLimit.DatacardParser

This is just a convenient wrapper with less option wrangling.

'''

from optparse import OptionParser
from HiggsAnalysis.CombinedLimit.DatacardParser import parseCard

# The DatacardParser takes some wacky arguments
_parser = OptionParser()
_parser.add_option("-s", "--stat",   dest="stat",          default=False, action="store_true")  # ignore systematic uncertainties to consider statistical uncertainties only
_parser.add_option("-S", "--force-shape", dest="shape",    default=True, action="store_true")  # ignore systematic uncertainties to consider statistical uncertainties only
_parser.add_option("-a", "--asimov", dest="asimov",  default=False, action="store_true")
(_options, _args) = _parser.parse_args([])
_options.bin = True # fake that is a binary output, so that we parse shape lines

def read_card(filename):
    file = open(filename, 'r')
    datacard = parseCard(file, _options)
    return datacard

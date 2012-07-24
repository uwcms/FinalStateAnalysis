'''

Reads a .txt file and returns the output from

HiggsAnalysis.CombinedLimit.DatacardParser

This is just a convenient wrapper with less option wrangling.

'''

from optparse import OptionParser
from HiggsAnalysis.CombinedLimit.DatacardParser import \
        parseCard, addDatacardParserOptions
from uncertainties import ufloat

# The DatacardParser takes some wacky arguments
_parser = OptionParser()
addDatacardParserOptions(_parser)
(_options, _args) = _parser.parse_args([])
_options.bin = True # fake that is a binary output, so that we parse shape lines

def read_card(filename):
    file = open(filename, 'r')
    datacard = parseCard(file, _options)
    return datacard

def create_uncertainties(card):
    ''' Create a dictionary of named systematics in [card]

    Systematics are centered at zero with sigma=1, using the uncertainties
    package.

    '''
    all_systematics = {}
    for syst in card.systs:
        all_systematics[syst[0]] = ufloat((0, 1), syst[0])
    return all_systematics

def get_exp_with_error(card, bin, process, systematics, exclude=None):
    ''' Get the expected value for a process, with uncertainty.

    The uncertainy is created out of the systematics dictionary
    that can be created with create_uncertainties(card).
    This allows you to correctly add up the expected values.
    '''
    expected = card.exp[bin][process]
    total_relative_error = 1
    for syst in card.systs:
        if exclude and syst[0] in exclude:
            continue
        error_object = systematics[syst[0]]
        error = syst[4][bin][process]
        if error and error != 1:
            if isinstance(error, list): # up/down format
                error = error[1]
            percent_error = error - 1
            multiplier = 1 + percent_error*error_object
            total_relative_error = total_relative_error*multiplier
    return expected, (total_relative_error)

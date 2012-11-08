'''

A library for determining significant figures
=============================================

From: https://twiki.cern.ch/twiki/bin/view/CMS/Internal/PubGuidelines

---+++ Significant figures for measurements and uncertainties

   * In CMS papers, the standard is to use at most two significant figures for all quoted uncertainties, unless only one significant figure is appropriate.

   * The precision quoted for the uncertainty should match the precision quoted for the central value associated with it.

Examples:

   * 27.4 &#177; 0.1 (stat.) &#177; 2.1 (syst.)  - the measurement and the statistical uncertainty are given to only one digit after the decimal point to match the precision of the systematic uncertainty.

   * 27.40 &#177; 0.14 (stat.) &#177; 0.85 (syst.) - now the measurement and the statistical uncertainty are given to two digits after the decimal point to match the precision of the systematic uncertainty.

   * 27.4 &#177; 1.3 (stat.) &#177; 0.2 (syst.) - the systematic uncertainty is given with only 1 significant figure, to match the precision of the statistical uncertainty.

If an uncertainty is so small compared to the other uncertainties so that this guideline can't be followed, don't quote the value of that uncertainty. Just say it is negligible compared to the other
uncertainties.  For example, if the statistical uncertainty on a measurement is &#177;0.001 and the systematic uncertainty is 2.2, we would quote the result as

   * 27.4  &#177; 2.2 (syst.), with a negligible statistical uncertainty

Notice our convention for labeling the statistical and systematic uncertainties: "(stat.)" and "(syst.)", with a period at the end of each abbreviation and a space before and after the parentheses.


Author: Evan K. Friis

'''

import math

def find_nth_sig_fig(x, n, min_sig_fig=-999):
    ''' Get the decimal place of the nth significant figure

    If n is less than min_sig_fig, only give one significant figure.

    >>> find_nth_sig_fig(0.52, 2)
    -2

    Specify a minimum sig fig.

    >>> find_nth_sig_fig(0.52, 2, -1)
    -1

    At least one sig. fig. is always given.

    >>> find_nth_sig_fig(0.0052, 2, -1)
    -3

    >>> find_nth_sig_fig(152, 2)
    1
    >>> find_nth_sig_fig(152, 1)
    2
    >>> find_nth_sig_fig(1, 2)
    -1
    '''

    log10 = math.log10(x)
    sigfig = int(math.floor(log10) - (n-1))
    # Only give 1 sigfig if below threshold
    if sigfig < min_sig_fig:
        sigfig += (n-1)
    return sigfig

def sigfigs(x, err, n_error=2, min_sig_fig=-999):
    ''' Round x and err to their appropriate representations.

    The n_error parameter controls how many significant figures of the error
    are relevant.

    Returns a pair of strings.

    >>> sigfigs(100, 0.5, 1)
    ('100.0', '0.5')
    >>> sigfigs(0.067, 0.1, 1)
    ('0.1', '0.1')
    >>> sigfigs(0.067, 0.0264, 2)
    ('0.067', '0.026')

    Provided a minimum sigfig.  Values lower than this will be rounded to only
    one signficant figure.

    >>> sigfigs(0.067, 0.0264, 2, -1)
    ('0.07', '0.03')

    >>> sigfigs(0.067, 0.0267, 2)
    ('0.067', '0.027')

    '''
    power = find_nth_sig_fig(err, n_error, min_sig_fig)
    x = round(x, -power)
    err = round(err, -power)

    def str_format(x):
        if power >= 0:
            # Use integer formating
            return "%i" % x
        # Use float formatting
        return ("%0." + str(abs(power)) + "f") % x

    return str_format(x), str_format(err)


if __name__ == "__main__":
    import doctest; doctest.testmod()

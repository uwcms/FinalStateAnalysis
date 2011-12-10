'''

Given a file, tree path, and a set of cuts, figure out:

    1) which cuts fail
    2) which cuts fail when all other cuts pass

To be used for cross checks.

Author: Evan K. Friis

'''

import collections

CutEffect = collections.namedtuple(
    'CutEffect', ['all', 'passed', 'passed_all_but'])

def get_cut_effect(cuts, cut_index, tree):
    '''
    Returns a tuple given the total number of entries, the number of entries
    which pass all cuts but this one, and the number of entries which pass the
    cut at cut_index.
    '''
    n_pass_this_cut = tree.GetEntries(cuts[cut_index])
    n_pass_all_cuts = tree.GetEntries(' && '.join(cuts))
    cut_copy = cuts[:]
    print cut_copy
    cut_copy.remove(cuts[cut_index])
    print cut_copy
    n_pass_all_cuts_but_this = tree.GetEntries(' && '.join(cut_copy))
    n_all = tree.GetEntries()

    return CutEffect(n_all, n_pass_this_cut, n_pass_all_cuts_but_this)

def get_cut_effects(cuts, tree, extras=None):
    '''
    Return a dictionary giving the effect of each cut in [cuts] on [tree].

    Output:
        {
            'CUT' : (n_all, n_pass_all, n_pass_CUT, n_pass_all_but_CUT)
        }
    '''
    output = {}
    for icut, cut, in enumerate(cuts):
        to_pass = cuts[:]
        if extras:
            to_pass += extras
        output[cut] = get_cut_effect(to_pass, icut, tree)
    return output

'''

Tools for messing about with lumis and JSON files

Author: Evan K. Friis, UW

'''

def group_by_run(sorted_run_lumis):
    '''
    Generate a list of lists run-lumi tuples, grouped by run
    Example:
    >>> run_lumis = [(100, 1), (100, 2), (150, 1), (150, 2), (150, 8)]
    >>> list(group_by_run(run_lumis))
    [(100, [1, 2]), (150, [1, 2, 8])]

    '''
    current_run = None
    output = []
    for run, lumi in sorted_run_lumis:
        if current_run is None or run == current_run:
            output.append(lumi)
        else:
            yield (current_run, output)
            output = [lumi]
        current_run = run
    yield (current_run, output)

def collapse_ranges_in_list(xs):
    '''
    Generate a list of contiguous ranges in a list of numbers.
    Example:
    >>> list(collapse_ranges_in_list([1, 2, 3, 5, 8, 9, 10]))
    [[1, 3], [5, 5], [8, 10]]
    '''
    output = []
    for x in xs:
        if not output:
            # Starting new range
            output = [x, x]
        elif x == output[1]+1:
            output[1] = x
        else:
            yield output
            output = [x, x]
    yield output


def json_summary(run_lumi_set):
    '''
    Compute a crab -report like json summary for a set of runs and lumis.
    Example:
    >>> run_lumis = [(100, 2), (100, 1), (150, 1), (150, 2), (150, 8)]
    >>> # Disable indentation
    >>> json_summary(run_lumis)
    {'150': [[1, 2], [8, 8]], '100': [[1, 2]]}
    '''
    run_lumis = sorted(run_lumi_set)
    output = {}
    if not run_lumis:
        return output
    for run, lumis_in_run in group_by_run(run_lumis):
        output[str(run)] = list(collapse_ranges_in_list(lumis_in_run))
    return output

if __name__ == "__main__":
    import doctest; doctest.testmod()

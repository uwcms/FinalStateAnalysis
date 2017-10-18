'''

CFG Cleaner
===========

Clean cruft out of CMS configuration files.

Author: Evan K. Friis, UW Madison

Removing unused modules
-----------------------

Getting all EDProducers/Analzers attached to the process but not in a
cms.Path.

>>> process = cms.Process('TEST')
>>> process.isRun = cms.EDAnalyzer("AnAnalzyer")
>>> process.p = cms.Path(process.isRun)
>>> process.neverRun = cms.EDAnalyzer("AnotherAnalyzer")

Get a list of unrun modules

>>> get_unrun_modules(process)
set(['neverRun'])

Remove all unrun modules

>>> clean_unrun_modules(process) # returns modules killed
set(['neverRun'])
>>> hasattr(process, 'neverRun')
False

Getting all modules *used* in the Path
--------------------------------------

>>> process = cms.Process('TEST')
>>> process.first = cms.EDProducer(
...     "Producer",
...     src = cms.InputTag('src1'),
... )
>>> process.second = cms.EDProducer(
...     "Producer",
...     src = cms.InputTag('first'),
... )
>>> process.notRun = cms.EDProducer("NotRun", src = cms.InputTag('notused'))
>>> process.p = cms.Path(process.first*process.second)
>>> get_all_used_modules(process)
set(['src1', 'first'])

Getting all modules, run, but never used
----------------------------------------

process.second is run, but nothing uses it's output as input

>>> run_but_unused(process)
set(['second'])

Killing the cruft
-----------------

Get rid of unneeded modules.

>>> process = cms.Process('TEST')

C depends on B depends on A.

>>> process.a = cms.EDProducer('A', src = cms.InputTag('a_reco'))
>>> process.b = cms.EDProducer('B', src = cms.InputTag('a'))
>>> process.c = cms.EDProducer('C', src = cms.InputTag('b'))

F depends on E depends on D

>>> process.d = cms.EDProducer('D', src = cms.InputTag('a_reco'))
>>> process.e = cms.EDProducer('E', src = cms.InputTag('d'))
>>> process.f = cms.EDProducer('F', src = cms.InputTag('e'))

Define the Path

>>> process.p = cms.Path(
...     process.a*process.b*process.c*process.d*process.e*process.f)

Define our output commands.  We keep C, so the C->B->A chain is kept.  D,E,F
are not kept, so the whole chain can be deleted.

>>> output_commands = ['*_c_*_*']
>>> kill_unused(process, output_commands)
set(['e', 'd', 'f'])


Get modules which match an output command
-----------------------------------------

Takes as input an iterable of module names, and a list of output commands.
Returns a set of matching modules.

>>> output_commands = ['drop *', '*_second_*_*']
>>> filter_by_output_command(['second', 'first'], output_commands)
set(['second'])
>>> output_commands = ['keep *', '*_second_*_*']
>>> filter_by_output_command(['second', 'first'], output_commands)
set(['second', 'first'])

Internal Utilities
==================

Extracting InputTags
--------------------
>>> process.module = cms.EDAnalyzer(
...     'AnAnalyzer',
...     src = cms.InputTag('a'),
...     extras = cms.InputTag('b'),
...     subpset = cms.PSet(subsrc = cms.InputTag('c')),
...     subvpset = cms.VPSet(cms.PSet(subsrc23 = cms.VInputTag('d', 'e')))
... )
>>> result = get_all_input_tags(process.module)
>>> result == set("abcde")
True


'''

import FWCore.ParameterSet.Config as cms
import fnmatch
import logging
import itertools

log = logging.getLogger("cfgcleaner")


def get_run_modules(process):
    ''' Get all modules that are in a Path.

    Returns a set of strings
    '''
    all_modules_in_a_path = set([])
    for pathname in itertools.chain(process.paths, process.endpaths):
        path = getattr(process, pathname)
        if None in path.moduleNames():
            import pdb
            pdb.set_trace()
            print "None in path", pathname
            print path.moduleNames()
        all_modules_in_a_path |= path.moduleNames()
    return all_modules_in_a_path


def get_unrun_modules(process):
    ''' Get all modules names not attached to a Path

    Returns a set of strings.
    '''

    all_modules_in_a_path = get_run_modules(process)
    # Get list of all modules
    all_modules = set(process.analyzers.keys()
                      + process.producers.keys()
                      + process.filters.keys())
    return all_modules - all_modules_in_a_path


def clean_unrun_modules(process):
    ''' Get the unrun modules and delete them from the process

    Modifies the process, returning a set of the killed modules.
    '''
    to_kill = get_unrun_modules(process)
    killed = set([])
    for module in to_kill:
        killed.add(module)
        delattr(process, module)
    return killed


def get_all_input_tags(module):
    ''' Parses a module and extracts all InputTags inside.

    Returns a set of module names.
    Based on code from PatAlgos/helpers.py

    '''
    input_tags = set([])
    is_producer = isinstance(module, cms.EDProducer)
    if is_producer and module.type_() == "CandViewShallowCloneCombiner":
        input_tags |= set([x for x in module.decay.value().split()])

    for name in module.parameters_().keys():
        value = getattr(module, name)
        type = value.pythonTypeName()
        if type.endswith('.PSet'):
            # Recurse
            input_tags = input_tags | get_all_input_tags(value)
        elif type.endswith('.VPSet'):
            # Loop and recurse
            for subpset in value:
                input_tags = input_tags | get_all_input_tags(subpset)
        elif type.endswith('.VInputTag'):
            for inputtag in value:
                # Can be defined as a list of strings
                if not isinstance(inputtag, cms.InputTag):
                    input_tags.add(cms.InputTag(inputtag).moduleLabel)
                else:
                    input_tags.add(inputtag.moduleLabel)
        elif type.endswith('.InputTag'):
            input_tags.add(value.moduleLabel)
    return input_tags


def get_all_used_modules(process):
    ''' Find modules appearing in an InputTag in the path or are an EDFilter'''
    used_input_tags = set([])
    for module_name in get_run_modules(process):
        module = getattr(process, module_name)
        is_filter = isinstance(module, cms.EDFilter)
        if is_filter or isinstance(module, cms.OutputModule):
            used_input_tags.add(module_name)
        used_input_tags |= get_all_input_tags(module)
    return set([x for x in used_input_tags])


def run_but_unused(process):
    ''' Find all modules that are run but not used.

    "Not used" means not appearing in an InputTag of another
    module that is ran in this process.
    '''
    run_modules = get_run_modules(process)
    used_input_tags = set([])
    # Keep track of all InputTags used in this process
    for module_name in run_modules:
        module = getattr(process, module_name)
        # If it is a EDFilter, it is always used, since it can affect the Path
        is_filter = isinstance(module, cms.EDFilter)
        if is_filter or isinstance(module, cms.OutputModule):
            used_input_tags.add(module_name)
        used_input_tags |= get_all_input_tags(module)
    return run_modules - used_input_tags


def filter_by_output_command(modules, output_commands):
    matching_modules = set([])
    warned = set([])
    for module in modules:
        is_kept = False
        for command in output_commands:
            if command == 'keep *':
                is_kept = True
                break
            elif command == 'drop *':
                continue
            elif command.split('_')[0] != '*' and command.split('_')[1] == '*':
                if command not in warned:
                    log.info("Warning, I can't interperet:", command,
                             "I might drop your product!")
                    warned.add(command)
                continue
            elif fnmatch.fnmatchcase(module, command.split('_')[1]):
                is_kept = True
                break
        if is_kept:
            matching_modules.add(module)
    return matching_modules


def kill_unused(process, output_commands):
    ''' Delete run but unused modules from all Paths and the process.

    Returns a set of modules killed.
    '''
    # We have to iterate on this - we might kill some unused modules, and after
    # they are killed, previous modules in the chain are now no longer used.
    killed = set([])
    done = False
    i = 0
    while not done:
        i += 1
        suspects = run_but_unused(process)
        # Check if they are kept
        kept_suspects = filter_by_output_command(suspects, output_commands)
        guilty_suspects = suspects - kept_suspects
        log.info("Discovered %i bad guys to clean in iteration %i",
                 len(guilty_suspects), i)
        # No more guilty guys.  We are done.
        if not guilty_suspects:
            done = True
        for guilty in guilty_suspects:
            module = getattr(process, guilty)
            # Delete from all paths
            for pathname in itertools.chain(process.paths, process.endpaths):
                path = getattr(process, pathname)
                path.remove(module)
            #delattr(process, guilty)
            killed.add(guilty)
    return killed


def clean_cruft(process, output_commands):
    ''' Clean the cruft in a CFG

    Deletes all un-run modules.
    Deletes all modules that are run, but never used, and not kept.

    Returns a tuple of deleted (set(un-run), set(un-used)) modules.
    '''
    # This is always complete on the first run.
    #unrun = clean_unrun_modules(process)
    # HACK - don't clena this, it can leave process.Nones in sequences
    unrun = set([])
    unused = kill_unused(process, output_commands)
    killed = set([])
    #killed = clean_unrun_modules(process)
    #unrun = None
    #unused = run_but_unused(process)
    return unrun, unused, killed

if __name__ == "__main__":
    import doctest
    doctest.testmod()

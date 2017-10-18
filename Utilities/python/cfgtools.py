'''

Tools for manipulating CMSSW python configuration objects
=========================================================

Author: Evan K. Friis UW Madison

Chaining Modules in a Sequence
------------------------------

You can use [chain_sequence] to connect the inputs and outputs of objects in a
sequence.  Per default, the output of each module is connected to the next
modules ['src'] input.  You can specify additional PSet keys which should
be considered as a <src_name> as well.

>>> import FWCore.ParameterSet.Config as cms
>>> proc = cms.Process("TEST")
>>> proc.pA = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.pB = cms.EDProducer("AProducer", inputSrc = cms.InputTag("fixme"))
>>> proc.pC = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.pD = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.subseq = cms.Sequence(proc.pB + proc.pC)
>>> proc.seq = cms.Sequence(proc.pA + proc.subseq + proc.pD)
>>> end_result = chain_sequence(proc.seq, "start", ("src", "inputSrc"))
>>> proc.pA.src
cms.InputTag("start")
>>> proc.pB.inputSrc
cms.InputTag("pA")
>>> proc.pC.src
cms.InputTag("pB")
>>> proc.pD.src
cms.InputTag("pC")
>>> end_result
cms.InputTag("pD")

You can disable a module from being chained by adding noSeqChain = cms.bool(True)
to the parameters.

>>> proc.pA = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.pB = cms.EDProducer("AProducer", src = cms.InputTag("fixme"),
...                          noSeqChain= cms.bool(True))
>>> proc.pC = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.seq = cms.Sequence(proc.pA + proc.pB + proc.pC)
>>> end_result = chain_sequence(proc.seq, "start")
>>> proc.pB.src
cms.InputTag("fixme")
>>> proc.pC.src
cms.InputTag("pA")
>>> end_result
cms.InputTag("pC")

Using format strings in cfg objects
-----------------------------------

Mimic the API of string.format in CMSSW cfg objects.  The object is changed in
place.

Based on code from helpers.py of PatAlgos

>>> filter = cms.EDFilter(
...     "MyFilter",
...     src = cms.InputTag("{thesrc}"),
...     isNotTouched = cms.string("JustAString"),
...     psetsAreDescendedInto = cms.PSet(
...         toFormat = cms.string('{toFormat}'),
...         vectorsAreTo = cms.vstring('{v1}', '{v2}')
...     ),
...     vpsetsTo = cms.VPSet(
...        cms.PSet(
...             subpset = cms.string('{toFormat}')
...        )
...     )
... )
>>> to_replace = {
...     'thesrc' : 'newsrc',
...     'toFormat' : 'inAPSet',
...     'v1' : 'a',
...     'v2' : 'b',
... }
>>> format(filter, **to_replace)
>>> filter.src
cms.InputTag("newsrc")
>>> filter.vpsetsTo[0].subpset
cms.string('inAPSet')
>>> filter.psetsAreDescendedInto.vectorsAreTo[1]
'b'

Mimicking string 'replace' method
---------------------------------

Mimic the API of string.replace.  Used to build format strings by the
Selectors.templates modules.  The parameter names can be replaced as well.

>>> filter = cms.PSet(
...   objectPt = cms.string('{object}.pt'),
...   objectEta = cms.string('{object}.eta'),
...   objectSubInfo = cms.PSet(
...      objectCharge = cms.vstring('{object}.charge1', '{object}.charge2')
...   ),
... )
>>> newfilter = replace(filter, object='muon')
>>> newfilter.muonPt
cms.string('{muon}.pt')
>>> newfilter.muonEta
cms.string('{muon}.eta')
>>> newfilter.muonSubInfo.muonCharge[0],newfilter.muonSubInfo.muonCharge[1]
('{muon}.charge1', '{muon}.charge2')
>>> hasattr(newfilter, 'objectPt')
False

The original PSet isn't modified.

>>> hasattr(filter, 'muonPt')
False
>>> filter.objectPt
cms.string('{object}.pt')
>>> filter.objectSubInfo.objectCharge[0],filter.objectSubInfo.objectCharge[1]
('{object}.charge1', '{object}.charge2')

'''

import FWCore.ParameterSet.Config as cms
# Need regular expressions for removal of non-miniAOD branches
import re

class SequenceChainer(object):
    def __init__(self, input_src, src_names):
        self.current_src = input_src
        self.src_names = src_names
    def enter(self, visitee):
        skip = hasattr(visitee, 'noSeqChain') and visitee.noSeqChain
        if skip:
            return
        for src_name in self.src_names:
            if hasattr(visitee, src_name):
                setattr(visitee, src_name, cms.InputTag(self.current_src))
                self.current_src = visitee.label()
                break
    def leave(self, visitee):
        pass

def chain_sequence(sequence, input_src, src_names=('src',)):
    chainer = SequenceChainer(input_src, src_names)
    sequence.visit(chainer)
    return cms.InputTag(chainer.current_src)

def format(cfg_object, **replacements):
    if isinstance(cfg_object, cms._Parameterizable):
        # If this is a PSet like type (PSet, EDFilter, etc), recurse down
        for par in cfg_object.parameters_().keys():
            # Do this so we get objects, not copies
            value = getattr(cfg_object, par)
            # Recurse down
            format(value, **replacements)
    # Otherwise check if we need to update this
    if isinstance(cfg_object, cms.string):
        cfg_object.setValue(cfg_object.value().format(**replacements))
    elif isinstance(cfg_object, cms.vstring):
        formatted = []
        for x in cfg_object:
            formatted.append(x.format(**replacements))
        cfg_object.setValue(formatted)
    elif isinstance(cfg_object, cms.InputTag):
        cfg_object.setValue(cfg_object.value().format(**replacements))
    elif isinstance(cfg_object, cms.VPSet):
        for subpset in cfg_object:
            format(subpset, **replacements)

def _descending_length(items):
    ''' Return a sequence sorted so the longest elements are at the front
    >>> list(_descending_length(['long', 'longest', 'longer']))
    ['longest', 'longer', 'long']
    '''
    for item in reversed(sorted(items, key=len)):
        yield item

def replace_str(string_obj, **replacements):
    ''' Do a bunch of replacements in the string.

    The replacements are done in order of descending length.

    >>> replace_str('long longer longest',
    ...             long='bong', longer='donger', longest='gongest')
    'bong donger gongest'
    '''

    output = string_obj
    # Sort the strings to replace by descending length
    for substr in _descending_length(replacements.keys()):
        output = output.replace(substr, replacements[substr])
    return output

def replace(cfg_object, **replacements):
    if isinstance(cfg_object, cms._Parameterizable):
        output = cfg_object.clone()
        # If this is a PSet like type (PSet, EDFilter, etc), recurse down
        for par in cfg_object.parameters_().keys():
            # Do this so we get objects, not copies
            value = getattr(cfg_object, par)
            # Recurse down
            new_value = replace(value, **replacements)
            new_name = replace_str(par, **replacements)

            setattr(output, new_name, new_value)
            # Check if the name changed - delete the old one.
            if new_name != par:
                delattr(output, par)

        return output
    # Otherwise check if we need to update this
    if isinstance(cfg_object, cms.string):
        new_str = replace_str(cfg_object.value(), **replacements)
        return cms.string(new_str)
    elif isinstance(cfg_object, cms.vstring):
        formatted = []
        for x in cfg_object:
            formatted.append(replace_str(x, **replacements))
        return cms.vstring(formatted)
    elif isinstance(cfg_object, cms.InputTag):
        formatted = replace_str(cfg_object.value(), **replacements)
        return cms.InputTag(formatted)
    elif isinstance(cfg_object, cms.VPSet):
        output = cms.VPSet()
        for subpset in cfg_object:
            output += replace(subpset, **replacements)
        return output

def remove(cfg_object, removals):
    ''' helper function for PSet.remove(*removals) '''
    if not isinstance(cfg_object, cms._Parameterizable):
        return cfg_object

    output = cfg_object.clone()

    for key in output.parameters_().keys():
        if removals.match(key):
            delattr(output, key)
            continue
        setattr(output, key, remove(getattr(output, key), removals))

    return output        


class PSet(cms.PSet):
    def __init__(self, *args, **kwargs):
        ''' Convenient version of PSet constructor

        Automatically deduces the correct type of the arguments.

        >>> mypset = PSet(
        ...   aString = 'willBeACmsString',
        ...   aCmsString = 'willStayACmsString',
        ...   boolsWork = True,
        ...   soDoFloats = 0.5,
        ...   andInts = 2,
        ... )
        >>> mypset.aString
        cms.string('willBeACmsString')
        >>> mypset.aCmsString
        cms.string('willStayACmsString')
        >>> mypset.boolsWork
        cms.bool(True)
        >>> mypset.soDoFloats
        cms.double(0.5)
        >>> mypset.andInts
        cms.int32(2)
        '''
        # Reduce boiler plate of input arguments
        for key in kwargs.keys():
            value = kwargs[key]
            if isinstance(value, str):
                kwargs[key] = cms.string(value)
            elif isinstance(value, float):
                kwargs[key] = cms.double(value)
            elif isinstance(value, bool):
                kwargs[key] = cms.bool(value)
            elif isinstance(value, int):
                kwargs[key] = cms.int32(value)

        super(PSet, self).__init__(*args, **kwargs)

    def clone(self):
        ''' Make a copy.

        >>> mytpset = PSet(
        ...     a = 'a', b = 'b'
        ... )
        >>> clone = mytpset.clone()

        The clone is still a PSet.

        >>> isinstance(clone, PSet)
        True
        >>> clone.a = 'a2'
        >>> mytpset.a, clone.a
        (cms.string('a'), cms.string('a2'))
        '''
        output = super(PSet, self).clone()
        output.__class__ = self.__class__
        return output

    def replace(self, **replacements):
        ''' Apply the replacements.  Returns a modified copy.

        >>> mytpset = PSet(
        ...     object = 'objectPt'
        ... )
        >>> replaced = mytpset.replace(object='muon')
        >>> replaced.muon
        cms.string('muonPt')
        '''
        return replace(self, **replacements)

    def format(self, **replacements):
        ''' Apply the formatting.  Returns a modified copy.

        >>> mytpset = PSet(
        ...     muonPt = '{muon}.pt'
        ... )
        >>> replaced = mytpset.format(muon='daughter(0)')
        >>> replaced.muonPt
        cms.string('daughter(0).pt')
        '''
        clone = self.clone()
        format(clone, **replacements)
        return clone
    
    def remove(self, removals):
        ''' 
        Remove item from PSet, return modified copy.

        Will move recursively down chains of PSets, but if a 
            PSet-in-a-PSet has a name in removals, the whole
            sub-PSet is removed

        removals should be a regular expression that catches all the items to be removed, 
            e.g. re.compile("(*MVAMet*)|([emtgj][1-9]?MtTo[Pp][fF]Met)"

        >>> mytpset = PSet(
        ...     foo = 'foo'
        ...     fob = 'fob'
        ...     bar = 'bar'
        ...     ebar = 'ebar'
        ...     tbar = 'tbar'
        ...     bbar = 'bbar'
        ... )
        >>> toremove = re.compile("(foo)|([emt]?bar)")
        >>> removed = mytpset.remove(toremove)
        >>> hasattr(removed, 'foo')
        False
        >>> hasattr(removed, 'fob')
        True
        >> hasattr(removed, 'bar')
        False
        >> hasattr(removed, 'ebar')
        False
        >> hasattr(removed, 'tbar')
        False
        >> hasattr(removed, 'bbar')
        True
        '''
        output = self.clone()
        for key in output.parameters_().keys():
            if removals.match(key):
                delattr(output, key)
                continue
            setattr(output, key, remove(getattr(output, key), removals))
        return output
        
class GetInfoVisotor(object):
    def __init__(self):
        self.info = []
    def enter(self, module):
        label = module.label() if module.hasLabel_() else ''
        kind  = module.type_() if hasattr(module,'type_') else type(module)
        self.info.append(
            ( label,
              kind
          )
        )
    def leave(self, module):
        pass

def get_cms_iterable_info(iterable):
    visitor = GetInfoVisotor()
    iterable.visit(visitor)
    return visitor.info

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
    doctest.testmod()

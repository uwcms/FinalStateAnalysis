'''

Tools for manipulating CMSSW python configuration objects
=========================================================

Author: Evan K. Friis UW Madison

Chaining Modules in a Sequence
------------------------------

You can use [chain_sequence] to connect the inputs and outputs of objects
in a sequence.  The output of each module is connected to the next modules
['src'] input.

>>> import FWCore.ParameterSet.Config as cms
>>> proc = cms.Process("TEST")
>>> proc.pA = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.pB = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.pC = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.pD = cms.EDProducer("AProducer", src = cms.InputTag("fixme"))
>>> proc.subseq = cms.Sequence(proc.pB + proc.pC)
>>> proc.seq = cms.Sequence(proc.pA + proc.subseq + proc.pD)
>>> end_result = chain_sequence(proc.seq, "start")
>>> proc.pA.src
cms.InputTag("start")
>>> proc.pB.src
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

'''

import FWCore.ParameterSet.Config as cms

class SequenceChainer(object):
    def __init__(self, input_src):
        self.current_src = input_src
    def enter(self, visitee):
        skip = hasattr(visitee, 'noSeqChain') and visitee.noSeqChain
        if hasattr(visitee, 'src') and not skip:
            visitee.src = cms.InputTag(self.current_src)
            self.current_src = visitee.label()
    def leave(self, visitee):
        pass

def chain_sequence(sequence, input_src):
    chainer = SequenceChainer(input_src)
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

if __name__ == "__main__":
    import doctest
    doctest.testmod()

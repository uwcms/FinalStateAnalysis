'''

Tools for manipulating cms.Sequence objects.

Author: Evan K. Friis UW Madison

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
'''

import FWCore.ParameterSet.Config as cms

class SequenceChainer(object):
    def __init__(self, input_src):
        self.current_src = input_src
    def enter(self, visitee):
        if hasattr(visitee, 'src'):
            visitee.src = cms.InputTag(self.current_src)
            self.current_src = visitee.label()
    def leave(self, visitee):
        pass

def chain_sequence(sequence, input_src):
    chainer = SequenceChainer(input_src)
    sequence.visit(chainer)
    return cms.InputTag(chainer.current_src)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

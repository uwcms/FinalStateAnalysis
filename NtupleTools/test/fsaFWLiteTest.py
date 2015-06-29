import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.AutoLibraryLoader.enable()

#cms python data types
import FWCore.ParameterSet.Config as cms

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

events = Events("file:ntuplize.root")

fs4Mu, fs4MuLabel = Handle("edm::OwnVector<PATFinalState,edm::ClonePolicy<PATFinalState> >"), "cleanedFinalStateMuMuMuMu"
gen, genLabel = Handle("std::vector<reco::GenParticle>"), "prunedGenParticles"


n4MuFS = 0
for iev, ev in enumerate(events):

    ev.getByLabel(fs4MuLabel, fs4Mu)
    ev.getByLabel(genLabel, gen)

    print "event %d:%d:%d: %d 4 mu final states:"%(ev.eventAuxiliary().run(),
                                                   ev.eventAuxiliary().luminosityBlock(),
                                                   ev.eventAuxiliary().event(),
                                                   len(fs4Mu.product()))
    for ifs, fs in enumerate(fs4Mu.product()):
        n4MuFS += 1
        print "    %d: 4l Mass: %.3f"%(ifs, fs.p4fsr("FSRCand").M())
        for i in range(4):
            print '        mu %d: charge %d, pt %.3f'%(i, fs.daughter(i).pdgId()/abs(fs.daughter(i).pdgId()), fs.daughter(i).pt())
        print "    # jets: %d"%len(fs.evt().jets())
    
    print "    Final state gen muons:"
    for g in gen.product():
        if abs(g.pdgId()) == 13 and g.status() == 1:
            print "        pt: %.3f  eta: %.3f  phi: %.3f"%(g.pt(), g.eta(), g.phi())

    if n4MuFS > 10:
        break

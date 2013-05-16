import FWCore.ParameterSet.Config as cms

def renew_jet_matching(process, sequence, obj, src, jetsrc):
    process.load("FinalStateAnalysis.PatTools.%s.pat%sEmbedJetInfo_cfi" % (obj, obj.capitalize()[:-1]))
    module = getattr(process, 'pat%sEmbedJetInfo' % obj.capitalize())
    module.src = src
    module.jetSrc = jetsrc
    sequence += module
    return module.label() 

def rerun_QGJetID(process, fs_daughter_inputs):
    process.load("FinalStateAnalysis.PatTools.jets.patJetQuarkGluonID_cfi")
    process.QGTagger.srcJets= fs_daughter_inputs['jets']
    process.patJetsQGID.src = fs_daughter_inputs['jets']
    fs_daughter_inputs['jets'] = 'patJetsQGID'
    process.renew_jet_matching = cms.Sequence()
    for obj in ['electrons', 'muons', 'taus']:
        fs_daughter_inputs[obj] = \
            renew_jet_matching(process,
                               process.renew_jet_matching,
                               obj,
                               fs_daughter_inputs[obj],
                               fs_daughter_inputs['jets']
                )
    process.rerun_QGJetID = cms.Path(process.embedQGJetID * process.renew_jet_matching)
    return process.rerun_QGJetID

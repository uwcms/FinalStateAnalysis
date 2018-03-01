# Embed IDs for taus
import FWCore.ParameterSet.Config as cms

def preTaus(process, tSrc, vSrc,**kwargs):

    postfix = kwargs.pop('postfix','')
    rerunMvaIDs = bool(kwargs.pop('rerunMvaIDs', 0))


    if rerunMvaIDs :
        from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
        process.load('RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi')
        from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import \
            patDiscriminationByIsolationMVArun2v1raw, patDiscriminationByIsolationMVArun2v1VLoose
	#from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import *

	tauIdDiscrMVA_trainings_run2_2017 = {
	  'tauIdMVAIsoDBoldDMwLT2017' : "tauIdMVAIsoDBoldDMwLT2017",
	  }
	tauIdDiscrMVA_WPs_run2_2017 = {
	  'tauIdMVAIsoDBoldDMwLT2017' : {
	    'Eff95' : "DBoldDMwLTEff95",
	    'Eff90' : "DBoldDMwLTEff90",
	    'Eff80' : "DBoldDMwLTEff80",
	    'Eff70' : "DBoldDMwLTEff70",
	    'Eff60' : "DBoldDMwLTEff60",
	    'Eff50' : "DBoldDMwLTEff50",
	    'Eff40' : "DBoldDMwLTEff40"
	    }
	  }
	tauIdDiscrMVA_2017_version = "v1"
	def loadMVA_WPs_run2_2017(process):     
           for training, gbrForestName in tauIdDiscrMVA_trainings_run2_2017.items():
        	 process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
        	    cms.PSet(
        	       record = cms.string('GBRWrapperRcd'),
        	       tag = cms.string("RecoTauTag_%s%s" % (gbrForestName, tauIdDiscrMVA_2017_version)),
        	       label = cms.untracked.string("RecoTauTag_%s%s" % (gbrForestName, tauIdDiscrMVA_2017_version))
        	    )
        	 )
        	 for WP in tauIdDiscrMVA_WPs_run2_2017[training].keys():
        	    process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
        	       cms.PSet(
        	          record = cms.string('PhysicsTGraphPayloadRcd'),
        	          tag = cms.string("RecoTauTag_%s%s_WP%s" % (gbrForestName, tauIdDiscrMVA_2017_version, WP)),
        	          label = cms.untracked.string("RecoTauTag_%s%s_WP%s" % (gbrForestName, tauIdDiscrMVA_2017_version, WP))
        	       )
        	    )

        	 process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
        	    cms.PSet(
        	       record = cms.string('PhysicsTFormulaPayloadRcd'),
        	       tag = cms.string("RecoTauTag_%s%s_mvaOutput_normalization" % (gbrForestName, tauIdDiscrMVA_2017_version)),
        	       label = cms.untracked.string("RecoTauTag_%s%s_mvaOutput_normalization" % (gbrForestName, tauIdDiscrMVA_2017_version))
        	    )
)
	loadMVA_WPs_run2_2017(process)

        process.rerunDiscriminationByIsolationMVArun2v1raw = patDiscriminationByIsolationMVArun2v1raw.clone(
           PATTauProducer = cms.InputTag(tSrc),
           Prediscriminants = noPrediscriminants,
           loadMVAfromDB = cms.bool(True),
           mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1"), # name of the training you want to use
           mvaOpt = cms.string("DBoldDMwLTwGJ"), # option you want to use for your training (i.e., which variables are used to compute the BDT score)
           requireDecayMode = cms.bool(True),
           verbosity = cms.int32(0)
        )
        
        process.rerunDiscriminationByIsolationMVArun2v1VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
           PATTauProducer = cms.InputTag(tSrc),    
           Prediscriminants = noPrediscriminants,
           toMultiplex = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw'),
           key = cms.InputTag('rerunDiscriminationByIsolationMVArun2v1raw:category'),
           loadMVAfromDB = cms.bool(True),
           mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_mvaOutput_normalization"), # normalization fo the training you want to use
           mapping = cms.VPSet(
              cms.PSet(
                 category = cms.uint32(0),
                 cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff90"), # this is the name of the working point you want to use
                 variable = cms.string("pt"),
              )
           )
        )
        
        # here we produce all the other working points for the training
        process.rerunDiscriminationByIsolationMVArun2v1Loose = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v1Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff80")
        process.rerunDiscriminationByIsolationMVArun2v1Medium = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v1Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff70")
        process.rerunDiscriminationByIsolationMVArun2v1Tight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v1Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff60")
        process.rerunDiscriminationByIsolationMVArun2v1VTight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v1VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff50")
        process.rerunDiscriminationByIsolationMVArun2v1VVTight = process.rerunDiscriminationByIsolationMVArun2v1VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v1VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v1_WPEff40")
        
        # this sequence has to be included in your cms.Path() before your analyzer which accesses the new variables is called.
        process.rerunMvaIsolation2SeqRun2 = cms.Path(
           process.rerunDiscriminationByIsolationMVArun2v1raw
           * process.rerunDiscriminationByIsolationMVArun2v1VLoose
           * process.rerunDiscriminationByIsolationMVArun2v1Loose
           * process.rerunDiscriminationByIsolationMVArun2v1Medium
           * process.rerunDiscriminationByIsolationMVArun2v1Tight
           * process.rerunDiscriminationByIsolationMVArun2v1VTight
           * process.rerunDiscriminationByIsolationMVArun2v1VVTight
        )
        process.schedule.append( process.rerunMvaIsolation2SeqRun2 )

        # embed rerun MVA IDs
        modName = 'miniTausEmbedRerunMVAIDs{0}'.format(postfix)
        mod = cms.EDProducer(
            "MiniAODTauRerunIDEmbedder",
            src = cms.InputTag(tSrc),
            idRaw = cms.InputTag("rerunDiscriminationByIsolationMVArun2v1raw"),
            idVLoose = cms.InputTag("rerunDiscriminationByIsolationMVArun2v1VLoose"),
            idLoose = cms.InputTag("rerunDiscriminationByIsolationMVArun2v1Loose"),
            idMedium = cms.InputTag("rerunDiscriminationByIsolationMVArun2v1Medium"),
            idTight = cms.InputTag("rerunDiscriminationByIsolationMVArun2v1Tight"),
            idVTight = cms.InputTag("rerunDiscriminationByIsolationMVArun2v1VTight"),
            idVVTight = cms.InputTag("rerunDiscriminationByIsolationMVArun2v1VVTight"),
        )
        tSrc = modName
        setattr(process,modName,mod)

        pathName = 'runMiniAODTauRerunMVAIDEmbedding{0}'.format(postfix)
        path = cms.Path(getattr(process,modName))
        setattr(process,pathName,path)
        process.schedule.append(getattr(process,pathName))



    modName = 'genembeddedTaus{0}'.format(postfix)
    mod=cms.EDProducer("PATTauGenInfoEmbedder",
          src=cms.InputTag(tSrc)
    )
    setattr(process,modName,mod)
    tSrc = modName
    modPath = 'embeddedTaus{0}'.format(postfix)
    setattr(process,modPath,cms.Path(getattr(process,modName)))
    
    process.schedule.append(getattr(process,modPath))

    # embed IP stuff
    modName = 'miniTausEmbedIp{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODTauIpEmbedder",
        src = cms.InputTag(tSrc),
        vtxSrc = cms.InputTag(vSrc),
    )
    tSrc = modName
    setattr(process,modName,mod)

    pathName = 'runMiniAODTauIpEmbedding{0}'.format(postfix)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))


    return tSrc

def postTaus(process, tSrc, jSrc,**kwargs):
    postfix = kwargs.pop('postfix','')
    modName = 'miniAODTauJetInfoEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODTauJetInfoEmbedder",
        src = cms.InputTag(tSrc),
        embedBtags = cms.bool(False),
        suffix = cms.string(''),
        jetSrc = cms.InputTag(jSrc),
        maxDeltaR = cms.double(0.5),
    )
    setattr(process,modName,mod)
    tSrc = modName
    modPath = 'TauJetInfoEmbedding{0}'.format(postfix)
    setattr(process,modPath,cms.Path(getattr(process,modName)))
    process.schedule.append(getattr(process,modPath))

    return tSrc


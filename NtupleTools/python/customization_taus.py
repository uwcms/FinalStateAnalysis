# Embed IDs for taus
import FWCore.ParameterSet.Config as cms
import re

def processDeepProducer(process, producer_name, tauIDSources, workingPoints_):
        for target,points in workingPoints_.iteritems():
            cuts = cms.PSet()
            setattr(tauIDSources, 'by{}VS{}raw'.format(producer_name[0].upper()+producer_name[1:], target),
                        cms.InputTag(producer_name, 'VS{}'.format(target)))
            for point,cut in points.iteritems():
                setattr(cuts, point, cms.string(str(cut)))

                setattr(tauIDSources, 'by{}{}VS{}'.format(point, producer_name[0].upper()+producer_name[1:], target),
                        cms.InputTag(producer_name, 'VS{}{}'.format(target, point)))
            setattr(getattr(process, producer_name), 'VS{}WP'.format(target), cuts)
	    #if "deep" in producer_name:
	    # 	raise RuntimeError('File "{}"'.format(tauIDSources))

def getDpfTauVersion(file_name):
        """returns the DNN version. File name should contain a version label with data takig year (2011-2, 2015-8) and \
           version number (vX), e.g. 2017v0, in general the following format: {year}v{version}"""
        version_search = re.search('201[125678]v([0-9]+)[\._]', file_name)
        if not version_search:
            raise RuntimeError('File "{}" has an invalid name pattern, should be in the format "{year}v{version}". \
                                Unable to extract version number.'.format(file_name))
        version = version_search.group(1)
	return int(version)

def getDeepTauVersion(file_name):
        """returns the DeepTau year, version, subversion. File name should contain a version label with data takig year \
        (2011-2, 2015-8), version number (vX) and subversion (pX), e.g. 2017v0p6, in general the following format: \
        {year}v{version}p{subversion}"""
        version_search = re.search('(201[125678])v([0-9]+)(p[0-9]+|)[\._]', file_name)
        if not version_search:
            raise RuntimeError('File "{}" has an invalid name pattern, should be in the format "{year}v{version}p{subversion}". \
                                Unable to extract version number.'.format(file_name))
        year = version_search.group(1)
        version = version_search.group(2)
        subversion = version_search.group(3)
        if len(subversion) > 0:
            subversion = subversion[1:]
        else:
            subversion = 0
        return int(year), int(version), int(subversion)


def preTaus(process, year, isEmbedded, tSrc, vSrc,**kwargs):

    postfix = kwargs.pop('postfix','')
    rerunMvaIDs = bool(kwargs.pop('rerunMvaIDs', 0))

    if rerunMvaIDs :
        from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
        process.load('RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi')
        from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import \
            patDiscriminationByIsolationMVArun2v1raw, patDiscriminationByIsolationMVArun2v1VLoose
        #from RecoTauTag.RecoTau.PATTauDiscriminationAgainstElectronMVA6_cfi import * #NEW

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
        tauIdDiscrMVA_2017_version2 = "v2"
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

                 process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
                    cms.PSet(
                       record = cms.string('GBRWrapperRcd'),
                       tag = cms.string("RecoTauTag_%s%s" % (gbrForestName, tauIdDiscrMVA_2017_version2)),
                       label = cms.untracked.string("RecoTauTag_%s%s" % (gbrForestName, tauIdDiscrMVA_2017_version2))
                    )
                 )
                 for WP in tauIdDiscrMVA_WPs_run2_2017[training].keys():
                    process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
                       cms.PSet(
                          record = cms.string('PhysicsTGraphPayloadRcd'),
                          tag = cms.string("RecoTauTag_%s%s_WP%s" % (gbrForestName, tauIdDiscrMVA_2017_version2, WP)),
                          label = cms.untracked.string("RecoTauTag_%s%s_WP%s" % (gbrForestName, tauIdDiscrMVA_2017_version2, WP))
                       )
                    )

                 process.loadRecoTauTagMVAsFromPrepDB.toGet.append(
                    cms.PSet(
                       record = cms.string('PhysicsTFormulaPayloadRcd'),
                       tag = cms.string("RecoTauTag_%s%s_mvaOutput_normalization" % (gbrForestName, tauIdDiscrMVA_2017_version2)),
                       label = cms.untracked.string("RecoTauTag_%s%s_mvaOutput_normalization" % (gbrForestName, tauIdDiscrMVA_2017_version2))
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

        process.rerunDiscriminationByIsolationMVArun2v2raw = patDiscriminationByIsolationMVArun2v1raw.clone(
           PATTauProducer = cms.InputTag(tSrc),
           Prediscriminants = noPrediscriminants,
           loadMVAfromDB = cms.bool(True),
           mvaName = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2"), # name of the training you want to use
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

        process.rerunDiscriminationByIsolationMVArun2v2VLoose = patDiscriminationByIsolationMVArun2v1VLoose.clone(
           PATTauProducer = cms.InputTag(tSrc),
           Prediscriminants = noPrediscriminants,
           toMultiplex = cms.InputTag('rerunDiscriminationByIsolationMVArun2v2raw'),
           key = cms.InputTag('rerunDiscriminationByIsolationMVArun2v2raw:category'),
           loadMVAfromDB = cms.bool(True),
           mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_mvaOutput_normalization"), # normalization fo the training you want to use
           mapping = cms.VPSet(
              cms.PSet(
                 category = cms.uint32(0),
                 cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff90"), # this is the name of the working point you want to use
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

        process.rerunDiscriminationByIsolationMVArun2v2VVLoose = process.rerunDiscriminationByIsolationMVArun2v2VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v2VVLoose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff95")
        process.rerunDiscriminationByIsolationMVArun2v2Loose = process.rerunDiscriminationByIsolationMVArun2v2VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v2Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff80")
        process.rerunDiscriminationByIsolationMVArun2v2Medium = process.rerunDiscriminationByIsolationMVArun2v2VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v2Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff70")
        process.rerunDiscriminationByIsolationMVArun2v2Tight = process.rerunDiscriminationByIsolationMVArun2v2VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v2Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff60")
        process.rerunDiscriminationByIsolationMVArun2v2VTight = process.rerunDiscriminationByIsolationMVArun2v2VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v2VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff50")
        process.rerunDiscriminationByIsolationMVArun2v2VVTight = process.rerunDiscriminationByIsolationMVArun2v2VLoose.clone()
        process.rerunDiscriminationByIsolationMVArun2v2VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoDBoldDMwLT2017v2_WPEff40")

	##NEW DPF 2017v1
	#tauIDSources = cms.PSet()
	#workingPoints_ = {
        #    "all": {"Tight" : 0.123} #FIXME: define WP
        #}

        #file_name = 'RecoTauTag/TrainingFiles/data/DPFTauId/DPFIsolation_2017v1_quantized.pb'
        #process.dpfTau2016v1 = cms.EDProducer("DPFIsolation",
        #    pfcands     = cms.InputTag('packedPFCandidates'),
        #    taus        = cms.InputTag(tSrc),
        #    vertices    = cms.InputTag(vSrc),
        #    graph_file  = cms.string(file_name),
        #    version     = cms.uint32(getDpfTauVersion(file_name)),
        #    mem_mapped  = cms.bool(False)
        #)
	#processDeepProducer(process,'dpfTau2016v1', tauIDSources, workingPoints_)

	##NEW DPF 2016v0
        #tauIDSources = cms.PSet()
        #workingPoints_ = {
        #     "all": {
        #         "Tight" : "if(decayMode == 0) return (0.898328 - 0.000160992 * pt);" + \
        #                   "if(decayMode == 1) return (0.910138 - 0.000229923 * pt);" + \
        #                   "if(decayMode == 10) return (0.873958 - 0.0002328 * pt);" + \
        #                   "return 99.0;"
        #     }
        #}
        #file_name = 'RecoTauTag/TrainingFiles/data/DPFTauId/DPFIsolation_2017v0_quantized.pb'
        #process.dpfTau2016v0 = cms.EDProducer("DPFIsolation",
        #     pfcands     = cms.InputTag('packedPFCandidates'),
        #     taus        = cms.InputTag(tSrc),
        #     vertices    = cms.InputTag(vSrc),
        #     graph_file  = cms.string(file_name),
        #     version     = cms.uint32(getDpfTauVersion(file_name)),
        #     mem_mapped  = cms.bool(False)
        #)

	#processDeepProducer(process,'dpfTau2016v0', tauIDSources, workingPoints_)

	## Deep Tau v2
        tauIDSources = cms.PSet()
        workingPoints_ = {
                "e": {
                    "VVVLoose": 0.0630386,
                    "VVLoose": 0.1686942,
                    "VLoose": 0.3628130,
                    "Loose": 0.6815435,
                    "Medium": 0.8847544,
                    "Tight": 0.9675541,
                    "VTight": 0.9859251,
                    "VVTight": 0.9928449,
                },
                "mu": {
                    "VLoose": 0.1058354,
                    "Loose": 0.2158633,
                    "Medium": 0.5551894,
                    "Tight": 0.8754835,
                },
                "jet": {
                    "VVVLoose": 0.2599605,
                    "VVLoose": 0.4249705,
                    "VLoose": 0.5983682,
                    "Loose": 0.7848675,
                    "Medium": 0.8834768,
                    "Tight": 0.9308689,
                    "VTight": 0.9573137,
                    "VVTight": 0.9733927,
                },
	}

        file_names = [
             'core:RecoTauTag/TrainingFiles/data/DeepTauId/deepTau_2017v2p6_e6_core.pb',
             'inner:RecoTauTag/TrainingFiles/data/DeepTauId/deepTau_2017v2p6_e6_inner.pb',
             'outer:RecoTauTag/TrainingFiles/data/DeepTauId/deepTau_2017v2p6_e6_outer.pb',
        ]
        process.deepTau2017v2p1 = cms.EDProducer("DeepTauId",
                electrons              = cms.InputTag('slimmedElectrons'),
                muons                  = cms.InputTag('slimmedMuons'),
                taus                   = cms.InputTag(tSrc),
                pfcands                = cms.InputTag('packedPFCandidates'),
                vertices               = cms.InputTag('offlineSlimmedPrimaryVertices'),
                rho                    = cms.InputTag('fixedGridRhoAll'),
                graph_file             = cms.vstring(file_names),
                mem_mapped             = cms.bool(True),
                version                = cms.uint32(getDeepTauVersion(file_names[0])[1]),
                debug_level            = cms.int32(0),
                disable_dxy_pca        = cms.bool(True)

        )

        processDeepProducer(process,'deepTau2017v2p1', tauIDSources, workingPoints_)


	##NEW deep Tau
        #tauIDSources = cms.PSet()
        #workingPoints_ = {
        #    "e": {
        #        "VVVLoose" : 0.96424,
        #        "VVLoose" : 0.98992,
        #        "VLoose" : 0.99574,
        #        "Loose": 0.99831,
        #        "Medium": 0.99868,
        #        "Tight": 0.99898,
        #        "VTight": 0.99911,
        #        "VVTight": 0.99918
        #    },
        #    "mu": {
        #        "VVVLoose" : 0.959619,
        #        "VVLoose" : 0.997687,
        #        "VLoose" : 0.999392,
        #        "Loose": 0.999755,
        #        "Medium": 0.999854,
        #        "Tight": 0.999886,
        #        "VTight": 0.999944,
        #        "VVTight": 0.9999971
        #    },
        #    "jet": {
        #        "VVVLoose" : 0.5329,
        #        "VVLoose" : 0.7645,
        #        "VLoose" : 0.8623,
        #        "Loose": 0.9140,
        #        "Medium": 0.9464,
        #        "Tight": 0.9635,
        #        "VTight": 0.9760,
        #        "VVTight": 0.9859
        #    }
        #}
        #file_name = 'RecoTauTag/TrainingFiles/data/DeepTauId/deepTau_2017v1_20L1024N_quantized.pb'
        #process.deepTau2017v1 = cms.EDProducer("DeepTauId",
        #    electrons              = cms.InputTag("slimmedElectrons"),
        #    muons                  = cms.InputTag("slimmedMuons"),
        #    taus                   = cms.InputTag(tSrc),
        #    graph_file             = cms.string(file_name),
        #    mem_mapped             = cms.bool(False)
        #)

	#processDeepProducer(process,'deepTau2017v1', tauIDSources, workingPoints_)

	#NEW against ele 2018

        antiElectronDiscrMVA6_version = "MVA6v3_noeveto"
        ### Define new anti-e discriminants
        ## Raw
        from RecoTauTag.RecoTau.PATTauDiscriminationAgainstElectronMVA6_cfi import patTauDiscriminationAgainstElectronMVA6
        process.patTauDiscriminationByElectronRejectionMVA62018Raw = patTauDiscriminationAgainstElectronMVA6.clone(
            Prediscriminants = noPrediscriminants, #already selected for MiniAOD
            vetoEcalCracks = cms.bool(False), #keep taus in EB-EE cracks
            mvaName_NoEleMatch_wGwoGSF_BL = 'RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_BL',
            mvaName_NoEleMatch_wGwoGSF_EC = 'RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_EC',
            mvaName_NoEleMatch_woGwoGSF_BL = 'RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_BL',
            mvaName_NoEleMatch_woGwoGSF_EC = 'RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_EC',
            mvaName_wGwGSF_BL = 'RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_BL',
            mvaName_wGwGSF_EC = 'RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_EC',
            mvaName_woGwGSF_BL = 'RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_BL',
            mvaName_woGwGSF_EC = 'RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_EC'
        )
        ## WPs
        from RecoTauTag.RecoTau.PATTauDiscriminantCutMultiplexer_cfi import patTauDiscriminantCutMultiplexer
        # VLoose
        process.patTauDiscriminationByVLooseElectronRejectionMVA62018 = patTauDiscriminantCutMultiplexer.clone(
            PATTauProducer = process.patTauDiscriminationByElectronRejectionMVA62018Raw.PATTauProducer,
            Prediscriminants = process.patTauDiscriminationByElectronRejectionMVA62018Raw.Prediscriminants,
            toMultiplex = cms.InputTag("patTauDiscriminationByElectronRejectionMVA62018Raw"),
            key = cms.InputTag("patTauDiscriminationByElectronRejectionMVA62018Raw","category"),
            mapping = cms.VPSet(
                cms.PSet(
                    category = cms.uint32(0),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_BL_WPeff98'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(2),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_BL_WPeff98'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(5),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_BL_WPeff98'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(7),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_BL_WPeff98'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(8),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_EC_WPeff98'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(10),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_EC_WPeff98'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(13),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_EC_WPeff98'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(15),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_EC_WPeff98'),
                    variable = cms.string('pt')
                )
            )
        )
        # Loose
        process.patTauDiscriminationByLooseElectronRejectionMVA62018 = process.patTauDiscriminationByVLooseElectronRejectionMVA62018.clone(
            mapping = cms.VPSet(
                cms.PSet(
                    category = cms.uint32(0),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_BL_WPeff90'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(2),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_BL_WPeff90'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(5),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_BL_WPeff90'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(7),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_BL_WPeff90'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(8),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_EC_WPeff90'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(10),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_EC_WPeff90'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(13),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_EC_WPeff90'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(15),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_EC_WPeff90'),
                    variable = cms.string('pt')
                )
            )
        )
        # Medium
        process.patTauDiscriminationByMediumElectronRejectionMVA62018 = process.patTauDiscriminationByVLooseElectronRejectionMVA62018.clone(
            mapping = cms.VPSet(
                cms.PSet(
                    category = cms.uint32(0),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_BL_WPeff80'),
                    variable = cms.string('pt')
                 ),
                cms.PSet(
                    category = cms.uint32(2),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_BL_WPeff80'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(5),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_BL_WPeff80'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(7),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_BL_WPeff80'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(8),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_EC_WPeff80'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(10),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_EC_WPeff80'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(13),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_EC_WPeff80'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(15),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_EC_WPeff80'),
                    variable = cms.string('pt')
                )
            )
        )
        # Tight
        process.patTauDiscriminationByTightElectronRejectionMVA62018 = process.patTauDiscriminationByVLooseElectronRejectionMVA62018.clone(
            mapping = cms.VPSet(
                cms.PSet(
                    category = cms.uint32(0),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_BL_WPeff70'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(2),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_BL_WPeff70'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(5),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_BL_WPeff70'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(7),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_BL_WPeff70'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(8),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_EC_WPeff70'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(10),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_EC_WPeff70'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(13),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_EC_WPeff70'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(15),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_EC_WPeff70'),
                    variable = cms.string('pt')
                )
            )
        )
        # VTight
        process.patTauDiscriminationByVTightElectronRejectionMVA62018 = process.patTauDiscriminationByVLooseElectronRejectionMVA62018.clone(
            mapping = cms.VPSet(
                cms.PSet(
                    category = cms.uint32(0),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_BL_WPeff60'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(2),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_BL_WPeff60'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(5),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_BL_WPeff60'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(7),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_BL_WPeff60'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(8),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_woGwoGSF_EC_WPeff60'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(10),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_NoEleMatch_wGwoGSF_EC_WPeff60'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(13),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_woGwGSF_EC_WPeff60'),
                    variable = cms.string('pt')
                ),
                cms.PSet(
                    category = cms.uint32(15),
                    cut = cms.string('RecoTauTag_antiElectron'+antiElectronDiscrMVA6_version+'_gbr_wGwGSF_EC_WPeff60'),
                    variable = cms.string('pt')
                )
            )
        )
        ### Put all new anti-e discrminats to a sequence
        process.patTauDiscriminationByElectronRejectionMVA62018Task = cms.Task(
            process.patTauDiscriminationByElectronRejectionMVA62018Raw,
            process.patTauDiscriminationByVLooseElectronRejectionMVA62018,
            process.patTauDiscriminationByLooseElectronRejectionMVA62018,
            process.patTauDiscriminationByMediumElectronRejectionMVA62018,
            process.patTauDiscriminationByTightElectronRejectionMVA62018,
            process.patTauDiscriminationByVTightElectronRejectionMVA62018
        )
        process.patTauDiscriminationByElectronRejectionMVA62018Seq = cms.Sequence(process.patTauDiscriminationByElectronRejectionMVA62018Task)
        
        # this sequence has to be included in your cms.Path() before your analyzer which accesses the new variables is called.
        process.rerunMvaIsolation2SeqRun2 = cms.Path(
           process.rerunDiscriminationByIsolationMVArun2v1raw
           * process.rerunDiscriminationByIsolationMVArun2v1VLoose
           * process.rerunDiscriminationByIsolationMVArun2v1Loose
           * process.rerunDiscriminationByIsolationMVArun2v1Medium
           * process.rerunDiscriminationByIsolationMVArun2v1Tight
           * process.rerunDiscriminationByIsolationMVArun2v1VTight
           * process.rerunDiscriminationByIsolationMVArun2v1VVTight
	   * process.rerunDiscriminationByIsolationMVArun2v2raw
           * process.rerunDiscriminationByIsolationMVArun2v2VVLoose
           * process.rerunDiscriminationByIsolationMVArun2v2VLoose
           * process.rerunDiscriminationByIsolationMVArun2v2Loose
           * process.rerunDiscriminationByIsolationMVArun2v2Medium
           * process.rerunDiscriminationByIsolationMVArun2v2Tight
           * process.rerunDiscriminationByIsolationMVArun2v2VTight
           * process.rerunDiscriminationByIsolationMVArun2v2VVTight
	   #* process.dpfTau2016v1
           #* process.dpfTau2016v0
           #* process.deepTau2017v1
           * process.deepTau2017v2p1
	   * process.patTauDiscriminationByElectronRejectionMVA62018Seq
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
            idRawv2 = cms.InputTag("rerunDiscriminationByIsolationMVArun2v2raw"),
            idVVLoosev2 = cms.InputTag("rerunDiscriminationByIsolationMVArun2v2VVLoose"),
            idVLoosev2 = cms.InputTag("rerunDiscriminationByIsolationMVArun2v2VLoose"),
            idLoosev2 = cms.InputTag("rerunDiscriminationByIsolationMVArun2v2Loose"),
            idMediumv2 = cms.InputTag("rerunDiscriminationByIsolationMVArun2v2Medium"),
            idTightv2 = cms.InputTag("rerunDiscriminationByIsolationMVArun2v2Tight"),
            idVTightv2 = cms.InputTag("rerunDiscriminationByIsolationMVArun2v2VTight"),
            idVVTightv2 = cms.InputTag("rerunDiscriminationByIsolationMVArun2v2VVTight"),
	    #byDpfTau2016v1VSallraw = cms.InputTag("dpfTau2016v1","VSall"),
    	    #byTightDpfTau2016v1VSall = cms.InputTag("dpfTau2016v1","VSallTight"),
            #byDpfTau2016v0VSallraw = cms.InputTag("dpfTau2016v0","VSall"),
            #byTightDpfTau2016v0VSall = cms.InputTag("dpfTau2016v0","VSallTight"),
 	    #byDeepTau2017v1VSmuraw = cms.InputTag("deepTau2017v1","VSmu"),
    	    #byLooseDeepTau2017v1VSmu = cms.InputTag("deepTau2017v1","VSmuLoose"),
    	    #byMediumDeepTau2017v1VSmu = cms.InputTag("deepTau2017v1","VSmuMedium"),
    	    #byTightDeepTau2017v1VSmu = cms.InputTag("deepTau2017v1","VSmuTight"),
    	    #byVLooseDeepTau2017v1VSmu = cms.InputTag("deepTau2017v1","VSmuVLoose"),
    	    #byVTightDeepTau2017v1VSmu = cms.InputTag("deepTau2017v1","VSmuVTight"),
    	    #byVVLooseDeepTau2017v1VSmu = cms.InputTag("deepTau2017v1","VSmuVVLoose"),
    	    #byVVTightDeepTau2017v1VSmu = cms.InputTag("deepTau2017v1","VSmuVVTight"),
    	    #byVVVLooseDeepTau2017v1VSmu = cms.InputTag("deepTau2017v1","VSmuVVVLoose"),
            #byDeepTau2017v1VSeraw = cms.InputTag("deepTau2017v1","VSe"),
            #byLooseDeepTau2017v1VSe = cms.InputTag("deepTau2017v1","VSeLoose"),
            #byMediumDeepTau2017v1VSe = cms.InputTag("deepTau2017v1","VSeMedium"),
            #byTightDeepTau2017v1VSe = cms.InputTag("deepTau2017v1","VSeTight"),
            #byVLooseDeepTau2017v1VSe = cms.InputTag("deepTau2017v1","VSeVLoose"),
            #byVTightDeepTau2017v1VSe = cms.InputTag("deepTau2017v1","VSeVTight"),
            #byVVLooseDeepTau2017v1VSe = cms.InputTag("deepTau2017v1","VSeVVLoose"),
            #byVVTightDeepTau2017v1VSe = cms.InputTag("deepTau2017v1","VSeVVTight"),
            #byVVVLooseDeepTau2017v1VSe = cms.InputTag("deepTau2017v1","VSeVVVLoose"),
	    #byDeepTau2017v1VSjetraw = cms.InputTag("deepTau2017v1","VSjet"),
            #byLooseDeepTau2017v1VSjet = cms.InputTag("deepTau2017v1","VSjetLoose"),
            #byMediumDeepTau2017v1VSjet = cms.InputTag("deepTau2017v1","VSjetMedium"),
            #byTightDeepTau2017v1VSjet = cms.InputTag("deepTau2017v1","VSjetTight"),
            #byVLooseDeepTau2017v1VSjet = cms.InputTag("deepTau2017v1","VSjetVLoose"),
            #byVTightDeepTau2017v1VSjet = cms.InputTag("deepTau2017v1","VSjetVTight"),
            #byVVLooseDeepTau2017v1VSjet = cms.InputTag("deepTau2017v1","VSjetVVLoose"),
            #byVVTightDeepTau2017v1VSjet = cms.InputTag("deepTau2017v1","VSjetVVTight"),
            #byVVVLooseDeepTau2017v1VSjet = cms.InputTag("deepTau2017v1","VSjetVVVLoose"),

            byDeepTau2017v2p1VSmuraw = cms.InputTag("deepTau2017v2p1","VSmu"),
            byLooseDeepTau2017v2p1VSmu = cms.InputTag("deepTau2017v2p1","VSmuLoose"),
            byMediumDeepTau2017v2p1VSmu = cms.InputTag("deepTau2017v2p1","VSmuMedium"),
            byTightDeepTau2017v2p1VSmu = cms.InputTag("deepTau2017v2p1","VSmuTight"),
            byVLooseDeepTau2017v2p1VSmu = cms.InputTag("deepTau2017v2p1","VSmuVLoose"),
            byVTightDeepTau2017v2p1VSmu = cms.InputTag("deepTau2017v2p1","VSmuVTight"),
            byVVLooseDeepTau2017v2p1VSmu = cms.InputTag("deepTau2017v2p1","VSmuVVLoose"),
            byVVTightDeepTau2017v2p1VSmu = cms.InputTag("deepTau2017v2p1","VSmuVVTight"),
            byVVVLooseDeepTau2017v2p1VSmu = cms.InputTag("deepTau2017v2p1","VSmuVVVLoose"),
            byDeepTau2017v2p1VSeraw = cms.InputTag("deepTau2017v2p1","VSe"),
            byLooseDeepTau2017v2p1VSe = cms.InputTag("deepTau2017v2p1","VSeLoose"),
            byMediumDeepTau2017v2p1VSe = cms.InputTag("deepTau2017v2p1","VSeMedium"),
            byTightDeepTau2017v2p1VSe = cms.InputTag("deepTau2017v2p1","VSeTight"),
            byVLooseDeepTau2017v2p1VSe = cms.InputTag("deepTau2017v2p1","VSeVLoose"),
            byVTightDeepTau2017v2p1VSe = cms.InputTag("deepTau2017v2p1","VSeVTight"),
            byVVLooseDeepTau2017v2p1VSe = cms.InputTag("deepTau2017v2p1","VSeVVLoose"),
            byVVTightDeepTau2017v2p1VSe = cms.InputTag("deepTau2017v2p1","VSeVVTight"),
            byVVVLooseDeepTau2017v2p1VSe = cms.InputTag("deepTau2017v2p1","VSeVVVLoose"),
            byDeepTau2017v2p1VSjetraw = cms.InputTag("deepTau2017v2p1","VSjet"),
            byLooseDeepTau2017v2p1VSjet = cms.InputTag("deepTau2017v2p1","VSjetLoose"),
            byMediumDeepTau2017v2p1VSjet = cms.InputTag("deepTau2017v2p1","VSjetMedium"),
            byTightDeepTau2017v2p1VSjet = cms.InputTag("deepTau2017v2p1","VSjetTight"),
            byVLooseDeepTau2017v2p1VSjet = cms.InputTag("deepTau2017v2p1","VSjetVLoose"),
            byVTightDeepTau2017v2p1VSjet = cms.InputTag("deepTau2017v2p1","VSjetVTight"),
            byVVLooseDeepTau2017v2p1VSjet = cms.InputTag("deepTau2017v2p1","VSjetVVLoose"),
            byVVTightDeepTau2017v2p1VSjet = cms.InputTag("deepTau2017v2p1","VSjetVVTight"),
            byVVVLooseDeepTau2017v2p1VSjet = cms.InputTag("deepTau2017v2p1","VSjetVVVLoose"),

            againstElectronMVA6Raw2018 = cms.InputTag("patTauDiscriminationByElectronRejectionMVA62018Raw"),
            againstElectronMVA6category2018 = cms.InputTag("patTauDiscriminationByElectronRejectionMVA62018Raw","category"),
            againstElectronVLooseMVA62018 = cms.InputTag("patTauDiscriminationByVLooseElectronRejectionMVA62018"),
            againstElectronLooseMVA62018 = cms.InputTag("patTauDiscriminationByLooseElectronRejectionMVA62018"),
            againstElectronMediumMVA62018 = cms.InputTag("patTauDiscriminationByMediumElectronRejectionMVA62018"),
            againstElectronTightMVA62018 = cms.InputTag("patTauDiscriminationByTightElectronRejectionMVA62018"),
	    againstElectronVTightMVA62018 = cms.InputTag("patTauDiscriminationByVTightElectronRejectionMVA62018"),
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

    # embed trigger filters
    modName = 'minitriggerfilterTaus{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODTauTriggerFilterEmbedder",
        src=cms.InputTag(tSrc),
        bits = cms.InputTag("TriggerResults","","HLT"),
        objects = cms.InputTag("slimmedPatTrigger"),
        #bits = cms.InputTag("TriggerResults","","SIMembedding"),
        #objects = cms.InputTag("slimmedPatTrigger","","MERGE"),
    )
    if isEmbedded:
        mod.bits=cms.InputTag("TriggerResults","","SIMembedding")
        mod.objects=cms.InputTag("slimmedPatTrigger","","MERGE")
	if year=="2016":
	   mod.objects=cms.InputTag("slimmedPatTrigger","","PAT")
    tSrc = modName
    setattr(process,modName,mod)

    pathName = 'runTriggerFilterTauEmbedding{0}'.format(postfix)
    modPath = cms.Path(getattr(process,modName))
    setattr(process,pathName,modPath)
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


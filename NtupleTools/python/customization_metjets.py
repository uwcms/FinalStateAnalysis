# Embed IDs for jets
import FWCore.ParameterSet.Config as cms
import os

def preMETFromJES(process, jSrc, vSrc, metSrc,mSrc, eSrc, **kwargs):
    postfix = kwargs.pop('postfix','')
    jType = kwargs.pop('jType','AK4PFchs')
    runningLocal = kwargs.pop('runningLocal',False)

    if True :
        # Provide proper path name for Jet Uncertainty file
        # V10 is most recent version for JES Uncertainties
        # https://hypernews.cern.ch/HyperNews/CMS/get/jes/642/1/1.html
        if runningLocal : fName = "../../NtupleTools/data/Autumn18_V19_MC_UncertaintySources_AK4PFchs.txt" # recommended by JetMET
        else :
            cmsswversion=os.environ['CMSSW_VERSION']
            fName = "{0}/src/FinalStateAnalysis/NtupleTools/data/Autumn18_V19_MC_UncertaintySources_AK4PFchs.txt".format(cmsswversion)

        modName = 'miniAODMETJesSystematicsEmbedding{0}'.format(postfix)
        mod = cms.EDProducer(
	    "MiniAODMETJesSystematicsEmbedder",
            src = cms.InputTag(jSrc),
            srcMET=cms.InputTag(metSrc),
            corrLabel = cms.string(jType),
            fName = cms.string(fName)
        )
        metSrc = modName
        setattr(process,modName,mod)

        pathName = 'metJESSystematicsEmbedding{0}'.format(postfix)
        path = cms.Path(getattr(process,modName))
        setattr(process,pathName,path)

        print modName+" for  MET?" 
 
        process.schedule.append(getattr(process,pathName))

        #modName = 'miniAODMETUesSystEmbedding{0}'.format(postfix)
        #mod = cms.EDProducer(
        #    "MiniAODMETUesSystEmbedder",
        #    srcMET=cms.untracked.InputTag(metSrc),
        #    srcPF = cms.untracked.InputTag("pfCandsForUnclusteredUnc"),
        #)
        #metSrc = modName
        #setattr(process,modName,mod)

        #pathName = 'metUesSystematicsEmbedding{0}'.format(postfix)
        #path = cms.Path(getattr(process,modName))
        #setattr(process,pathName,path)

        #print modName+" for  MET?"

        #process.schedule.append(getattr(process,pathName))


    print metSrc 

    return metSrc


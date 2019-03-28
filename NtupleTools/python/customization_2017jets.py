# Embed IDs for jets
import FWCore.ParameterSet.Config as cms
import os

def preJets(process, jSrc, vSrc, metSrc,mSrc, eSrc, **kwargs):
    postfix = kwargs.pop('postfix','')
    jType = kwargs.pop('jType','AK4PFchs')
    doBTag = kwargs.pop('doBTag',False)
    doFullJESUnc = kwargs.pop('doFullJESUnc',False)
    runningLocal = kwargs.pop('runningLocal',False)


    mod = cms.EDProducer(
        "MiniAODJetIdEmbedder2017",
        src=cms.InputTag(jSrc)
    )
    modName = 'miniPatJets{0}'.format(postfix)
    setattr(process,modName,mod)
    jSrc = modName

    pathName = 'runMiniAODJetEmbedding{0}'.format(postfix)
    setattr(process,pathName,cms.Path(getattr(process,modName)))
    process.schedule.append(getattr(process,pathName))

    # embed BTag SFs
    if doBTag :
        modName = 'miniJetsEmbedBTagSFLoose{0}'.format(postfix)
        mod = cms.EDProducer(
            "MiniAODJetBTagSFLooseEmbedder",
            src=cms.InputTag(jSrc)
        )
        jSrc = modName
        setattr(process,modName,mod)

        pathName = 'runMiniAODJetBTagSFLooseEmbedding{0}'.format(postfix)
        path = cms.Path(getattr(process,modName))
        setattr(process,pathName,path)
        process.schedule.append(getattr(process,pathName))

    # embed BTag SFs
    if doBTag :
        modName = 'miniJetsEmbedBTagSFMedium{0}'.format(postfix)
        mod = cms.EDProducer(
            "MiniAODJetBTagSFMediumEmbedder",
            src=cms.InputTag(jSrc)
        )
        jSrc = modName
        setattr(process,modName,mod)

        pathName = 'runMiniAODJetBTagSFMediumEmbedding{0}'.format(postfix)
        path = cms.Path(getattr(process,modName))
        setattr(process,pathName,path)
        process.schedule.append(getattr(process,pathName))

    # doFullJESUnc 
    if doFullJESUnc :
        # Provide proper path name for Jet Uncertainty file
        # V10 is most recent version for JES Uncertainties
        # https://hypernews.cern.ch/HyperNews/CMS/get/jes/642/1/1.html
        # recommended by HTT Twiki for 2017 data (6 Nov. 2018):
        # - https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsToTauTauWorking2017#Jet/MET_uncertainty_treatment
        # - linked to: https://github.com/cms-jet/JECDatabase/blob/master/textFiles/Fall17_17Nov2017F_V32_DATA/Fall17_17Nov2017F_V32_DATA_UncertaintySources_AK4PFchs.txt
        if runningLocal : fName = "../../NtupleTools/data/Fall17_17Nov2017F_V32_DATA_UncertaintySources_AK4PFchs.txt" 
        else :
            cmsswversion=os.environ['CMSSW_VERSION']
            fName = "{0}/src/FinalStateAnalysis/NtupleTools/data/Fall17_17Nov2017F_V32_DATA_UncertaintySources_AK4PFchs.txt".format(cmsswversion)

        modName = 'miniAODJetFullSystematicsEmbedding{0}'.format(postfix)
        mod = cms.EDProducer(
	    "MiniAODJetFullSystematicsEmbedder",
            src = cms.InputTag(jSrc),
            srcMET=cms.InputTag(metSrc),
            corrLabel = cms.string(jType),
            fName = cms.string(fName)
        )
        jSrc = modName
        setattr(process,modName,mod)

        pathName = 'jetFullSystematicsEmbedding{0}'.format(postfix)
        path = cms.Path(getattr(process,modName))
        setattr(process,pathName,path)

        print modName+" for  MET?" 
 
        process.schedule.append(getattr(process,pathName))


    print jSrc 

    # embed IP stuff
    modName = 'miniJetsEmbedIp{0}'.format(postfix)
    mod = cms.EDProducer(
        "MiniAODJetIpEmbedder",
        src = cms.InputTag(jSrc),
        vtxSrc = cms.InputTag(vSrc),
    )
    jSrc = modName
    setattr(process,modName,mod)

    pathName = 'runMiniAODJetIpEmbedding{0}'.format(postfix)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)
    process.schedule.append(getattr(process,pathName))

    print jSrc

    modName = 'miniAODJetSystematicsEmbedding{0}'.format(postfix)
    mod = cms.EDProducer(
	"MiniAODJetSystematicsEmbedder",
        src = cms.InputTag(jSrc),
        corrLabel = cms.string(jType)
    )
    jSrc = modName
    setattr(process,modName,mod)

    pathName = 'jetSystematicsEmbedding{0}'.format(postfix)
    path = cms.Path(getattr(process,modName))
    setattr(process,pathName,path)
  
    process.schedule.append(getattr(process,pathName))

    return jSrc


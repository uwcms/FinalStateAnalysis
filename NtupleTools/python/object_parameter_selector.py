###############################################################################
##                                                                           ##
##     object_parameter_selector.py                                          ##
##                                                                           ##
##     Provides a function that takes a (possibly-ordered) dictionary of     ##
##     selection parameters and puts the necessary modules in the CMS        ##
##     process.                                                              ##
##                                                                           ##
##     setup_selections(process, moduleName, inputs, params)                 ##
##         process    : The process                                          ##
##         moduleName : A string to name the modules to avoid conflicts.     ##
##                      Modules are named as: fullParticleName + moduleName  ##
##                      So if you pass in "Preselection" as moduleName,      ##
##                      electrons processed by it will be in the event       ##
##                      stream under module 'electronPreselection'.          ##
##         inputs     : A dictionary giving the current name of each         ##
##                      collection, in the format of fs_daughter_inputs.     ##
##         params     : For each type of object that should undergo          ##
##                      selection, this dictionary contains and item keyed   ##
##                      to the appropriate letter (e.g. 'e' for electrons).  ##
##                      A string selects the objects with that string. A     ##
##                      dictionary is interpreted as the parameters for      ##
##                      a delta-R based overlap selector. The item           ##
##                      'selection' should be a selection string. Then for   ##
##                      each other type of particle the object should be     ##
##                      cleaned against, there should be a dictionary        ##
##                      giving the parameters for the cleaning:              ##
##                            deltaR : DeltaR to trigger cleaning            ##
##                            selection : selection string for the object    ##
##         Returns a cms.Sequence with the modules (which are automatically  ##
##             added to the process).                                        ##
##                                                                           ##
##                                                                           ##
##    Author: Nate Woods, U. Wisconsin                                       ##
##                                                                           ##
###############################################################################

import FWCore.ParameterSet.Config as cms


fullNames = { 
    'e' : 'electron',
    'm' : 'muon',
    't' : 'tau',
    'g' : 'photon',
    'j' : 'jet',
    'v' : 'vertex',
}

def getName(obj, capitalize=False):
    if capitalize:
        return fullNames[obj][0].upper()+fullNames[obj][1:]
    return fullNames[obj]

def getPlural(obj, capitalize=False):
    if obj[0] == 'v':
        return 'Vertices' if capitalize else 'vertices'
    return getName(obj, capitalize) + 's'


def setup_selections(process, moduleName, inputs, params):
    ''' 
    NB: be careful if your selections depend on each other (e.g.
    if you might fail to select an electron that could veto a jet).
    In this case, params should be an OrderedDict instead of a 
    regular python dict to avoid unpredictable behavior.
    '''
    seq = cms.Sequence()

    for obj, selector in params.iteritems():
        if obj[0] == 'v':
            module = cms.EDFilter("VertexSelector",
                                  src = cms.InputTag(inputs[getPlural(obj)]),
                                  cut = cms.string(selector),
                                  filter = cms.bool(True),
                                  )  

        # string indicates simple selection
        elif isinstance(selector, str):
            module = cms.EDFilter(
                "PAT%sSelector"%getName(obj, True),
                src=cms.InputTag(inputs[getPlural(obj)]),
                cut=cms.string(selector),
                filter=cms.bool(False),
                )
        else:
            # otherwise, do delta R cross-cleaning
            assert isinstance(selector, dict), "Invalid selection parameters for %s"%moduleName
            
            selection = selector.pop('selection', '')

            overlapParams = cms.PSet()
            for part, overlap in selector.iteritems():
                subSelection = overlap.pop('selection', '')
                particleParams = cms.PSet(
                    src=cms.InputTag(inputs[getPlural(part)]),
                    algorithm=cms.string("byDeltaR"),
                    preselection=cms.string(subSelection),
                    deltaR=cms.double(overlap.get('deltaR', 0.3)),
                    checkRecoComponents=cms.bool(False),
                    pairCut=cms.string(''),
                    requireNoOverlaps=cms.bool(True),
                    )
                setattr(overlapParams, getName(part), particleParams)

            module = cms.EDProducer(
                "PAT%sCleaner"%getName(obj, True),
                src = cms.InputTag(inputs[getPlural(obj)]),
                preselection = cms.string(selection),
                checkOverlaps = overlapParams,
                finalCut = cms.string(''),
                )

        # add this module to the process with the right name
        setattr(process, getName(obj)+moduleName, module)
        seq += module
        
        # use the correct name for this object if it's needed by other selector modules
        inputs[getPlural(obj)] = getName(obj)+moduleName

    return seq

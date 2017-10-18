'''

TauVarParsing

Extend the default options provided by the VarParsing class to include
some common tau related use cases.

Author: Evan K. Friis, UW Madison

See: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T

'''
import os
import sys

import FWCore.ParameterSet.VarParsing as VarParsing
try:
    import Configuration.PyReleaseValidation.autoCond as autoCond
except ImportError:
    # Moved in 52X
    import Configuration.AlCa.autoCond as autoCond
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes

class TauVarParsing(VarParsing.VarParsing):
    '''
    TauVarParsing
    Create an object that will parse the CLI arguments.
    You can additionally specify additional options in the constructor.
    The type of the option will be inferred.

    Example:
    >>> # Create a parser with some extra options and defaults
    >>> parse = TauVarParsing(myIndex=2, myLabel="pippo", myFlag=False)
    >>> parse.myIndex
    2
    >>> parse.myLabel
    'pippo'
    >>> parse.myFlag
    0
    >>> # The default global tag is automatically configured
    >>> 'MC_' in parse.globalTag
    True
    >>> # Building the lumi mask
    >>> parse.lumiMask = "/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions11/7TeV/Reprocessing/Cert_170249-172619_7TeV_ReReco5Aug_Collisions11_JSON_v2.txt"
    >>> parse.buildPoolSourceLumiMask()[0]
    u'170722:110-170722:287'
    >>> parse.firstRun = 171282 # these values are inclusive
    >>> parse.lastRun = 171369
    >>> parse.buildPoolSourceLumiMask()[0]
    u'171282:1-171282:12'
    >>> parse.buildPoolSourceLumiMask()[-1]
    u'171369:144-171369:161'

    '''
    type_map = {
        str : VarParsing.VarParsing.varType.string,
        int : VarParsing.VarParsing.varType.int,
        float : VarParsing.VarParsing.varType.float
    }
    def __init__(self, **kwargs):
        # Call the base constructor with the 'analysis' defaults
        super(TauVarParsing, self).__init__('analysis')
        # Now register some extra common cases
        self.register('globalTag',
                      autoCond.autoCond['mc'], # Default value
                      self.multiplicity.singleton,
                      self.varType.string,
                      "Global Tag Conditions")
        self.register('isMC',
                      0, # Default value
                      self.multiplicity.singleton,
                      self.varType.int,
                      "Flag to indicate job uses MC")
        self.register('hltProcess',
                      'HLT',
                      self.multiplicity.singleton,
                      self.varType.string,
                      "HLT Process name")
        self.register('firstRun',
                      1,
                      self.multiplicity.singleton,
                      self.varType.int,
                      "First run to process, used w/ lumiMask")
        self.register('lastRun',
                      -1,
                      self.multiplicity.singleton,
                      self.varType.int,
                      "Last run to process [-1 = all], used w/ lumiMask")
        self.register('processName',
                      'TauAnalysis',
                      self.multiplicity.singleton,
                      self.varType.string,
                      "cms.Process name")
        self.register('saveFinalEvents',
                      'TauAnalysis',
                      self.multiplicity.singleton,
                      self.varType.int,
                      "Save the final events")
        self.register('triggerBits',
                      '',
                      self.multiplicity.list,
                      self.varType.string,
                      "List of trigger bit specifications [RunRange:]Path")
        self.register('lumiMask',
                      '',
                      self.multiplicity.singleton,
                      self.varType.string,
                      "Path to lumi mask JSON file")
        self.register('eventsToProcess',
                      '',
                      self.multiplicity.list,
                      self.varType.string,
                      "Events to process")

        # Get extra options w/ their defaults
        for key, value in kwargs.iteritems():
            # We use ints for bools
            if type(value) is bool:
                value = int(value)
            self.register(key,
                          value,
                          self.multiplicity.singleton,
                          self.type_map[type(value)],
                          "Custom arg: %s" % key)

    # Override the stupid setupTags function
    def setupTags(self, **kwargs):
        pass

    def buildPoolSourceLumiMask(self):
        # From https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideGoodLumiSectionsJSONFile#cmsRun
        jsonFile = self.lumiMask
        if not os.path.exists(jsonFile):
            raise IOError("Lumi mask file %s does not exist!" % jsonFile)
        lumiList = LumiList.LumiList(filename = jsonFile)
        runs = lumiList.getRuns()
        bad_runs = []
        for run in runs:
            is_good = True
            if int(run) < self.firstRun:
                is_good = False
            if self.lastRun > -1 and int(run) > self.lastRun:
                is_good = False
            if not is_good:
                bad_runs.append(run)
        lumiList.removeRuns(bad_runs)
        lumisToProcess = CfgTypes.untracked(CfgTypes.VLuminosityBlockRange())
        lumisToProcess.extend(lumiList.getCMSSWString().split(','))
        return lumisToProcess

    # Override the default argument parse command, with better error reporting
    def parseArguments(self):
        try:
            super(TauVarParsing, self).parseArguments()
        except:
            sys.stderr.write("Caught an exception parsing cmdline arguments,"
                             " the input arguments are: "
                             + " ".join(sys.argv) + "\n")
            raise

if __name__ == "__main__":
    import doctest
    doctest.testmod()


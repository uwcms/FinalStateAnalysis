from FinalStateAnalysis.TMegaSelector.megaselect import TMegaPySelector

class TestSelector(TMegaPySelector):
    def MegaProcess(self, entry):
        print entry
        return True

#from ROOT import TPySelector
#class TestSelector(TPySelector):
    #def Version(self):
        #return 2
    #def Process(self, entry):
        #print entry
        #return True

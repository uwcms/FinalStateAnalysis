from ROOT import TPySelector

class TestPlainPySelector(TPySelector):
    def Version(self):
        return 2
    def Process(self, entry):
        print entry
        return True

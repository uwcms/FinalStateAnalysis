from FinalStateAnalysis.Utilities.rootbindings import ROOT

def make_scaler(file_path, roovar_path, error_scale=0):
    '''make_scaler(file_path, roovar_path) --> lambda function(x):
    Takes the roorealvar found in roovar_path in the root file file_path and build a function f(x): x/var'''
    tfile  = ROOT.TFile.Open(file_path)
    rooVar = tfile.Get(roovar_path)
    value  = rooVar.getVal()
    if error_scale == 1:
        value += rooVar.getErrorHi()
    elif error_scale == -1:
        value -= rooVar.getErrorLo()
    
    del rooVar
    tfile.Close()
    if value == 0:
        raise ZeroDivisionError("make_scaler(%s, %s): value got by the function is zero, function returned will crash!" % (file_path, roovar_path))
    def scaler(x):
        '%s, %s' % (file_path, roovar_path)
        return x/value
    return scaler 

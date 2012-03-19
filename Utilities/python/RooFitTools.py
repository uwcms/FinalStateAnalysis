import ROOT
import os
import sys

# Generate missing RooFit iterator dictionaries
# See: http://root.cern.ch/phpBB3/viewtopic.php?f=14&t=11376
current_path = ROOT.gROOT.GetMacroPath()
new_path = ':'.join([
    "$CMSSW_BASE/src/FinalStateAnalysis/Utilities/python/",
    "$CMSSW_BASE/src/FinalStateAnalysis/Utilities/interface/",
    current_path,
])
ROOT.gInterpreter.AddIncludePath(os.environ['ROOFITSYS']+'/include')
ROOT.gROOT.SetMacroPath(new_path)
ROOT.gSystem.AddIncludePath("-I$ROOFITSYS/include")
ROOT.gSystem.SetDynamicPath(
    os.environ['ROOFITSYS'] + "/lib:" + ROOT.gSystem.GetDynamicPath())

ROOT.gROOT.LoadMacro(
    "roofit_iterators.h+"
)


def iter_collection(rooAbsCollection):
    ''' Create a generator over a RooAbsCollection

    >>> import ROOT
    >>> a = ROOT.RooRealVar("a", "a", 1.0, 0, 2)
    >>> b = ROOT.RooRealVar("b", "b", 2.0, 0, 2)
    >>> argset = ROOT.RooArgSet(a, b)
    >>> [ x.getVal() for x in iter_collection(argset) ]
    [1.0, 2.0]
    '''

    iterator = rooAbsCollection.createIterator()
    object = iterator.Next()
    while object:
        yield object
        object = iterator.Next()

def make_stack_arguments(*component_pdfs_and_colors, **kwargs):
    output_argsets = []
    comp_args_names_colors = []
    for i in range(len(component_pdfs_and_colors)):
        #print i
        #print component_pdfs_and_colors
        pdf, color, name = component_pdfs_and_colors[i]
        comp_arg_string = ",".join(
            pdf for pdf, color, name in component_pdfs_and_colors[i:])
        comp_arg = ROOT.RooFit.Components(comp_arg_string)
        fill_arg = ROOT.RooFit.FillColor(color)
        line_arg = ROOT.RooFit.LineColor(color)
        drawopt_arg = ROOT.RooFit.DrawOption("f")
        comp_args_names_colors.append((comp_arg_string, name, color))
        back_arg = ROOT.RooFit.MoveToBack()
        output_argset = [comp_arg, fill_arg, drawopt_arg, line_arg]
        output_argsets.append(output_argset)

    def legend_maker(frame, legend):
        for i in range(int(frame.numItems())):
            name = frame.nameOf(i)
            longest_match = ''
            longest_nice_name = None
            for arg, niceName, color in comp_args_names_colors:
                if arg in name and len(arg) > len(longest_match):
                    longest_match = arg
                    longest_nice_name = niceName
            if longest_nice_name:
                obj = frame.findObject(name)
                legend.AddEntry(obj, longest_nice_name, "f")

    return output_argsets, legend_maker

def make_stack(name, title, xvar, rooAddPdf):
    ''' Build a THStack from a RooAddPdf composite object
    '''
    coefficients = list(iter_collection(pdf.coefList()))
    pdfs = list(iter_collection(rooAddPdf.pdfList()))
    assert(pdfs.size() == coefficients.size())
    output = ROOT.THStack(name, title)
    keep = []
    for coef, pdf in zip(coefficients, pdfs):
        histo = pdf.createHistogram(pdf.getName()+"_histo", xvar)
        coef_val = coef.getVal()
        #print histo.Integral()
        histo.Scale(coef_val)
        #print histo.Integral()
        keep.append(histo)
        #output.Add(

def make_combo_data(name, title, fit_vars, categories, name_data_map):
    ''' Build a combo data set using a category.

    Need to to this complicated mess to work around limitation of number
    of RooCmdArgs that can be passed in the constructor.

    >>> import ROOT
    >>> x = ROOT.RooRealVar("x", "x", 0, -5, 5)
    >>> mean = ROOT.RooRealVar("mu", "mu", 1, 0.0, 2)
    >>> sigma = ROOT.RooRealVar("sig", "sig", 1, 0.0, 2)
    >>> pdf = ROOT.RooGaussian("pdf", "pdf", x, mean, sigma)
    >>> dataA = pdf.generateBinned(ROOT.RooArgSet(x), 100)
    >>> dataB = pdf.generateBinned(ROOT.RooArgSet(x), 100)
    >>> cat = ROOT.RooCategory("catA", "catB")
    >>> combo = make_combo_data("the_name", "title", ROOT.RooArgList(x), cat,
    ...    [("catA",dataA),("catB",dataB)])
    >>> type(combo)
    <class '__main__.RooDataHist'>
    >>> combo.GetName()
    'the_name'

    '''
    keep = []
    names = ROOT.TObjArray()
    histos = ROOT.TObjArray()
    for histoName, histo in name_data_map:
        nameStr = ROOT.TObjString(histoName)
        names.Add(nameStr)
        histos.Add(histo)
        keep.append((nameStr, histo))
    return ROOT.makeComboDataSet(name, title, fit_vars, categories,
                                 names, histos)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

'''

Make the fit functions used to fit the fake rate and put them in a RooWorkspace

Author: Evan K. Friis

'''

import ROOT
import logging

if __name__ == "__main__":
    log = logging.getLogger("make_fit_models")
    logging.basicConfig(level=logging.INFO)

    log.info("Building RooWorkspace")
    ws = ROOT.RooWorkspace("fit_models")
    # Workaround the fact that import is reserved in python
    def ws_import(*args):
        getattr(ws, 'import')(*args)

    x = ROOT.RooRealVar('x', 'The x axis (usually pt)', 100, 0, 200)

    log.info("Defining landau fit model")
    # Landau parameters
    scale = ROOT.RooRealVar("scale", "Landau Scale", 0.5, 0, 10)
    mu = ROOT.RooRealVar("mu", "Landau #mu", 10, 0, 100)
    sigma = ROOT.RooRealVar("sigma", "Landau #sigma", 1, 0.5, 10)
    constant = ROOT.RooRealVar("offset", "constant", 1.0e-2, 0, 1)

    landau_func_str = "scale*TMath::Landau(x,mu,sigma,0)+offset"
    landau_func = ROOT.RooFormulaVar(
        "landau_func", "Fake Rate (Landau)", landau_func_str,
        ROOT.RooArgList(scale, mu, sigma, constant, x))

    ws_import(landau_func)

    log.info("Defining expo fit model")

    expo_func_str = "scale*TMath::Exp(-1*x*mu)+offset"
    expo_func = ROOT.RooFormulaVar(
        "expo_func", "Fake Rate (Exp.)", expo_func_str,
        ROOT.RooArgList(scale, mu, constant, x))

    ws_import(expo_func)

    log.info("Defining optional constraint")
    # This pulls the fits to the left.
    constraint = ROOT.RooRealVar(
        "constraint", "Constraint factor", -0.5, -10, -0)
    constraint.setConstant(True)
    constrain_mu = ROOT.RooExponential("mu_constraint", "Mu constraint",
                                       mu, constraint)
    ws_import(constrain_mu)

    log.info("Defining efficiency helpers")
    roo_cut = ROOT.RooCategory("cut", "cutr")
    roo_cut.defineType("accept", 1)
    roo_cut.defineType("reject", 0)
    ws_import(roo_cut)

    ws.writeToFile("fit_models.root")

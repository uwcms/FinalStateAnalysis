'''
TNPPlotter
=========

Functions to plot the results of TNPFitter output

Author: Evan K. Friis, UW Madison

'''

import ROOT
import os

BASE_DIR = 'plots'

def plot_fit(workspace, fit_results):
    canvas = ROOT.TCanvas("asdf", "asdf", 1200, 600)
    canvas.Divide(2)
    passPdf = workspace.pdf('pdfPass')
    failPdf = workspace.pdf('pdfFail')
    dataPass = workspace.data('pass_binned')
    dataPass = workspace.data('pass_binned')

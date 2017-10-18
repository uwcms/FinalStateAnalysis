#! /usr/bin/env python
__doc__ = '''
Simple script that takes as input one or more json files and produces a limit plot
'''

import rootpy.io as io
from FinalStateAnalysis.Utilities.struct import struct
from FinalStateAnalysis.Utilities.solarized import colors
import FinalStateAnalysis.Utilities.prettyjson as prettyjson
from rootpy.plotting.graph import Graph
import rootpy.plotting as plotting
import rootpy.plotting.views as views
from optparse import OptionParser
import os
import ROOT
import math

def json2graph(json_dict, load_error=None, **kwargs):
    limit   = json_dict['limits']
    ret     = Graph(npoints = len(limit.keys()), **kwargs)
    for i, x in enumerate(sorted(limit.keys())): #fills it (why it is not available in the default constructor???)
        y = limit[x]['median']
        ret.SetPoint(i, float(x), y)
        if load_error:
            eyh = abs(limit[x]['+'+load_error] - y)
            eyl = abs(limit[x]['-'+load_error] - y)
            ret.SetPointError(i, 0, 0, eyl, eyh)
    return ret

parser = OptionParser(description=__doc__)
parser.add_option('--output', '-o', type=str, default = 'limit_plot',
                  help='file name to be used',dest='outfile')
parser.add_option('--xtitle', type=str, default = "m_{H} [GeV]",
                  help='x axis title',dest='xtitle')
parser.add_option('--ytitle', type=str, default = "95% CL limit on #sigma/#sigma_{SM}",
                  help='y axis title',dest='ytitle')
parser.add_option('--xrange', type=str, default = "",
                  help='x range',dest='xrange')
parser.add_option('--yrange', type=str, default = "",
                  help='y range',dest='yrange')
parser.add_option('--logy', action='store_true', dest='logy', default = False,
                  help='log scale on y axis')
parser.add_option('--legend-on-the-left', action='store_true', dest='legend_left', default = False,
                  help='puts the legend on the left')

## parser.add_option('--png', action='store_true', dest='png', default = False,
##                   help='prints in png format')
## parser.add_option('--pdf', action='store_true', dest='pdf', default = False,
##                   help='prints in pdf format')
## parser.add_option('--tex', action='store_true', dest='tex', default = False,
##                   help='prints in LaTex format')
## parser.add_option('--txt', action='store_true', dest='txt', default = False,
##                   help='prints in txt format')
## parser.add_option('--root', action='store_true', dest='root', default = False,
##                   help='prints in root format')
## parser.add_option('--cpp', action='store_true', dest='cpp', default = False,
##                   help='prints in .C format')


(options,jsons) = parser.parse_args()
jmaps= [prettyjson.loads( open(json).read() ) for json in jsons]

exps = [j for j in jmaps if j['kind'] == 'expected']
exp  = exps[0] if len(exps) > 0 else None

obss = [j for j in jmaps if j['kind'] == 'observed']
obs  = obss[0] if len(obss) > 0 else None

canvas   = plotting.Canvas(name='adsf', title='asdf')
to_print = []
one_line = None

if exp:
    to_print.append(
        json2graph(
            exp,
            load_error='2sigma',
            name='2sigma',
            drawstyle = 'A3',
            legendstyle = 'F',
            fillcolor = ROOT.kYellow,
            title = '#pm 2#sigma expected',
            fillstyle = 'solid',
            )
        )
    to_print.append(
        json2graph(
            exp,
            load_error='1sigma',
            name='1sigma',
            drawstyle = '3 SAME',
            legendstyle = 'F',
            fillcolor = ROOT.kGreen,
            title = '#pm 1#sigma expected',
            fillstyle = 'solid',
            )
        )
    to_print.append(
        json2graph(
            exp,
            name='expected',
            drawstyle = 'L SAME',
            legendstyle = 'L',
            linecolor = ROOT.kRed,
            linewidth = 3,
            linestyle = 1,
            title = 'expected'
            )
        )
    mass_points = [i for i in to_print[-1].x()]
    one_line = Graph(
        len(mass_points),
        name='unity',
        drawstyle = 'L SAME',
        inlegend  = False,
        linecolor = ROOT.kBlue,
        linewidth = 3,
        )
    for i, m in enumerate(mass_points):
        one_line.SetPoint(i, m, 1.)


if obs:
    to_print.append(
        json2graph(
            obs,
            name='observed',
            markerstyle = 20,
            markersize  = 1,
            linecolor = ROOT.kBlack,
            linewidth = 3,
            linestyle = 1,
            drawstyle = 'PL SAME' if exp else 'PL',
            legendstyle = 'PL',
            title = 'observed'
            )
        )
    
    if not one_line:
        mass_points = [i for i in to_print[-1].x()]
        one_line = Graph(
            len(mass_points),
            name='unity',
            drawstyle = 'L SAME',
            inlegend  = False,
            linecolor = ROOT.kBlue,
            linewidth = 3,
            )
        for i, m in enumerate(mass_points):
            one_line.SetPoint(i, m, 1.)

to_print[0].GetXaxis().SetTitle(options.xtitle)
to_print[0].GetYaxis().SetTitle(options.ytitle)

if options.xrange:
    r = eval(options.xrange)
    to_print[0].GetXaxis().SetRangeUser(r[0], r[1])
if options.yrange:
    r = eval(options.yrange)
    to_print[0].GetYaxis().SetRangeUser(r[0], r[1])

if options.logy:
    canvas.SetLogy(True)
canvas.SetGridx()
canvas.SetGridy()

for graph in to_print:
    graph.Draw()

one_line.Draw()

legend = plotting.Legend(len(to_print), rightmargin=0.07, topmargin=0.05, leftmargin=0.45) \
    if not options.legend_left else \
    plotting.Legend(len(to_print), leftmargin=0.03, topmargin=0.05, rightmargin=0.65)
legend.SetEntrySeparation(0.0)
legend.SetMargin(0.35)

for graph in to_print[::-1]:
    legend.AddEntry(graph)

legend.Draw()
canvas.SaveAs(options.outfile+'.png')
canvas.SaveAs(options.outfile+'.pdf')

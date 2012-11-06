import ROOT
from THBin import zipBins
import array

def HistToTGRaphErrors(h):
    'Transforms a TH1/ rootpy.THist into a TGRaphErrors with same values and errors'
    x, y, ex, ey = (array.array('d',[]), array.array('d',[]), array.array('d',[]), array.array('d',[]) )
    for ibin in zipBins(h):
        x.append( ibin.center )
        y.append( ibin.content )
        ex.append( ibin.width / 2. )
        ey.append( ibin.error )
    gr = ROOT.TGraphErrors(len(x),x,y,ex,ey)
    gr.SetTitle( h.GetTitle() )
    gr.SetMarkerColor( h.GetMarkerColor() )
    gr.SetMarkerStyle( h.GetMarkerStyle() )
    #gr.SetFillColor( h.GetFillColor() )
    return gr

def HistStackToTGRaphErrors(stack):
    'Transforms a rootpy.HistStack into a TGRaphErrors with same values and errors'
    return HistToTGRaphErrors( sum(stack.GetHists()) )

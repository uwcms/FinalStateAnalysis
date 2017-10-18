import ROOT

def cms_preliminary(int_lumi, is_preliminary=True, lumi_on_top=False):
    # Objects that shouldn't be GC'ed
    keep = []
    latex = ROOT.TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    keep.append(latex.DrawLatex(0.90,0.96,"#sqrt{s} = 7 TeV"));
    if int_lumi > 0. and not lumi_on_top:
        #latex.SetTextAlign(31);
        latex.SetTextAlign(11);
        keep.append(latex.DrawLatex(
            0.90,0.96,
            "%.1f fb^{-1} at #sqrt{s} = 7 TeV" % (int_lumi/1000.0)
        ));
    else:
        keep.append(latex.DrawLatex(0.90,0.96, "#sqrt{s} = 7 TeV"));

    latex.SetTextAlign(11);
    label_text = "CMS preliminary"
    if not is_preliminary:
        label_text = "CMS"
    if lumi_on_top:
        label_text += " L = %.1f fb^{-1}" % (int_lumi/1000.0)
    keep.append(latex.DrawLatex(0.18,0.96, label_text));
    #latex.DrawLatex(0.18,0.96,"CMS 2010");
    return latex

class RootColor(object):
    colors_added = {}
    def __init__(self, r, g, b):
        if (r, g, b) in self.colors_added:
            self.color = self.colors_added[(r,g,b)]
        else:
            # Convert each to float
            def floatify(x):
                if isinstance(x, int):
                    x = x/255.0
                return x
            float_r = floatify(r)
            float_g = floatify(g)
            float_b = floatify(b)
            index = 1500
            if self.colors_added:
                index = max(
                    x.GetNumber() for x in self.colors_added.values())+1
            self.color = ROOT.TColor(index, float_r, float_g, float_b)
            self.colors_added[(r, g, b)] = self.color
        self.code = self.color.GetNumber()

    def r(self):
        return self.color.GetRed()
    def g(self):
        return self.color.GetGreen()
    def b(self):
        return self.color.GetBlue()

    def h(self):
        return self.color.GetHue()
    def s(self):
        return self.color.GetSaturation()
    def l(self):
        return self.color.GetLight()

    def hls2rgb(self, h, l, s):
        #r, g, b = ROOT.Float(-1), ROOT.Float(-1), ROOT.Float(-1)
        #print r
        #self.color.HLS2RGB(h, l, s, r, g, b)
        # See http://root.cern.ch/phpBB3/viewtopic.php?t=7151
        from ctypes import c_float, POINTER, CFUNCTYPE
        c_float_p = POINTER( c_float )
        TRGB2HSV = CFUNCTYPE( None, c_float, c_float, c_float, c_float_p, c_float_p, c_float_p )
        RGB2HSV = TRGB2HSV( ROOT.gROOT.ProcessLine( "TColor::HLS2RGB" ) )
        r, g, b = c_float(), c_float(), c_float()
        RGB2HSV(h, l, s, r, g, b)
        return (float(r.value), float(g.value), float(b.value))

    def lighter(self, fraction):
        # Make a lighter version
        h = self.h()
        l = self.l()
        s = self.s()
        l *= fraction
        r, g, b = self.hls2rgb(h, l, s)
        return RootColor(r, g, b)


colors = {
    'ewk_yellow' : RootColor(255, 204, 51),
    'ewk_dark_yellow' : RootColor(191, 153, 38),
    'ewk_orange' : RootColor(255, 102, 0),
    'ewk_purple' : RootColor(153, 51, 204),
    'ewk_light_purple' : RootColor(153, 51, 204).lighter(1.5),
    'ewk_red' : RootColor(153, 0, 0),
    'light_blue' : RootColor(102, 255, 255),
    'med_blue' : RootColor(0, 153, 255),
    'blue' : RootColor(0, 0, 255),
    'red' : RootColor(255, 0, 0),
    'green_blue' : RootColor(0, 255, 153),
    'white' : RootColor(255, 255, 255),
    'black' : RootColor(0, 0, 0),
    'grey' : RootColor(150, 150, 150),
}

ewk_colors = [
    color for name, color in colors.iteritems() if 'ewk' in name
]

def apply_style(th1, **kwargs):
    if 'color' in kwargs:
        if hasattr(kwargs['color'], 'code'):
            th1.SetFillColor(kwargs['color'].code)
            th1.SetLineColor(kwargs['color'].code)
        else:
            th1.SetFillColor(kwargs['color'])
            th1.SetLineColor(kwargs['color'])

        th1.SetFillStyle(1)
    if 'marker_size' in kwargs:
        th1.SetMarkerSize(kwargs['marker_size'])
    if 'marker_style' in kwargs:
        th1.SetMarkerStyle(kwargs['marker_style'])
    if 'draw_opt' in kwargs:
        th1.SetOption(kwargs['draw_opt'])
    if 'line_width' in kwargs:
        th1.SetLineWidth(kwargs['line_width'])
    if 'line_color' in kwargs:
        if hasattr(kwargs['line_color'], 'code'):
            th1.SetLineColor(kwargs['line_color'].code)
        else:
            th1.SetLineColor(kwargs['line_color'])
    if 'fill_color' in kwargs:
        if hasattr(kwargs['fill_color'], 'code'):
            th1.SetFillColor(kwargs['fill_color'].code)
        else:
            th1.SetFillColor(kwargs['fill_color'])
    if 'fill_style' in kwargs:
        th1.SetFillStyle(kwargs['fill_style'])
    th1.SetFillStyle(1001)



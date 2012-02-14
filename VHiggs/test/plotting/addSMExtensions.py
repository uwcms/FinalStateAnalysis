#!/usr/bin/env python

'''

Add signal templates scaled to correspond to the FF and SM4 models.


'''

import ROOT
import re
from rootpy.io import open
import logging
import sys

log = logging.getLogger("statshapes")
logging.basicConfig(level=logging.INFO)

ROOT.gSystem.AddIncludePath('-IHCSaW/Higgs_CS_and_Width_Fermiophobic/include')
ROOT.gSystem.AddIncludePath('-IHCSaW/Higgs_CS_and_Width/include')
ROOT.gSystem.AddIncludePath('-IHCSaW/Higgs_CS_and_Width_SM4/include')

ROOT.gROOT.ProcessLine('.L HCSaW/Higgs_CS_and_Width_SM4/src/HiggsCSandWidthSM4.cc+')
ROOT.gROOT.ProcessLine('.L HCSaW/Higgs_CS_and_Width/src/HiggsCSandWidth.cc+')
ROOT.gROOT.ProcessLine('.L HCSaW/Higgs_CS_and_Width_Fermiophobic/src/HiggsCSandWidthFermi.cc+')

# Define the lookup tables
_sm = ROOT.HiggsCSandWidth();
_ff = ROOT.HiggsCSandWidthFermi()
_sm4 = ROOT.HiggsCSandWidthSM4()


def get_FF_correction(mass):
    ''' Returns a tuple w/ scale factors for Htautau and HWW '''
    ff_hww_br = _ff.HiggsWidth(10, mass)/_ff.HiggsWidth(0, mass)
    sm_hww_br = _sm.HiggsWidth(10, mass)/_sm.HiggsWidth(0, mass)
    return 0.0, ff_hww_br/sm_hww_br

def get_SM4_correction(mass):
    ''' Returns a tuple w/ scale factors for Htautau and HWW '''
    sm4_hww_br = _sm4.HiggsWidth(10, mass)/_sm4.HiggsWidth(0, mass)
    sm_hww_br = _sm.HiggsWidth(10, mass)/_sm.HiggsWidth(0, mass)

    sm4_htt_br = _sm4.HiggsWidth(2, mass)/_sm4.HiggsWidth(0, mass)
    sm_htt_br = _sm.HiggsWidth(2, mass)/_sm.HiggsWidth(0, mass)

    # WH xsec is the same in both
    xsec_scale = 1

    return xsec_scale*(sm4_htt_br/sm_htt_br), xsec_scale*(sm4_hww_br/sm_hww_br)

def update_file(f):
    for thing in f.walk(class_pattern='TH1*'):
        path, subdirs, histos = thing
        directory = f.get(path)
        directory.cd()

        log.info("==> examining directory %s", path)
        if not histos:
            continue

        vhtt_matcher = re.compile('VH(?P<mass>\d+)$')
        vhww_matcher = re.compile('VH(?P<mass>\d+)WW$')
        for histo in histos:
            vhtt_match = vhtt_matcher.match(histo)
            vhww_match = vhww_matcher.match(histo)
            if vhtt_match:
                # Correct the VHtautau cass
                mass = int(vhtt_match.group('mass'))
                ff_corr, _ = get_FF_correction(mass)
                sm4_corr, _ = get_SM4_correction(mass)
                sm_histo = directory.Get(histo)
                ff_histo = sm_histo.Clone(histo + 'FF')
                sm4_histo = sm_histo.Clone(histo + 'SM4')
                ff_histo.Scale(ff_corr)
                sm4_histo.Scale(sm4_corr)
                ff_histo.Write(ff_histo.GetName(), ROOT.TObject.kOverwrite)
                sm4_histo.Write(sm4_histo.GetName(), ROOT.TObject.kOverwrite)

            elif vhww_match:
                # Correct the VHWW cass
                mass = int(vhww_match.group('mass'))
                _, ff_corr = get_FF_correction(mass)
                _, sm4_corr = get_SM4_correction(mass)
                sm_histo = directory.Get(histo)
                ff_histo = sm_histo.Clone(histo + 'FF')
                sm4_histo = sm_histo.Clone(histo + 'SM4')
                ff_histo.Scale(ff_corr)
                sm4_histo.Scale(sm4_corr)
                ff_histo.Write(ff_histo.GetName(), ROOT.TObject.kOverwrite)
                sm4_histo.Write(sm4_histo.GetName(), ROOT.TObject.kOverwrite)

if __name__ == "__main__":
    filename = sys.argv[1]
    log.info("Updating file: %s", filename)
    f = open(filename, 'update')
    update_file(f)

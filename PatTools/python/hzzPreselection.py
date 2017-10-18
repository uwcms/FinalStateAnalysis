"""
String-based preselections for HZZ4L leptons.

Author D. Austin Belknap, UW Madison
"""

def getStrings():
    """
    Return the muon and electron selection strings
    """
    muon_string = ( 
            'pt > 5.0 &'
            'abs(eta) < 2.4 &'
            'userFloat("ipDXY") < 0.5 &'
            'userFloat("dz") < 1.0 &'
            '(isGlobalMuon | isTrackerMuon) &'
            'abs(userFloat("ip3DS")) < 4.0 &'
            'pfCandidateRef().isNonnull()' )
    
    elec_string = (
            'pt > 7.0 &'
            'abs(superCluster().eta) < 2.5 &'
            'userFloat("ipDXY") < 0.5 &'
            'userFloat("dz") < 1.0 &'
            'gsfTrack().trackerExpectedHitsInner().numberOfHits() <= 1 &'
            'abs(userFloat("ip3DS")) < 4.0' )
    
    elec_mva = ('('
            '(5 < pt & pt < 10 &'
                '((abs(superCluster().eta) < 0.8 & electronID("mvaNonTrigV0") > 0.47) |'
                '(0.8 < abs(superCluster().eta) & abs(superCluster().eta) < 1.479 & electronID("mvaNonTrigV0") > 0.004) |'
                '(1.479 < abs(superCluster().eta) & electronID("mvaNonTrigV0") > 0.295) ) ) |'
            '(10 < pt &'
                '((abs(superCluster().eta) < 0.8 & electronID("mvaNonTrigV0") > -0.34) |'
                '(0.8 < abs(superCluster().eta) & abs(superCluster().eta) < 1.479 & electronID("mvaNonTrigV0") > -0.65) |'
                '(1.479 < abs(superCluster().eta) & electronID("mvaNonTrigV0") > 0.6) ) )'
                ')' )
    
    elec_string = elec_string + '&' + elec_mva

    return (muon_string, elec_string)

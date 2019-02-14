#############################################################################
#                                                                           #
#        uniqueness_cut_generator.py                                        #
#                                                                           #
#        Returns a dictionary of cuts specifying how we remove unwanted     #
#            final states from FSA ntuples. Formerly a long block of        #
#            code in ntuple_builder.py.                                     #
#        Skim cuts and other options (e.g. hzz, dblH) may be specified      #
#            with keyword arguments.                                        #
#                                                                           #
#        Ported from ntuple_builder.py by Nate Woods, U. Wisconsin.         #
#                                                                           #
#############################################################################


from collections import OrderedDict


object_order_ = 'emtgj'

def uniqueness_cuts(channel, ptCuts={'e':'0','m':'0','t':'0','g':'0','j':'0'},
                    etaCuts={'e':'10','m':'10','t':'10','g':'10','j':'10'},
                    **kwargs):
    '''
    Cut strings are returned in the order they should be done, keyed to the
    appropriate name (for purposes of cut flow histograms, etc.).
    '''
    cuts = OrderedDict()

    # sort channel objects
    channel = sorted(channel, key=lambda x: object_order_.index(x))

    # count legs of each type and make sure all are valid
    counts = OrderedDict()
    for leg in channel:
        if leg not in counts:
            counts[leg] = 1
        else:
            counts[leg] += 1
        assert leg in ptCuts and leg in etaCuts, "Invalid object %s in channel %s"%(leg, channel)

    # Pt and eta cuts on all legs
    for i, leg in enumerate(channel):
        cuts["Leg%dPt"%i] = 'daughter(%d).pt > %s'%(i,ptCuts[leg])
        cuts["Leg%dEta"%i] = 'abs(daughter(%d).eta) < %s'%(i,etaCuts[leg])

    # optional other selections
    for skimCut in kwargs.get('skimCuts', []):
        cuts[skimCut] = skimCut

    # Cuts specific to the number of objects of a given type are placed 
    # into cut dictionary in situ
    firstIndex = 0
    for obj, count in counts.iteritems():
        if count == 2:
            uniqueness_2(cuts, obj, firstIndex, **kwargs)
        elif count == 3:
            uniqueness_3(cuts, obj, firstIndex, **kwargs)
        elif count == 4:
            uniqueness_4(cuts, obj, firstIndex, **kwargs)
        elif count == 5:
            uniqueness_5(cuts, obj, firstIndex, **kwargs)
        firstIndex += count
        
    return cuts


def uniqueness_2(cuts, obj, firstIndex, **kwargs):
    '''
    Order the objects by pt.
    '''
    cuts['%s_UniqueByPt'%obj] = 'orderedInPt(%d, %d)'%(firstIndex, firstIndex+1)
    

def uniqueness_3(cuts, obj, firstIndex, **kwargs):
    '''
    Put the best Z candidate first, and order the first two objects by pt.
    '''
    idx = [firstIndex + x for x in range(3)]

    hzz = kwargs.get("hzz", False)
    zh = kwargs.get("zh", False)

    if hzz:
        cutstr = 'zCompatibilityWithUserCands(%d, %d, "dretFSRCand") < zCompatibilityWithUserCands(%d, %d, "dretFSRCand")'
    elif zh:
        cutstr = 'likeSigned(%d, %d) <= likeSigned(%d, %d)'
    else:
        cutstr = 'zCompatibility(%d, %d) < zCompatibility(%d, %d)'

    cuts['Z12_Better_Z13'] = cutstr%(idx[0], idx[1], idx[0], idx[2])

    cuts['Z12_Better_Z23'] = cutstr%(idx[0], idx[1], idx[1], idx[2])
    
    cuts['%s_UniqueByPt'%obj] = 'orderedInPt(%d, %d)'%(idx[0], idx[1])


def uniqueness_4(cuts, obj, firstIndex, **kwargs):
    '''
    Put the best Z first, order the first and second by pt, order the third and fourth by pt.
    
    In hzz mode, it's the same except that we only care about ordering the Z candidates, not
    removing redundant ones.

    In dblH mode, the first two must be positive, the third and fourth must be negative, and 
    both pairs are ordered by pt.
    '''
    idx = [firstIndex + x for x in range(4)]

    if kwargs.get('dblH', False):
        cuts['hpp12_and_hmm34'] = 'hppCompatibility(%d, %d, 1) && hppCompatibility(%d, %d, -1)'%(idx[0],
                                                                                                 idx[1],
                                                                                                 idx[2],
                                                                                                 idx[3])
        return

    hzz = kwargs.get("hzz", False)

    if hzz:
        cutstr = 'zCompatibilityWithUserCands(%d, %d, "dretFSRCand") < zCompatibilityWithUserCands(%d, %d, "dretFSRCand")'
    else:
        cutstr = 'zCompatibility(%d, %d) < zCompatibility(%d, %d)'

    if not hzz:
        cuts['Z12_Better_Z13'] = cutstr%(idx[0], idx[1], idx[0], idx[2])
        cuts['Z12_Better_Z23'] = cutstr%(idx[0], idx[1], idx[1], idx[2])
        cuts['Z12_Better_Z14'] = cutstr%(idx[0], idx[1], idx[0], idx[3])
        cuts['Z12_Better_Z24'] = cutstr%(idx[0], idx[1], idx[1], idx[3])

    cuts['Z12_Better_Z34'] = cutstr%(idx[0], idx[1], idx[2], idx[3])
    cuts['%s_UniqueByPt12'%obj] = 'orderedInPt(%d, %d)'%(idx[0], idx[1])
    cuts['%s_UniqueByPt34'%obj] = 'orderedInPt(%d, %d)'%(idx[2], idx[3])


def uniqueness_5(cuts, obj, firstIndex, **kwargs):
    '''
    Put the best Z first, order the first and second by pt, order the third and fourth by pt.
    
    In hzz mode, it's the same except that we only care about ordering the Z candidates, not
    removing redundant ones.

    In dblH mode, the first two must be positive, the third and fourth must be negative, and 
    both pairs are ordered by pt.
    '''
    idx = [firstIndex + x for x in range(5)]
    cuts['%s_UniqueByPt12'%obj] = 'orderedInPt(%d, %d)'%(idx[0], idx[1])
    cuts['%s_UniqueByPt13'%obj] = 'orderedInPt(%d, %d)'%(idx[0], idx[2])
    cuts['%s_UniqueByPt14'%obj] = 'orderedInPt(%d, %d)'%(idx[0], idx[3])
    cuts['%s_UniqueByPt15'%obj] = 'orderedInPt(%d, %d)'%(idx[0], idx[4])
    cuts['%s_UniqueByPt23'%obj] = 'orderedInPt(%d, %d)'%(idx[1], idx[2])
    cuts['%s_UniqueByPt24'%obj] = 'orderedInPt(%d, %d)'%(idx[1], idx[3])
    cuts['%s_UniqueByPt25'%obj] = 'orderedInPt(%d, %d)'%(idx[1], idx[4])
    cuts['%s_UniqueByPt34'%obj] = 'orderedInPt(%d, %d)'%(idx[2], idx[3])
    cuts['%s_UniqueByPt35'%obj] = 'orderedInPt(%d, %d)'%(idx[2], idx[4])
    cuts['%s_UniqueByPt45'%obj] = 'orderedInPt(%d, %d)'%(idx[3], idx[4])


#############################################################################
#                                                                           #
#   channel_handling.py                                                     #
#                                                                           #
#   Some functions to handle the various decay channels, the groups they    #
#   inhabit, and the objects in them.                                       #
#                                                                           #
#   Nate Woods, U. Wisconsin                                                #
#                                                                           #
#############################################################################



_FINAL_STATE_GROUPS = {
    'zh': ['eeem', 'eeet', 'eemt', 'eett', 'emmm', 'emmt', 'mmmt', 'mmtt'],
    'zz': ['eeee', 'eemm', 'mmmm'],
    'zgg': ['eegg', 'mmgg'],
    'llt': ['emt', 'mmt', 'eet', 'mmm', 'emm', 'mm', 'ee', 'em'],
    'zg': ['mmg', 'eeg'],
    'zgxtra': ['mgg', 'emg', 'egg'],
    'dqm': ['e', 'm', 't', 'g', 'j'],
    '3lep': ['eee', 'eem', 'eet', 'emm', 'emt', 'ett', 
             'mmm', 'mmt', 'mtt', 'ttt'],
    '4lep': ['eeee', 'eeem', 'eeet', 'eemm', 'eemt', 'eett', 'emmm', 
             'emmt', 'emtt', 'ettt', 'mmmm', 'mmmt', 'mmtt', 'mttt', 'tttt'],
}


def order_final_state(state):
    '''
    Sorts final state objects into order expected by FSA.
    
    Sorts string of characters into ordr defined by "order." Invalid 
    characters are ignored, and a warning is printed to stdout
    
    returns the sorted string
    '''
    order = "emtgj"
    for obj in state:
        if obj not in order:
            print "invalid Final State object "\
                "'%s' ignored" % obj
            state = state.replace(obj, "")
    return ''.join(sorted(state, key=lambda x: order.index(x)))
 

def parseChannels(channels):
    '''
    Take a comma-separated string or listlike iterable of such strings 
    indicating one or more channels or groups of channels, and yield
    the individual channels. String can contain groups.
    '''
    if isinstance(channels, str):
        chanList = [c.strip() for c in channels.lower().split(',')]
        for ch in chanList:
            if ch in _FINAL_STATE_GROUPS:
                for c in _FINAL_STATE_GROUPS[ch]:
                    yield c
            else:
                yield order_final_state(ch)
    else:
        try:
            for ch in channels:
                for c in parseChannels(ch):
                    yield c
        except TypeError:
            print ("I only know how to deal with channels given as strings or "
                   "listlike iterables of strings")
            raise

_channel_handling_object_map_ = {}
def mapObjects(channel):
    '''
    From a channel of the form 'eemm' or 'eet', return a list of objects of 
    the form ['e1','e2','m1','m2'] or ['e1','e2','t'].
    Objects are in the order of the channel.
    '''
    try:
        return _channel_handling_object_map_[channel]
    except KeyError:
        nObjects = OrderedDict()
        counters = {}
        
        for obj in set(channel):
            nObjects[obj] = channel.count(obj)
            counters[obj] = 1
    
        objects = []
        for obj in channel:
            if nObjects[obj] == 1:
                objects.append(obj)
            else:
                objects.append(obj+str(counters[obj]))
                counters[obj] += 1
        
        # global declaration not needed
        _channel_handling_object_map_[channel] = objects
        return objects

from FinalStateAnalysis.NtupleTools.ntuple_builder import _producer_translation
def get_channel_suffix(state):
    '''
    Returns the suffix FSA puts on the end of produer and class names, e.g.
    "ElecElecMuTau" for final state 'eemt'.
    Doesn't sort, so state should already be in the right order.
    '''
    return ''.join(_producer_translation[obj] for obj in state)



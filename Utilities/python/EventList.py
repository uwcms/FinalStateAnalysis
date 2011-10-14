import FWCore.ParameterSet.Config as cms
import re

_matcher = re.compile('^(?P<run>\d+):(?P<lumi>\d+):(?P<evt>\d+)')

class EventList(object):
    ''' Build a framework VEventRange from a file containing run:lumi:evt keys.
    >>> class MockFile(object):
    ...    def readlines(self):
    ...        for x in range(3):
    ...            yield '155:%i:%i' % (x*2, x)
    >>> mockfile = MockFile()
    >>> evt_list = EventList(mockfile)
    >>> evt_list.eventRange()
    cms.untracked.VEventRange("155:0:0", "155:2:1", "155:4:2")
    '''
    def __init__(self, file):
        self.file = file
        line_no = 0
        self.run_lumi_evts = []
        for line in self.file.readlines():
            line_no += 1
            line = line.strip()
            # skip blanks
            if not line:
                continue
            match = _matcher.match(line)
            if not match:
                raise ValueError("Could not parse line %i: %s"
                                 % (line_no, line))
            run_lumi_evt = tuple(
                int(match.group(x)) for x in ['run', 'lumi', 'evt'])
            self.run_lumi_evts.append(run_lumi_evt)
    def eventRange(self):
        output = cms.untracked.VEventRange()
        for run_lumi_evt in self.run_lumi_evts:
            output.append(':'.join(map(str,run_lumi_evt)))
        return output

if __name__ == "__main__":
    import doctest
    doctest.testmod()

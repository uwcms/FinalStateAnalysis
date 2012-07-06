'''

A rootpy histogram "view" which blinds out histos whose path matches a regex.

Author: Evan K. Friis, UW Madison

'''

from rootpy.plotting import views
import re

class BlindView(views._FolderView):
    def __init__(self, directory, regex):
        super(BlindView, self).__init__(directory)
        self.regex = re.compile(regex)

    def apply_view(self, thingy):
        # Set in base class
        path = self.getting
        if self.regex.match(path):
            # We need to blind
            clone = thingy.Clone()
            clone.Reset() # Remove entries
            return clone
        # Not blinded
        return thingy

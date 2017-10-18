'''

An easier way to open a group of files and sum them together.  Supports globs.

Author: Evan K. Friis, UW Madison

Example:

    FileView("path/to/file1.root", "path/to/file2.root", "path/to/files*.root")

'''

import glob
from rootpy import io
from rootpy.plotting import views

class FileView(views.SumView):
    def __init__(self, *paths):
        self.filenames = []
        for path in paths:
            self.filenames.extend(glob.glob(path))
        self.files = []
        for filename in self.filenames:
            self.files.append(io.open(filename, 'read'))
        # Sum them together.
        super(FileView, self).__init__(**self.files)

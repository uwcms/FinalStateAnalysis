''' Utilities to find data using the $MEGAPATH search path

Author: Evan K. Friis, UW Madison

'''

import logging
import os

# Where to look for files.
SEARCH_PATHS = ['.'] + os.environ.get("MEGAPATH", "").split(':')
log = logging.getLogger(__name__)


def resolve_file(path, nolocal=False):
    """ Mangle an input path string for ROOT consumption.

    If nolocal is True, don't look in non-HDFS directories.

    """
    if path.startswith('root://'):
        return path
    if not os.path.isabs(path):
        for search_path in SEARCH_PATHS:
            if nolocal and '/store' not in search_path:
                continue
            full_path = os.path.join(search_path, path)
            if os.path.isfile(full_path):
                path = full_path
                break
    return path


def find_input_files(input_file_list, nolocal=False):
    """ Generate all of the input files given the input_file_list.

    If input_file_list ends with '.txt', use it as an input list.
    Otherwise, treat it as a comma separated list of files.

    If the files have relative paths, search through the paths in $MEGAPATH
    (colon separated)for the first directory containing the desired file.


    """

    if '.txt' in input_file_list:
        log.info("Checking inputs file %s exists..." % input_file_list)
        # Get the inputs to make sure it exists
        if not os.path.exists(input_file_list):
            log.error(
                "Error: inputs %s input file does not exist", input_file_list)
            sys.exit(5)
        with open(input_file_list) as inputs_file:
            for line in inputs_file:
                line = line.strip()
                if line and not line.startswith('#'):
                    yield resolve_file(line, nolocal)
    else:
        for x in input_file_list.split(','):
            yield resolve_file(x.strip(), nolocal)

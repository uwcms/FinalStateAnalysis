'''

A multiprocessor Process object which takes an input list of files,
analyzes, them, and stores the results in output ROOT files.

'''

from FileProcessor import FileProcessor
from ChainProcessor import ChainProcessor
import hashlib
import multiprocessing
import os
import signal
import tempfile

def make_hashed_filename(to_process):
    ''' Make an output file from the hash of the file(s) to process '''
    hash = hashlib.md5(os.environ['LOGNAME']) # so users don't collide
    if isinstance(to_process, basestring):
        hash.update(to_process)
        return hash.hexdigest() + '.root'
    else:
        for input_file in to_process:
            hash.update(input_file)
        return hash.hexdigest() + '.root'

class MegaWorker(multiprocessing.Process):
    log = multiprocessing.get_logger()
    def __init__(self, input_file_queue, results_queue, treename, selector,
                 output_dir=None, **kwargs):
        super(MegaWorker, self).__init__()
        self.input = input_file_queue
        self.output = results_queue
        self.tree = treename
        self.selector = selector
        self.output_dir = output_dir
        if self.output_dir is None:
            self.output_dir = tempfile.gettempdir()
        # Passed to selector
        self.options = kwargs

    def run(self):
        # ignore sigterm signal and let parent take care of this
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        while True:
            to_process = self.input.get()
            # Poison pill
            if to_process is None:
                self.log.info("Got poison pill - shutting down")
                break

            # Make a unique output file name
            output_file_name = os.path.join(
                self.output_dir, make_hashed_filename(to_process))

            # Do we need to chain the files or not?
            processor_class = FileProcessor
            if isinstance(to_process, basestring):
                self.log.info("Processing file %s => %s",
                              to_process, output_file_name)
            else:
                processor_class = ChainProcessor
                self.log.info("Processing %i files => %s",
                              len(to_process), output_file_name)

            try:
                processor = processor_class(
                    to_process, self.tree, self.selector,
                    output_file_name, self.log, **self.options)

                # Check if we want to profile the script
                profile_dir_base = os.environ.get('megaprofile', None)
                result = None
                if profile_dir_base is None:
                    result = processor.process()
                else:
                    import cProfile
                    profile_dir = os.path.join(
                        profile_dir_base,
                        self.selector.__name__,
                    )
                    if not os.path.exists(profile_dir):
                        os.makedirs(profile_dir)
                    profile_output = os.path.join(
                        profile_dir,
                        make_hashed_filename(to_process).replace('.root', '.prf')
                    )
                    cProfile.runctx('result = processor.process()',
                                    globals(), locals(), profile_output)
                    # Fake this.
                    result = (len(to_process), output_file_name)
                self.output.put(result)
            except:
                # If we fail, put a poison pill to stop the merge job.
                self.log.error("Caught exception in worker, killing merger")
                self.output.put(None)
                raise

'''

A multiprocessor Process object which takes an input list of files,
analyzes, them, and stores the results in output ROOT files.

'''

from FileProcessor import FileProcessor
import hashlib
import multiprocessing
import os
import signal
import tempfile

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
                self.output_dir,
                hashlib.md5(to_process).hexdigest() + '.root')

            self.log.info("Processing file %s => %s",
                          to_process, output_file_name)

            try:
                processor = FileProcessor(to_process, self.tree, self.selector,
                                          output_file_name, self.log,
                                          **self.options)
                result = processor.process()
                self.output.put(result)
            except:
                # If we fail, put a poison pill to stop the merge job.
                self.log.error("Caught exception in worker, killing merger")
                self.output.put(None)
                raise

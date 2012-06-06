'''

A Process object which takes a list of files and hadd's them together.

Author: Evan K. Friis, UW Madison

'''

import hashlib
import multiprocessing
import os
from progressbar import ETA, ProgressBar, FormatLabel, Bar
from Queue import Empty
import shutil
import signal
import subprocess
import tempfile

class MegaMerger(multiprocessing.Process):
    log = multiprocessing.get_logger()
    def __init__(self, input_file_queue, output_file, ninputs):
        super(MegaMerger, self).__init__()
        self.input = input_file_queue
        self.output = output_file
        self.first_merge = True
        self.ninputs = ninputs
        self.processed = 0
        self.pbar = ProgressBar(widgets=[
            FormatLabel('Processed %(value)i/' + str(ninputs) + ' files. '),
            ETA(), Bar('>')], maxval=ninputs).start()
        self.pbar.update(0)
        self.processed_entries = 0
        self.procs_to_clean = None
        self.files_to_clean = None

    def merge_into_output(self, files):
        self.files_to_clean = list(files)
        self.log.info("Merging %i into output %s", len(files), self.output)
        # Merge into a temporary output file
        output_file_hash = hashlib.md5()
        for file in files:
            output_file_hash.update(file)

        output_file_name = os.path.join(
            tempfile.gettempdir(),
            output_file_hash.hexdigest() + '.root')

        command = ['hadd', output_file_name]

        # If we are doing a later merge, we need to include the
        # "merged-so-far"
        if self.first_merge:
            self.first_merge = False
        else:
            command.append(self.output)

        for file in files:
            command.append(file)

        # Now run the command
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        self.procs_to_clean = proc

        while proc.returncode is None:
            _, stderr = proc.communicate()
        self.log.info("Merge completed with exit code: %i", proc.returncode)
        self.log.info("Output file is: %s, moving to %s", output_file_name,
                      self.output)
        shutil.move(output_file_name, self.output)
        self.log.info("Processed %i entries so far", self.processed_entries)

        # Cleanup.  We don't need to cleanup the temporary output, since it
        # is moved.
        while self.files_to_clean:
            os.remove(self.files_to_clean.pop())
        return proc.returncode

    def stop(self):
        ''' Gracefully stop, killing any child hadds '''
        self.log.warning("STOPPING Merger process")
        if self.procs_to_clean:
            self.log.warning("Killing child hadd process")
            self.procs_to_clean.kill()
        if self.files_to_clean:
            self.log.warning("Deleting temporary root files")
            for file in files:
                if os.path.exists(file):
                    os.remove(file)

    def run(self):
        # ignore sigterm signal and let parent take care of this
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        while True:
            # Check if we are done merging
            done = False
            inputs_to_merge = []
            # Accumulate some files to merge
            while True:
                try:
                    self.log.debug("trying to get")
                    to_merge = self.input.get(timeout=1)
                    self.log.debug("got %s", to_merge)
                    # Check for poison pill
                    if to_merge is None:
                        self.log.info("Got poison pill - shutting down")
                        done = True
                        break
                    inputs_to_merge.append(to_merge)
                    self.processed += 1
                    self.pbar.update(self.processed)
                    # Make it merge the files if the queue is stacking up.
                    if len(inputs_to_merge) > 15:
                        break
                except Empty:
                    self.log.debug("empty to get")
                    # Noting to merge right now
                    break
            if inputs_to_merge:
                files_to_merge = []
                for entries, file in inputs_to_merge:
                    self.processed_entries  += entries
                    files_to_merge.append(file)
                self.merge_into_output(files_to_merge)
            if done:
                return

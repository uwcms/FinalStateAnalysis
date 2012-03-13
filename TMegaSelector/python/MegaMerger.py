'''

A Process object which takes a list of files and hadd's them together.

Author: Evan K. Friis, UW Madison


'''

import multiprocessing
from Queue import Empty
import signal
import subprocess
import os

class MegaMerger(multiprocessing.Process):
    log = multiprocessing.get_logger()
    def __init__(self, input_file_queue, output_file):
        super(MegaMerger, self).__init__()
        self.input = input_file_queue
        self.output = output_file
        self.first_merge = True

    def merge_into_output(self, files):
        self.log.info("Merging %i into output %s", len(files), self.output)
        command = ['hadd', '-f', self.output]
        # If we are doing a later merge, we need to include the
        # "merged-so-far"
        if not self.first_merge:
            command.append(self.output)
            self.first_merge = False

        for file in files:
            command.append(file)

        print command
        # Now run the command
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        while proc.returncode is None:
            _, stderr = proc.communicate()
        self.log.info("Merge completed with exit code: %i", proc.returncode)
        # Cleanup
        for file in files:
            os.remove(file)
        return proc.returncode

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
                    self.log.info("trying to get")
                    to_merge = self.input.get(timeout=2)
                    self.log.info("got %s", to_merge)
                    self.input.task_done()
                    # Check for poison pill
                    if to_merge is None:
                        self.log.info("Got poison pill - shutting down")
                        done = True
                        break
                    inputs_to_merge.append(to_merge)
                except Empty:
                    self.log.info("empty to get")
                    # Noting to merge right now
                    break
            if inputs_to_merge:
                self.merge_into_output([x[1] for x in inputs_to_merge])
            if done:
                return

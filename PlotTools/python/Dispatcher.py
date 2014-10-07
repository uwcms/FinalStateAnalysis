'''

Process dispatcher function for Mega framework

'''

import multiprocessing
from MegaWorker import MegaWorker
from MegaMerger import MegaMerger
import sys
import errno

def group_list(files, n=1):
    ''' Merge an iterable into groups of N '''
    if n==1:
        for file in files:
            yield file
    else:
        clump = []
        for file in files:
            clump.append(file)
            if len(clump) == n:
                yield clump
                clump = []
        # Return any stragglers
        if clump:
            yield clump

class MegaDispatcher(object):
    log = multiprocessing.get_logger()
    def __init__(self, files, treename, output_file, selector, nworkers,
                 nchain=1):
        self.files = files
        self.treename = treename
        self.output_file = output_file
        self.selector = selector
        self.nworkers = nworkers
        # Figure out how many inputs to chain together
        self.nchain=nchain

    def build_workers(self, input_q, result_q):
        workers = [
            MegaWorker(input_q, result_q, self.treename, self.selector)
            for x in range(self.nworkers)
        ]
        return workers

    def run(self):
        input_q = multiprocessing.Queue()
        # add the files to be processed
        self.log.info(
            "Putting %i files into the process queue, grouped into %i file chunks",
                      len(self.files), self.nchain)
        for file in group_list(self.files, self.nchain):
            input_q.put(file)

        result_q = multiprocessing.Queue()

        everything_will_turn_out_okay = True

        try:
            workers = self.build_workers(input_q, result_q)

            # Start workers
            for worker in workers:
                worker.start()
                # Add poison pill for this worker
                input_q.put(None)
            input_q.close()

            self.log.info("Started %i workers", len(workers))

            # Start the merger
            merger = MegaMerger(result_q, self.output_file, len(self.files))
            merger.start()

            self.log.info("Started the merger process")

            # Require all the workers to finish
            #input_q.join()
            for i, worker in enumerate(workers):
                interrupted = True
                while interrupted:
                    try: # Avoid weird crashes from certain user system settings changes
                        worker.join()
                        interrupted = False
                    except OSError, e:
                        if e.errno == errno.EINTR:
                            self.log.debug("Received EINTR from system, probably because of user system settings change")
                            # interrupted, will just try to join again
                        else:
                            raise
                exit_code = worker.exitcode
                if exit_code:
                    everything_will_turn_out_okay = False
                    self.log.error("Working %i exited with code: %i",
                                   i, worker.exitcode)

            if not everything_will_turn_out_okay:
                self.log.error("A worker died.  Terminating merger and exiting")
                merger.terminate()
                sys.exit(2)

            self.log.info("All process jobs have completed.")

            # Add a poison pill at the end of the results
            result_q.put(None)
            result_q.close()

            self.log.info("Waiting for merge jobs to complete")

            # Require the merger to finish
            #result_q.join()
            merger.join()
        except KeyboardInterrupt:
            self.log.error("Ctrl-c detected, terminating everything")
            for i, worker in enumerate(workers):
                self.log.error("Terminating worker %i", i)
                worker.terminate()
            self.log.error("Terminating merger")
            merger.terminate()
            sys.exit(1)

        self.log.info("All merge jobs have completed.")

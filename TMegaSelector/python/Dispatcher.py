'''

Process dispatcher function for Mega framework

'''

import multiprocessing
from MegaWorker import MegaWorker
from MegaMerger import MegaMerger

class MegaDispatcher(object):
    log = multiprocessing.get_logger()
    def __init__(self, files, treename, output_file, selector, nworkers):
        self.files = files
        self.treename = treename
        self.output_file = output_file
        self.selector = selector
        self.nworkers = nworkers

    def run(self):
        input_q = multiprocessing.Queue()
        # add the files to be processed
        self.log.info("Putting %i files into the process queue",
                      len(self.files))
        for file in self.files:
            input_q.put(file)

        result_q = multiprocessing.Queue()

        workers = [
            MegaWorker(input_q, result_q, self.treename, self.selector)
            for x in range(self.nworkers)
        ]


        # Start workers
        for worker in workers:
            worker.start()
            # Add poison pill for this worker
            input_q.put(None)
        input_q.close()

        self.log.info("Started %i workers", len(workers))

        # Start the merger
        merger = MegaMerger(result_q, self.output_file)
        merger.start()

        self.log.info("Started the merger process")

        # Require all the workers to finish
        #input_q.join()
        for worker in workers:
            worker.join()

        self.log.info("All process jobs have completed.")

        # Add a poison pill at the end of the results
        result_q.put(None)
        result_q.close()

        self.log.info("Waiting for merge jobs to complete")

        # Require the merger to finish
        #result_q.join()
        merger.join()
        self.log.info("All merge jobs have completed.")

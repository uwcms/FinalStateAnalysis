'''

A threaded wrapper around the query_lumis_in_dataset function in datatools.py

Author: Evan K. Friis, UW

'''

from FinalStateAnalysis.Utilities.lumitools import json_summary
import logging
from datatools import query_files, query_lumis
from threading import Thread
from Queue import Queue

log = logging.getLogger("dbslumis")

# Worker function
def query_lumi_from_queue(input, output):
    while True:
        file = input.get()
        lumis = query_lumis(file)
        log.debug("Got lumis from %s", file)
        output.put(lumis)
        input.task_done()

def query_lumis_in_dataset(dataset, threads=7):
    files = query_files(dataset)
    to_query = Queue()
    for file in files:
        to_query.put(file)

    log.info("Getting lumis from %i files", len(files))

    results = Queue()
    workers = []
    for i in range(threads):
        worker = Thread(target=query_lumi_from_queue,
                        args = (to_query, results))
        worker.start()
        workers.append(worker)

    # Wait for everything to be processed
    to_query.join()

    log.info("Finished getting lumis")

    mega_set = set([])

    while not results.empty():
        subset = results.get()
        mega_set |= subset
    return json_summary(mega_set)

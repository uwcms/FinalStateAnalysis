'''

A threaded wrapper around the query_lumis_in_dataset function in datatools.py

Author: Evan K. Friis, UW

'''

import copy
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
        output.put((file, lumis))
        input.task_done()

def query_lumis_in_dataset(dataset, current, threads=7):
    files = query_files(dataset)
    to_query = Queue()
    count = 0
    for file in files:
        if file not in current:
            count += 1
            to_query.put(file)

    log.info("Getting lumis from %i files", count)

    results = Queue()
    workers = []
    for i in range(threads):
        worker = Thread(target=query_lumi_from_queue,
                        args = (to_query, results))
        worker.start()
        workers.append(worker)

    # Wait for everything to be processed
    try:
        to_query.join()
    except KeyboardInterrupt:
        log.error("Caught Ctrl-C, quitting")

    log.info("Finished getting lumis")
    output = copy.deepcopy(current)
    while not results.empty():
        file, lumis = results.get()
        output[file] = json_summary(lumis)
    return output

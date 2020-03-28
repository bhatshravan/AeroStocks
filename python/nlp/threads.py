import logging
import os
from queue import Queue
from threading import Thread
from time import time
from datetime import datetime, timedelta, date
import combined as combined
import csv
from slugify import slugify
import os.path
from os import path


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class DownloadWorker(Thread):

    def __init__(self, queue, x):
        Thread.__init__(self)
        self.queue = queue
        self.x = x

    def run(self):
        while True:
            row, newspaper = self.queue.get()
            x = self.x
            try:
                combined.downloadRawsAndPolarity(row, newspaper)
                # combined.getPolarityScore(row, newspaper)
            finally:
                self.queue.task_done()


def main():
    ts = time()

    newspaper = "economic"
    inputFile = "economic-merged.csv"

    # newspaper = "moneycontrol"
    # inputFile = "moneyctl-merged-buisness.csv"

    inputFileOpen = open('../data/news/'+newspaper+"/"+inputFile, 'rt')
    inputFile = csv.reader(inputFileOpen)

    queue = Queue()
    for x in range(15):
        worker = DownloadWorker(queue, x)
        worker.daemon = True
        worker.start()

    for idx, row in enumerate(inputFile):
        # if(idx > 900):
        #     break

        # if(prints >= 100):
        #     prints = 0
        #     print("Positive:{}, Negative:{}, Neutral:{}, Total={}".format(
        #         p, n, e, (p+n+e)))

        if(row[0] == ""):
            continue
        logger.info('Queueing {}'.format(row[0][0:120]))
        queue.put((row, newspaper))

    queue.join()
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()

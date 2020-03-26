import logging
import os
from queue import Queue
from threading import Thread
from time import time
from datetime import datetime, timedelta, date
import moneyctl as mtl
import economic as ecl
import deccan as dcl

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
            link = self.queue.get()
            x = self.x
            try:

                # Moneycontrol
                # url = "https://www.moneycontrol.com/news/business/page-" + \
                #     str(link)
                # mtl.downloadMtlAll(url, x)

                # Economic times
                # ecl.downloadEconomicAll(link, x)
                dcl.downloadDeccanAll(link, x)

            finally:
                self.queue.task_done()


def main():
    ts = time()

    # Moneycontrol
    # pages = [x for x in range(1, 1500)]

    # Economic
    # pages = [x for x in range(43647, 43914)]

    # Deccan
    date1 = date(2019, 9, 2)
    date2 = date(2020, 3, 25)
    pages = [d.strftime('%Y/%m/%d') for d in (date1 + timedelta(days=i)
                                              for i in range((date2 - date1).days + 1))]

    queue = Queue()
    for x in range(8):
        worker = DownloadWorker(queue, x)
        worker.daemon = True
        worker.start()
    for link in pages:
        logger.info('Queueing {}'.format(link))
        queue.put((link))
    queue.join()
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()

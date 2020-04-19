import logging
import os
from queue import Queue
from threading import Thread
from time import time
from datetime import datetime, timedelta, date
import moneyctl as mtl
import economic as ecl
import deccan as dcl
import firstpost as fpl

import multiprocessing


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
                ecl.downloadEconomicAll(link, x)

                # FirstPost
                # fpl.downloadFirstPostAll(link, x)

                # Deccan
                # dcl.downloadDeccanAll(link, x)

            finally:
                self.queue.task_done()


def threads():
    ts = time()

    # Moneycontrol
    # pages = [x for x in range(1, 1500)]

    # Economic
    # pages = [x for x in range(43647, 43914)]
    # pages = [x for x in range(40179, 43921)]

    # FirstPost
    # pages = [x for x in range(2, 560)]

    # Deccan
    # date1 = date(2019, 9, 2)
    # date2 = date(2020, 3, 25)
    # pages = [d.strftime('%Y/%m/%d') for d in (date1 + timedelta(days=i)
    #                                           for i in range((date2 - date1).days + 1))]

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


def processes():
    lists = []
    page = 0
    # 43921

    #economic
    # for x in range(40909, 43921):
    #     lists.append((x, page))
    #     page = page+1
    #     if page > 11:
    #         page = 0

    # Deccan
    # date1 = date(2012, 1, 1)
    # date2 = date(2020, 3, 31)
    # pages = [d.strftime('%Y/%m/%d') for d in (date1 + timedelta(days=i)
    #                                           for i in range((date2 - date1).days + 1))]

    # for pagess in pages:
    #     lists.append((pagess, page))    
    #     page = page+1
    #     if page > 11:
    #         page = 0

    # FirstPost
    # for x in range(2, 3202):
    #     lists.append((x, page))
    #     page = page+1
    #     if page > 11:
    #         page = 0

    # Monecontrol
    for x in range(1, 25000):
        lists.append((x, page))
        page = page+1
        if page > 11:
            page = 0

    print("\n\nLists:", lists)

    with multiprocessing.Pool(processes=12) as pool:
        # pool.starmap(ecl.downloadEconomicAll, lists)
        # pool.starmap(dcl.downloadDeccanAll, lists)
        # pool.starmap(fpl.downloadFirstPostAll, lists)
        pool.starmap(mtl.downloadMtlAll, lists)


if __name__ == '__main__':
    # main()
    processes()
# headline,url,date,realdate,category

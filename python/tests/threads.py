import logging
import os
from queue import Queue
from threading import Thread
from time import time
import moneyctl as mtl

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
                # download_link(directory, link)
                url = "https://www.moneycontrol.com/news/business/"+link
                # mtl.downloadMtlAll()
                print(url, x)
            finally:
                self.queue.task_done()


def main():
    ts = time()

    pages = [x for x in range(300, 303)]

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

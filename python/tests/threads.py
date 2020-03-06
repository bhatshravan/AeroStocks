import logging
import os
from queue import Queue
from threading import Thread
from time import time

from download import setup_download_dir, get_links, download_link


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            directory, link = self.queue.get()
            try:
                download_link(directory, link)
            finally:
                self.queue.task_done()


def main():
    ts = time()
    client_id = os.getenv('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    links = get_links(client_id)
    queue = Queue()
    for x in range(8):
        worker = DownloadWorker(queue)
        worker.daemon = True
        worker.start()
    for link in links:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
    queue.join()
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()

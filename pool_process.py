import logging

from multiprocessing import Process, Queue
from threading import current_thread, Thread

logging.basicConfig(level=logging.INFO)

def _run(q):
    while True:
        logging.info(f"{current_thread().name} {q.qsize()}")
        p = q.get()
        if p is None:
            break
        p.start()
        p.join()
        q.task_done()

class Pool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.threads = []
        self.queue = Queue()

    def map(self, func, args):
        for i in range(self.max_workers):
            t = Process(target=_run, args=(self.queue, ))
            t.start()
            self.threads.append(t)

        for a in args:
            self.queue.put(Process(target=func, args=(a, )))

        #self.queue.join()

        for i in range(self.max_workers):
            self.queue.put(None)

        for t in self.threads:
            logging.info(f"{t.name} JOINED")
            t.join()
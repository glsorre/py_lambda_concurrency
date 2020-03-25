import logging

from multiprocessing import Process, Queue
from threading import current_thread, Thread

def _run(q):
    while True:
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

        for i in range(self.max_workers):
            self.queue.put(None)

        for t in self.threads:
            logging.info(f"{t.name} JOINED")
            t.join()
from multiprocessing import Process
from threading import current_thread, Thread
from queue import Queue

def _run(q):
    while True:
        p = q.get()
        if p is None:
            break
        p.start()
        p._popen.wait()
        q.task_done()

class Pool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.threads = []
        self.queue = Queue()

    def map(self, func, args):
        for i in range(self.max_workers):
            t = Thread(target=_run, args=(self.queue, ))
            t.start()
            self.threads.append(t)

        for a in args:
            self.queue.put(Process(target=func, args=(a, )))

        self.queue.join()

        for i in range(self.max_workers):
            self.queue.put(None)

    def close(self):
        for t in self.threads:
            t.join()
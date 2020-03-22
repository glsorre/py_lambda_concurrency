from multiprocessing import Process
from queue import Queue

class Pool:
    def __init__(self, max_workers):
        self.max_workers = max_workers
        self.processes = []
        self.queue = Queue()

    def map(self, func, args):
        for arg in args:
            p = Process(target=func, args=(arg, ))
            self.queue.put(p)

        for i in range(self.max_workers):
            p = self.queue.get()
            p.start()                  
            self.processes.append(p)

        while self.queue.qsize() > 0:
            dead_processes = [p for p in self.processes if not p.is_alive()]
            alive_processes = [p for p in self.processes if p.is_alive()]
            for p in dead_processes:
                self.processes.remove(p)
                p.join()
                p.close()
            for p in range(0, len(alive_processes)):
                p = self.queue.get()
                p.start()                  
                self.processes.append(p)

    def close(self):
        for p in self.processes:
            p.join()
            p.close()
